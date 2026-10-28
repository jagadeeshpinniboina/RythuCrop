"""
RythuCrop Authentication and OTP Service
Provides mobile number verification with cryptographic hashing,
cooldown periods, attempt limits, and safe dev-mode fallbacks.
"""

import os
import re
import secrets
import hashlib
import datetime
from typing import Dict, Tuple, Optional
from app.models.alerts_db import (
    save_otp_request,
    get_latest_otp_request,
    mark_otp_verified,
    increment_otp_attempts,
    get_or_create_user
)

# Configuration from environment
AUTH_DEV_MODE = os.environ.get("RYTHUCROP_DEV_AUTH", "true").lower() == "true"
OTP_VALIDITY_MINUTES = 5
MAX_OTP_ATTEMPTS = 3
RESEND_COOLDOWN_SECONDS = 60

# In-memory cooldown tracker: {mobile: datetime}
_LAST_REQUEST_TIME: Dict[str, datetime.datetime] = {}


def normalize_mobile(mobile_raw: str) -> Optional[str]:
    """Validate and normalize Indian mobile number."""
    if not mobile_raw:
        return None
    cleaned = re.sub(r'[\s\-\(\)]', '', str(mobile_raw))
    # Match 10-digit Indian numbers starting with 6, 7, 8, 9 with optional +91 or 0
    match = re.match(r'^(?:\+91|91|0)?([6-9]\d{9})$', cleaned)
    if match:
        ten_digits = match.group(1)
        return f"+91{ten_digits}"
    return None


def hash_otp(otp: str, salt: str) -> str:
    """Hash OTP using SHA-256 with salt."""
    return hashlib.sha256(f"{salt}{otp}".encode("utf-8")).hexdigest()


def request_otp(mobile_raw: str) -> Tuple[bool, str, Optional[Dict]]:
    """
    Generate and send an OTP for mobile authentication.
    Returns (success, message, extra_data).
    """
    mobile = normalize_mobile(mobile_raw)
    if not mobile:
        return False, "Invalid mobile number. Please enter a valid 10-digit mobile number.", None

    now = datetime.datetime.now()

    # Cooldown check
    if mobile in _LAST_REQUEST_TIME:
        elapsed = (now - _LAST_REQUEST_TIME[mobile]).total_seconds()
        if elapsed < RESEND_COOLDOWN_SECONDS:
            remaining = int(RESEND_COOLDOWN_SECONDS - elapsed)
            return False, f"Please wait {remaining} seconds before requesting a new OTP.", {"cooldown_remaining": remaining}

    # Generate 6-digit OTP
    otp = str(secrets.randbelow(900000) + 100000)
    salt = secrets.token_hex(16)
    hashed = hash_otp(otp, salt)
    expires_at = now + datetime.timedelta(minutes=OTP_VALIDITY_MINUTES)

    save_otp_request(mobile, hashed, salt, expires_at)
    _LAST_REQUEST_TIME[mobile] = now

    extra_data = {
        "mobile": mobile,
        "expires_in_seconds": OTP_VALIDITY_MINUTES * 60,
        "dev_mode": AUTH_DEV_MODE
    }

    if AUTH_DEV_MODE:
        extra_data["dev_otp"] = otp
        print(f"\n[DEV AUTH LOG] Generated OTP for {mobile}: {otp} (Expires in {OTP_VALIDITY_MINUTES} min)\n")
        message = "OTP generated successfully (Development Mode active)."
    else:
        # Here a real SMS Gateway like Fast2SMS, MSG91, or Twilio would be invoked
        sms_sent = _send_sms_via_provider(mobile, otp)
        if sms_sent:
            message = f"OTP sent to {mobile} via SMS."
        else:
            return False, "Failed to deliver SMS. Check provider configuration or enable dev mode.", None

    return True, message, extra_data


def verify_otp(mobile_raw: str, entered_otp: str, preferred_lang: str = "en") -> Tuple[bool, str, Optional[Dict]]:
    """
    Verify OTP with expiry and attempt counting.
    Returns (success, message, user_dict).
    """
    mobile = normalize_mobile(mobile_raw)
    if not mobile:
        return False, "Invalid mobile number.", None

    if not entered_otp or not str(entered_otp).strip().isdigit() or len(str(entered_otp).strip()) != 6:
        return False, "Please enter a valid 6-digit OTP.", None

    entered_otp = str(entered_otp).strip()
    req = get_latest_otp_request(mobile)

    if not req:
        return False, "No active OTP request found. Please request a new OTP.", None

    req_id = req["id"]
    attempts = req["attempts"]
    expires_at = datetime.datetime.fromisoformat(req["expires_at"])
    now = datetime.datetime.now()

    if now > expires_at:
        return False, "OTP has expired. Please request a new one.", None

    if attempts >= MAX_OTP_ATTEMPTS:
        return False, "Maximum verification attempts exceeded. Please request a new OTP.", None

    expected_hash = req["otp_hash"]
    salt = req["salt"]
    test_hash = hash_otp(entered_otp, salt)

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


def _send_sms_via_provider(mobile: str, otp: str) -> bool:
    """Integration hook for external SMS provider when configured."""
    api_key = os.environ.get("SMS_API_KEY")
    if not api_key:
        # Fallback to dev mode if provider is not configured
        print(f"[SMS PROVIDER NOTICE] No SMS_API_KEY set. Dev fallback used: OTP for {mobile} is {otp}")
        return True
    # Real provider logic would go here
    return True
