"""
RythuCrop Farm Planning Recommendation Engine
High-precision agronomic scoring engine with strict seasonal gating,
soil-water affinity matrices, anti-monopoly balancing, and rotation diversification.
"""

from typing import Dict, List, Any, Tuple
from app.data.crops_data import CROP_DATA
from app.data.agri_taxonomy import FARM_PLANNING_21_CROPS, normalize_crop_name

# Area classification bounds
LAND_AREA_SUITABILITY = {
    'Small': (0.1, 2.0),
    'Medium': (2.0, 10.0),
    'Large': (10.0, float('inf'))
}


def normalize_season(season_raw: str) -> str:
    """Normalizes input season string into standard canonical key."""
    s = str(season_raw).strip().lower()
    if "kharif" in s or "monsoon" in s:
        return "Kharif"
    elif "rabi" in s or "winter" in s:
        return "Rabi"
    elif "summer" in s or "zaid" in s:
        return "Summer"
    elif "whole" in s or "year" in s or "annual" in s or "perennial" in s:
        return "Whole Year"
    return "Kharif"


def normalize_soil(soil_raw: str) -> str:
    """Normalizes input soil type into standard canonical key."""
    s = str(soil_raw).strip().lower()
    if "black" in s:
        return "Black Soil"
    elif "red" in s:
        return "Red Soil"
    elif "clay" in s:
        return "Clay Soil"
    elif "sandy" in s:
        return "Sandy Soil"
    elif "alluvial" in s:
        return "Alluvial"
    return "Loamy"


def normalize_irrigation(irrig_raw: str) -> str:
    """Normalizes water availability input into standard canonical key."""
    i = str(irrig_raw).strip().lower()
    if "good" in i or "high" in i or "assured" in i:
        return "Good water availability"
    elif "low" in i:
        return "Low water availability"
    elif "rainfed" in i or "dryland" in i:
        return "Rainfed"
    return "Moderate water availability"


def generate_timeline_guidance(crop: str, season: str, irrigation: str, lang: str = "en") -> Dict[str, str]:
    """Generates automated timeline and irrigation guidance for farm planning."""
    s_lower = season.lower()
    is_zaid = "summer" in s_lower or "zaid" in s_lower
    is_rabi = "rabi" in s_lower or "winter" in s_lower
    is_whole = "whole" in s_lower or "year" in s_lower

    if is_whole:
        sowing = "June to August or February to March (Perennial / Annual planting)"
        vegetative = "Months 2 - 5: Intensive root establishment, tillering/branching, and organic basal feeding"
        flowering = "Months 6 - 9: Vegetative stabilization, button/cane development, and micronutrient fertigation"
        harvest = "Months 10 - 14: Staggered commercial harvest or annual cane/rhizome cutting"
    elif is_zaid:
        sowing = "Late Feb to Mid March (Zaid / Summer cycle)"
        vegetative = "Weeks 3 - 6: Active canopy expansion; inter-cultivation & mulching"
        flowering = "Weeks 7 - 10: Critical flowering & pod setting; maintain frequent light irrigations"
        harvest = "May to June: Dry pod/grain maturity; harvest before pre-monsoon showers"
    elif is_rabi:
        sowing = "Mid October to November (Post-monsoon Rabi sowing)"
        vegetative = "Weeks 3 - 7: Active tillering & root branching; apply 1st nitrogen top-dress"
        flowering = "Weeks 8 - 12: Panicle emergence / anthesis; ensure zero moisture stress"
        harvest = "March to April: Golden grain maturity; harvest at 14-16% moisture"
    else:  # Kharif / Monsoon
        sowing = "June to July (With the onset of southwest monsoon)"
        vegetative = "Weeks 3 - 6: Active tillering / canopy establishment; weed control critical"
        flowering = "Weeks 7 - 11: Heading & grain/pod fill; monitor for stem borer and blight"
        harvest = "October to November: Field drainage & harvest when 85% panicles turn golden"

    irrig_lower = irrigation.lower()
    if "rainfed" in irrig_lower:
        irrig_note = "Conserve soil moisture with contour bunding and organic mulching; apply life-saving protective irrigation if monsoon breaks exceed 10 days."
    elif "low" in irrig_lower:
        irrig_note = "Adopt drip or micro-sprinkler fertigation (saves 35-40% water); prioritize irrigations at crown root initiation and flowering."
    else:
        irrig_note = "Schedule 4-5 timed irrigations aligned with crown root, active tillering, flowering, and grain filling stages."

    res = {
        "sowing_window": sowing,
        "vegetative_phase": vegetative,
        "flowering_phase": flowering,
        "harvest_window": harvest,
        "irrigation_advice": irrig_note
    }

    if lang and lang != "en":
        from app.data.farm_planning_i18n import localize_text
        res = {k: localize_text(v, lang) for k, v in res.items()}

    return res


