"""
RythuCrop Twilio WhatsApp Live OTP Gateway & Dispatcher Module
Dispatches real 6-digit verification codes via Twilio WhatsApp Sandbox API.
"""

import os
import logging
from typing import Tuple
from twilio.rest import Client

logger = logging.getLogger("rythucrop.sms")


def is_sms_configured() -> bool:
    """Returns True if Twilio WhatsApp gateway credentials should be called."""
    dev_auth = os.environ.get("RYTHUCROP_DEV_AUTH", "false").lower() == "true"
    if dev_auth:
        return False
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
    return bool(account_sid and auth_token)


def send_sms_otp(mobile_number, otp_code) -> Tuple[bool, str]:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "+17372508034").strip()

    cleaned_mobile = "".join(filter(str.isdigit, str(mobile_number)))[-10:]

    if not is_sms_configured():
        print(f"[TWILIO NOTICE] Dev mode active or credentials not configured.")
        print(f"[BACKEND OTP FOR +91{cleaned_mobile}]: {otp_code}")
        return True, f"OTP generated (Dev Mode) for +91{cleaned_mobile}."

    print(f"[TWILIO DISPATCH] Attempting WhatsApp OTP to +91{cleaned_mobile} with SID: {account_sid[:8]}...")

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your RythuCrop verification OTP is: {otp_code}. Valid for 5 minutes.",
            from_=f"whatsapp:{from_number}",
            to=f"whatsapp:+91{cleaned_mobile}"
        )
        print(f"[TWILIO SUCCESS] Message SID: {message.sid}")
        return True, "OTP sent successfully via WhatsApp"
    except Exception as e:
        print(f"[TWILIO ERROR]: {str(e)}")
        # Fallback logging to terminal so user is NEVER blocked
        print(f"[BACKEND OTP FOR +91{cleaned_mobile}]: {otp_code}")
        return False, str(e)


def send_otp_sms(mobile: str, otp: str, masked_mobile: str = "") -> Tuple[bool, str]:
    """Alias for send_sms_otp for backward compatibility."""
    return send_sms_otp(mobile, otp)
