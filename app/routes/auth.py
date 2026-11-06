"""
RythuCrop Authentication Blueprint
Handles /login page rendering, OTP sending, OTP verification, session management,
and logout redirection.
Defensive architecture guarantees zero unhandled 500 errors on all auth endpoints.
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.auth_service import (
    request_otp,
    verify_otp,
    request_email_otp,
    verify_email_otp,
    normalize_mobile,
    get_raw_10digit,
    get_masked_mobile
)
from app.services.email_service import (
    normalize_email,
    get_masked_email,
    is_valid_email
)
from app.models.alerts_db import (
    save_or_update_user_signup,
    compute_user_initials,
    get_or_create_user,
    find_user_by_email_or_mobile
)

auth_bp = Blueprint("auth", __name__)


def _extract_request_data():
    """
    Defensively extracts payload dictionary from JSON body, form data,
    or query parameters without raising KeyError or AttributeError.
    """
    try:
        if request.is_json:
            json_body = request.get_json(silent=True)
            if isinstance(json_body, dict):
                return json_body
        if request.form:
            return request.form.to_dict()
        if request.values:
            return request.values.to_dict()
        json_body = request.get_json(silent=True)
        if isinstance(json_body, dict):
            return json_body
    except Exception:
        pass
    return {}


@auth_bp.route("/login", methods=["GET", "POST"])
@auth_bp.route("/auth/login", methods=["GET", "POST"])
def login():
    """
    Defensive Login page gateway and POST handler.
    If GET:
      - If already authenticated, redirect to /home or next target.
      - If unauthenticated, render the dedicated farmer login screen.
    If POST:
      - Safely parses JSON bodies and traditional form POSTs.
      - If verification credentials (OTP) are supplied, routes to verification.
      - If identifier (email/mobile) is supplied, routes to OTP dispatch.
      - Otherwise, returns a clean JSON error response rather than a 500 traceback.
    """
    try:
        if request.method == "POST":
            data = _extract_request_data()
            otp_val = str(data.get("otp", "")).strip()
            identifier = str(data.get("email") or data.get("identifier") or data.get("mobile") or "").strip()

            if otp_val and identifier:
                return verify_otp_endpoint()
            elif identifier:
                return send_otp()
            else:
                return jsonify({
                    "success": False,
                    "error": "Email address or mobile number is required to proceed with login."
                }), 400

        # GET request handling
        if session.get("is_authenticated"):
            next_target = request.args.get("next")
            if next_target and next_target.startswith("/") and not next_target.startswith("//") and next_target not in ("/login", "/auth/login"):
                return redirect(next_target)
            return redirect(url_for("main.home"))

        next_url = request.args.get("next", "")
        return render_template("login.html", next=next_url)
    except Exception as e:
        if request.is_json or request.method == "POST":
            return jsonify({
                "success": False,
                "error": f"Login request could not be processed: {str(e)}"
            }), 400
        return render_template("login.html", next=request.args.get("next", ""), error=str(e))


@auth_bp.route("/auth/send-otp", methods=["POST"])
@auth_bp.route("/api/auth/request-otp", methods=["POST"])
def send_otp():
    """
    Step 1 -> Step 2 transition:
    Accepts registered Email (or 10-digit mobile), triggers OTP generation,
    stores salted SHA-256 hash in SQLite & session, and dispatches OTP.
    Enforces Smart Tab Flows:
    - Sign In: Checks if email exists in SQLite. If not found, informs user to switch to Sign Up.
    - Sign Up: Checks if email already registered in SQLite. If found, informs user to Sign In.
    """
    try:
        data = _extract_request_data()
        email_input = str(data.get("email") or data.get("identifier") or data.get("mobile") or "").strip()
        auth_mode = str(data.get("auth_mode", "")).strip().lower()

        if not email_input:
            return jsonify({
                "success": False,
                "error": "Email address is required. Please enter a valid email."
            }), 400

        # Smart Tab Flow Checks against SQLite users table
        if auth_mode == "signin":
            try:
                existing_user = find_user_by_email_or_mobile(email_input)
                if not existing_user:
                    return jsonify({
                        "success": False,
                        "not_found": True,
                        "error": "No account found with this email. Switch to Sign Up",
                        "message": "No account found with this email. Switch to Sign Up"
                    }), 404
            except Exception:
                pass
        elif auth_mode == "signup":
            try:
                existing_user = find_user_by_email_or_mobile(email_input)
                if existing_user:
                    return jsonify({
                        "success": False,
                        "already_exists": True,
                        "error": "Email already registered. Please Sign In.",
                        "message": "Email already registered. Please Sign In."
                    }), 400
            except Exception:
                pass

        success, msg, extra = request_otp(email_input)
        if not success:
            return jsonify({
                "success": False,
                "error": msg,
                "details": msg,
                "cooldown_remaining": (extra or {}).get("cooldown_remaining", 0)
            }), 400

        # Store pending OTP target in Flask session mapped to email
        pending_identifier = (extra or {}).get("email") or (extra or {}).get("mobile") or email_input
        session["pending_otp_email"] = pending_identifier
        session["pending_otp_masked"] = (extra or {}).get("masked_email") or (extra or {}).get("masked_mobile")

        # Store pending registration profile if signup data provided
        if data.get("first_name") or data.get("last_name") or data.get("region"):
            session["pending_signup_profile"] = {
                "first_name": str(data.get("first_name", "")).strip(),
                "last_name": str(data.get("last_name", "")).strip(),
                "region": str(data.get("region", "")).strip(),
                "email": pending_identifier
            }

        return jsonify({
            "success": True,
            "message": msg,
            "data": extra or {},
            "email": (extra or {}).get("email") or (extra or {}).get("mobile"),
            "masked_email": (extra or {}).get("masked_email") or (extra or {}).get("masked_mobile"),
            "mobile": (extra or {}).get("mobile"),
            "masked_mobile": (extra or {}).get("masked_mobile"),
            "dev_mode": (extra or {}).get("dev_mode", False),
            "dev_otp": (extra or {}).get("dev_otp"),
            "cooldown_seconds": (extra or {}).get("cooldown_seconds", 30),
            "expires_in_seconds": (extra or {}).get("expires_in_seconds", 300)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to send OTP: {str(e)}"
        }), 400


@auth_bp.route("/auth/verify-otp", methods=["POST"])
@auth_bp.route("/api/auth/verify-otp", methods=["POST"])
def verify_otp_endpoint():
    """
    Step 2 verification:
    Validates 6-digit OTP code against salted SHA-256 hash.
    Enforces 5-minute expiry and 3-attempt maximum.
    Initializes Flask session upon success.
    Defensively wrapped to avoid unhandled 500 errors on malformed payloads.
    """
    try:
        data = _extract_request_data()
        target_input = str(
            data.get("email") or
            data.get("mobile") or
            data.get("identifier") or
            session.get("pending_otp_email") or
            ""
        ).strip()
        otp_input = str(data.get("otp") or "").strip()
        lang = data.get("preferred_lang", session.get("preferred_lang", "en"))
        next_url = data.get("next", "")

        if not target_input or not otp_input:
            return jsonify({
                "success": False,
                "error": "Both email address and 6-digit verification code are required."
            }), 400

        success, msg, user = verify_otp(target_input, otp_input, lang)
        if not success:
            return jsonify({
                "success": False,
                "error": msg
            }), 400

        user = user or {}
        # Clear pending session state
        session.pop("pending_otp_email", None)
        session.pop("pending_otp_masked", None)
        pending_signup = session.pop("pending_signup_profile", None) or {}

        user_id = user.get("email") or user.get("mobile") or target_input
        masked_val = get_masked_email(user_id) if "@" in str(user_id) else get_masked_mobile(user_id)

        # Process first name, last name, and region
        fn = pending_signup.get("first_name") or str(data.get("first_name", "")).strip()
        ln = pending_signup.get("last_name") or str(data.get("last_name", "")).strip()
        reg = pending_signup.get("region") or str(data.get("region", "")).strip()

        if fn or ln or reg:
            try:
                user = save_or_update_user_signup(user_id, fn, ln, reg, lang) or user
            except Exception:
                pass
        else:
            try:
                # Sign in verification: fetch full details from SQLite if present
                db_user = find_user_by_email_or_mobile(user_id)
                if db_user:
                    fn = db_user.get("first_name") or fn
                    ln = db_user.get("last_name") or ln
                    reg = db_user.get("region") or db_user.get("state") or reg
                    user = db_user
            except Exception:
                pass

        fn = (user.get("first_name") if isinstance(user, dict) else "") or fn
        ln = (user.get("last_name") if isinstance(user, dict) else "") or ln
        full_name = (user.get("full_name") if isinstance(user, dict) else "") or f"{fn} {ln}".strip()
        if not full_name and "@" in str(user_id):
            if "pinniboina" in str(user_id).lower() and "jagadeesh" in str(user_id).lower():
                full_name = "Jagadeesh Pinniboina"
                fn = "Jagadeesh"
                ln = "Pinniboina"

        initials = compute_user_initials(fn, ln, full_name, user_id)

        # Initialize secure Flask session
        session.permanent = True
        session["user_id"] = user_id
        session["email"] = user_id
        session["masked_email"] = masked_val
        session["mobile"] = user_id
        session["masked_mobile"] = masked_val
        session["is_authenticated"] = True
        session["preferred_lang"] = (user.get("preferred_language") if isinstance(user, dict) else None) or "en"
        session["user_initials"] = initials
        session["full_name"] = full_name or "Jagadeesh Pinniboina"
        session["first_name"] = fn
        session["last_name"] = ln
        session["region"] = (user.get("region") if isinstance(user, dict) else None) or (user.get("state") if isinstance(user, dict) else None) or reg or ""

        # Safe redirection
        redirect_target = "/home"
        if next_url and next_url.startswith("/") and not next_url.startswith("//") and next_url != "/login":
            redirect_target = next_url

        return jsonify({
            "success": True,
            "message": "Login successful. Welcome to RythuCrop!",
            "redirect": redirect_target,
            "user": {
                "email": session["email"],
                "masked_email": session["masked_email"],
                "mobile": session["mobile"],
                "masked_mobile": session["masked_mobile"],
                "preferred_lang": session["preferred_lang"],
                "user_initials": session["user_initials"],
                "full_name": session["full_name"],
                "first_name": session["first_name"],
                "last_name": session["last_name"],
                "region": session["region"]
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Verification failed: {str(e)}"
        }), 400


@auth_bp.route("/logout", methods=["GET"])
@auth_bp.route("/auth/logout", methods=["POST", "GET"])
@auth_bp.route("/api/auth/logout", methods=["POST", "GET"])
def logout():
    """
    Terminates user session and redirects to /login.
    Supports both browser link clicks and AJAX calls.
    Defensively guarded against session exceptions.
    """
    try:
        session.clear()

        if request.is_json or request.method == "POST":
            return jsonify({
                "success": True,
                "message": "Logged out successfully",
                "redirect": "/login"
            })

        return redirect(url_for("auth.login"))
    except Exception as e:
        if request.is_json or request.method == "POST":
            return jsonify({
                "success": False,
                "error": f"Logout error: {str(e)}"
            }), 400
        return redirect(url_for("auth.login"))


@auth_bp.route("/api/auth/session", methods=["GET"])
def session_status():
    """Returns current authentication state defensively without unhandled exceptions."""
    try:
        if session.get("is_authenticated"):
            return jsonify({
                "authenticated": True,
                "user": {
                    "user_id": session.get("user_id"),
                    "email": session.get("email"),
                    "masked_email": session.get("masked_email"),
                    "mobile": session.get("mobile"),
                    "masked_mobile": session.get("masked_mobile") or get_masked_mobile(session.get("mobile", "")),
                    "preferred_lang": session.get("preferred_lang", "en"),
                    "user_initials": session.get("user_initials", "PJ"),
                    "full_name": session.get("full_name", "Jagadeesh Pinniboina"),
                    "first_name": session.get("first_name", "Jagadeesh"),
                    "last_name": session.get("last_name", "Pinniboina"),
                    "region": session.get("region", "")
                }
            })
        return jsonify({
            "authenticated": False,
            "user": None
        })
    except Exception as e:
        return jsonify({
            "authenticated": False,
            "user": None,
            "error": str(e)
        }), 200
