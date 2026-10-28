"""
RythuCrop Crop Recommendation and Farm Planning Engine
Combines 51-class Random Forest soil-climate recommendation with
agronomic heuristic scoring for Farm Planning.
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional

from app.data.agri_taxonomy import (
    CROP_CATALOGUE,
    FARM_PLANNING_21_CROPS,
    normalize_crop_name
)


class CropInputError(ValueError):
    pass


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FEATURE_COLUMNS = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "saved_models",
    "crop_recommendation_model.pkl"
)

# Input validation ranges based on agricultural bounds
INPUT_RANGES = {
    "N": {"min": 0, "max": 140, "description": "Nitrogen"},
    "P": {"min": 5, "max": 145, "description": "Phosphorus"},
    "K": {"min": 5, "max": 205, "description": "Potassium"},
    "temperature": {"min": 8, "max": 44, "description": "Temperature"},
    "humidity": {"min": 14, "max": 100, "description": "Humidity"},
    "ph": {"min": 3, "max": 10, "description": "Soil pH"},
    "rainfall": {"min": 20, "max": 300, "description": "Rainfall"}
}

# The 21 crops for Farm Planning
FARM_PLANNING_CROPS = FARM_PLANNING_21_CROPS

# Crop characteristics mapping
CROP_CHARACTERISTICS = {
    'Arecanut': {'seasons': ['Kharif', 'Rabi', 'Whole Year'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Some experience', 'Experienced']},
    'Arhar/Tur': {'seasons': ['Kharif', 'Rabi'], 'soils': ['Black Soil', 'Red Soil', 'Clay Soil', 'Loamy'], 'water': ['Low water availability', 'Rainfed', 'Moderate water availability'], 'experience': ['Beginner', 'Some experience', 'Experienced']},
    'Bajra': {'seasons': ['Kharif', 'Summer'], 'soils': ['Sandy Soil', 'Red Soil', 'Loamy'], 'water': ['Low water availability', 'Rainfed'], 'experience': ['Beginner', 'Some experience', 'Experienced']},
    'Black pepper': {'seasons': ['Kharif', 'Rabi', 'Whole Year'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Experienced']},
    'Castor seed': {'seasons': ['Kharif', 'Rabi'], 'soils': ['Sandy Soil', 'Red Soil', 'Loamy'], 'water': ['Low water availability', 'Moderate water availability', 'Rainfed'], 'experience': ['Beginner', 'Some experience']},
    'Coconut': {'seasons': ['Kharif', 'Whole Year'], 'soils': ['Sandy Soil', 'Red Soil', 'Loamy'], 'water': ['Good water availability'], 'experience': ['Experienced', 'Some experience']},
    'Cotton(lint)': {'seasons': ['Kharif', 'Summer'], 'soils': ['Black Soil', 'Red Soil', 'Clay Soil'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Some experience', 'Experienced']},
    'Dry chillies': {'seasons': ['Rabi', 'Summer', 'Kharif'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Moderate water availability', 'Low water availability'], 'experience': ['Some experience', 'Experienced']},
    'Gram': {'seasons': ['Rabi', 'Winter'], 'soils': ['Black Soil', 'Loamy', 'Clay Soil'], 'water': ['Rainfed', 'Low water availability'], 'experience': ['Beginner', 'Some experience', 'Experienced']},
    'Groundnut': {'seasons': ['Kharif', 'Summer'], 'soils': ['Sandy Soil', 'Red Soil', 'Loamy'], 'water': ['Moderate water availability', 'Low water availability', 'Rainfed'], 'experience': ['Beginner', 'Some experience']},
    'Jute': {'seasons': ['Kharif'], 'soils': ['Loamy', 'Clay Soil'], 'water': ['Good water availability'], 'experience': ['Some experience', 'Beginner']},
    'Maize': {'seasons': ['Kharif', 'Rabi', 'Summer'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Beginner', 'Some experience', 'Experienced']},
    'Onion': {'seasons': ['Rabi', 'Summer', 'Kharif'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Moderate water availability'], 'experience': ['Some experience', 'Experienced']},
    'Potato': {'seasons': ['Rabi', 'Winter'], 'soils': ['Loamy', 'Sandy Soil'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Beginner', 'Some experience']},
    'Rice': {'seasons': ['Kharif', 'Rabi', 'Summer'], 'soils': ['Clay Soil', 'Loamy'], 'water': ['Good water availability'], 'experience': ['Beginner', 'Some experience', 'Experienced']},
    'Soyabean': {'seasons': ['Kharif'], 'soils': ['Black Soil', 'Loamy'], 'water': ['Moderate water availability', 'Low water availability'], 'experience': ['Beginner', 'Some experience']},
    'Sugarcane': {'seasons': ['Kharif', 'Rabi', 'Whole Year'], 'soils': ['Black Soil', 'Loamy', 'Clay Soil'], 'water': ['Good water availability'], 'experience': ['Some experience', 'Experienced']},
    'Sunflower': {'seasons': ['Kharif', 'Rabi', 'Summer'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Moderate water availability', 'Low water availability'], 'experience': ['Beginner', 'Some experience']},
    'Tobacco': {'seasons': ['Rabi', 'Winter'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Moderate water availability'], 'experience': ['Some experience', 'Experienced']},
    'Turmeric': {'seasons': ['Kharif'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Some experience', 'Experienced']},
    'Wheat': {'seasons': ['Rabi', 'Winter'], 'soils': ['Black Soil', 'Loamy', 'Clay Soil'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Beginner', 'Some experience', 'Experienced']},
}

GOAL_PREFERENCES = {
    'Higher yield': ['Rice', 'Sugarcane', 'Maize', 'Wheat', 'Potato', 'Onion'],
    'Lower water use': ['Gram', 'Bajra', 'Groundnut', 'Arhar/Tur', 'Castor seed', 'Soyabean'],
    'Lower input cost': ['Gram', 'Arhar/Tur', 'Bajra', 'Soyabean', 'Groundnut', 'Maize'],
    'Balanced farming': ['Maize', 'Sunflower', 'Groundnut', 'Cotton(lint)', 'Wheat', 'Turmeric'],
}

LAND_AREA_SUITABILITY = {
    'Small': (0.1, 2),
    'Medium': (2, 10),
    'Large': (10, float('inf'))
}

LAND_AREA_CROP_PREFERENCES = {
    'Small': [
        'Gram', 'Bajra', 'Groundnut', 'Arhar/Tur',
        'Castor seed', 'Sunflower', 'Soyabean',
        'Onion', 'Dry chillies', 'Potato'
    ],
    'Medium': [
        'Maize', 'Groundnut', 'Sunflower', 'Cotton(lint)',
        'Soyabean', 'Wheat', 'Gram', 'Turmeric',
        'Onion', 'Arhar/Tur'
    ],
    'Large': [
        'Rice', 'Wheat', 'Maize', 'Sugarcane',
        'Cotton(lint)', 'Jute', 'Soyabean',
        'Sunflower', 'Groundnut'
    ]
}

_REC_MODEL = None


def load_recommendation_model():
    global _REC_MODEL
    if _REC_MODEL is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Recommendation model not found: {MODEL_PATH}")
        _REC_MODEL = joblib.load(MODEL_PATH)
    return _REC_MODEL


def validate_crop_input(input_data: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[Dict[str, float]]]:
    """Validate crop recommendation input values against training bounds."""
    required_fields = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

    for field in required_fields:
        if field not in input_data or input_data[field] is None or str(input_data[field]).strip() == "":
            return False, f"Missing required value: {field}", None

    validated = {}
    for field in required_fields:
        try:
            value = float(input_data[field])
            validated[field] = value
        except (TypeError, ValueError):
            return False, f"Invalid numeric value for {field}", None

    # Strict check: No negative values allowed
    for field in required_fields:
        value = validated[field]
        if value < 0:
            range_info = INPUT_RANGES[field]
            return False, f"{range_info['description']} cannot be negative. Please enter a value of 0 or greater.", None

    # Range boundaries check
    for field in required_fields:
        value = validated[field]
        range_info = INPUT_RANGES[field]
        if value < range_info["min"] or value > range_info["max"]:
            return False, f"{range_info['description']} value {value} is outside typical range ({range_info['min']}–{range_info['max']}). Please enter a value in the expected range.", None

    return True, None, validated


def recommend_crop_top3(input_data: Dict[str, Any]) -> List[str]:
    """Return top 3 crops from the trained Crop Recommendation model."""
    is_valid, error_msg, validated = validate_crop_input(input_data)
    if not is_valid:
        raise CropInputError(error_msg)

    model = load_recommendation_model()
    df = pd.DataFrame([validated], columns=FEATURE_COLUMNS)

    probabilities = model.predict_proba(df)[0]
    ranked = sorted(
        zip(model.classes_, probabilities),
        key=lambda item: item[1],
        reverse=True
    )
    return [crop for crop, _ in ranked[:3]]


def recommend_crop_top3_detailed(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Return top 3 crops with confidence percentages and agronomic suitability."""
    is_valid, error_msg, validated = validate_crop_input(input_data)
    if not is_valid:
        raise CropInputError(error_msg)

    model = load_recommendation_model()
    df = pd.DataFrame([validated], columns=FEATURE_COLUMNS)

    probabilities = model.predict_proba(df)[0]
    ranked = sorted(
        zip(model.classes_, probabilities),
        key=lambda item: item[1],
        reverse=True
    )

    top_results = []
    for rank, (crop_class, prob) in enumerate(ranked[:3], 1):
        _, cat_info = normalize_crop_name(crop_class)
        top_results.append({
            "rank": rank,
            "crop_id": crop_class,
            "name": cat_info["name"] if cat_info else crop_class.capitalize(),
            "confidence_pct": round(float(prob) * 100, 1),
            "category": cat_info["category"] if cat_info else "Agricultural Crop",
            "duration": cat_info["duration_days"] if cat_info else "Seasonal",
            "water_req": cat_info["water_req"] if cat_info else "Moderate",
            "advisory": cat_info["advisory_tips"] if cat_info else {}
        })

    return {
        "recommended_crop": top_results[0]["crop_id"] if top_results else None,
        "top_3": [r["crop_id"] for r in top_results],
        "top_3_detailed": top_results
    }


