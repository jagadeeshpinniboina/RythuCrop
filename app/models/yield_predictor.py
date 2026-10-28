"""
Pre-Harvest Yield Prediction Engine
Uses retrained Leakage-Free Random Forest Pipeline with Target Log-Transformation.
Predicts yield per hectare and calculates total estimated production.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any

from app.data.geo_data import get_state_agri_baseline
from app.data.agri_taxonomy import normalize_crop_name

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "saved_models", "crop_yield_model.pkl")

# Cached model instance
_YIELD_MODEL = None


def load_yield_model():
    global _YIELD_MODEL
    if _YIELD_MODEL is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Yield model artifact not found: {MODEL_PATH}")
        _YIELD_MODEL = joblib.load(MODEL_PATH)
    return _YIELD_MODEL


def predict_yield(input_data: Dict[str, Any]) -> float:
    """
    Core prediction endpoint maintaining backward-compatible float return value.
    Full detailed dict available via `predict_yield_detailed`.
    """
    details = predict_yield_detailed(input_data)
    return details["predicted_yield_tonnes_ha"]


def predict_yield_detailed(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Location, crop, and crop-year sensitive pre-harvest yield inference.
    Takes into account area, regional agro-climatic conditions, and fertilizer.
    Does NOT require total production as input.
    """
    model = load_yield_model()

    crop_raw = str(input_data.get("Crop", "Rice")).strip()
    season = str(input_data.get("Season", "Kharif")).strip()
    state = str(input_data.get("State", "Andhra Pradesh")).strip()

    # Normalize crop name to canonical dataset string
    _, cat_info = normalize_crop_name(crop_raw)
    crop_dataset_name = cat_info["yield_dataset_name"] if cat_info and cat_info["yield_dataset_name"] else crop_raw

    # Crop year validation
    try:
        crop_year = int(input_data.get("Crop_Year", 2020))
    except (ValueError, TypeError):
        crop_year = 2020

    # Area and unit conversion
    area_unit = str(input_data.get("area_unit", "acres")).lower()
    try:
        area_raw = float(input_data.get("Area", 1.0))
        if area_raw <= 0:
            area_raw = 1.0
    except (ValueError, TypeError):
        area_raw = 1.0

    if area_unit == "hectares" or area_unit == "ha":
        area_ha = area_raw
        area_acres = area_ha / 0.404686
    else:  # default acres
        area_acres = area_raw
        area_ha = area_acres * 0.404686

    # Regional agro-climatic defaults if not supplied by user
    baseline = get_state_agri_baseline(state)

    try:
        rainfall = float(input_data.get("Annual_Rainfall", 0))
        if rainfall <= 0:
            rainfall = float(baseline["rainfall"])
    except (ValueError, TypeError):
        rainfall = float(baseline["rainfall"])

    try:
        fertilizer = float(input_data.get("Fertilizer", 0))
        if fertilizer <= 0:
            fertilizer = round(baseline["fertilizer_per_ha"] * area_ha, 2)
    except (ValueError, TypeError):
        fertilizer = round(baseline["fertilizer_per_ha"] * area_ha, 2)

    try:
        pesticide = float(input_data.get("Pesticide", 0))
        if pesticide <= 0:
            pesticide = round(baseline["pesticide_per_ha"] * area_ha, 2)
    except (ValueError, TypeError):
        pesticide = round(baseline["pesticide_per_ha"] * area_ha, 2)

    # Prepare DataFrame matching trained model columns
    inference_df = pd.DataFrame([{
        "Crop": crop_dataset_name,
        "Season": season,
        "State": state,
        "Crop_Year": crop_year,
        "Area": area_ha,
        "Annual_Rainfall": rainfall,
        "Fertilizer": fertilizer,
        "Pesticide": pesticide
    }])

    # Predict
    raw_pred = model.predict(inference_df)
    pred_val = float(max(0.01, raw_pred[0]))

    is_coconut = "coconut" in crop_dataset_name.lower()
    yield_unit = "nuts/ha" if is_coconut else "tonnes/ha"
    acre_unit = "nuts/acre" if is_coconut else "quintals/acre"

    if is_coconut:
        yield_tonnes_ha = pred_val
        yield_per_acre = round(yield_tonnes_ha * 0.404686, 1)
        estimated_production = round((yield_tonnes_ha * area_ha) / 1000.0, 1)  # in 1000 nuts
        production_unit = "thousand nuts"
    else:
        yield_tonnes_ha = round(pred_val, 2)
        # 1 tonne/ha = 4.04686 quintals/acre
        yield_per_acre = round(yield_tonnes_ha * 4.04686, 2)
        estimated_production = round(yield_tonnes_ha * area_ha, 2)
        production_unit = "tonnes"

    return {
        "crop": crop_dataset_name,
        "state": state,
        "season": season,
        "crop_year": crop_year,
        "area_acres": round(area_acres, 2),
        "area_ha": round(area_ha, 2),
        "predicted_yield": yield_tonnes_ha,
        "predicted_yield_tonnes_ha": yield_tonnes_ha,
        "predicted_yield_per_acre": yield_per_acre,
        "yield_unit": yield_unit,
        "acre_unit": acre_unit,
        "estimated_production": estimated_production,
        "production_unit": production_unit,
        "annual_rainfall_used": rainfall,
        "fertilizer_used": fertilizer,
        "pesticide_used": pesticide,
        "methodology": "Pre-harvest Random Forest Regression (DES Agricultural Statistics)",
        "limitations": "Estimates assume normal seasonal weather without severe unseasonal floods, extreme hailstorms, or major pest outbreaks."
    }
