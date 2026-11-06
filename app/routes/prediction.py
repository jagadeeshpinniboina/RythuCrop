from flask import request, jsonify, render_template, session

from app import app

from app.services.auth_service import login_required

from app.models.predictor import (

    CropInputError,

    recommend_crop,

    recommend_crop_top3,

    recommend_crop_top3_detailed,

    recommend_farm_plan,

    recommend_farm_plan_detailed

)

from app.models.yield_predictor import (

    predict_yield,

    predict_yield_detailed,

    get_compatible_crops_for_state

)





@app.route("/predict/", methods=["GET"])

@login_required

def predict_page():

    return render_template("predict.html")





@app.route("/predict", methods=["POST"])

@app.route("/predict-crop", methods=["POST"])

@app.route("/recommend_crop", methods=["POST"])

@app.route("/recommend-crop", methods=["POST"])

@app.route("/api/recommend-crop", methods=["POST"])

@app.route("/api/recommend_crop", methods=["POST"])

@app.route("/api/recommend", methods=["POST"])

@app.route("/api/predict-crop", methods=["POST"])

@login_required

def predict():

    if not (session.get("is_authenticated") and (session.get("user_id") or session.get("email"))):
        return jsonify({
            "status": "error",
            "message": "Authentication required. Please login with your Email.",
            "error": "Authentication required. Please login with your Email.",
            "redirect": "/login",
            "authenticated": False
        }), 401

    data = request.get_json()



    if not data:

        return jsonify({"error": "No input data provided"}), 400



    try:

        detailed_res = recommend_crop_top3_detailed(data)

        top_3 = detailed_res["top_3"]

        return jsonify({

            "recommended_crop": detailed_res["recommended_crop"],

            "top_3": top_3,

            "top_3_recommendations": top_3,

            "top_3_detailed": detailed_res["top_3_detailed"],

            "input": detailed_res.get("input", data)

        })



    except CropInputError as e:

        return jsonify({

            "error": str(e)

        }), 400



    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500





@app.route("/farm-plan", methods=["POST"])

@app.route("/farm-planning", methods=["POST"])

@app.route("/api/farm-plan", methods=["POST"])

@app.route("/api/farm-planning", methods=["POST"])

@login_required

def farm_plan():

    """Farm Planning recommendation endpoint - preserves existing contract."""

    if not (session.get("is_authenticated") and (session.get("user_id") or session.get("email"))):
        return jsonify({
            "status": "error",
            "message": "Authentication required. Please login with your Email.",
            "error": "Authentication required. Please login with your Email.",
            "redirect": "/login",
            "authenticated": False
        }), 401

    data = request.get_json()



    if not data:

        return jsonify({"error": "No input data provided"}), 400



    try:

        lang = str(data.get("lang") or request.args.get("lang") or session.get("lang") or "en").strip().lower()

        if lang not in ("en", "te", "hi", "ta", "kn", "ml", "mr", "bn", "gu", "od"):

            lang = "en"

        data["lang"] = lang



        result = recommend_farm_plan_detailed(data)



        return jsonify({

            "recommended_crops": result["recommended_crops"],

            "plan_details": result["plan_details"],

            "inputs_preserved": result["inputs_preserved"],

            "disclaimer": result["disclaimer"]

        })



    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500





@app.route("/predict-yield", methods=["POST"])

@app.route("/predict_yield", methods=["POST"])

@app.route("/api/yield", methods=["POST"])

@app.route("/api/predict-yield", methods=["POST"])

@login_required

def predict_yield_api():

    """Location, crop, and year sensitive pre-harvest yield endpoint."""

    if not (session.get("is_authenticated") and (session.get("user_id") or session.get("email"))):
        return jsonify({
            "status": "error",
            "message": "Authentication required. Please login with your Email.",
            "error": "Authentication required. Please login with your Email.",
            "redirect": "/login",
            "authenticated": False
        }), 401

    data = request.get_json()



    if not data:

        return jsonify({"error": "No input data provided"}), 400



    # Ensure benchmark crop year default when omitted by modern UI

    if not data.get("Crop_Year") and not data.get("crop_year"):

        data["Crop_Year"] = 2020



    try:

        result = predict_yield_detailed(data)



        return jsonify({

            "predicted_yield": result["predicted_yield_tonnes_ha"],

            "predicted_yield_tonnes_ha": result["predicted_yield_tonnes_ha"],

            "predicted_yield_per_acre": result["predicted_yield_per_acre"],

            "yield_unit": result["yield_unit"],

            "acre_unit": result["acre_unit"],

            "estimated_production": result["estimated_production"],

            "production_unit": result["production_unit"],

            "risk_level": result.get("risk_level", "Moderate Risk"),

            "climate_suitability": result.get("climate_suitability", "Moderate Feasibility"),

            "is_viable": result.get("is_viable", True),
            "season_mismatch": result.get("season_mismatch", False),
            "season_status": result.get("season_status", "Optimal"),
            "season_factor": result.get("season_factor", 1.0),
            "season_warning": result.get("season_warning"),

            "warning_key": result.get("warning_key"),

            "warning_message": result.get("warning_message"),

            "crop": result.get("crop"),

            "state": result.get("state"),

            "season": result.get("season"),

            "area_acres": result.get("area_acres"),

            "actionable_suggestions": result.get("actionable_suggestions", []),

            "detailed": result

        })



    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500





@app.route("/api/state-crops", methods=["GET"])

def get_state_crops():

    """Get agro-climatically compatible crops for a given state."""

    state = request.args.get("state", "").strip()

    compatible = get_compatible_crops_for_state(state)

    return jsonify({

        "state": state,

        "compatible_crops": compatible

    })