def recommend_crop(input_data: Dict[str, Any]) -> str:
    top_3 = recommend_crop_top3(input_data)
    return top_3[0] if top_3 else FARM_PLANNING_CROPS[0]


def recommend_farm_plan(farm_data: Dict[str, Any]) -> List[str]:
    """
    Recommend suitable crops based on Farm Planning inputs.
    Strictly preserves the 6 payload inputs:
        land, season, soil, irrigation, goal, experience
    Returns:
        list of recommended crop names (from 21 crops)
    """
    detailed = recommend_farm_plan_detailed(farm_data)
    return detailed["recommended_crops"]


def recommend_farm_plan_detailed(farm_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detailed Farm Planning recommendation engine.
    Preserves all 6 inputs and provides water, soil, season, and risk analysis.
    """
    try:
        land = float(farm_data.get('land', 1.0))
        if land <= 0:
            land = 1.0
    except (ValueError, TypeError):
        land = 1.0

    season = str(farm_data.get('season', 'Kharif')).strip()
    soil = str(farm_data.get('soil', 'Loamy')).strip()
    irrigation = str(farm_data.get('irrigation', 'Moderate water availability')).strip()
    goal = str(farm_data.get('goal', 'Balanced farming')).strip()
    experience = str(farm_data.get('experience', 'Beginner')).strip()

    # Determine land size category
    land_size = 'Small'
    for size_cat, (min_land, max_land) in LAND_AREA_SUITABILITY.items():
        if min_land <= land < max_land:
            land_size = size_cat
            break
    else:
        land_size = 'Large'

    crop_scores = {crop: 0 for crop in FARM_PLANNING_CROPS}
    crop_reasons = {crop: [] for crop in FARM_PLANNING_CROPS}

    for crop in FARM_PLANNING_CROPS:
        if crop not in CROP_CHARACTERISTICS:
            continue

        char = CROP_CHARACTERISTICS[crop]
        score = 0

        # Season matching (30 points)
        if season in char['seasons'] or 'Whole Year' in char['seasons']:
            score += 30
            crop_reasons[crop].append(f"Highly suited for {season} season")
        elif season == 'Summer' and 'Kharif' in char['seasons']:
            score += 15
        elif season == 'Winter' and 'Rabi' in char['seasons']:
            score += 15

        # Soil matching (25 points)
        if soil in char['soils']:
            score += 25
            crop_reasons[crop].append(f"Thrives in {soil}")
        elif soil == 'Sandy Soil' and 'Loamy' in char['soils']:
            score += 12
        elif soil == 'Black Soil' and 'Clay Soil' in char['soils']:
            score += 15

        # Water availability matching (25 points)
        if irrigation in char['water']:
            score += 25
            crop_reasons[crop].append(f"Compatible with {irrigation}")
        elif irrigation == 'Moderate water availability':
            score += 12
        elif irrigation == 'Low water availability' and 'Rainfed' in char['water']:
            score += 18
            crop_reasons[crop].append("High drought and moisture stress tolerance")

        # Experience matching (15 points)
        if experience in char['experience']:
            score += 15
        elif experience == 'Some experience' and 'Beginner' in char['experience']:
            score += 10

        # Land area matching (10 points)
        if crop in LAND_AREA_CROP_PREFERENCES.get(land_size, []):
            score += 10
            crop_reasons[crop].append(f"Efficient land utilization for {land} acres")

        # Goal alignment (5 points)
        if crop in GOAL_PREFERENCES.get(goal, []):
            score += 5
            crop_reasons[crop].append(f"Directly supports {goal.lower()} target")

        crop_scores[crop] = score

    ranked = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)

    recommended_crops = []
    plan_details = []

    for crop, score in ranked:
        if score > 0 or len(recommended_crops) < 2:
            recommended_crops.append(crop)
            _, cat_info = normalize_crop_name(crop)
            reasons = crop_reasons[crop] if crop_reasons[crop] else ["Suitable agronomic baseline"]
            plan_details.append({
                "crop": crop,
                "score": score,
                "reasons": reasons,
                "soil_consideration": f"{soil} requires proper aeration and organic matter addition.",
                "water_consideration": f"Ensure moisture scheduling matching {irrigation.lower()}.",
                "risks": "Seasonal rainfall fluctuations, pest pressure during vegetative growth, and harvest market volatility.",
                "next_steps": "Test soil NPK/micronutrient levels, prepare certified seed with fungicide dressing, and confirm local mandi availability."
            })
        if len(recommended_crops) >= 5:
            break

    if len(recommended_crops) < 2:
        for crop, score in ranked[:3]:
            if crop not in recommended_crops:
                recommended_crops.append(crop)

    return {
        "recommended_crops": recommended_crops,
        "plan_details": plan_details,
        "inputs_preserved": {
            "land": land,
            "season": season,
            "soil": soil,
            "irrigation": irrigation,
            "goal": goal,
            "experience": experience
        },
        "disclaimer": "These are agro-advisory suggestions based on machine learning and agronomic heuristics. Actual yields depend on local weather, timely cultivation, and disease management."
    }