def recommend_farm_plan(farm_data: Dict[str, Any]) -> List[str]:
    """
    Recommend suitable crops based on Farm Planning inputs.
    Strictly preserves the 6 payload inputs and returns top 5 crops from FARM_PLANNING_21_CROPS.
    """
    detailed = recommend_farm_plan_detailed(farm_data)
    return detailed["recommended_crops"]


def recommend_farm_plan_detailed(farm_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Comprehensive agronomic farm planning engine.
    Applies strict season gating, accurate soil-water affinity matrices,
    anti-monopoly balancing, and rotational diversity.
    """
    # Retrieve active user language dynamically from payload, request context, or session
    lang = farm_data.get('lang')
    if not lang:
        try:
            from flask import request, session, has_request_context
            if has_request_context():
                lang = (
                    request.args.get('lang') or 
                    (request.is_json and request.get_json(silent=True) and request.get_json(silent=True).get('lang')) or
                    session.get('lang') or 
                    'en'
                )
        except Exception:
            lang = 'en'
    lang = str(lang or 'en').strip().lower()
    if lang not in ('en', 'te', 'hi', 'ta', 'kn', 'ml', 'mr', 'bn', 'gu', 'od'):
        lang = 'en'

    try:
        land = float(farm_data.get('land', 1.0))
        if land <= 0:
            land = 1.0
    except (ValueError, TypeError):
        land = 1.0

    raw_season = str(farm_data.get('season', 'Kharif')).strip()
    raw_soil = str(farm_data.get('soil', 'Loamy')).strip()
    raw_irrigation = str(farm_data.get('irrigation', 'Moderate water availability')).strip()
    goal = str(farm_data.get('goal', 'Balanced farming')).strip()
    experience = str(farm_data.get('experience', 'Beginner')).strip()

    norm_season = normalize_season(raw_season)
    norm_soil = normalize_soil(raw_soil)
    norm_irrigation = normalize_irrigation(raw_irrigation)

    # Determine land size category
    land_size = 'Small'
    for size_cat, (min_l, max_l) in LAND_AREA_SUITABILITY.items():
        if min_l <= land < max_l:
            land_size = size_cat
            break
    else:
        land_size = 'Large'

    crop_scores: Dict[str, int] = {}
    crop_reasons: Dict[str, List[str]] = {}

    for crop_name in FARM_PLANNING_21_CROPS:
        if crop_name not in CROP_DATA:
            continue

        c = CROP_DATA[crop_name]
        score = 0
        reasons: List[str] = []

        is_plantation = c.get("crop_type") == "plantation"
        is_perennial = c.get("crop_type") in ("plantation", "perennial")

        # -------------------------------------------------------------
        # 1. STRICT SEASON GATING & PERENNIAL GATING
        # -------------------------------------------------------------
        if norm_season == "Whole Year":
            if "Whole Year" in c["seasons"]:
                score += 35
                reasons.append("Highly suited for Whole Year annual/plantation cycle")
            else:
                # Perennial/plantation crops take priority for Whole Year plans
                score -= 50
        elif is_plantation or is_perennial:
            # Plantation & Perennial crops (Arecanut, Coconut, Black pepper, Sugarcane, Turmeric)
            # MUST ONLY qualify when Season == "Whole Year" (-100 penalty otherwise)
            score -= 100
        elif norm_season == "Kharif":
            if "Kharif" in c["seasons"]:
                score += 30
                reasons.append("Highly suited for Kharif season")
            else:
                # Strictly penalize non-Kharif or perennial crops
                score -= 80
        elif norm_season == "Rabi":
            if "Rabi" in c["seasons"]:
                score += 30
                reasons.append("Highly suited for Rabi season")
            else:
                # Strictly penalize non-Rabi or perennial crops
                score -= 80
        elif norm_season == "Summer":
            if "Summer" in c["seasons"]:
                score += 30
                reasons.append("High heat tolerance suited for Summer (Zaid) season")
            else:
                # Water-heavy Kharif/Rabi crops get -100 penalty in Summer
                score -= 100

        # Special Rice check: Rice in Summer or Rabi requires Good water availability
        if crop_name == "Rice" and norm_season in ("Summer", "Rabi") and norm_irrigation != "Good water availability":
            score -= 90

        # -------------------------------------------------------------
        # 2. SOIL TYPE COMPATIBILITY MATRIX
        # -------------------------------------------------------------
        soil_affinity = c["soils"].get(norm_soil, 0)
        score += soil_affinity
        if soil_affinity >= 24:
            reasons.append(f"Thrives in {raw_soil}")
        elif soil_affinity > 10:
            reasons.append(f"Moderately adaptable to {raw_soil}")

        # -------------------------------------------------------------
        # 3. WATER AVAILABILITY MATCHING
        # -------------------------------------------------------------
        water_affinity = c["water_affinity"].get(norm_irrigation, 0)
        score += water_affinity
        if water_affinity >= 24:
            reasons.append(f"Compatible with {raw_irrigation}")
        elif norm_irrigation in ("Low water availability", "Rainfed") and water_affinity >= 18:
            reasons.append("High drought and moisture stress tolerance")

        # -------------------------------------------------------------
        # 4. ROTATION & SOIL HEALTH (ANTI-MONOPOLY & LEGUME BONUS)
        # -------------------------------------------------------------
        rot_group = c.get("rotation_group", "")
        soil_dep = c.get("soil_depletion", "medium")

        if rot_group in ("legume_pulse", "legume_oilseed") or soil_dep == "restorative":
            # Pulses and legumes fix atmospheric nitrogen and enrich soil
            score += 10
            reasons.append("Restores soil nitrogen and enriches rotational soil health")
        elif soil_dep == "exhaustive":
            # Heavy feeding crops (Maize, Sugarcane, Potato)
            if goal in ("Lower input cost", "Lower water use"):
                score -= 12
            else:
                score -= 2  # Slight dampening to prevent monopolizing

        # -------------------------------------------------------------
        # 5. GOAL & EXPERIENCE ALIGNMENT
        # -------------------------------------------------------------
        if goal in c.get("goals", []):
            score += 8
            reasons.append(f"Directly supports {goal.lower()} target")

        if experience in c.get("experience", []):
            score += 10
        elif experience == "Some experience" and "Beginner" in c.get("experience", []):
            score += 8
        elif experience == "Beginner" and "Experienced" in c.get("experience", []) and len(c.get("experience", [])) == 1:
            score -= 15  # Complex crop for complete beginner

        # -------------------------------------------------------------
        # 6. LAND AREA PREFERENCE
        # -------------------------------------------------------------
        if land_size in c.get("land_suitability", []):
            score += 6
            reasons.append(f"Efficient land utilization for {land} acres")

        crop_scores[crop_name] = score
        crop_reasons[crop_name] = reasons

    # Rank crops by score descending
    ranked = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)

    recommended_crops: List[str] = []
    plan_details: List[Dict[str, Any]] = []

    # Category diversity tracker to avoid 5 identical cereals
    seen_groups: Dict[str, int] = {}

    for crop_name, score in ranked:
        if score <= 0:
            continue

        c_info = CROP_DATA.get(crop_name, {})
        grp = c_info.get("rotation_group", "general")

        # Allow at most 2 crops from the exact same rotation group unless Whole Year or list is small
        if norm_season != "Whole Year" and seen_groups.get(grp, 0) >= 2 and len(recommended_crops) < 4:
            continue

        recommended_crops.append(crop_name)
        seen_groups[grp] = seen_groups.get(grp, 0) + 1

        import re
        from app.data.farm_planning_i18n import localize_text, CROP_PLAN_ADVISORY, ECONOMICS_TRANSLATIONS

        timeline = generate_timeline_guidance(crop_name, raw_season, raw_irrigation, lang=lang)
        timeline_en = generate_timeline_guidance(crop_name, raw_season, raw_irrigation, lang="en")
        reasons_en = list(crop_reasons.get(crop_name, ["Suitable agronomic baseline"]))
        reasons = [localize_text(r, lang) for r in reasons_en] if lang != "en" else list(reasons_en)

        econ = c_info.get("economics", {
            "estimated_cost_per_acre": "₹15,000 - ₹25,000",
            "estimated_gross_return": "₹40,000 - ₹65,000",
            "estimated_profit_per_acre": "₹22,000 - ₹40,000",
            "market_demand": "Active local mandi demand"
        })

        crop_adv = CROP_PLAN_ADVISORY.get(crop_name)
        if not crop_adv:
            norm_key = re.sub(r"[\(\)\s/]", "_", crop_name.lower()).strip("_")
            crop_adv = CROP_PLAN_ADVISORY.get(norm_key, {})

        en_soil = c_info.get("soil_guidance", f"{raw_soil} requires proper aeration and organic matter addition.")
        en_water = c_info.get("water_scheduling", f"Ensure moisture scheduling matching {raw_irrigation.lower()}.")
        en_risks = c_info.get("risks", "Seasonal rainfall fluctuations, pest pressure during vegetative growth, and harvest market volatility.")
        en_next = c_info.get("next_steps", "Test soil NPK/micronutrient levels, prepare certified seed with fungicide dressing, and confirm local mandi availability.")

        if lang != "en" and crop_adv:
            soil_guidance = crop_adv.get("soil_guidance", {}).get(lang) or localize_text(en_soil, lang)
            water_scheduling = crop_adv.get("water_scheduling", {}).get(lang) or localize_text(en_water, lang)
            risks = crop_adv.get("risks", {}).get(lang) or localize_text(en_risks, lang)
            next_steps = crop_adv.get("next_steps", {}).get(lang) or localize_text(en_next, lang)
            market_demand = crop_adv.get("market_demand", {}).get(lang) or econ.get("market_demand", "")
        else:
            soil_guidance = en_soil
            water_scheduling = en_water
            risks = en_risks
            next_steps = en_next
            market_demand = econ.get("market_demand", "Active local mandi demand")

        # Economics
        per_acre_suffix = ECONOMICS_TRANSLATIONS.get("per_acre_suffix", {}).get(lang, " / acre") if lang != "en" else " / acre"
        econ_entry = dict(econ)
        if lang != "en":
            for cost_k in ["estimated_cost_per_acre", "estimated_gross_return", "estimated_profit_per_acre"]:
                if cost_k in econ_entry:
                    val = str(econ_entry[cost_k])
                    if "₹" not in val and not val.startswith("Rs"):
                        val = f"₹{val}"
                    clean_val = re.sub(r"\s*/\s*(?:acre|ఎకరాకి|एकड़|ஏக்கர்|ಎಕರೆಗೆ|ഏക്കറിന്|एकर|একর|એકર|ଏକର)?$", "", val, flags=re.IGNORECASE)
                    econ_entry[cost_k] = f"{clean_val}{per_acre_suffix}"
            econ_entry["market_demand"] = market_demand

        detail_entry = {
            # Legacy keys (expected by frontend renderFarmPlanResults and existing tests)
            "crop": crop_name,
            "score": score,
            "reasons": reasons,
            "timeline_guidance": timeline,
            "soil_consideration": soil_guidance,
            "water_consideration": water_scheduling,
            "risks": risks,
            "next_steps": next_steps,
            # New modern API keys and multilingual fields
            "crop_name": crop_name,
            "suitability_score": score,
            "key_reasons": reasons,
            "soil_guidance": soil_guidance,
            "water_scheduling": water_scheduling,
            "economics": econ_entry,
            "reasons_en": reasons_en,
            "timeline_guidance_en": timeline_en,
            "soil_consideration_en": en_soil,
            "water_consideration_en": en_water,
            "risks_en": en_risks,
            "next_steps_en": en_next,
            "lang": lang
        }
        plan_details.append(detail_entry)

        if len(recommended_crops) >= 5:
            break

    # Fallback to ensure at least 2 crops if score filtering was too stringent
    if len(recommended_crops) < 2:
        for crop_name, score in ranked:
            if crop_name not in recommended_crops:
                recommended_crops.append(crop_name)
                c_info = CROP_DATA.get(crop_name, {})
                timeline = generate_timeline_guidance(crop_name, raw_season, raw_irrigation, lang=lang)
                timeline_en = generate_timeline_guidance(crop_name, raw_season, raw_irrigation, lang="en")
                reasons_en = list(crop_reasons.get(crop_name, ["Suitable agronomic baseline"]))
                reasons = [localize_text(r, lang) for r in reasons_en] if lang != "en" else list(reasons_en)
                econ = c_info.get("economics", {
                    "estimated_cost_per_acre": "₹15,000 - ₹25,000",
                    "estimated_gross_return": "₹40,000 - ₹65,000",
                    "estimated_profit_per_acre": "₹22,000 - ₹40,000",
                    "market_demand": "Active local mandi demand"
                })
                crop_adv = CROP_PLAN_ADVISORY.get(crop_name)
                if not crop_adv:
                    norm_key = re.sub(r"[\(\)\s/]", "_", crop_name.lower()).strip("_")
                    crop_adv = CROP_PLAN_ADVISORY.get(norm_key, {})

                en_soil = c_info.get("soil_guidance", f"{raw_soil} requires proper aeration and organic matter addition.")
                en_water = c_info.get("water_scheduling", f"Ensure moisture scheduling matching {raw_irrigation.lower()}.")
                en_risks = c_info.get("risks", "Seasonal rainfall fluctuations, pest pressure during vegetative growth, and harvest market volatility.")
                en_next = c_info.get("next_steps", "Test soil NPK/micronutrient levels, prepare certified seed with fungicide dressing, and confirm local mandi availability.")

                if lang != "en" and crop_adv:
                    soil_guidance = crop_adv.get("soil_guidance", {}).get(lang) or localize_text(en_soil, lang)
                    water_scheduling = crop_adv.get("water_scheduling", {}).get(lang) or localize_text(en_water, lang)
                    risks = crop_adv.get("risks", {}).get(lang) or localize_text(en_risks, lang)
                    next_steps = crop_adv.get("next_steps", {}).get(lang) or localize_text(en_next, lang)
                    market_demand = crop_adv.get("market_demand", {}).get(lang) or econ.get("market_demand", "")
                else:
                    soil_guidance = en_soil
                    water_scheduling = en_water
                    risks = en_risks
                    next_steps = en_next
                    market_demand = econ.get("market_demand", "Active local mandi demand")

                per_acre_suffix = ECONOMICS_TRANSLATIONS.get("per_acre_suffix", {}).get(lang, " / acre") if lang != "en" else " / acre"
                econ_entry = dict(econ)
                if lang != "en":
                    for cost_k in ["estimated_cost_per_acre", "estimated_gross_return", "estimated_profit_per_acre"]:
                        if cost_k in econ_entry:
                            val = str(econ_entry[cost_k])
                            if "₹" not in val and not val.startswith("Rs"):
                                val = f"₹{val}"
                            clean_val = re.sub(r"\s*/\s*(?:acre|ఎకరాకి|एकड़|ஏக்கர்|ಎಕರೆಗೆ|ഏക്കറിന്|एकर|একর|એકર|ଏକର)?$", "", val, flags=re.IGNORECASE)
                            econ_entry[cost_k] = f"{clean_val}{per_acre_suffix}"
                    econ_entry["market_demand"] = market_demand

                plan_details.append({
                    "crop": crop_name,
                    "score": max(score, 10),
                    "reasons": reasons,
                    "timeline_guidance": timeline,
                    "soil_consideration": soil_guidance,
                    "water_consideration": water_scheduling,
                    "risks": risks,
                    "next_steps": next_steps,
                    "crop_name": crop_name,
                    "suitability_score": max(score, 10),
                    "key_reasons": reasons,
                    "soil_guidance": soil_guidance,
                    "water_scheduling": water_scheduling,
                    "economics": econ_entry,
                    "reasons_en": reasons_en,
                    "timeline_guidance_en": timeline_en,
                    "soil_consideration_en": en_soil,
                    "water_consideration_en": en_water,
                    "risks_en": en_risks,
                    "next_steps_en": en_next,
                    "lang": lang
                })
            if len(recommended_crops) >= 5:
                break

    disclaimer = "These are agro-advisory suggestions based on machine learning and agronomic heuristics. Actual yields depend on local weather, timely cultivation, and disease management."
    if lang != "en":
        from app.data.farm_planning_i18n import localize_text
        disclaimer = localize_text(disclaimer, lang)

    return {
        "recommended_crops": recommended_crops,
        "plan_details": plan_details,
        "inputs_preserved": {
            "land": land,
            "season": raw_season,
            "soil": raw_soil,
            "irrigation": raw_irrigation,
            "goal": goal,
            "experience": experience
        },
        "disclaimer": disclaimer
    }
