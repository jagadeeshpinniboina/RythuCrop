"""
RythuCrop Crop Recommendation and Farm Planning Engine
Combines 51-class Random Forest soil-climate recommendation with
agronomic heuristic scoring for Farm Planning.
"""

import os
import joblib
import pandas as pd
import numpy as np
import threading
from typing import Dict, List, Any, Tuple, Optional

from app.data.agri_taxonomy import (
    CROP_CATALOGUE,
    FARM_PLANNING_21_CROPS,
    normalize_crop_name
)
from app.data.crops_data import CROP_DATA
from app.services.farm_planning import (
    recommend_farm_plan,
    recommend_farm_plan_detailed,
    generate_timeline_guidance,
    LAND_AREA_SUITABILITY
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

# Crop characteristics mapping derived from CROP_DATA for backward compatibility
CROP_CHARACTERISTICS = {
    crop: {
        'seasons': data.get('seasons', []),
        'soils': list(data.get('soils', {}).keys()),
        'water': list(data.get('water_affinity', {}).keys()),
        'experience': data.get('experience', [])
    }
    for crop, data in CROP_DATA.items()
}

GOAL_PREFERENCES = {
    'Higher yield': ['Rice', 'Sugarcane', 'Maize', 'Wheat', 'Potato', 'Onion'],
    'Lower water use': ['Gram', 'Bajra', 'Groundnut', 'Arhar/Tur', 'Castor seed', 'Soyabean'],
    'Lower input cost': ['Gram', 'Arhar/Tur', 'Bajra', 'Soyabean', 'Groundnut', 'Maize'],
    'Balanced farming': ['Maize', 'Sunflower', 'Groundnut', 'Cotton(lint)', 'Wheat', 'Turmeric'],
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

_MODEL_LOCK = threading.Lock()
_REC_MODEL = None
_CROP_STATS = None


def load_recommendation_model():
    global _REC_MODEL
    if _REC_MODEL is None:
        with _MODEL_LOCK:
            if _REC_MODEL is None:
                if not os.path.exists(MODEL_PATH):
                    raise FileNotFoundError(f"Recommendation model not found: {MODEL_PATH}")
                _REC_MODEL = joblib.load(MODEL_PATH)
    return _REC_MODEL


def get_crop_agronomic_stats() -> Dict[str, Any]:
    """Load and cache crop statistical bounds from merged dataset for agronomic distance and dynamic diagnosis."""
    global _CROP_STATS
    if _CROP_STATS is not None:
        return _CROP_STATS

    with _MODEL_LOCK:
        if _CROP_STATS is not None:
            return _CROP_STATS
        csv_path = os.path.join(BASE_DIR, "ml", "data", "merged_crop_dataset.csv")
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                features = FEATURE_COLUMNS
                means = df.groupby('label')[features].mean().to_dict(orient='index')
                stds = df.groupby('label')[features].std().replace(0, 1.0).to_dict(orient='index')
                mins = df.groupby('label')[features].min().to_dict(orient='index')
                maxs = df.groupby('label')[features].max().to_dict(orient='index')
                _CROP_STATS = {
                    'means': means,
                    'stds': stds,
                    'mins': mins,
                    'maxs': maxs
                }
                return _CROP_STATS
            except Exception:
                pass

        _CROP_STATS = {'means': {}, 'stds': {}, 'mins': {}, 'maxs': {}}
        return _CROP_STATS



# Canonical biological species synonym map to prevent alias duplicates from appearing simultaneously in top 3
CANONICAL_SYNONYM_MAP = {
    "chickpea": "bengal gram",
    "gram": "bengal gram",
    "bengal gram": "bengal gram",
    "bengal_gram": "bengal gram",
    "pigeonpeas": "red gram (arhar / tur)",
    "arhar": "red gram (arhar / tur)",
    "tur": "red gram (arhar / tur)",
    "arhar_tur": "red gram (arhar / tur)",
    "arhar/tur": "red gram (arhar / tur)",
    "red gram": "red gram (arhar / tur)",
    "blackgram": "urad dal",
    "urad": "urad dal",
    "urad dal": "urad dal",
    "urad_dal": "urad dal",
    "black gram": "urad dal",
    "mothbeans": "moth bean",
    "mothbean": "moth bean",
    "moth bean": "moth bean",
    "moth_beans": "moth bean",
    "mungbean": "green gram (moong)",
    "mung": "green gram (moong)",
    "moong": "green gram (moong)",
    "green gram": "green gram (moong)",
    "green_gram": "green gram (moong)",
    "soybean": "soyabean",
    "soyabean": "soyabean",
    "cotton": "cotton",
    "cotton(lint)": "cotton"
}


SOIL_AFFINITIES = {
    "black soil": {
        "preferred": {"cotton", "soyabean", "wheat", "chickpea", "sorghum", "pigeonpeas", "sugarcane", "sunflower", "maize", "groundnut", "gram", "arhar_tur"},
        "avoid": {"tea", "rubber", "coffee"}
    },
    "red soil": {
        "preferred": {"groundnut", "ragi", "bajra", "maize", "castor_seed", "mothbeans", "mungbean", "tobacco", "potato", "pigeonpeas", "cotton", "blackgram"},
        "avoid": {"jute"}
    },
    "alluvial soil": {
        "preferred": {"rice", "wheat", "sugarcane", "jute", "maize", "mustard", "banana", "cotton", "tobacco", "chickpea", "lentil", "papaya", "mango"},
        "avoid": set()
    },
    "clay loam": {
        "preferred": {"rice", "wheat", "gram", "sugarcane", "lentil", "cotton", "soyabean", "chickpea", "maize", "jute"},
        "avoid": {"watermelon", "muskmelon"}
    },
    "sandy loam": {
        "preferred": {"watermelon", "muskmelon", "groundnut", "bajra", "potato", "mothbeans", "cowpea", "cucumber", "onion", "tomato"},
        "avoid": {"rice", "jute"}
    },
    "laterite soil": {
        "preferred": {"coffee", "tea", "cashew", "coconut", "rubber", "arecanut", "black_pepper", "tapioca"},
        "avoid": {"cotton", "wheat"}
    }
}

CROP_GUILDS = {
    # Pulses / Legumes
    "chickpea": "pulse", "gram": "pulse", "bengal gram": "pulse",
    "pigeonpeas": "pulse", "arhar_tur": "pulse", "red gram (arhar / tur)": "pulse",
    "mungbean": "pulse", "green gram (moong)": "pulse",
    "blackgram": "pulse", "urad dal": "pulse",
    "mothbeans": "pulse", "moth bean": "pulse",
    "lentil": "pulse", "kidneybeans": "pulse", "soyabean": "pulse", "groundnut": "pulse",

    # Cereals / Heavy Feeders / Commercial Fibers
    "rice": "cereal", "wheat": "cereal", "maize": "cereal", "sorghum": "cereal",
    "jowar": "cereal", "bajra": "cereal", "ragi": "cereal",
    "cotton": "cereal", "sugarcane": "cereal", "jute": "cereal",

    # Horticultural / Fruits / Plantation / Spices
    "coffee": "hort", "tea": "hort", "coconut": "hort", "banana": "hort", "mango": "hort",
    "grapes": "hort", "apple": "hort", "orange": "hort", "papaya": "hort",
    "pomegranate": "hort", "arecanut": "hort", "black_pepper": "hort", "turmeric": "hort",
    "rubber": "hort", "cashew": "hort",

    # Short duration / Cucurbits / Vegetables
    "watermelon": "veg", "muskmelon": "veg", "tomato": "veg", "potato": "veg", "onion": "veg", "cucumber": "veg"
}

INPUT_SOIL_ADVICE_EN = {
    "pulse_low": "Optimal natural synergy: Biological nitrogen fixation reduces synthetic dependency. Treat seed with Rhizobium & PSB; highly compatible with organic soil biomes.",
    "pulse_moderate": "Balanced starter nutrition: Apply starter N with full P&K basal dose; follow ICAR integrated nutrient management to promote nodule health.",
    "pulse_intensive": "Reduce excessive chemical N: High synthetic nitrogen suppresses root nodulation and increases pest attraction. Apply neem cake and balanced micronutrients.",

    "cereal_low": "High organic matter required: Heavy nutrient feeder. Apply 10–12 t/ha well-decomposed FYM, green manuring (dhaincha), and bio-NPK consortia to support vigorous growth.",
    "cereal_moderate": "Optimal input efficiency: Split nitrogen into 3 doses (50% basal, 25% tillering, 25% flowering) with integrated pest management (IPM) to sustain soil fertility.",
    "cereal_intensive": "Soil structure protection needed: Intensive chemical application risks soil compaction and acidification. Incorporate gypsum/biochar and apply zinc & boron.",

    "hort_low": "Superior quality response: Organic mulching and compost enrich mycorrhizae, improving fruit aroma and shelf life without chemical residues.",
    "hort_moderate": "Balanced canopy & fruit nutrition: Apply fertigation with balanced N:P:K; use Trichoderma root drenching to protect against fungal root wilt.",
    "hort_intensive": "Pesticide management advised: Rotate pesticide chemical groups (MoA) to prevent insect resistance; apply humic acid to prevent soil acidification.",

    "veg_low": "Safe organic harvest: Fast-maturing crop thrives with vermiwash and neem-based biopesticides, ensuring high market premium with zero chemical residues.",
    "veg_moderate": "Precision fertigation recommended: Deliver balanced water-soluble nutrients through drip irrigation to boost size and reduce foliar fungal infections.",
    "veg_intensive": "Observe Pre-Harvest Intervals (PHI): Intensive spraying requires strict adherence to waiting periods before picking; alternate with bio-fungicides to clear residues."
}


def get_crop_guild(crop_id: str) -> str:
    norm = str(crop_id).strip().lower().replace("_", " ").replace("-", " ")
    canon = get_canonical_crop_species(crop_id)
    return CROP_GUILDS.get(norm) or CROP_GUILDS.get(canon) or "cereal"


def get_canonical_crop_species(crop_id: str) -> str:
    """Returns canonical biological species identifier to strictly prevent alias duplication."""
    if not crop_id:
        return ""
    key = str(crop_id).strip().lower().replace("-", "_")
    if key in CANONICAL_SYNONYM_MAP:
        return CANONICAL_SYNONYM_MAP[key]
    key_spaces = str(crop_id).strip().lower()
    if key_spaces in CANONICAL_SYNONYM_MAP:
        return CANONICAL_SYNONYM_MAP[key_spaces]
    cat_id, _ = normalize_crop_name(crop_id)
    if cat_id and cat_id in CANONICAL_SYNONYM_MAP:
        return CANONICAL_SYNONYM_MAP[cat_id]
    return cat_id if cat_id else key


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


def is_crop_climate_compatible(crop: str, input_data: Dict[str, float], stats: Dict[str, Any]) -> bool:
    """
    Strictly filters out climate-mismatched crops from alternative recommendations (Rank 2 and Rank 3).
    """
    temp = input_data["temperature"]
    hum = input_data["humidity"]
    rain = input_data["rainfall"]

    # 1. Temperate cold-climate crops (e.g. apple)
    # Apple requires temperate chilling; strictly incompatible in tropical heat (>25°C), heavy rainfall, or extreme humidity
    if crop == "apple":
        if temp > 25.0 or rain > 150.0 or hum < 60.0:
            return False

    c_mins = stats.get('mins', {}).get(crop, {})
    c_maxs = stats.get('maxs', {}).get(crop, {})
    if not c_mins or not c_maxs:
        return True

    # 2. General biological envelope tolerance
    if temp < c_mins.get("temperature", 0) - 6.0 or temp > c_maxs.get("temperature", 50) + 6.0:
        return False
    if hum < c_mins.get("humidity", 0) - 15.0 or hum > c_maxs.get("humidity", 100) + 15.0:
        return False
    if rain < c_mins.get("rainfall", 0) * 0.35 or rain > c_maxs.get("rainfall", 500) * 2.2:
        return False

    # 3. Water-sensitive pulse/legume gating (pulses suffer fatal wilt/rot under heavy rainfall)
    if crop in ("chickpea", "lentil", "mothbeans", "kidneybeans") and rain > 160.0:
        return False

    # 4. Wetland crop gating (rice and jute fail without adequate water)
    if crop in ("rice", "jute") and (rain < 100.0 or hum < 60.0):
        return False

    # 5. Cucurbit fruit cracking gating
    if crop in ("watermelon", "muskmelon") and rain > 130.0:
        return False

    # 6. Cotton boll rot gating
    if crop == "cotton" and rain > 160.0:
        return False

    return True


def recommend_crop_top3_detailed(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Return top 3 crops with calibrated confidence percentages, climate gating, and dynamic diagnosis."""
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

    stats = get_crop_agronomic_stats()
    means = stats.get('means', {})
    stds = stats.get('stds', {})
    mins = stats.get('mins', {})
    maxs = stats.get('maxs', {})

    # 1. Rank #1 must strictly remain the top ML prediction
    top1_crop, top1_prob = ranked[0]
    seen_species = {get_canonical_crop_species(top1_crop)}

    # 2. Select Rank #2 and Rank #3 from climate-compatible alternatives with strict species deduplication
    inp_v = np.array([validated[f] for f in FEATURE_COLUMNS])
    weights = np.array([1.0, 1.0, 1.0, 1.5, 1.2, 1.0, 1.5])

    candidates = []
    alt_probs = [p for c, p in ranked[1:]]
    max_alt_p = max(alt_probs) if alt_probs else 0.01
    if max_alt_p <= 0:
        max_alt_p = 0.01

    for c, p in ranked[1:]:
        c_spec = get_canonical_crop_species(c)
        if c_spec in seen_species:
            continue
        if not is_crop_climate_compatible(c, validated, stats):
            continue

        if c in means and c in stds:
            m = np.array([means[c].get(f, 0.0) for f in FEATURE_COLUMNS])
            s = np.array([stds[c].get(f, 1.0) for f in FEATURE_COLUMNS])
            z = (inp_v - m) / s
            dist = float(np.sqrt(np.sum(weights * (z ** 2))))
            fit = float(np.exp(-dist / 8.0))
        else:
            fit = 0.5

        ml_score = float(p / max_alt_p) if max_alt_p > 0 else 0.0
        comb_score = 0.5 * ml_score + 0.5 * fit
        candidates.append((c, p, comb_score, fit, c_spec))

    candidates.sort(key=lambda x: x[2], reverse=True)

    # Pick top distinct biological species for Rank 2 and Rank 3
    selected_alts = []
    for cand in candidates:
        cand_crop, cand_p, cand_score, cand_fit, cand_spec = cand
        if cand_spec not in seen_species:
            selected_alts.append((cand_crop, cand_p, cand_score, cand_fit))
            seen_species.add(cand_spec)
        if len(selected_alts) >= 2:
            break

    # Fallback to ensure we ALWAYS have at least 2 distinct alternative candidates
    if len(selected_alts) < 2:
        for c, p in ranked[1:]:
            c_spec = get_canonical_crop_species(c)
            if c_spec in seen_species:
                continue
            if c == "apple" and (validated["temperature"] > 25.0 or validated["rainfall"] > 150.0):
                continue
            if c in means and c in stds:
                m = np.array([means[c].get(f, 0.0) for f in FEATURE_COLUMNS])
                s = np.array([stds[c].get(f, 1.0) for f in FEATURE_COLUMNS])
                z = (inp_v - m) / s
                dist = float(np.sqrt(np.sum(weights * (z ** 2))))
                fit = float(np.exp(-dist / 8.0))
            else:
                fit = 0.1
            selected_alts.append((c, p, fit, fit))
            seen_species.add(c_spec)
            if len(selected_alts) >= 2:
                break

    top2_candidate = selected_alts[0] if len(selected_alts) > 0 else ("maize", 0.0, 0.5, 0.5)
    top3_candidate = selected_alts[1] if len(selected_alts) > 1 else ("sorghum", 0.0, 0.3, 0.3)

    # 3. Normalize probability distribution across Top 3
    # Rank #1 remains dominant, while Rank #2 and Rank #3 display practical viable alternatives
    p1 = float(top1_prob)
    p2 = float(top2_candidate[1])
    p3 = float(top3_candidate[1])

    if p1 >= 0.85 or p2 < 0.10 or p3 < 0.05:
        conf1 = round(min(80.0, max(72.0, 70.0 + p1 * 10.0)), 1)
        rem = round(100.0 - conf1, 1)
        conf3 = round(max(6.0, min(8.5, rem * 0.35)), 1)
        conf2 = round(100.0 - conf1 - conf3, 1)
        confs = [conf1, conf2, conf3]
    else:
        tot = p1 + p2 + p3
        if tot <= 0:
            tot = 1.0
        c1 = (p1 / tot) * 100
        c2 = (p2 / tot) * 100
        c3 = (p3 / tot) * 100
        if c3 < 6.0:
            c3 = 6.0
            rem = 94.0
            c1 = round((p1 / (p1 + p2)) * rem, 1)
            c2 = round(100.0 - c1 - c3, 1)
            confs = [c1, c2, c3]
        else:
            conf1 = round(c1, 1)
            conf2 = round(c2, 1)
            conf3 = round(100.0 - conf1 - conf2, 1)
            confs = [conf1, conf2, conf3]

    chosen_tuples = [
        (top1_crop, top1_prob, 1.0, 0.95),
        top2_candidate,
        top3_candidate
    ]

    top_results = []
    n_val = validated["N"]
    p_val = validated["P"]
    k_val = validated["K"]
    ph_val = validated["ph"]
    temp_val = validated["temperature"]
    rain_val = validated["rainfall"]

    for rank, ((crop_class, raw_prob, score, fit), conf) in enumerate(zip(chosen_tuples, confs), 1):
        _, cat_info = normalize_crop_name(crop_class)

        # Dynamic Agronomic Diagnosis tailored per crop
        c_mins = mins.get(crop_class, {})
        c_maxs = maxs.get(crop_class, {})

        c_n_min = c_mins.get("N", 60.0)
        c_n_max = c_maxs.get("N", 120.0)
        c_p_min = c_mins.get("P", 35.0)
        c_p_max = c_maxs.get("P", 80.0)
        c_k_min = c_mins.get("K", 35.0)
        c_k_max = c_maxs.get("K", 90.0)
        c_ph_min = c_mins.get("ph", 6.0)
        c_ph_max = c_maxs.get("ph", 7.5)

        if n_val < c_n_min:
            n_desc = "Slight nitrogen deficit"
        elif n_val > c_n_max:
            n_desc = "High nitrogen reserve"
        else:
            n_desc = "Optimal vegetative nitrogen"

        if p_val < c_p_min:
            p_desc = "Phosphorus deficit"
        elif p_val > c_p_max:
            p_desc = "Elevated phosphorus"
        else:
            p_desc = "Balanced for root architecture"

        if k_val < c_k_min:
            k_desc = "Low potash buffer"
        elif k_val > c_k_max:
            k_desc = "High potash reserve"
        else:
            k_desc = "Robust stress & disease tolerance"

        if ph_val < c_ph_min:
            ph_desc = f"pH {ph_val} (Mildly Acidic)"
        elif ph_val > c_ph_max:
            ph_desc = f"pH {ph_val} (Mildly Alkaline)"
        else:
            ph_desc = f"pH {ph_val} (Neutral — high nutrient availability)"

        if rank == 1:
            climate_desc = f"{temp_val}°C & {rain_val}mm rainfall provide strong agro-climatic alignment"
            feasibility_score = min(98, max(85, int(70 + fit * 20 + conf * 0.1)))
        elif rank == 2:
            climate_desc = f"{temp_val}°C & {rain_val}mm rainfall provide suitable agro-climatic conditions"
            feasibility_score = min(94, max(78, int(60 + fit * 25 + conf * 0.4)))
        else:
            climate_desc = f"{temp_val}°C & {rain_val}mm rainfall provide suitable agro-climatic conditions"
            feasibility_score = min(89, max(72, int(56 + fit * 25 + conf * 0.5)))

        feasibility_status = "High Agronomic Feasibility" if feasibility_score >= 70 else "Moderate Agronomic Feasibility"
        n_disp = int(n_val) if n_val == int(n_val) else n_val
        p_disp = int(p_val) if p_val == int(p_val) else p_val
        k_disp = int(k_val) if k_val == int(k_val) else k_val
        npk_str = f"N: {n_disp} ({n_desc}) • P: {p_disp} ({p_desc}) • K: {k_disp} ({k_desc})"

        feasibility = {
            "soil_npk_analysis": npk_str,
            "soil_ph_suitability": ph_desc,
            "climate_suitability": climate_desc,
            "input_temperature": temp_val,
            "input_rainfall": rain_val,
            "feasibility_index": f"{feasibility_score}/100 {feasibility_status}",
            "feasibility_score": feasibility_score,
            "feasibility_status": feasibility_status,
            "overall_verdict": f"{feasibility_status} ({feasibility_score}%)",
            "npk_analysis": npk_str,
            "ph_compatibility": ph_desc,
            "climate_alignment": climate_desc,
            "soil_n_status": f"N: {n_val} ({n_desc})",
            "soil_p_status": f"P: {p_val} ({p_desc})",
            "soil_k_status": f"K: {k_val} ({k_desc})",
            "ph_suitability": ph_desc
        }

        top_results.append({
            "rank": rank,
            "crop_id": crop_class,
            "canonical_species": get_canonical_crop_species(crop_class),
            "name": cat_info["name"] if cat_info else crop_class.capitalize(),
            "input_temperature": temp_val,
            "input_rainfall": rain_val,
            "confidence_pct": conf,
            "category": cat_info["category"] if cat_info else "Agricultural Crop",
            "duration": cat_info["duration_days"] if cat_info else "Seasonal",
            "water_req": cat_info["water_req"] if cat_info else "Moderate",
            "cultivation_feasibility": feasibility,
            "npk_analysis": npk_str,
            "ph_compatibility": ph_desc,
            "climate_alignment": climate_desc,
            "feasibility_score": feasibility_score,
            "feasibility_status": feasibility_status,
            "advisory": cat_info["advisory_tips"] if cat_info else {}
        })

    return {
        "recommended_crop": top_results[0]["crop_id"] if top_results else None,
        "top_3": [r["crop_id"] for r in top_results],
        "top_3_detailed": top_results,
        "input": validated
    }


def recommend_crop_top3(input_data: Dict[str, Any]) -> List[str]:
    """Return top 3 crops from the trained Crop Recommendation model."""
    detailed = recommend_crop_top3_detailed(input_data)
    return detailed["top_3"]


def recommend_crop(input_data: Dict[str, Any]) -> str:
    top_3 = recommend_crop_top3(input_data)
    return top_3[0] if top_3 else FARM_PLANNING_CROPS[0]


# Farm planning functions (recommend_farm_plan, recommend_farm_plan_detailed, generate_timeline_guidance)
# are imported and exported from app.services.farm_planning above.
__all__ = [
    "CropInputError",
    "recommend_crop",
    "recommend_crop_top3",
    "recommend_crop_top3_detailed",
    "recommend_farm_plan",
    "recommend_farm_plan_detailed",
    "generate_timeline_guidance",
    "CROP_CHARACTERISTICS",
    "FARM_PLANNING_CROPS",
    "FEATURE_COLUMNS",
    "INPUT_RANGES",
]


# ==============================================================================
# IN-MEMORY MODEL PRE-WARMING (Eliminates Disk I/O Latency)
# ==============================================================================
try:
    load_recommendation_model()
    get_crop_agronomic_stats()
except Exception:
    pass
