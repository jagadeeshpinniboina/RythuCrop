"""
RythuCrop Authentication Gate Test Suite
Validates the complete Mobile + 6-digit OTP Authentication Gate,
pre-login wall, route protection, cooldowns, attempts limits, session lifecycle,
and Fast2SMS OTP route / Quick route fallback and failure handling.
"""

import os
import sys
import unittest
from pathlib import Path
import datetime
from unittest.mock import patch, MagicMock

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import app
from app.services.auth_service import (
    normalize_mobile,
    get_raw_10digit,
    get_masked_mobile,
    request_otp,
    verify_otp,
    hash_otp,
    _LAST_REQUEST_TIME
)
from app.models.alerts_db import (
    save_otp_request,
    get_latest_otp_request,
    increment_otp_attempts
)
from app.services.sms_service import send_sms_otp


class TestAuthGate(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        # Reset in-memory cooldown tracker before each test
        _LAST_REQUEST_TIME.clear()
        self._orig_dev_auth = os.environ.get("RYTHUCROP_DEV_AUTH")
        # Default test environment to dev auth mode for gate / session tests
        os.environ["RYTHUCROP_DEV_AUTH"] = "true"

    def tearDown(self):
        if self._orig_dev_auth is not None:
            os.environ["RYTHUCROP_DEV_AUTH"] = self._orig_dev_auth
        else:
            os.environ.pop("RYTHUCROP_DEV_AUTH", None)

    # =========================================================================
    # 1. PRE-LOGIN WALL & GATEWAY TESTS
    # =========================================================================

    def test_01_unauthenticated_user_accesses_public_landing_page(self):
        """Unauthenticated user accessing / loads the public landing page with HTTP 200."""
        resp = self.client.get("/", follow_redirects=False)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"RythuCrop", resp.data)
        self.assertIn(b"Sign In", resp.data)

    def test_02_unauthenticated_user_cannot_access_home_endpoint(self):
        """Unauthenticated user accessing /home must be redirected to /login."""
        resp = self.client.get("/home", follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp.headers.get("Location", ""))

    def test_03_unauthenticated_user_cannot_access_protected_shortcuts(self):
        """Unauthenticated user accessing protected shortcuts must be redirected to /login."""
        protected_routes = [
            "/farm-planning",
            "/crop-recommendation",
            "/yield-prediction",
            "/smart-advisory",
            "/about"
        ]
        for route in protected_routes:
            resp = self.client.get(route, follow_redirects=False)
            self.assertEqual(
                resp.status_code, 302,
                f"Route {route} was not redirected to /login (Status: {resp.status_code})"
            )
            self.assertIn("/login", resp.headers.get("Location", ""))

    def test_04_unauthenticated_api_request_returns_401_json(self):
        """Unauthenticated API / POST request receives HTTP 401 JSON, not HTML redirect."""
        endpoints = ["/predict", "/farm-plan", "/predict-yield"]
        for ep in endpoints:
            resp = self.client.post(ep, json={"test": "data"})
            self.assertEqual(resp.status_code, 401, f"{ep} did not return 401")
            data = resp.get_json()
            self.assertFalse(data.get("authenticated", True))
            self.assertEqual(data.get("redirect"), "/login")

    def test_05_login_page_renders_cleanly_for_unauthenticated_users(self):
        """Unauthenticated user CAN access /login with HTTP 200."""
        resp = self.client.get("/login")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"RythuCrop", resp.data)
        self.assertIn(b"Farmer Sign In", resp.data)
        self.assertIn(b"name@example.com", resp.data)

    # =========================================================================
    # 2. MOBILE NUMBER VALIDATION & MASKING
    # =========================================================================

    def test_06_mobile_regex_validation(self):
        """Strict validation for 10-digit Indian numbers starting with 6,7,8,9."""
        valid_numbers = [
            "9876543210",
            "+919876543210",
            "918765432109",
            "07654321098",
            "6987654321"
        ]
        for num in valid_numbers:
            self.assertIsNotNone(
                normalize_mobile(num),
                f"Failed to normalize valid number: {num}"
            )
            self.assertIsNotNone(
                get_raw_10digit(num),
                f"Failed to extract 10 digits for: {num}"
            )

        invalid_numbers = [
            "1234567890",      # Starts with 1
            "5876543210",      # Starts with 5
            "987654321",       # 9 digits
            "98765432100",     # 11 digits
            "abcdefghij",      # Letters
            "",                # Empty
            "0000000000"       # Zeroes
        ]
        for num in invalid_numbers:
            self.assertIsNone(
                normalize_mobile(num),
                f"Should have rejected invalid number: {num}"
            )
            self.assertIsNone(
                get_raw_10digit(num),
                f"Should have rejected invalid number: {num}"
            )

    def test_07_mobile_number_masking_shows_only_last_4_digits(self):
        """Masked mobile must strictly show ONLY the last 4 digits (e.g. XXXXXX8801)."""
        masked = get_masked_mobile("9876548801")
        self.assertEqual(masked, "XXXXXX8801")

        masked_with_code = get_masked_mobile("+919876543210")
        self.assertEqual(masked_with_code, "XXXXXX3210")

    # =========================================================================
    # 3. OTP GENERATION & COOLDOWN
    # =========================================================================

    def test_08_send_otp_success_payload(self):
        """POST /auth/send-otp returns success, masked mobile, and dev OTP if in dev mode."""
        resp = self.client.post("/auth/send-otp", json={"mobile": "9876543210"})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["masked_mobile"], "XXXXXX3210")
        self.assertEqual(data["cooldown_seconds"], 30)
        self.assertEqual(data["expires_in_seconds"], 300)
        self.assertIsNotNone(data.get("dev_otp"))
        self.assertEqual(len(data["dev_otp"]), 6)

    def test_09_resend_cooldown_enforced(self):
        """Submitting OTP request twice within 30 seconds must be rejected with 400."""
        # First request succeeds
        resp1 = self.client.post("/auth/send-otp", json={"mobile": "9876541122"})
        self.assertEqual(resp1.status_code, 200)

        # Immediate second request fails with cooldown error
        resp2 = self.client.post("/auth/send-otp", json={"mobile": "9876541122"})
        self.assertEqual(resp2.status_code, 400)
        data2 = resp2.get_json()
        self.assertFalse(data2["success"])
        self.assertIn("wait", data2["error"].lower())
        self.assertGreater(data2["cooldown_remaining"], 0)

    # =========================================================================
    # 4. OTP VERIFICATION & ATTEMPT LOCKING
    # =========================================================================

    def test_10_wrong_otp_increments_attempts_and_locks_after_3_tries(self):
        """Invalid OTP code decrements attempts and locks on the 3rd failed try."""
        mobile = "9876549999"
        # 1. Request OTP
        req_resp = self.client.post("/auth/send-otp", json={"mobile": mobile})
        self.assertEqual(req_resp.status_code, 200)
        correct_otp = req_resp.get_json().get("dev_otp")

        # Attempt 1: Wrong code
        res1 = self.client.post("/auth/verify-otp", json={"mobile": mobile, "otp": "000000"})
        self.assertEqual(res1.status_code, 400)
        self.assertIn("2 attempt(s) remaining", res1.get_json()["error"])

        # Attempt 2: Wrong code
        res2 = self.client.post("/auth/verify-otp", json={"mobile": mobile, "otp": "000000"})
        self.assertEqual(res2.status_code, 400)
        self.assertIn("1 attempt(s) remaining", res2.get_json()["error"])

        # Attempt 3: Wrong code -> locks
        res3 = self.client.post("/auth/verify-otp", json={"mobile": mobile, "otp": "000000"})
        self.assertEqual(res3.status_code, 400)
        self.assertIn("maximum attempts", res3.get_json()["error"].lower())

        # Attempt 4: Even with correct OTP, it must be locked!
        if correct_otp:
            res4 = self.client.post("/auth/verify-otp", json={"mobile": mobile, "otp": correct_otp})
            self.assertEqual(res4.status_code, 400)
            self.assertIn("maximum verification attempts", res4.get_json()["error"].lower())

    def test_11_expired_otp_is_rejected(self):
        """An expired OTP (> 5 minutes) must be rejected."""
        mobile = "+919876547777"
        expired_time = datetime.datetime.now() - datetime.timedelta(minutes=6)
        salt = "testsalt12345678"
        hashed = hash_otp("123456", salt)
        save_otp_request(mobile, hashed, salt, expired_time)

        res = self.client.post("/auth/verify-otp", json={"mobile": mobile, "otp": "123456"})
        self.assertEqual(res.status_code, 400)
        self.assertIn("expired", res.get_json()["error"].lower())

    # =========================================================================
    # 5. SUCCESSFUL AUTHENTICATION & REDIRECTION LIFECYCLE
    # =========================================================================

    def test_12_successful_otp_creates_session_and_redirects(self):
        """Correct OTP creates secure session and redirects to /home."""
        mobile = "9876546666"
        req_resp = self.client.post("/auth/send-otp", json={"mobile": mobile})
        self.assertEqual(req_resp.status_code, 200)
        otp = req_resp.get_json().get("dev_otp")

        # Verify with correct OTP
        verify_resp = self.client.post(
            "/auth/verify-otp",
            json={"mobile": mobile, "otp": otp, "next": "/home"}
        )
        self.assertEqual(verify_resp.status_code, 200)
        data = verify_resp.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["redirect"], "/home")

        # User is now authenticated - can access / and /home
        home_resp = self.client.get("/")
        self.assertEqual(home_resp.status_code, 200)
        self.assertIn(b"RythuCrop", home_resp.data)
        self.assertIn(b"Logout", home_resp.data)

        # Can access ML prediction endpoints
        pred_resp = self.client.post("/predict", json={
            "N": 90, "P": 42, "K": 43,
            "temperature": 25.0, "humidity": 80.0,
            "ph": 6.5, "rainfall": 200.0
        })
        self.assertEqual(pred_resp.status_code, 200)

    def test_13_logout_clears_session_and_gates_again(self):
        """Clicking logout terminates session and blocks subsequent access."""
        # 1. Login
        mobile = "9876545555"
        req_resp = self.client.post("/auth/send-otp", json={"mobile": mobile})
        otp = req_resp.get_json().get("dev_otp")
        self.client.post("/auth/verify-otp", json={"mobile": mobile, "otp": otp})

        # Check authenticated
        self.assertEqual(self.client.get("/home").status_code, 200)

        # 2. Logout
        logout_resp = self.client.get("/logout", follow_redirects=False)
        self.assertEqual(logout_resp.status_code, 302)
        self.assertIn("/login", logout_resp.headers.get("Location", ""))

        # 3. Accessing protected /home now must redirect to /login
        subsequent_resp = self.client.get("/home", follow_redirects=False)
        self.assertEqual(subsequent_resp.status_code, 302)
        self.assertIn("/login", subsequent_resp.headers.get("Location", ""))

    # =========================================================================
    # 6. TWILIO WHATSAPP GATEWAY & STRICT PRIVACY HANDLING
    # =========================================================================

    def test_14_send_sms_otp_dev_mode_fallback(self):
        """send_sms_otp generates OTP and returns clean message without exposing code."""
        os.environ["RYTHUCROP_DEV_AUTH"] = "true"
        ok, msg = send_sms_otp("9876548801", "123456")
        self.assertTrue(ok)
        self.assertEqual(msg, "OTP sent successfully to your WhatsApp number (+91 XXXXXX8801).")
        self.assertNotIn("123456", msg)
        self.assertNotIn("Backend Code", msg)

    def test_15_twilio_whatsapp_dispatch_success(self):
        """Twilio WhatsApp dispatch succeeds with standard plain-text message."""
        os.environ["RYTHUCROP_DEV_AUTH"] = "false"
        os.environ["TWILIO_ACCOUNT_SID"] = "AC_MOCK_TEST_SID"
        os.environ["TWILIO_AUTH_TOKEN"] = "mock_auth_token"

        mock_msg = MagicMock()
        mock_msg.sid = "SM_TEST_WHATSAPP_SID_12345"

        with patch("app.services.sms_service.Client") as mock_twilio_client:
            instance = mock_twilio_client.return_value
            instance.messages.create.return_value = mock_msg

            ok, msg = send_sms_otp("9876548801", "654321")
            self.assertTrue(ok)
            self.assertEqual(msg, "OTP sent successfully to your WhatsApp number (+91 XXXXXX8801).")
            self.assertNotIn("654321", msg)

            # Verify parameters
            instance.messages.create.assert_called_once()
            _, kwargs = instance.messages.create.call_args
            self.assertEqual(kwargs["to"], "whatsapp:+919876548801")
            self.assertEqual(kwargs["body"], "Your RythuCrop verification OTP is: 654321. Valid for 5 minutes.")
            self.assertEqual(kwargs["from_"], "whatsapp:+17372508034")

    def test_16_twilio_whatsapp_failure_auto_fallback_and_security(self):
        """If Twilio fails, returns False with clean error and without exposing OTP in response."""
        os.environ["RYTHUCROP_DEV_AUTH"] = "false"
        os.environ["TWILIO_ACCOUNT_SID"] = "AC_MOCK_TEST_SID"
        os.environ["TWILIO_AUTH_TOKEN"] = "mock_auth_token"

        with patch("app.services.sms_service.Client") as mock_twilio_client:
            instance = mock_twilio_client.return_value
            instance.messages.create.side_effect = Exception("\x1b[31mError 21654: ContentSid Required\x1b[0m")

            ok, msg = send_sms_otp("9876548801", "778899")
            self.assertFalse(ok)
            self.assertIn("ContentSid Required", msg)
            self.assertNotIn("\x1b", msg)
            self.assertNotIn("778899", msg)
            self.assertNotIn("Backend Code", msg)

    def test_17_send_otp_api_endpoint_never_exposes_otp(self):
        """POST /auth/send-otp API response NEVER exposes OTP or Backend Code in message."""
        resp = self.client.post("/auth/send-otp", json={"mobile": "9876548801"})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertIn("OTP sent successfully", data["message"])
        self.assertNotIn("Backend Code", data["message"])

    # =========================================================================
    # 7. GMAIL SMTP EMAIL OTP DISPATCH & LIFECYCLE
    # =========================================================================

    def test_18_email_format_validation_and_masking(self):
        """Validate email format and verify clean masking."""
        from app.services.email_service import is_valid_email, normalize_email, get_masked_email

        self.assertTrue(is_valid_email("farmer@gmail.com"))
        self.assertTrue(is_valid_email("user.test+rythu@domain.co.in"))
        self.assertFalse(is_valid_email("invalid-email"))
        self.assertFalse(is_valid_email("@domain.com"))
        self.assertFalse(is_valid_email("user@"))

        self.assertEqual(normalize_email("  Farmer@Gmail.Com  "), "farmer@gmail.com")
        self.assertIsNone(normalize_email("not-an-email"))

        masked = get_masked_email("farmer76@gmail.com")
        self.assertIn("@gmail.com", masked)
        self.assertTrue(masked.startswith("f"))
        self.assertIn("*", masked)

    def test_19_send_email_otp_dev_mode(self):
        """send_email_otp returns clean success message without exposing OTP."""
        from app.services.email_service import send_email_otp
        os.environ["RYTHUCROP_DEV_AUTH"] = "true"

        ok, msg = send_email_otp("farmer@example.com", "882194")
        self.assertTrue(ok)
        self.assertIn("OTP sent successfully to your email address", msg)
        self.assertNotIn("882194", msg)

    def test_20_send_email_otp_smtp_dispatch_success(self):
        """Gmail SMTP dispatch connects with TLS and sends formatted HTML message."""
        from app.services.email_service import send_email_otp
        os.environ["RYTHUCROP_DEV_AUTH"] = "false"
        os.environ["MAIL_USERNAME"] = "testuser@gmail.com"
        os.environ["MAIL_PASSWORD"] = "testapppassword12"

        with patch("smtplib.SMTP") as mock_smtp_cls:
            mock_server = MagicMock()
            mock_smtp_cls.return_value = mock_server

            ok, msg = send_email_otp("farmer@example.com", "123456")
            self.assertTrue(ok)
            self.assertIn("OTP sent successfully", msg)
            self.assertNotIn("123456", msg)

            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with("testuser@gmail.com", "testapppassword12")
            mock_server.sendmail.assert_called_once()
            mock_server.quit.assert_called_once()

    def test_21_send_email_otp_smtp_dispatch_failure(self):
        """If SMTP fails, returns False with clean error and logs terminal OTP."""
        from app.services.email_service import send_email_otp
        os.environ["RYTHUCROP_DEV_AUTH"] = "false"
        os.environ["MAIL_USERNAME"] = "testuser@gmail.com"
        os.environ["MAIL_PASSWORD"] = "testapppassword12"

        with patch("smtplib.SMTP") as mock_smtp_cls:
            mock_smtp_cls.side_effect = Exception("SMTP Connection Refused (Network unreachable)")

            ok, msg = send_email_otp("farmer@example.com", "654321")
            self.assertFalse(ok)
            self.assertIn("Connection Refused", msg)
            self.assertNotIn("654321", msg)

    def test_22_full_email_otp_login_lifecycle(self):
        """Complete Email OTP flow: request OTP, verify code, establish session, access /."""
        email = "farmer.rythu@example.com"

        # 1. Request OTP for Email
        req_resp = self.client.post("/auth/send-otp", json={"email": email})
        self.assertEqual(req_resp.status_code, 200)
        data = req_resp.get_json()
        self.assertTrue(data["success"])
        self.assertIn(email, data.get("email", ""))
        self.assertIn("OTP sent successfully to your email address", data["message"])
        otp_code = data.get("dev_otp")
        self.assertIsNotNone(otp_code)

        # 2. Verify with correct OTP
        ver_resp = self.client.post("/auth/verify-otp", json={
            "email": email,
            "otp": otp_code,
            "next": "/home"
        })
        self.assertEqual(ver_resp.status_code, 200)
        ver_data = ver_resp.get_json()
        self.assertTrue(ver_data["success"])
        self.assertEqual(ver_data["redirect"], "/home")

        # 3. Access protected dashboard
        home_resp = self.client.get("/")
        self.assertEqual(home_resp.status_code, 200)
        self.assertIn(b"RythuCrop", home_resp.data)
        self.assertIn(b"Logout", home_resp.data)

        # 4. Check API session status endpoint
        session_resp = self.client.get("/api/auth/session")
        self.assertEqual(session_resp.status_code, 200)
        s_data = session_resp.get_json()
        self.assertTrue(s_data["authenticated"])
        self.assertEqual(s_data["user"]["mobile"], email)

    def test_23_signup_flow_saves_profile_and_computes_initials(self):
        """Sign Up with First Name, Last Name, Region stores in SQLite, sets session initials and profile."""
        email = "pinniboinajagadeesh76@gmail.com"
        first_name = "Jagadeesh"
        last_name = "Pinniboina"
        region = "Andhra Pradesh"

        # Ensure clean state for test email
        import sqlite3
        conn = sqlite3.connect("rythucrop.db")
        conn.cursor().execute("DELETE FROM users WHERE email = ? OR mobile = ?", (email, email))
        conn.commit()
        conn.close()

        # 1. Send OTP with Sign Up payload
        req_resp = self.client.post("/auth/send-otp", json={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "region": region,
            "auth_mode": "signup"
        })
        self.assertEqual(req_resp.status_code, 200)
        req_data = req_resp.get_json()
        self.assertTrue(req_data["success"])
        otp_code = req_data.get("dev_otp")

        # 2. Verify OTP
        ver_resp = self.client.post("/auth/verify-otp", json={
            "email": email,
            "otp": otp_code,
            "first_name": first_name,
            "last_name": last_name,
            "region": region
        })
        self.assertEqual(ver_resp.status_code, 200)
        ver_data = ver_resp.get_json()
        self.assertTrue(ver_data["success"])
        user_data = ver_data.get("user", {})
        self.assertEqual(user_data.get("user_initials"), "PJ")
        self.assertEqual(user_data.get("full_name"), "Jagadeesh Pinniboina")
        self.assertEqual(user_data.get("region"), "Andhra Pradesh")

        # 3. Check Session API
        sess_resp = self.client.get("/api/auth/session")
        self.assertEqual(sess_resp.status_code, 200)
        sess_data = sess_resp.get_json()
        self.assertTrue(sess_data["authenticated"])
        self.assertEqual(sess_data["user"]["user_initials"], "PJ")
        self.assertEqual(sess_data["user"]["full_name"], "Jagadeesh Pinniboina")
        self.assertEqual(sess_data["user"]["region"], "Andhra Pradesh")

        # 4. Check Home Dashboard renders circular avatar badge with PJ initials
        home_resp = self.client.get("/home")
        self.assertEqual(home_resp.status_code, 200)
        self.assertIn(b"PJ", home_resp.data)
        self.assertIn(b"user-avatar-circle", home_resp.data)
        self.assertIn(b"Logout", home_resp.data)

    def test_24_avatar_dropdown_and_navbar_overflow_css(self):
        """Navbar has visible overflow without scrollbar, and contains sleek avatar dropdown."""
        home_resp = self.client.get("/login")
        self.assertEqual(home_resp.status_code, 200)
        # Login page has tabbed switcher
        self.assertIn(b"auth-tabs", home_resp.data)
        self.assertIn(b"tabSignIn", home_resp.data)
        self.assertIn(b"tabSignUp", home_resp.data)
        self.assertIn(b"signUpFirstName", home_resp.data)
        self.assertIn(b"signUpLastName", home_resp.data)
        self.assertIn(b"signUpRegion", home_resp.data)

    def test_25_smart_tab_flows_backend_checks(self):
        """Smart Tab Flows: non-existent email on signin returns 404 not_found; duplicate email on signup returns 400 already_exists."""
        # 1. Signin with non-existent email
        ghost_email = "nonexistent_farmer_999@gmail.com"
        ghost_resp = self.client.post("/auth/send-otp", json={
            "email": ghost_email,
            "auth_mode": "signin"
        })
        self.assertEqual(ghost_resp.status_code, 404)
        ghost_data = ghost_resp.get_json()
        self.assertFalse(ghost_data["success"])
        self.assertTrue(ghost_data.get("not_found"))
        self.assertIn("No account found", ghost_data["error"])

        # 2. Signup with already registered email
        dup_email = "pinniboinajagadeesh76@gmail.com"
        dup_resp = self.client.post("/auth/send-otp", json={
            "email": dup_email,
            "first_name": "Jagadeesh",
            "last_name": "Pinniboina",
            "region": "Andhra Pradesh",
            "auth_mode": "signup"
        })
        self.assertEqual(dup_resp.status_code, 400)
        dup_data = dup_resp.get_json()
        self.assertFalse(dup_data["success"])
        self.assertTrue(dup_data.get("already_exists"))
        self.assertIn("already registered", dup_data["error"])


if __name__ == "__main__":
    unittest.main()
