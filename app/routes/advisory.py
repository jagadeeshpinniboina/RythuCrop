# -*- coding: utf-8 -*-
"""
RythuCrop - Smart Advisory Route
Provides authenticated cultivation advisory endpoints.
"""
from flask import request, jsonify, session
from app import app
from app.services.auth_service import login_required
from app.data.agri_taxonomy import CROP_CATALOGUE


@app.route("/api/advisory", methods=["GET", "POST"])
@app.route("/api/crop-advisory", methods=["GET", "POST"])
@app.route("/advisory/data", methods=["GET", "POST"])
@login_required
def advisory_api():
    """
    Smart Advisory API Endpoint - strictly requires active user authentication.
    Rejects unauthenticated requests with HTTP 401.
    """
    if not (session.get("is_authenticated") and (session.get("user_id") or session.get("email"))):
        return jsonify({
            "status": "error",
            "message": "Authentication required. Please login with your Email.",
            "error": "Authentication required. Please login with your Email.",
            "authenticated": False,
            "redirect": "/login"
        }), 401

    data = request.get_json(silent=True) or {}
    crop = request.args.get("crop") or data.get("crop") or "rice"
    lang = request.args.get("lang") or data.get("lang") or "en"
    priority = request.args.get("priority") or data.get("priority") or "care"

    cat_entry = CROP_CATALOGUE.get(crop, {})
    tips = cat_entry.get("advisory_tips", {})

    return jsonify({
        "status": "success",
        "authenticated": True,
        "crop": crop,
        "lang": lang,
        "priority": priority,
        "advisory": tips,
        "message": "Advisory verified successfully."
    })
