"""
RythuCrop Multi-Provider SMS Dispatcher
Supports Twilio, Fast2SMS, MSG91, and Development Mock Mode.
"""

import os
import logging
from typing import Tuple
import requests

logger = logging.getLogger("rythucrop.sms")


def is_sms_configured() -> bool:
    """Returns True if any production SMS gateway is configured."""
    if os.environ.get("FAST2SMS_API_KEY", "").strip():
        return True
    if os.environ.get("MSG91_AUTH_KEY", "").strip() and os.environ.get("MSG91_TEMPLATE_ID", "").strip():
        return True
    if os.environ.get("TWILIO_ACCOUNT_SID", "").strip() and os.environ.get("TWILIO_AUTH_TOKEN", "").strip():
        return True
    return False


def send_otp_sms(mobile: str, otp: str, masked_mobile: str) -> Tuple[bool, str]:
    """
    Sends 6-digit OTP to user's mobile number.
    Returns (success: bool, status_message: str).
    
    Priority order:
    1. Fast2SMS (Indian SMS Gateway) if FAST2SMS_API_KEY is configured
    2. MSG91 (Indian SMS Gateway) if MSG91_AUTH_KEY is configured
    3. Twilio (Global SMS Gateway) if TWILIO_ACCOUNT_SID is configured
    4. Development Mock Mode (Console Logging + UI Toast) fallback
    """
    raw_mobile = mobile.replace("+91", "").strip()
    full_mobile = f"+91{raw_mobile}"
    message = f"Your RythuCrop verification code is {otp}. Valid for 5 minutes. Do not share this OTP with anyone."

    # 1. Fast2SMS Integration
    fast2sms_key = os.environ.get("FAST2SMS_API_KEY", "").strip()
    if fast2sms_key:
        try:
            url = "https://www.fast2sms.com/dev/bulkV2"
            headers = {"authorization": fast2sms_key}
            payload = {
                "variables_values": otp,
                "route": "otp",
                "numbers": raw_mobile
            }
            res = requests.post(url, headers=headers, data=payload, timeout=8)
            if res.status_code == 200 and res.json().get("return"):
                logger.info(f"Fast2SMS OTP sent successfully to {masked_mobile}")
                return True, f"OTP sent to {masked_mobile} via SMS."
            else:
                logger.warning(f"Fast2SMS returned error: {res.text}. Falling back to dev mock.")
        except Exception as e:
            logger.error(f"Fast2SMS dispatch error: {e}")

    # 2. MSG91 Integration
    msg91_auth = os.environ.get("MSG91_AUTH_KEY", "").strip()
    msg91_template = os.environ.get("MSG91_TEMPLATE_ID", "").strip()
    if msg91_auth and msg91_template:
        try:
            url = "https://api.msg91.com/api/v5/otp"
            headers = {"authkey": msg91_auth, "Content-Type": "application/json"}
            payload = {
                "template_id": msg91_template,
                "mobile": f"91{raw_mobile}",
                "otp": otp
            }
            res = requests.post(url, headers=headers, json=payload, timeout=8)
            if res.status_code == 200 and res.json().get("type") == "success":
                logger.info(f"MSG91 OTP sent successfully to {masked_mobile}")
                return True, f"OTP sent to {masked_mobile} via SMS."
            else:
                logger.warning(f"MSG91 returned error: {res.text}. Falling back to dev mock.")
        except Exception as e:
            logger.error(f"MSG91 dispatch error: {e}")

    # 3. Twilio Integration
    twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
    twilio_token = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
    twilio_from = os.environ.get("TWILIO_PHONE_NUMBER", "").strip()
    if twilio_sid and twilio_token and twilio_from:
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
            data = {
                "From": twilio_from,
                "To": full_mobile,
                "Body": message
            }
            res = requests.post(url, data=data, auth=(twilio_sid, twilio_token), timeout=8)
            if res.status_code in [200, 201]:
                logger.info(f"Twilio OTP sent successfully to {masked_mobile}")
                return True, f"OTP sent to {masked_mobile} via SMS."
            else:
                logger.warning(f"Twilio returned error: {res.text}. Falling back to dev mock.")
        except Exception as e:
            logger.error(f"Twilio dispatch error: {e}")

    # 4. Development Mock Mode (Clear Terminal Logging)
    print("\n" + "=" * 64)
    print(f" [DEV MOCK OTP for +91{masked_mobile}]: {otp} ")
    print(" (Expires in 5 minutes | 30s resend cooldown)")
    print("=" * 64 + "\n")

    return True, f"OTP sent to {masked_mobile} (Development Mock Mode)"
