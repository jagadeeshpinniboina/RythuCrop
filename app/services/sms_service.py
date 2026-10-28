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
    """Returns True if a live Fast2SMS API key is configured."""
    key = os.environ.get("FAST2SMS_API_KEY", "").strip()
    return bool(key) and key not in PLACEHOLDER_KEYS and not key.startswith("your_")


def send_sms_otp(mobile_number: str, otp_code: str) -> Tuple[bool, str]:
    """
    Sends a real 6-digit OTP SMS to an Indian 10-digit mobile number
    using the Fast2SMS Quick/OTP API endpoint (https://www.fast2sms.com/dev/bulkV2).
    
    Parameters:
        mobile_number (str): 10-digit Indian phone number (or with +91/0 prefix).
        otp_code (str): 6-digit verification code.
        
    Returns:
        (success: bool, status_message: str)
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
    api_key = os.environ.get("FAST2SMS_API_KEY", "").strip()

    # 2. Real Fast2SMS Live API Dispatch if FAST2SMS_API_KEY is configured
    if is_sms_configured():
        headers = {
            "authorization": api_key,
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache"
        }
        payload = {
            "variables_values": str(otp_code),
            "route": "otp",
            "numbers": cleaned
        }
        try:
            logger.info(f"Dispatching live SMS OTP via Fast2SMS to +91{masked}...")
            res = requests.post(FAST2SMS_ENDPOINT, data=payload, headers=headers, timeout=10)
            
            res_data = {}
            try:
                res_data = res.json()
            except Exception:
                pass

            if res.status_code == 200 and res_data.get("return") is True:
                logger.info(f"Fast2SMS OTP successfully delivered to +91{masked}")
                return True, f"OTP sent successfully to {masked} via SMS."
            else:
                raw_msg = res_data.get("message")
                if isinstance(raw_msg, list) and len(raw_msg) > 0:
                    detail = raw_msg[0]
                else:
                    detail = str(raw_msg or res.text or f"HTTP status {res.status_code}")
                logger.error(f"Fast2SMS rejected dispatch to +91{masked}: {detail}")
                return False, "Unable to send SMS. Please check your network or try again."

        except requests.exceptions.RequestException as e:
            logger.error(f"Fast2SMS network connection failure while sending to +91{masked}: {e}")
            return False, "Unable to send SMS. Please check your network or try again."
        except Exception as e:
            logger.error(f"Unexpected error in Fast2SMS dispatch to +91{masked}: {e}")
            return False, "Unable to send SMS. Please check your network or try again."

    # 3. Development / Test Fallback (when FAST2SMS_API_KEY is placeholder or not set)
    print("\n" + "=" * 64)
    print(f" [RythuCrop SMS]: FAST2SMS_API_KEY not set. Console OTP for +91{masked}: {otp_code} ")
    print(" (Expires in 5 minutes | 30s resend cooldown)")
    print("=" * 64 + "\n")
    return True, f"OTP sent to {masked}."


def send_otp_sms(mobile: str, otp: str, masked_mobile: str = "") -> Tuple[bool, str]:
    """Backward-compatible alias for send_sms_otp."""
    return send_sms_otp(mobile, otp)
