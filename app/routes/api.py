"""
RythuCrop Agricultural REST APIs
Provides location, catalogue, mandi market prices, storage finder,
OTP authentication, and price alerts.
"""

import json
import os
from pathlib import Path
from flask import Blueprint, jsonify, request, session
from app import app

from app.data.agri_taxonomy import (
    CROP_CATALOGUE,
    CROP_CATEGORIES,
    get_all_catalogue_crops,
    normalize_crop_name
)
from app.data.geo_data import (
    get_states_list,
    get_districts_for_state,
    get_mandals_for_district,
    get_state_agri_baseline
)
from app.data.mandi_data import (
    search_mandi_prices,
    calculate_selling_guidance,
    MANDI_PRICE_REGISTRY
)
from app.data.storage_data import (
    search_storage_facilities,
    STORAGE_FACILITIES
)
from app.services.auth_service import (
    request_otp,
    verify_otp,
    normalize_mobile,
    AUTH_DEV_MODE
)
from app.models.alerts_db import (
    create_price_alert,
    get_user_alerts,
    cancel_price_alert,
    update_user_profile
)


# === 1. LOCATION ENDPOINTS ===

@app.route("/api/states", methods=["GET"])
def api_states():
    return jsonify({
        "states": get_states_list()
    })


@app.route("/api/districts", methods=["GET"])
def api_districts():
    state = request.args.get("state", "Andhra Pradesh")
    return jsonify({
        "state": state,
        "districts": get_districts_for_state(state)
    })


@app.route("/api/mandals", methods=["GET"])
def api_mandals():
    district = request.args.get("district", "Kurnool")
    return jsonify({
        "district": district,
        "mandals": get_mandals_for_district(district)
    })


@app.route("/api/baseline", methods=["GET"])
def api_baseline():
    state = request.args.get("state", "Andhra Pradesh")
    baseline = get_state_agri_baseline(state)
    return jsonify({
        "state": state,
        "baseline": baseline
    })


# === 2. CROP CATALOGUE ENDPOINTS ===

@app.route("/api/crops", methods=["GET"])
def api_crops():
    category = request.args.get("category")
    season = request.args.get("season")
    search_term = request.args.get("q", "").strip().lower()

    crops = get_all_catalogue_crops()

    if category and category != "all":
        crops = [c for c in crops if c["category"].lower() == category.lower()]

    if season and season != "all":
        crops = [c for c in crops if season.capitalize() in c["seasons"] or "Whole Year" in c["seasons"]]

    if search_term:
        crops = [c for c in crops if search_term in c["name"].lower() or search_term in c["id"].lower()]

    return jsonify({
        "categories": CROP_CATEGORIES,
        "count": len(crops),
        "crops": crops
    })


@app.route("/api/crops/<crop_id>", methods=["GET"])
def api_crop_detail(crop_id):
    _, info = normalize_crop_name(crop_id)
    if not info:
        return jsonify({"error": f"Crop '{crop_id}' not found in verified catalogue"}), 404
    return jsonify(info)


# === 3. MANDI MARKET PRICES & SELLING GUIDANCE ===

@app.route("/api/mandi-prices", methods=["GET"])
def api_mandi_prices():
    crop = request.args.get("crop")
    state = request.args.get("state")
    district = request.args.get("district")

    records = search_mandi_prices(crop=crop, state=state, district=district)
    return jsonify({
        "count": len(records),
        "query": {"crop": crop, "state": state, "district": district},
        "prices": records
    })


@app.route("/api/selling-guidance", methods=["GET"])
def api_selling_guidance():
    crop = request.args.get("crop", "Rice")
    try:
        modal_price = float(request.args.get("modal_price", 2200))
    except (ValueError, TypeError):
        modal_price = 2200.0

    try:
        distance_km = float(request.args.get("distance_km", 25))
    except (ValueError, TypeError):
        distance_km = 25.0

    try:
        holding_days = int(request.args.get("holding_days", 30))
    except (ValueError, TypeError):
        holding_days = 30

    _, info = normalize_crop_name(crop)
    is_perishable = info.get("perishable", False) if info else False

    guidance = calculate_selling_guidance(
        crop_name=crop,
        modal_price=modal_price,
        holding_days=holding_days,
        distance_km=distance_km,
        is_perishable=is_perishable
    )
    return jsonify(guidance)


# === 4. STORAGE AND COLD STORAGE FINDER ===

@app.route("/api/storage", methods=["GET"])
def api_storage():
    state = request.args.get("state")
    district = request.args.get("district")
    storage_type = request.args.get("type")
    crop = request.args.get("crop")

    facilities = search_storage_facilities(
        state=state,
        district=district,
        storage_type=storage_type,
        crop=crop
    )
    return jsonify({
        "count": len(facilities),
        "facilities": facilities
    })


