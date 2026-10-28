import os
import joblib
import pandas as pd
import numpy as np


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

# Input validation ranges based on training data
INPUT_RANGES = {
    "N": {"min": 0, "max": 140, "description": "Nitrogen"},
    "P": {"min": 5, "max": 145, "description": "Phosphorus"},
    "K": {"min": 5, "max": 205, "description": "Potassium"},
    "temperature": {"min": 8, "max": 44, "description": "Temperature"},
    "humidity": {"min": 14, "max": 100, "description": "Humidity"},
    "ph": {"min": 3, "max": 10, "description": "Soil pH"},
    "rainfall": {"min": 20, "max": 300, "description": "Rainfall"}
}

# Define the 21 crops for Farm Planning
FARM_PLANNING_CROPS = [
    'Arecanut', 'Arhar/Tur', 'Castor seed', 'Coconut', 'Cotton(lint)',
    'Dry chillies', 'Gram', 'Jute', 'Maize', 'Onion', 'Potato', 'Rice',
    'Sugarcane', 'Sunflower', 'Tobacco', 'Turmeric', 'Wheat', 'Bajra',
    'Black pepper', 'Groundnut', 'Soyabean'
]

# Crop characteristics mapping
CROP_CHARACTERISTICS = {
    'Arecanut': {'seasons': ['Kharif', 'Rabi'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Some experience', 'Experienced']},
    'Arhar/Tur': {'seasons': ['Kharif', 'Rabi'], 'soils': ['Black Soil', 'Red Soil', 'Clay Soil', 'Loamy'], 'water': ['Low water availability', 'Rainfed', 'Moderate water availability'], 'experience': ['Beginner', 'Some experience', 'Experienced']},
    'Bajra': {'seasons': ['Kharif', 'Summer'], 'soils': ['Sandy Soil', 'Red Soil', 'Loamy'], 'water': ['Low water availability', 'Rainfed'], 'experience': ['Beginner']},
    'Black pepper': {'seasons': ['Kharif', 'Rabi'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Experienced']},
    'Castor seed': {'seasons': ['Kharif', 'Rabi'], 'soils': ['Sandy Soil', 'Red Soil', 'Loamy'], 'water': ['Low water availability', 'Moderate water availability'], 'experience': ['Beginner']},
    'Coconut': {'seasons': ['Kharif'], 'soils': ['Sandy Soil', 'Red Soil', 'Loamy'], 'water': ['Good water availability'], 'experience': ['Experienced']},
    'Cotton(lint)': {'seasons': ['Kharif', 'Summer'], 'soils': ['Black Soil', 'Red Soil', 'Clay Soil'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Some experience', 'Experienced']},
    'Dry chillies': {'seasons': ['Rabi', 'Summer'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Moderate water availability', 'Low water availability'], 'experience': ['Some experience', 'Experienced']},
    'Gram': {'seasons': ['Rabi', 'Winter'], 'soils': ['Black Soil', 'Loamy', 'Clay Soil'], 'water': ['Rainfed', 'Low water availability'], 'experience': ['Beginner', 'Some experience']},
    'Groundnut': {'seasons': ['Kharif', 'Summer'], 'soils': ['Sandy Soil', 'Red Soil', 'Loamy'], 'water': ['Moderate water availability', 'Low water availability'], 'experience': ['Beginner', 'Some experience']},
    'Jute': {'seasons': ['Kharif'], 'soils': ['Loamy', 'Clay Soil'], 'water': ['Good water availability'], 'experience': ['Some experience']},
    'Maize': {'seasons': ['Kharif', 'Rabi', 'Summer'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Beginner', 'Some experience']},
    'Onion': {'seasons': ['Rabi', 'Summer', 'Kharif'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Moderate water availability'], 'experience': ['Some experience', 'Experienced']},
    'Potato': {'seasons': ['Rabi', 'Winter'], 'soils': ['Loamy', 'Sandy Soil'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Beginner', 'Some experience']},
    'Rice': {'seasons': ['Kharif', 'Rabi', 'Summer'], 'soils': ['Clay Soil', 'Loamy'], 'water': ['Good water availability'], 'experience': ['Beginner', 'Some experience', 'Experienced']},
    'Soyabean': {'seasons': ['Kharif'], 'soils': ['Black Soil', 'Loamy'], 'water': ['Moderate water availability', 'Low water availability'], 'experience': ['Beginner']},
    'Sugarcane': {'seasons': ['Kharif', 'Rabi'], 'soils': ['Black Soil', 'Loamy'], 'water': ['Good water availability'], 'experience': ['Some experience', 'Experienced']},
    'Sunflower': {'seasons': ['Kharif', 'Rabi', 'Summer'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Moderate water availability'], 'experience': ['Beginner', 'Some experience']},
    'Tobacco': {'seasons': ['Rabi', 'Winter'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Moderate water availability'], 'experience': ['Some experience', 'Experienced']},
    'Turmeric': {'seasons': ['Kharif'], 'soils': ['Black Soil', 'Red Soil', 'Loamy'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Some experience', 'Experienced']},
    'Wheat': {'seasons': ['Rabi', 'Winter'], 'soils': ['Black Soil', 'Loamy'], 'water': ['Good water availability', 'Moderate water availability'], 'experience': ['Beginner', 'Some experience', 'Experienced']},
}

# Goal-based crop preferences
GOAL_PREFERENCES = {
    'Higher yield': ['Rice', 'Sugarcane', 'Maize', 'Wheat', 'Potato', 'Onion'],
    'Lower water use': ['Gram', 'Bajra', 'Groundnut', 'Arhar/Tur', 'Castor seed', 'Soyabean'],
    'Lower input cost': ['Gram', 'Arhar/Tur', 'Bajra', 'Soyabean', 'Groundnut', 'Maize'],
    'Balanced farming': ['Maize', 'Sunflower', 'Groundnut', 'Cotton(lint)', 'Wheat', 'Turmeric'],
}

# Land area suitability (acres)
LAND_AREA_SUITABILITY = {
    'Small': (0.1, 2),      # 0.1-2 acres
    'Medium': (2, 10),       # 2-10 acres
    'Large': (10, float('inf'))  # 10+ acres
}

# Land-area crop preferences
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


def load_recommendation_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Recommendation model not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def validate_crop_input(input_data):
    """
    Validate crop recommendation input values against training data ranges.
    Returns: (is_valid, error_message, validated_data)
    """
    required_fields = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    
    # Check for missing fields
    for field in required_fields:
        if field not in input_data or input_data[field] is None or str(input_data[field]).strip() == "":
            return False, f"Missing required value: {field}", None
    
    # Try to convert to float
    validated = {}
    for field in required_fields:
        try:
            value = float(input_data[field])
            validated[field] = value
        except (TypeError, ValueError):
            return False, f"Invalid numeric value for {field}", None
    
    # Check for negative values (strict: no negative allowed)
    for field in required_fields:
        value = validated[field]
        if value < 0:
            range_info = INPUT_RANGES[field]
            return False, f"{range_info['description']} cannot be negative. Please enter a value of 0 or greater.", None
    
    # Check ranges with warnings
    for field in required_fields:
        value = validated[field]
        range_info = INPUT_RANGES[field]
        
        # Range check
        if value < range_info["min"]:
            return False, f"{range_info['description']} value {value} is below typical range ({range_info['min']}-{range_info['max']}). Please enter a value in the expected range.", None
        if value > range_info["max"]:
            return False, f"{range_info['description']} value {value} is above typical range ({range_info['min']}-{range_info['max']}). Please enter a value in the expected range.", None
    
    return True, None, validated


def get_crop_similarity_features(crop):
    """Get similarity features for crops not in the trained model."""
    # These are derived from the crop characteristics and typical conditions
    crop_profiles = {
        'Arecanut': {'N': 60, 'P': 50, 'K': 40, 'temp': 24, 'humidity': 75, 'ph': 6.5, 'rainfall': 150},
        'Bajra': {'N': 40, 'P': 35, 'K': 40, 'temp': 28, 'humidity': 50, 'ph': 6.0, 'rainfall': 40},
        'Castor seed': {'N': 50, 'P': 40, 'K': 50, 'temp': 26, 'humidity': 55, 'ph': 6.5, 'rainfall': 70},
        'Coconut': {'N': 70, 'P': 30, 'K': 60, 'temp': 27, 'humidity': 80, 'ph': 6.5, 'rainfall': 150},
        'Dry chillies': {'N': 80, 'P': 45, 'K': 60, 'temp': 24, 'humidity': 60, 'ph': 6.5, 'rainfall': 60},
        'Gram': {'N': 20, 'P': 35, 'K': 40, 'temp': 20, 'humidity': 50, 'ph': 7.0, 'rainfall': 50},
        'Groundnut': {'N': 20, 'P': 40, 'K': 40, 'temp': 25, 'humidity': 60, 'ph': 6.5, 'rainfall': 50},
        'Sugarcane': {'N': 120, 'P': 60, 'K': 80, 'temp': 24, 'humidity': 75, 'ph': 6.5, 'rainfall': 150},
        'Tobacco': {'N': 100, 'P': 50, 'K': 60, 'temp': 22, 'humidity': 65, 'ph': 6.5, 'rainfall': 70},
        'Turmeric': {'N': 80, 'P': 40, 'K': 60, 'temp': 25, 'humidity': 75, 'ph': 6.5, 'rainfall': 150},
    }
    return crop_profiles.get(crop, None)


def calculate_similarity(input_values, crop):
    """Calculate how suitable the input values are for a given crop."""
    profile = get_crop_similarity_features(crop)
    if not profile:
        return 0.5  # Default neutral score for unknown crops
    
    # Normalize features to 0-1 scale and calculate weighted distance
    distances = []
    # Note: weights use profile field names, not input field names
    weights = {'N': 1.0, 'P': 0.8, 'K': 0.8, 'temp': 1.0, 'humidity': 1.0, 'ph': 1.0, 'rainfall': 1.0}
    
    # Map input field names to profile field names
    field_mapping = {
        'N': 'N', 'P': 'P', 'K': 'K',
        'temperature': 'temp',
        'humidity': 'humidity',
        'ph': 'ph',
        'rainfall': 'rainfall'
    }
    
    for field, profile_field in field_mapping.items():
        if profile_field in profile:
            # Calculate normalized distance
            ideal = profile[profile_field]
            actual = input_values[field]
            # Use Gaussian-like scoring centered on ideal values
            diff = abs(actual - ideal)
            similarity = np.exp(-((diff / (ideal + 1)) ** 2))  # Avoid division by zero
            distances.append(similarity * weights[profile_field])  # Use profile_field for weights lookup
    
    if not distances:
        return 0.5
    
    return np.mean(distances)


def recommend_crop_top3(input_data):
    """Return the top 3 crops from the trained Crop Recommendation model."""
    is_valid, error_msg, validated = validate_crop_input(input_data)

    if not is_valid:
        raise CropInputError(error_msg)

    model = load_recommendation_model()

    # Use the exact feature names expected by the trained model.
    df = pd.DataFrame([validated], columns=FEATURE_COLUMNS)

    # Rank every crop known by the trained recommendation model.
    probabilities = model.predict_proba(df)[0]
    ranked = sorted(
        zip(model.classes_, probabilities),
        key=lambda item: item[1],
        reverse=True
    )

    # Return only the top 3 dynamically.
    return [crop for crop, _ in ranked[:3]]

def recommend_crop(input_data):
    """Recommend the top crop based on soil and climate parameters (ML-based)."""
    top_3 = recommend_crop_top3(input_data)
    return top_3[0] if top_3 else FARM_PLANNING_CROPS[0]


def recommend_farm_plan(farm_data):
    """
    Recommend suitable crops based on Farm Planning inputs.
    Uses rule-based logic with the 21-crop list.
    
    Args:
        farm_data: dict with keys:
            - land: land area in acres (float)
            - season: season name (str)
            - soil: soil type (str)
            - irrigation: water availability (str)
            - goal: main farming goal (str)
            - experience: farming experience level (str)
    
    Returns:
        list: list of recommended crop names (max 3-5 from 21 crops)
    """
    land = float(farm_data.get('land', 1))
    season = farm_data.get('season', 'Kharif')
    soil = farm_data.get('soil', 'Loamy')
    irrigation = farm_data.get('irrigation', 'Moderate water availability')
    goal = farm_data.get('goal', 'Balanced farming')
    experience = farm_data.get('experience', 'Beginner')
    
    # Determine land size category
    land_size = 'Small'
    for size_cat, (min_land, max_land) in LAND_AREA_SUITABILITY.items():
        if min_land <= land < max_land:
            land_size = size_cat
            break
    else:
        land_size = 'Large'
    
    # Initialize scores for all 21 crops
    crop_scores = {crop: 0 for crop in FARM_PLANNING_CROPS}
    
    # Score each crop
    for crop in FARM_PLANNING_CROPS:
        if crop not in CROP_CHARACTERISTICS:
            continue
            
        char = CROP_CHARACTERISTICS[crop]
        score = 0
        
        # Season matching (30 points max)
        if season in char['seasons']:
            score += 30
        elif season == 'Summer' and 'Kharif' in char['seasons']:
            score += 15  # Alternative
        elif season == 'Winter' and 'Rabi' in char['seasons']:
            score += 15  # Alternative
        
        # Soil matching (25 points max)
        if soil in char['soils']:
            score += 25
        elif soil == 'Sandy Soil' and 'Loamy' in char['soils']:
            score += 15  # Can work with loamy
        elif soil == 'Black Soil' and 'Clay Soil' in char['soils']:
            score += 15  # Similar characteristics
        
        # Water availability matching (25 points max)
        if irrigation in char['water']:
            score += 25
        elif irrigation == 'Moderate water availability':
            if 'Good water availability' in char['water']:
                score += 12
            elif 'Low water availability' in char['water']:
                score += 12
        elif irrigation == 'Low water availability' and 'Rainfed' in char['water']:
            score += 15
        
        # Experience level matching (15 points max)
        if experience in char['experience']:
            score += 15
        elif experience == 'Some experience' and 'Beginner' in char['experience']:
            score += 8  # Can still do it
        
        # Land area matching (10 points max)
        if crop in LAND_AREA_CROP_PREFERENCES.get(land_size, []):
            score += 10

        # Goal alignment (5 points)
        if crop in GOAL_PREFERENCES.get(goal, []):
            score += 5
        
        crop_scores[crop] = score
    
    # Sort crops by score
    ranked_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Return top 3-5 recommendations
    recommendations = []
    for crop, score in ranked_crops:
        if score > 0 or len(recommendations) < 2:  # Always return at least 2
            recommendations.append(crop)
        if len(recommendations) >= 5:
            break
    
    # If somehow we have less than 2, just take top 3 regardless
    if len(recommendations) < 2:
        recommendations = [crop for crop, score in ranked_crops[:3]]
    
    return recommendations
