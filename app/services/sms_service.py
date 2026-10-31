"""
RythuCrop Fast2SMS Live OTP Gateway & Dispatcher Module
Provides self-contained helper function send_sms_otp(mobile_number, otp_code)
for delivering real 6-digit OTP SMS via Fast2SMS Quick/OTP API.
"""

import os
import re
import logging
from typing import Tuple
import requests

logger = logging.getLogger("rythucrop.sms")

FAST2SMS_ENDPOINT = "https://www.fast2sms.com/dev/bulkV2"
PLACEHOLDER_KEYS = {"", "your_fast2sms_api_key_here", "PLACEHOLDER_FAST2SMS_KEY"}


def is_sms_configured() -> bool:
    """Returns True if live Fast2SMS dispatch should be attempted."""
    dev_auth = os.environ.get("RYTHUCROP_DEV_AUTH", "false").lower() == "true"
    if dev_auth:
        return False
    key = os.environ.get("FAST2SMS_API_KEY", "").strip()
    return bool(key) and key not in PLACEHOLDER_KEYS and not key.startswith("your_")


def send_sms_otp(mobile_number: str, otp_code: str) -> Tuple[bool, str]:
    """
    Sends a real 6-digit OTP SMS to an Indian 10-digit mobile number
    using the Fast2SMS Quick/OTP API endpoint (https://www.fast2sms.com/dev/bulkV2).
    
    1. Tries Option A (OTP route):
       {
           "variables_values": str(otp_code),
           "route": "otp",
           "numbers": str(mobile_number)
       }
    2. If Fast2SMS returns an error on route "otp", fallback cleanly to:
       Option B (Quick SMS route "q"):
       {
           "message": f"Your RythuCrop verification OTP is {otp_code}. Valid for 5 minutes.",
           "language": "english",
           "route": "q",
           "numbers": str(mobile_number)
       }
    3. If Fast2SMS balance or gateway fails completely:
       Logs real OTP to terminal: [BACKEND OTP FOR +91{mobile}]: {otp_code}
       Returns (False, detailed_error_message).
    """
    # 1. Clean and normalize mobile number to 10 digits
    cleaned = re.sub(r'\D', '', str(mobile_number or ""))
    if len(cleaned) == 12 and cleaned.startswith("91"):
        cleaned = cleaned[2:]
    elif len(cleaned) == 11 and cleaned.startswith("0"):
        cleaned = cleaned[1:]

    if not re.match(r'^[6-9]\d{9}$', cleaned):
        return False, "Invalid mobile number. Please enter a valid 10-digit Indian mobile number."

    masked = f"XXXXXX{cleaned[-4:]}"
    api_key = os.getenv("FAST2SMS_API_KEY", "").strip()

    # If Fast2SMS is not configured or in explicit dev mode
    if not is_sms_configured():
        print(f"[BACKEND OTP FOR +91{cleaned}]: {otp_code}")
        return True, f"OTP sent to {masked} (Dev Mode)."

    headers = {
        "authorization": api_key,
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache"
    }

    route_a_error = None

    # =========================================================================
    # Option A: OTP route
    # =========================================================================
    payload_a = {
        "variables_values": str(otp_code),
        "route": "otp",
        "numbers": str(cleaned)
    }

    try:
        response = requests.post(FAST2SMS_ENDPOINT, data=payload_a, headers=headers, timeout=10)
        print("[Fast2SMS DEBUG Response]:", response.status_code, response.text)

        res_a_json = {}
        try:
            res_a_json = response.json()
        except Exception:
            pass

        if response.status_code == 200 and res_a_json.get("return") is True:
            logger.info(f"Fast2SMS OTP sent via route 'otp' to +91{masked}")
            return True, f"OTP sent successfully to {masked} via SMS."

        msg_a = res_a_json.get("message")
        if isinstance(msg_a, list) and len(msg_a) > 0:
            msg_a = msg_a[0]
        route_a_error = str(msg_a or response.text or f"Status {response.status_code}")

    except Exception as e:
        logger.warning(f"Fast2SMS route 'otp' exception: {e}")
        route_a_error = str(e)

    # =========================================================================
    # Option B: Quick SMS route "q" (clean fallback)
    # =========================================================================
    payload_b = {
        "message": f"Your RythuCrop verification OTP is {otp_code}. Valid for 5 minutes.",
        "language": "english",
        "route": "q",
        "numbers": str(cleaned)
    }

    route_b_error = None
    try:
        response_b = requests.post(FAST2SMS_ENDPOINT, data=payload_b, headers=headers, timeout=10)
        print("[Fast2SMS DEBUG Response]:", response_b.status_code, response_b.text)

        res_b_json = {}
        try:
            res_b_json = response_b.json()
        except Exception:
            pass

        if response_b.status_code == 200 and res_b_json.get("return") is True:
            logger.info(f"Fast2SMS OTP sent via route 'q' to +91{masked}")
            return True, f"OTP sent successfully to {masked} via SMS."

        msg_b = res_b_json.get("message")
        if isinstance(msg_b, list) and len(msg_b) > 0:
            msg_b = msg_b[0]
        route_b_error = str(msg_b or response_b.text or f"Status {response_b.status_code}")

    except Exception as e:
        logger.error(f"Fast2SMS route 'q' exception: {e}")
        route_b_error = str(e)

    # =========================================================================
    # Fallback Graceful Handling:
    # If the Fast2SMS balance or gateway fails completely, log real OTP in terminal
    # =========================================================================
    print(f"[BACKEND OTP FOR +91{cleaned}]: {otp_code}")

    # Return a clear error message in API response json with details instead of generic failure
    detail = route_b_error or route_a_error or "Fast2SMS gateway unreachable"
    error_message = f"Fast2SMS Error: {detail}"
    return False, error_message


def send_otp_sms(mobile: str, otp: str, masked_mobile: str = "") -> Tuple[bool, str]:
    """Backward-compatible alias for send_sms_otp."""
    return send_sms_otp(mobile, otp)
