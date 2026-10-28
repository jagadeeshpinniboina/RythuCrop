from flask import request, jsonify, render_template
from app import app
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
    predict_yield_detailed
)


@app.route("/predict/", methods=["GET"])
def predict_page():
    return render_template("predict.html")


@app.route("/predict", methods=["POST"])
def predict():
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
            "top_3_detailed": detailed_res["top_3_detailed"]
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
def farm_plan():
    """Farm Planning recommendation endpoint - preserves existing contract."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
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
def predict_yield_api():
    """Location, crop, and year sensitive pre-harvest yield endpoint."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

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
            "detailed": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
