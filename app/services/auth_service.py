"""
RythuCrop Authentication and OTP Service
Provides mobile number verification with cryptographic hashing,
attempt limits, 30s resend cooldowns, 5m expiry, dual-mode SMS delivery,
and custom @login_required decorator.
"""

import os
import re
import secrets
import hashlib
import datetime
from functools import wraps
from typing import Dict, Tuple, Optional
from flask import session, request, redirect, url_for, jsonify

from app.models.alerts_db import (
    save_otp_request,
    get_latest_otp_request,
    mark_otp_verified,
    increment_otp_attempts,
    get_or_create_user
)
from app.services.sms_service import send_sms_otp, send_otp_sms, is_sms_configured

# Configuration
OTP_VALIDITY_MINUTES = 5
MAX_OTP_ATTEMPTS = 3
RESEND_COOLDOWN_SECONDS = 30
AUTH_DEV_MODE = os.environ.get("RYTHUCROP_DEV_AUTH", "true").lower() == "true"

# In-memory cooldown tracker: {normalized_mobile: datetime}
_LAST_REQUEST_TIME: Dict[str, datetime.datetime] = {}


def get_raw_10digit(mobile_raw: str) -> Optional[str]:
    """Extract and validate 10-digit Indian mobile number matching ^[6-9]\\d{9}$."""
    if not mobile_raw:
        return None
    cleaned = re.sub(r'[\s\-\(\)\+]', '', str(mobile_raw))
    # Remove leading 91 or 0 if present
    if len(cleaned) == 12 and cleaned.startswith("91"):
        cleaned = cleaned[2:]
    elif len(cleaned) == 11 and cleaned.startswith("0"):
        cleaned = cleaned[1:]
    
    if re.match(r'^[6-9]\d{9}$', cleaned):
        return cleaned
    return None


def normalize_mobile(mobile_raw: str) -> Optional[str]:
    """Validate and normalize Indian mobile number to E.164 +91XXXXXXXXXX."""
    raw_10 = get_raw_10digit(mobile_raw)
    if raw_10:
        return f"+91{raw_10}"
    return None


def get_masked_mobile(mobile_raw: str) -> str:
    """Return masked mobile number showing ONLY last 4 digits (e.g. XXXXXX8801)."""
    raw_10 = get_raw_10digit(mobile_raw)
    if raw_10:
        return f"XXXXXX{raw_10[-4:]}"
    clean = re.sub(r'\D', '', str(mobile_raw or ""))
    if len(clean) >= 4:
        return f"XXXXXX{clean[-4:]}"
    return "XXXXXX0000"


def hash_otp(otp: str, salt: str) -> str:
    """Hash OTP using SHA-256 with cryptographically generated salt."""
    return hashlib.sha256(f"{salt}{otp}".encode("utf-8")).hexdigest()