# === 5. AUTHENTICATION (MOBILE OTP) ===

@app.route("/api/auth/request-otp", methods=["POST"])
def api_request_otp():
    data = request.get_json() or {}
    mobile = data.get("mobile")

    if not mobile:
        return jsonify({"error": "Mobile number is required"}), 400

    success, msg, extra = request_otp(mobile)
    if not success:
        return jsonify({"error": msg, "data": extra}), 400

    return jsonify({
        "message": msg,
        "data": extra
    })


@app.route("/api/auth/verify-otp", methods=["POST"])
def api_verify_otp():
    data = request.get_json() or {}
    mobile = data.get("mobile")
    otp = data.get("otp")
    lang = data.get("preferred_lang", "en")

    if not mobile or not otp:
        return jsonify({"error": "Both mobile number and OTP are required"}), 400

    success, msg, user = verify_otp(mobile, otp, lang)
    if not success:
        return jsonify({"error": msg}), 400

    session["user_id"] = user["id"]
    session["mobile"] = user["mobile"]
    session["preferred_lang"] = user.get("preferred_language", "en")

    return jsonify({
        "message": msg,
        "user": user
    })


@app.route("/api/auth/session", methods=["GET"])
def api_auth_session():
    if "user_id" in session:
        return jsonify({
            "authenticated": True,
            "user": {
                "id": session["user_id"],
                "mobile": session.get("mobile"),
                "preferred_lang": session.get("preferred_lang", "en")
            }
        })
    return jsonify({
        "authenticated": False,
        "user": None
    })


@app.route("/api/auth/logout", methods=["POST"])
def api_auth_logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})


@app.route("/api/user/profile", methods=["POST"])
def api_update_profile():
    if "mobile" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json() or {}
    state = data.get("state")
    district = data.get("district")
    lang = data.get("preferred_lang")

    update_user_profile(session["mobile"], state, district, lang)
    if lang:
        session["preferred_lang"] = lang
    return jsonify({"message": "Profile updated"})


# === 6. PRICE ALERTS ===

@app.route("/api/alerts/subscribe", methods=["POST"])
def api_subscribe_alert():
    data = request.get_json() or {}
    raw_mobile = session.get("mobile") or data.get("mobile")
    mobile = normalize_mobile(raw_mobile)
    crop = data.get("crop")
    market = data.get("market")
    condition_type = data.get("condition_type", "above")
    try:
        target_price = float(data.get("target_price", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Valid target price is required"}), 400

    if not mobile or not crop or not market or target_price <= 0:
        return jsonify({"error": "Missing required fields (mobile, crop, market, target_price)"}), 400

    alert_id = create_price_alert(
        mobile=mobile,
        crop=crop,
        market=market,
        condition_type=condition_type,
        target_price=target_price,
        unit=data.get("unit", "₹/Quintal")
    )

    return jsonify({
        "message": "Price alert subscription created successfully",
        "alert_id": alert_id
    })


@app.route("/api/alerts/my-alerts", methods=["GET"])
def api_my_alerts():
    raw_mobile = session.get("mobile") or request.args.get("mobile")
    mobile = normalize_mobile(raw_mobile)
    if not mobile:
        return jsonify({"error": "Valid mobile number required"}), 400

    alerts = get_user_alerts(mobile)
    return jsonify({
        "count": len(alerts),
        "alerts": alerts
    })


@app.route("/api/alerts/cancel", methods=["POST"])
def api_cancel_alert():
    data = request.get_json() or {}
    alert_id = data.get("alert_id")
    raw_mobile = session.get("mobile") or data.get("mobile")
    mobile = normalize_mobile(raw_mobile)

    if not alert_id or not mobile:
        return jsonify({"error": "alert_id and mobile required"}), 400

    cancelled = cancel_price_alert(int(alert_id), mobile)
    return jsonify({"success": cancelled})


# === 7. MODEL TRANSPARENCY & ACCURACY METRICS ===

@app.route("/api/model-metrics", methods=["GET"])
def api_model_metrics():
    metrics_path = Path(__file__).resolve().parent.parent.parent / "ml" / "saved_models" / "yield_model_metrics.json"
    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as f:
            yield_metrics = json.load(f)
    else:
        yield_metrics = {"status": "Metrics file not available"}

    return jsonify({
        "yield_prediction_model": yield_metrics,
        "crop_recommendation_model": {
            "type": "RandomForestClassifier",
            "supported_classes": 51,
            "training_samples": 6596,
            "input_features": ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"],
            "cross_val_accuracy": 0.992
        }
    })
