"""
RythuCrop Gmail SMTP Email OTP Dispatcher Module
Dispatches 6-digit verification codes via Gmail SMTP (or any standard SMTP server)
using Python's built-in smtplib and email.mime modules.
Supports clean HTML styling, TLS encryption, graceful exception logging,
and terminal secret OTP fallback.
"""

import os
import re
import smtplib
import logging
from typing import Tuple, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger("rythucrop.email")

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


def is_valid_email(email: str) -> bool:
    """Validate standard email format."""
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def normalize_email(email_raw: str) -> Optional[str]:
    """Strip whitespace and lowercase email."""
    if not email_raw:
        return None
    cleaned = str(email_raw).strip().lower()
    if is_valid_email(cleaned):
        return cleaned
    return None


def get_masked_email(email_raw: str) -> str:
    """
    Mask email address for farmer privacy.
    E.g. farmer.rythu@gmail.com -> f***u@gmail.com
    """
    norm = normalize_email(email_raw)
    if not norm or "@" not in norm:
        return "user@example.com"
    user_part, domain_part = norm.split("@", 1)
    if len(user_part) <= 2:
        masked_user = user_part[0] + "*"
    else:
        masked_user = user_part[0] + ("*" * min(len(user_part) - 2, 4)) + user_part[-1]
    return f"{masked_user}@{domain_part}"


def is_email_configured() -> bool:
    """Check if Gmail / SMTP credentials are fully provided."""
    dev_auth = os.environ.get("RYTHUCROP_DEV_AUTH", "false").lower() == "true"
    if dev_auth:
        return False
    username = os.getenv("MAIL_USERNAME", "").strip()
    password = os.getenv("MAIL_PASSWORD", "").strip()
    return bool(username and password)


def send_email_otp(recipient_email: str, otp_code: str) -> Tuple[bool, str]:
    """
    Dispatches 6-digit OTP to recipient_email via Gmail SMTP.
    
    - Host: os.getenv("MAIL_SERVER", "smtp.gmail.com")
    - Port: int(os.getenv("MAIL_PORT", 587))
    - Login: os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD")
    - TLS: server.starttls()
    - Subject: "RythuCrop Verification Code"
    - Body: Clean HTML message stating: "Your RythuCrop verification code is {otp_code}. Valid for 5 minutes."
    - Handles exceptions cleanly, logs errors, and logs secret console OTP if network fails.
    """
    norm_email = normalize_email(recipient_email)
    if not norm_email:
        return False, "Invalid email address format. Please enter a valid email."

    masked = get_masked_email(norm_email)
    success_msg = "OTP sent successfully to your email address."

    host = os.getenv("MAIL_SERVER", "smtp.gmail.com").strip()
    try:
        port = int(os.getenv("MAIL_PORT", "587").strip())
    except ValueError:
        port = 587

    username = os.getenv("MAIL_USERNAME", "").strip()
    password = os.getenv("MAIL_PASSWORD", "").strip()

    # In dev mode or when credentials are not configured, log OTP to console
    if not is_email_configured():
        print(f"[EMAIL NOTICE] Dev mode active or Gmail SMTP credentials not configured.")
        print(f"[SECRET TERMINAL OTP]: {otp_code}")
        return True, success_msg

    print(f"[EMAIL DISPATCH] Attempting Gmail SMTP dispatch to {norm_email} via {host}:{port} with user: {username}...")

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "RythuCrop Verification Code"
        msg["From"] = f"RythuCrop <{username}>"
        msg["To"] = norm_email

        plain_text = f"Your RythuCrop verification code is {otp_code}. Valid for 5 minutes."

        html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4fbf6; margin: 0; padding: 20px; }}
    .card {{ max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 14px; padding: 32px; border: 1px solid #dcfce7; box-shadow: 0 4px 16px rgba(0,0,0,0.06); }}
    .header {{ text-align: center; margin-bottom: 24px; }}
    .logo {{ font-size: 26px; font-weight: 800; color: #15803d; }}
    .otp-box {{ background: #f0fdf4; border: 2px dashed #22c55e; border-radius: 12px; padding: 18px; text-align: center; margin: 24px 0; }}
    .otp-code {{ font-size: 34px; font-weight: 800; letter-spacing: 8px; color: #166534; }}
    .footer {{ font-size: 12px; color: #64748b; text-align: center; margin-top: 24px; border-top: 1px solid #f1f5f9; padding-top: 16px; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="logo">🌾 RythuCrop</div>
      <p style="color: #475569; font-size: 14px; margin-top: 4px;">Smart Agriculture Decision Platform</p>
    </div>
    <p style="font-size: 15px; color: #334155;">Hello,</p>
    <p style="font-size: 15px; color: #334155;">Your RythuCrop verification code is:</p>
    <div class="otp-box">
      <span class="otp-code">{otp_code}</span>
    </div>
    <p style="font-size: 14px; color: #475569; text-align: center;">Valid for <strong>5 minutes</strong>. Do not share this code with anyone.</p>
    <div class="footer">
      <p>If you did not request this verification code, please ignore this email.</p>
      <p>&copy; 2026 RythuCrop — Government & ICAR Verified Agri Portal</p>
    </div>
  </div>
</body>
</html>"""

        msg.attach(MIMEText(plain_text, "plain", "utf-8"))
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        server = smtplib.SMTP(host, port, timeout=12)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        server.sendmail(username, [norm_email], msg.as_string())
        server.quit()

        print(f"[EMAIL SUCCESS] Verification email sent to {norm_email}")
        print(f"[SECRET TERMINAL OTP]: {otp_code}")
        return True, success_msg

    except Exception as e:
        err_msg = str(e).strip()
        print(f"[EMAIL ERROR DETAILS]: {err_msg}")
        print(f"[SECRET TERMINAL OTP]: {otp_code}")
        # Return fallback with clear notification
        return False, f"Unable to send email OTP: {err_msg}"
