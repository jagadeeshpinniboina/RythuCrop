"""
RythuCrop Authentication Blueprint
Handles /login page rendering, OTP sending, OTP verification, session management,
and logout redirection.
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.auth_service import (
    request_otp,
    verify_otp,
    normalize_mobile,
    get_raw_10digit,
    get_masked_mobile
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET"])
def login():
    """
    Login page gateway.
    If already authenticated, redirect to /home or next target.
    If unauthenticated, render the dedicated farmer login screen.
    """
    if session.get("is_authenticated"):
        next_target = request.args.get("next")
        if next_target and next_target.startswith("/") and not next_target.startswith("//"):
            return redirect(next_target)
        return redirect(url_for("main.home"))

    next_url = request.args.get("next", "")
    return render_template("login.html", next=next_url)


@auth_bp.route("/auth/send-otp", methods=["POST"])
@auth_bp.route("/api/auth/request-otp", methods=["POST"])
def send_otp():
    """
    Step 1 -> Step 2 transition:
    Accepts 10-digit Indian mobile number, triggers OTP generation,
    stores salted SHA-256 hash, and sends OTP via SMS or dev mock mode.
    """
    data = request.get_json() or {}
    mobile_input = data.get("mobile", "").strip()

    if not mobile_input:
        return jsonify({
            "success": False,
            "error": "Mobile number is required. Please enter a valid 10-digit number."
        }), 400

    success, msg, extra = request_otp(mobile_input)
    if not success:
        return jsonify({
            "success": False,
            "error": msg,
            "cooldown_remaining": (extra or {}).get("cooldown_remaining", 0)
        }), 400

    return jsonify({
        "success": True,
        "message": msg,
        "data": extra,
        "mobile": extra.get("mobile"),
        "masked_mobile": extra.get("masked_mobile"),
        "dev_mode": extra.get("dev_mode", False),
        "dev_otp": extra.get("dev_otp"),
        "cooldown_seconds": extra.get("cooldown_seconds", 30),
        "expires_in_seconds": extra.get("expires_in_seconds", 300)
    })


@auth_bp.route("/auth/verify-otp", methods=["POST"])
@auth_bp.route("/api/auth/verify-otp", methods=["POST"])
def verify_otp_endpoint():
    """
    Step 2 verification:
    Validates 6-digit OTP code against salted SHA-256 hash.
    Enforces 5-minute expiry and 3-attempt maximum.
    Initializes Flask session upon success.
    """
    data = request.get_json() or {}
    mobile_input = data.get("mobile", "").strip()
    otp_input = data.get("otp", "").strip()
    lang = data.get("preferred_lang", session.get("preferred_lang", "en"))
    next_url = data.get("next", "")

    if not mobile_input or not otp_input:
        return jsonify({
            "success": False,
            "error": "Both mobile number and 6-digit OTP are required."
        }), 400

    success, msg, user = verify_otp(mobile_input, otp_input, lang)
    if not success:
        return jsonify({
            "success": False,
            "error": msg
        }), 400

    # Initialize secure Flask session
    session.permanent = True
    session["user_id"] = user["mobile"]
    session["mobile"] = user["mobile"]
    session["masked_mobile"] = get_masked_mobile(user["mobile"])
    session["is_authenticated"] = True
    session["preferred_lang"] = user.get("preferred_language", "en")

    # Safe redirection
    redirect_target = "/home"
    if next_url and next_url.startswith("/") and not next_url.startswith("//") and next_url != "/login":
        redirect_target = next_url

    return jsonify({
        "success": True,
        "message": "Login successful. Welcome to RythuCrop!",
        "redirect": redirect_target,
        "user": {
            "mobile": user["mobile"],
            "masked_mobile": session["masked_mobile"],
            "preferred_lang": session["preferred_lang"]
        }
    })


@auth_bp.route("/logout", methods=["GET"])
@auth_bp.route("/auth/logout", methods=["POST", "GET"])
@auth_bp.route("/api/auth/logout", methods=["POST", "GET"])
def logout():
    """
    Terminates user session and redirects to /login.
    Supports both browser link clicks and AJAX calls.
    """
    session.clear()

    if request.is_json or request.method == "POST":
        return jsonify({
            "success": True,
            "message": "Logged out successfully",
            "redirect": "/login"
        })

    return redirect(url_for("auth.login"))


@auth_bp.route("/api/auth/session", methods=["GET"])
def session_status():
    """Returns current authentication state."""
    if session.get("is_authenticated"):
        return jsonify({
            "authenticated": True,
            "user": {
                "user_id": session.get("user_id"),
                "mobile": session.get("mobile"),
                "masked_mobile": session.get("masked_mobile") or get_masked_mobile(session.get("mobile", "")),
                "preferred_lang": session.get("preferred_lang", "en")
            }
        })
    return jsonify({
        "authenticated": False,
        "user": None
    })