def request_otp(mobile_raw: str) -> Tuple[bool, str, Optional[Dict]]:
    """
    Generate and send 6-digit OTP for mobile authentication.
    Enforces regex ^[6-9]\\d{9}$, 30-sec resend cooldown, 5-min expiry,
    and dispatches via SMS service (real or dev mock mode).
    Returns (success: bool, message: str, extra_data: Optional[Dict]).
    """
    mobile = normalize_mobile(mobile_raw)
    raw_10 = get_raw_10digit(mobile_raw)
    if not mobile or not raw_10:
        return False, "Invalid mobile number. Please enter a valid 10-digit mobile number starting with 6, 7, 8, or 9.", None

    now = datetime.datetime.now()

    # 30-second Resend Cooldown check
    if mobile in _LAST_REQUEST_TIME:
        elapsed = (now - _LAST_REQUEST_TIME[mobile]).total_seconds()
        if elapsed < RESEND_COOLDOWN_SECONDS:
            remaining = int(RESEND_COOLDOWN_SECONDS - elapsed)
            return False, f"Please wait {remaining} seconds before requesting a new OTP.", {
                "cooldown_remaining": remaining,
                "cooldown_seconds": RESEND_COOLDOWN_SECONDS
            }

    # Generate secure random 6-digit OTP
    otp = str(secrets.randbelow(900000) + 100000)
    salt = secrets.token_hex(16)
    hashed = hash_otp(otp, salt)
    expires_at = now + datetime.timedelta(minutes=OTP_VALIDITY_MINUTES)

    # Persist in SQLite database
    save_otp_request(mobile, hashed, salt, expires_at)
    _LAST_REQUEST_TIME[mobile] = now

    masked_mobile = get_masked_mobile(mobile)

    # Dispatch OTP via Fast2SMS Live Gateway (or dev console fallback)
    sms_ok, sms_msg = send_sms_otp(mobile, otp)
    if not sms_ok:
        return False, sms_msg, None

    is_dev = not is_sms_configured() or os.environ.get("RYTHUCROP_DEV_AUTH", "true").lower() == "true"

    extra_data = {
        "mobile": mobile,
        "raw_mobile": raw_10,
        "masked_mobile": masked_mobile,
        "expires_in_seconds": OTP_VALIDITY_MINUTES * 60,
        "cooldown_seconds": RESEND_COOLDOWN_SECONDS,
        "dev_mode": is_dev
    }

    if is_dev:
        extra_data["dev_otp"] = otp

    return True, sms_msg, extra_data


def verify_otp(mobile_raw: str, entered_otp: str, preferred_lang: str = "en") -> Tuple[bool, str, Optional[Dict]]:
    """
    Verify 6-digit OTP with expiry (5 min) and maximum attempt limiting (3 tries).
    Uses constant-time comparison against salted SHA-256 hash.
    Returns (success: bool, message: str, user_dict: Optional[Dict]).
    """
    mobile = normalize_mobile(mobile_raw)
    if not mobile:
        return False, "Invalid mobile number.", None

    otp_clean = str(entered_otp or "").strip()
    if not otp_clean.isdigit() or len(otp_clean) != 6:
        return False, "Please enter a valid 6-digit verification code.", None

    req = get_latest_otp_request(mobile)
    if not req:
        return False, "No active OTP request found. Please request a new OTP.", None

    req_id = req["id"]
    attempts = req["attempts"]
    expires_at = datetime.datetime.fromisoformat(req["expires_at"])
    now = datetime.datetime.now()

    if now > expires_at:
        return False, "OTP has expired (valid for 5 minutes). Please request a new OTP.", None

    if attempts >= MAX_OTP_ATTEMPTS:
        return False, "Maximum verification attempts (3) exceeded. Please request a new OTP.", None

    expected_hash = req["otp_hash"]
    salt = req["salt"]
    test_hash = hash_otp(otp_clean, salt)

    if secrets.compare_digest(expected_hash, test_hash):
        mark_otp_verified(req_id)
        user = get_or_create_user(mobile, preferred_lang)
        return True, "Login successful.", user
    else:
        increment_otp_attempts(req_id)
        remaining = MAX_OTP_ATTEMPTS - (attempts + 1)
        if remaining > 0:
            return False, f"Incorrect OTP. {remaining} attempt(s) remaining.", None
        else:
            return False, "Incorrect OTP. Maximum attempts reached. Please request a new OTP.", None


def login_required(f):
    """
    Custom decorator to protect endpoints.
    Unauthenticated users accessing web pages are redirected to /login.
    Unauthenticated requests to JSON/API endpoints receive HTTP 401 with redirect info.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_authenticated"):
            # Check if this is an API or JSON request
            is_api_request = (
                request.is_json or
                request.path.startswith("/api/") or
                (request.method == "POST" and request.path in ("/predict", "/farm-plan", "/predict-yield"))
            )
            if is_api_request:
                return jsonify({
                    "error": "Authentication required. Please login with your mobile number.",
                    "redirect": "/login",
                    "authenticated": False
                }), 401

            next_url = request.full_path if request.query_string else request.path
            return redirect(url_for("auth.login", next=next_url))
        return f(*args, **kwargs)
    return decorated_function
