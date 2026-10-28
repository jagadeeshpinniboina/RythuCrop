from flask import request, jsonify, render_template
from app import app
from app.models.predictor import (
    CropInputError,
    recommend_crop,
    recommend_crop_top3,
    recommend_farm_plan,
)
from app.models.yield_predictor import predict_yield


@app.route("/predict/", methods=["GET"])
def predict_page():
    return render_template("predict.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        top_3 = recommend_crop_top3(data)
        return jsonify({
            "recommended_crop": top_3[0] if top_3 else None,
            "top_3": top_3,
            "top_3_recommendations": top_3
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
    """Farm Planning recommendation endpoint"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        result = recommend_farm_plan(data)

        return jsonify({
            "recommended_crops": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/predict-yield", methods=["POST"])
def predict_yield_api():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        result = predict_yield(data)

        return jsonify({
            "predicted_yield": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500