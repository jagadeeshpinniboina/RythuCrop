"""
RythuCrop Twilio WhatsApp Live OTP Gateway & Dispatcher Module
Dispatches real 6-digit verification codes via Twilio WhatsApp Sandbox API.
Includes standard plain-text WhatsApp messaging, private backend console logging,
and guaranteed privacy (never exposing OTP in the UI or client API messages).
"""

import os
import re
import logging
from typing import Tuple
from twilio.rest import Client

logger = logging.getLogger("rythucrop.sms")

# ANSI escape sequence regex pattern for stripping terminal color codes
ANSI_ESCAPE_PATTERN = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def strip_ansi_codes(text: str) -> str:
    """Strips ANSI terminal escape codes from error messages so UI receives clean text."""
    if not text:
        return ""
    clean = ANSI_ESCAPE_PATTERN.sub('', str(text))
    return clean.encode('ascii', 'ignore').decode('ascii').strip()


def is_sms_configured() -> bool:
    """Returns True if Twilio WhatsApp gateway credentials should be called."""
    dev_auth = os.environ.get("RYTHUCROP_DEV_AUTH", "false").lower() == "true"
    if dev_auth:
        return False
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
    return bool(account_sid and auth_token)


def send_sms_otp(mobile_number, otp_code) -> Tuple[bool, str]:
    """
    Dispatches 6-digit OTP to mobile_number via Twilio WhatsApp Sandbox.
    
    1. Prints full verbose Twilio debug logs (Account SID, From, To).
    2. Sends standard plain text WhatsApp message:
       "Your RythuCrop verification OTP is: {otp_code}. Valid for 5 minutes."
    3. Logs details and errors to backend terminal console only.
    4. If Twilio returns an error, DOES NOT mask it as success, returns (False, clean_err).
    5. Returns success message NEVER exposing the OTP code to the UI:
       "OTP sent successfully to your WhatsApp number (+91 XXXXXX8801)."
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "+17372508034").strip()

    cleaned_mobile = "".join(filter(str.isdigit, str(mobile_number)))[-10:]
    masked_mobile = f"XXXXXX{cleaned_mobile[-4:]}"

    success_msg = f"OTP sent successfully to your WhatsApp number (+91 {masked_mobile})."

    if not is_sms_configured():
        print(f"[TWILIO NOTICE] Dev mode active or credentials not configured.")
        print(f"[SECRET TERMINAL OTP]: {otp_code}")
        return True, success_msg

    # Verify and format WhatsApp phone numbers strictly
    raw_from = from_number.replace('whatsapp:', '').strip()
    from_num = f"whatsapp:{raw_from}"
    to_num = f"whatsapp:+91{cleaned_mobile}"

    # Print full verbose Twilio debug logs
    print(f"[TWILIO DEBUG] Account SID: {account_sid[:8]}..., From: {from_num}, To: {to_num}")

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_=f"whatsapp:{from_number.replace('whatsapp:', '')}",
            to=f"whatsapp:+91{cleaned_mobile}",
            body=f"Your RythuCrop verification OTP is: {otp_code}. Valid for 5 minutes."
        )
        print(f"[TWILIO SUCCESS] Message SID: {message.sid}")
        print(f"[SECRET TERMINAL OTP]: {otp_code}")
        return True, success_msg
    except Exception as e:
        error_code = getattr(e, 'code', None)
        clean_err = strip_ansi_codes(str(e))
        print(f"[TWILIO ERROR DETAILS]: Code={error_code}, Msg={clean_err}")
        # Only log the OTP in the private backend terminal console for debugging
        print(f"[SECRET TERMINAL OTP]: {otp_code}")
        # DO NOT mask Twilio errors as generic success
        return False, clean_err


def send_otp_sms(mobile: str, otp: str, masked_mobile: str = "") -> Tuple[bool, str]:
    """Alias for send_sms_otp for backward compatibility."""
    return send_sms_otp(mobile, otp)
