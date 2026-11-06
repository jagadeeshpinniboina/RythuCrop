# Pre-Harvest Yield Prediction Engine
# Uses retrained Leakage-Free Random Forest Pipeline with Target Log-Transformation.
# Integrates strict ICAR State & Crop Agro-Climatic Feasibility Gating and Comprehensive Seasonal Affinity Matrix.
# Predicts yield per hectare and calculates total estimated production.
import os
import joblib
import numpy as np
import pandas as pd
import threading
from typing import Dict, Any, List, Optional
from app.data.geo_data import get_state_agri_baseline
from app.data.agri_taxonomy import normalize_crop_name

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "saved_models", "crop_yield_model.pkl")

# Cached model instance & thread lock
_YIELD_MODEL_LOCK = threading.Lock()
_YIELD_MODEL = None

def load_yield_model():
    global _YIELD_MODEL
    if _YIELD_MODEL is None:
        with _YIELD_MODEL_LOCK:
            if _YIELD_MODEL is None:
                if not os.path.exists(MODEL_PATH):
                    raise FileNotFoundError(f"Yield model artifact not found: {MODEL_PATH}")
                _YIELD_MODEL = joblib.load(MODEL_PATH)
    return _YIELD_MODEL

# ==============================================================================
# ICAR AGRO-CLIMATIC STATE FEASIBILITY MATRIX & GATING RULES
# ==============================================================================

AGRO_CLIMATIC_MATRIX = {
    # 1. Alpine / Cold Temperate Regions
    "jammu and kashmir": {
        "unviable": {
            "rice", "paddy", "sugarcane", "cotton", "cotton(lint)",
            "coconut", "arecanut", "cashewnut", "banana", "black pepper",
            "cardamom", "tapioca", "rubber", "jute", "groundnut",
            "soyabean", "soybean"
        },
        "reasons": {
            "rice": ("warning_jk_paddy", "High-altitude alpine temperatures and short thermal windows in Jammu & Kashmir restrict commercial wetland paddy productivity; extreme cold irrigation water causes severe spikelet sterility and vegetative stunting."),
            "paddy": ("warning_jk_paddy", "High-altitude alpine temperatures and short thermal windows in Jammu & Kashmir restrict commercial wetland paddy productivity; extreme cold irrigation water causes severe spikelet sterility and vegetative stunting."),
            "sugarcane": ("warning_frost_tropical", "Sub-zero winter temperatures, severe frost, and inadequate thermal heat units prevent cane elongation and sucrose accumulation, causing complete commercial failure."),
            "cotton": ("warning_frost_tropical", "Cotton requires 180–200 frost-free days with warm temperatures (>21°C). Alpine cold halts boll development and causes premature boll drop."),
            "cotton(lint)": ("warning_frost_tropical", "Cotton requires 180–200 frost-free days with warm temperatures (>21°C). Alpine cold halts boll development and causes premature boll drop."),
            "coconut": ("warning_palm_frost", "Tropical coastal palm; intolerant to sub-zero temperatures and frost, suffering fatal vascular chilling injury."),
            "arecanut": ("warning_palm_frost", "Perennial tropical palm highly susceptible to freezing winter temperatures and low atmospheric humidity."),
            "banana": ("warning_palm_frost", "Tropical herb highly sensitive to frost; sub-zero temperatures cause fatal pseudostem collapse and leaf necrosis."),
            "default": ("warning_default_mismatch", "Alpine climate, severe winter frost, and low cumulative heat units prevent viable commercial cultivation.")
        },
        "compatible": ["Wheat", "Barley", "Maize", "Potato", "Apple", "Rapeseed &Mustard", "Peas & beans (Pulses)"]
    },
    "ladakh": {
        "unviable": {
            "rice", "paddy", "sugarcane", "cotton", "cotton(lint)",
            "coconut", "arecanut", "cashewnut", "banana", "black pepper",
            "cardamom", "tapioca", "rubber", "jute", "groundnut",
            "soyabean", "soybean"
        },
        "reasons": {
            "rice": ("warning_jk_paddy", "Cold arid high-altitude conditions and freezing nights cause complete spikelet sterility in wetland rice."),
            "paddy": ("warning_jk_paddy", "Cold arid high-altitude conditions and freezing nights cause complete spikelet sterility in wetland rice."),
            "sugarcane": ("warning_frost_tropical", "Extreme freezing sub-zero temperatures and high altitude make sugarcane growth impossible."),
            "cotton": ("warning_frost_tropical", "Short growing season and extreme cold prevent cotton boll development."),
            "cotton(lint)": ("warning_frost_tropical", "Short growing season and extreme cold prevent cotton boll development."),
            "coconut": ("warning_palm_frost", "Intolerant to cold desert sub-zero winters."),
            "default": ("warning_default_mismatch", "Cold arid desert conditions with extreme freezing winters make tropical and wetland commercial crops biologically unviable.")
        },
        "compatible": ["Barley", "Wheat", "Potato", "Apple", "Peas & beans (Pulses)"]
    },
    "himachal pradesh": {
        "unviable": {
            "rice", "paddy", "soyabean", "soybean", "sugarcane", "cotton", "cotton(lint)",
            "coconut", "arecanut", "cashewnut", "banana", "black pepper", "cardamom",
            "tapioca", "rubber", "jute"
        },
        "reasons": {
            "rice": ("warning_jk_paddy", "High-altitude alpine temperatures and short thermal windows in Himachal Pradesh hill zones restrict commercial wetland paddy productivity; cold water causes severe spikelet sterility."),
            "paddy": ("warning_jk_paddy", "High-altitude alpine temperatures and short thermal windows in Himachal Pradesh hill zones restrict commercial wetland paddy productivity; cold water causes severe spikelet sterility."),
            "soyabean": ("warning_frost_tropical", "Soybean requires warm soil (>18°C) and consistent growing-degree days; alpine and hill cold stress causes severe floral abortion and pod failure."),
            "soybean": ("warning_frost_tropical", "Soybean requires warm soil (>18°C) and consistent growing-degree days; alpine and hill cold stress causes severe floral abortion and pod failure."),
            "sugarcane": ("warning_frost_tropical", "Hill terrain, freezing winter frost, and thermal deficit halt cane growth and cause frost damage."),
            "cotton": ("warning_frost_tropical", "Low thermal degree-days and frost destroy cotton boll formation."),
            "cotton(lint)": ("warning_frost_tropical", "Low thermal degree-days and frost destroy cotton boll formation."),
            "coconut": ("warning_palm_frost", "Intolerant to cold temperate winters and frost; fatal chilling injury."),
            "banana": ("warning_palm_frost", "Frost and low temperatures destroy tropical banana foliage and stems."),
            "default": ("warning_default_mismatch", "Temperate hill climate and seasonal frost prevent tropical plantation and cash crop maturation.")
        },
        "compatible": ["Apple", "Wheat", "Maize", "Potato", "Barley", "Ginger", "Garlic"]
    },
    # 2. Arid / Desert Region
    "rajasthan": {
        "unviable": {
            "apple", "saffron", "walnut", "coconut", "arecanut",
            "rubber", "tea", "coffee", "black pepper", "cardamom", "jute"
        },
        "reasons": {
            "apple": ("warning_temperate_chill", "Temperate pome fruits require 800–1200 cumulative winter chilling hours below 7°C; arid desert heat completely inhibits floral bud dormancy break."),
            "saffron": ("warning_temperate_chill", "Requires cold temperate mountain climate; arid desert heat and desiccating winds prevent corm growth."),
            "coconut": ("warning_arid_desiccation", "Arid desiccation, extreme summer heat (>45°C), and low relative humidity cause severe moisture stress and crown drying in tropical palms."),
            "arecanut": ("warning_arid_desiccation", "High atmospheric vapor pressure deficit and dry scorching winds cause severe canopy scorching."),
            "jute": ("warning_arid_desiccation", "Requires constant swampy riverine humidity and >1500mm rainfall; completely unviable in arid environments."),
            "default": ("warning_arid_desiccation", "Arid climate, extreme thermal stress, and lack of tropical humidity prevent viable cultivation.")
        },
        "compatible": ["Bajra", "Guar seed", "Moth", "Wheat", "Gram", "Rapeseed &Mustard", "Moong(Green Gram)", "Castor seed"]
    },
    # 3. Peninsular / Tropical South & Central (No High-Chill Temperate Crops)
    "andhra pradesh": {
        "unviable": {"apple", "saffron", "walnut", "almond"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Tropical climate lacks the requisite 800–1200 winter chilling hours (<7°C) essential for bud break; trees cannot set fruit."),
            "saffron": ("warning_temperate_chill", "Alpine mountain crop; cannot survive peninsular tropical heat and humidity."),
            "default": ("warning_temperate_chill", "High-chill temperate crop cannot break dormancy in tropical/subtropical climates.")
        },
        "compatible": ["Rice", "Cotton(lint)", "Groundnut", "Sugarcane", "Maize", "Dry chillies", "Turmeric", "Arhar/Tur", "Gram"]
    },
    "telangana": {
        "unviable": {"apple", "saffron", "walnut", "almond"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Tropical climate lacks the requisite 800–1200 winter chilling hours (<7°C) essential for bud break; trees cannot set fruit."),
            "default": ("warning_temperate_chill", "High-chill temperate crop cannot break dormancy in tropical/subtropical climates.")
        },
        "compatible": ["Cotton(lint)", "Rice", "Maize", "Soyabean", "Arhar/Tur", "Dry chillies", "Turmeric", "Groundnut"]
    },
    "tamil nadu": {
        "unviable": {"apple", "saffron", "walnut", "almond"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Tropical climate lacks the requisite winter chilling hours; trees cannot set floral buds."),
            "default": ("warning_temperate_chill", "High-chill temperate crop cannot break dormancy in tropical/subtropical climates.")
        },
        "compatible": ["Rice", "Banana", "Coconut", "Sugarcane", "Groundnut", "Cotton(lint)", "Maize", "Urad"]
    },
    "karnataka": {
        "unviable": {"apple", "saffron", "walnut", "almond"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Tropical climate lacks the requisite winter chilling hours; trees cannot set floral buds."),
            "default": ("warning_temperate_chill", "High-chill temperate crop cannot break dormancy in tropical/subtropical climates.")
        },
        "compatible": ["Maize", "Sugarcane", "Cotton(lint)", "Rice", "Groundnut", "Gram", "Turmeric", "Sunflower", "Arecanut", "Soyabean"]
    },
    "kerala": {
        "unviable": {"apple", "saffron", "walnut", "almond", "wheat"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Tropical coastal climate lacks requisite chilling hours; completely unviable."),
            "wheat": ("warning_kerala_wheat", "Hyper-humid tropical climate and warm winter temperatures induce severe fungal rust, poor tillering, and sterile grain shriveling."),
            "default": ("warning_default_mismatch", "Hyper-humid tropical climate is incompatible with high-chill or temperate dry-season crops.")
        },
        "compatible": ["Coconut", "Banana", "Rice", "Black pepper", "Cardamom", "Tapioca", "Arecanut", "Rubber"]
    },
    "maharashtra": {
        "unviable": {"apple", "saffron", "walnut", "almond"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Warm winter climate provides zero chilling hours below 7°C, preventing floral bud differentiation."),
            "default": ("warning_temperate_chill", "High-chill temperate crop cannot break dormancy in tropical/subtropical climates.")
        },
        "compatible": ["Cotton(lint)", "Soyabean", "Sugarcane", "Gram", "Arhar/Tur", "Onion", "Wheat", "Jowar", "Bajra"]
    },
    "gujarat": {
        "unviable": {"apple", "saffron", "walnut", "almond"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Hot semi-arid to tropical winter temperatures fail to fulfill dormancy chilling requirements."),
            "default": ("warning_temperate_chill", "High-chill temperate crop cannot break dormancy in tropical/subtropical climates.")
        },
        "compatible": ["Cotton(lint)", "Groundnut", "Castor seed", "Wheat", "Bajra", "Potato", "Onion", "Sesamum"]
    },
    "odisha": {
        "unviable": {"apple", "saffron", "walnut", "almond"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Humid tropical climate lacks winter chilling requirements."),
            "default": ("warning_temperate_chill", "High-chill temperate crop cannot break dormancy in tropical/subtropical climates.")
        },
        "compatible": ["Rice", "Groundnut", "Sugarcane", "Urad", "Moong(Green Gram)", "Turmeric", "Sesamum"]
    },
    # 4. Indo-Gangetic Plains & Central (Tropical Palm & High-Chill Incompatibilities)
    "punjab": {
        "unviable": {"apple", "saffron", "coconut", "arecanut", "cashewnut", "black pepper", "cardamom", "rubber", "tea", "coffee"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Summer temperatures exceed 44°C and winter lacks high-altitude chilling hours, leading to sunburn and poor fruit set."),
            "coconut": ("warning_palm_frost", "Sub-zero winter frost and extreme continental temperature fluctuations damage palm crowns and prevent nut set."),
            "arecanut": ("warning_palm_frost", "Frost and dry continental heat cause fatal vascular tissue breakdown."),
            "default": ("warning_palm_frost", "Continental temperature extremes and frost are incompatible with tropical palms and high-chill temperate crops.")
        },
        "compatible": ["Wheat", "Rice", "Cotton(lint)", "Maize", "Sugarcane", "Potato", "Rapeseed &Mustard", "Gram"]
    },
    "haryana": {
        "unviable": {"apple", "saffron", "coconut", "arecanut", "cashewnut", "black pepper", "cardamom", "rubber"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Scorching summer heat and lack of hill chilling hours make commercial pome fruit unviable."),
            "coconut": ("warning_palm_frost", "Severe winter frost induces fatal chilling injury in tropical palms."),
            "default": ("warning_palm_frost", "Extreme continental climate with frost prevents tropical palm and temperate fruit cultivation.")
        },
        "compatible": ["Wheat", "Rice", "Cotton(lint)", "Rapeseed &Mustard", "Bajra", "Sugarcane", "Gram"]
    },
    "uttar pradesh": {
        "unviable": {"apple", "saffron", "coconut", "arecanut", "cashewnut", "black pepper", "cardamom", "rubber"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Sub-tropical plains heat and lack of winter chilling prevent fruit formation."),
            "coconut": ("warning_palm_frost", "Winter frost and dry winds cause palm crown mortality."),
            "default": ("warning_palm_frost", "Sub-tropical plains climate is incompatible with tropical coastal palms and alpine temperate crops.")
        },
        "compatible": ["Sugarcane", "Wheat", "Rice", "Potato", "Maize", "Rapeseed &Mustard", "Gram", "Arhar/Tur"]
    },
    "bihar": {
        "unviable": {"apple", "saffron", "coconut", "arecanut", "cashewnut", "black pepper", "cardamom"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Plains climate lacks requisite winter chilling hours."),
            "coconut": ("warning_palm_frost", "Winter continental cold inhibits flowering and nut development."),
            "default": ("warning_palm_frost", "Plains climate is incompatible with tropical palms and alpine fruits.")
        },
        "compatible": ["Rice", "Wheat", "Maize", "Sugarcane", "Potato", "Gram", "Jute"]
    },
    "west bengal": {
        "unviable": {"apple", "saffron", "walnut", "almond"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Warm humid plains lack winter chilling hours essential for fruit tree dormancy break."),
            "default": ("warning_temperate_chill", "High-chill temperate crops cannot break dormancy in tropical/humid subtropical plains.")
        },
        "compatible": ["Rice", "Jute", "Potato", "Maize", "Rapeseed &Mustard"]
    },
    "madhya pradesh": {
        "unviable": {"apple", "saffron", "coconut", "arecanut", "cashewnut", "black pepper"},
        "reasons": {
            "apple": ("warning_temperate_chill", "Continental plateau heat and warm winters prevent bud dormancy break."),
            "coconut": ("warning_palm_frost", "Inadequate atmospheric humidity and cold winter nights cause severe moisture and thermal stress."),
            "default": ("warning_palm_frost", "Central continental plateau climate cannot support high-chill temperate or coastal tropical crops.")
        },
        "compatible": ["Soyabean", "Wheat", "Gram", "Cotton(lint)", "Maize", "Arhar/Tur", "Rapeseed &Mustard", "Garlic"]
    }
}

# ==============================================================================
# COMPREHENSIVE SEASON-CROP AGRONOMIC MATRIX (COVERING ALL CROPS)
# ==============================================================================

SEASON_CROP_AFFINITY_MATRIX = {
    # 1. KHARIF-DOMINANT CROPS
    "rice": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Optimal monsoon moisture and solar radiation during reproductive stage."},
        "rabi": {"factor": 0.88, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Sub-optimal cool temperatures slow seedling development; requires continuous irrigation."},
        "summer": {"factor": 0.55, "is_viable": True, "status": "Sub-Optimal", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Sub-Optimal Season / Thermal Stress", "desc": "High atmospheric evaporative demand and summer heat waves induce spikelet sterility without misting."},
        "whole year": {"factor": 0.95, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Year-round wetland cultivation where water supply is perennial."}
    },
    "cotton(lint)": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Warm growing season with long frost-free boll development."},
        "rabi": {"factor": 0.70, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Moderate Feasibility", "desc": "Lower nighttime temperatures slow boll opening and fiber lint elongation."},
        "summer": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_cotton_summer", "warning_message": "Severe Summer Heat Stress: Extreme atmospheric vapor pressure deficit causes square shedding and sterile boll abortion."},
        "whole year": {"factor": 0.80, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Moderate Feasibility", "desc": "Extended cotton cropping cycle subject to late-season pink bollworm pressure."}
    },
    "soyabean": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Warm soil (>20°C) and monsoon photoperiod favor optimal nodulation and vegetative canopy."},
        "rabi": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Short winter daylengths trigger early flowering with reduced branching."},
        "summer": {"factor": 0.50, "is_viable": True, "status": "Sub-Optimal", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Sub-Optimal Season / Thermal Stress", "desc": "Severe terminal heat stress and pod shattering during harvest."},
        "whole year": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Requires rotation management to prevent soil nutrient depletion."}
    },
    "groundnut": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Rainfed monsoon season provides high pegging soil friability."},
        "rabi": {"factor": 0.90, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Irrigated rabi groundnut achieves high pod density in peninsular India."},
        "summer": {"factor": 0.60, "is_viable": True, "status": "Sub-Optimal", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Sub-Optimal Season / Thermal Stress", "desc": "Intense heat and moisture stress harden soil surface, impairing peg penetration."},
        "whole year": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Multi-season rotation requiring soil calcium replenishment."}
    },
    "bajra": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "C4 photosynthetic efficiency in warm monsoon heat and light rain."},
        "rabi": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Cool winter nights slow vegetative elongation."},
        "summer": {"factor": 0.55, "is_viable": True, "status": "Sub-Optimal", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Sub-Optimal Season / Thermal Stress", "desc": "High atmospheric temperatures (>40°C) during anthesis desiccate pollen."},
        "whole year": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Year-round fodder and grain cultivation."}
    },
    "maize": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "High vegetative biomass accumulation in warm monsoon weather."},
        "rabi": {"factor": 0.90, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "High solar radiation and disease-free winter atmosphere produce dense cobs with irrigation."},
        "summer": {"factor": 0.55, "is_viable": True, "status": "Sub-Optimal", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Sub-Optimal Season / Thermal Stress", "desc": "Extreme summer heat causes pollen desiccation and poor kernel filling on cobs."},
        "whole year": {"factor": 0.90, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Well-suited for three-season crop rotation."}
    },
    "turmeric": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Requires 8-9 months of warm humid monsoon weather for rhizome development."},
        "rabi": {"factor": 0.40, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_seasonal_mismatch", "warning_message": "Late winter planting prevents adequate vegetative canopy development before summer dormancy, resulting in poor rhizome yield."},
        "summer": {"factor": 0.40, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_seasonal_mismatch", "warning_message": "High summer ground temperatures scorch emerging rhizome sprouts without heavy organic mulch."},
        "whole year": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Standard 9-month cultivation cycle spanning monsoon through winter."}
    },
    "arhar/tur": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Deep taproot development during monsoon establishes drought-tolerant podding."},
        "rabi": {"factor": 0.80, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Post-rainy rabi tur develops shorter plants with fewer pod-bearing branches."},
        "summer": {"factor": 0.45, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_seasonal_mismatch", "warning_message": "Severe summer aridity and heat abort flowers, resulting in near-zero pod setting."},
        "whole year": {"factor": 0.95, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Long-duration perennial and semi-perennial pigeonpea varieties."}
    },
    "jowar": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Monsoon sorghum grain and forage production."},
        "rabi": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Rabi sorghum under residual soil moisture in deep black soils."},
        "summer": {"factor": 0.55, "is_viable": True, "status": "Sub-Optimal", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Sub-Optimal Season / Thermal Stress", "desc": "Hot dry winds during grain filling reduce 1000-grain test weight."},
        "whole year": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Continuous multi-cut fodder and grain cropping."}
    },
    "jute": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "High monsoon humidity and flooding promote rapid bast fiber elongation."},
        "rabi": {"factor": 0.10, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_seasonal_mismatch", "warning_message": "Cold winter temperatures (<15°C) inhibit seed germination and stunt vegetative bast fiber elongation."},
        "summer": {"factor": 0.60, "is_viable": True, "status": "Sub-Optimal", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Sub-Optimal Season / Thermal Stress", "desc": "Pre-monsoon sowing with irrigation in eastern deltaic soils."},
        "whole year": {"factor": 0.70, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Restricted to subtropical riverine wetlands."}
    },

    # 2. RABI-STRICT CROPS
    "wheat": {
        "rabi": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Cool winter temperatures (12–25°C) ensure extensive tillering and optimal grain filling."},
        "kharif": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_wheat_kharif", "warning_message": "High Temperature & Waterlogging Risk: High heat during germination prevents tillering, causing crop failure."},
        "summer": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_wheat_summer", "warning_message": "Terminal Heat Stress: Scorching summer temperatures abort flowering and grain filling."},
        "whole year": {"factor": 0.05, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_wheat_summer", "warning_message": "Wheat cannot be cultivated year-round due to strict thermo-photoperiod and vernalization requirements."}
    },
    "barley": {
        "rabi": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Cool growing conditions optimize spikelet differentiation and malting grain quality."},
        "kharif": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_wheat_kharif", "warning_message": "High Temperature & Waterlogging Risk: Monsoon rains and heat cause seed rot and failure of vernalization."},
        "summer": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_wheat_summer", "warning_message": "Terminal Heat Stress: Scorching summer temperatures abort head development and force premature crop senescence."},
        "whole year": {"factor": 0.05, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_wheat_summer", "warning_message": "Barley cannot be cultivated year-round due to vernalization requirements."}
    },
    "gram": {
        "rabi": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Cool, dry winter weather promotes prolific nodulation, branching, and pod setting."},
        "kharif": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_gram_kharif", "warning_message": "Waterlogging & Root Rot Risk: Saturated monsoon soils trigger lethal collar rot and wilt in chickpea."},
        "summer": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_gram_summer", "warning_message": "Terminal Heat Stress: Intense summer heat aborts flowering and desiccates pollen, resulting in zero pod set."},
        "whole year": {"factor": 0.05, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_gram_summer", "warning_message": "Chickpea cannot be grown year-round due to root intolerance to humidity and heat."}
    },
    "rapeseed &mustard": {
        "rabi": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Clear sunny winter days and cool nights maximize seed oil synthesis."},
        "kharif": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_seasonal_mismatch", "warning_message": "Monsoon humidity and high temperatures trigger fatal white rust, damping-off, and stem rot in mustard."},
        "summer": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_seasonal_mismatch", "warning_message": "Desiccating summer heat aborts siliqua filling and severely reduces seed oil content."},
        "whole year": {"factor": 0.05, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_seasonal_mismatch", "warning_message": "Mustard requires cool winter growing season and cannot grow year-round."}
    },
    "potato": {
        "rabi": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Night temperatures of 15–20°C stimulate rapid stolon swelling and tuberization."},
        "kharif": {"factor": 0.15, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_seasonal_mismatch", "warning_message": "High night temperatures (>25°C) and monsoon dampness halt tuberization and trigger devastating late blight."},
        "summer": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_potato_summer", "warning_message": "Extreme Heat & Stolon Decay: Soil temperatures above 30°C rot seed tubers and arrest stolon development."},
        "whole year": {"factor": 0.20, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_potato_summer", "warning_message": "Potato requires cold winter nights for tuberization; year-round plains cultivation fails."}
    },

    # 3. ZAID / SUMMER SPECIALTY CROPS & FLEXIBLE ANNUALS
    "onion": {
        "rabi": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Rabi onion produces high-density, pungent bulbs with optimal storage life."},
        "kharif": {"factor": 0.80, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Kharif onion develops higher moisture, smaller bulb size, and susceptibility to purple blotch."},
        "summer": {"factor": 0.65, "is_viable": True, "status": "Sub-Optimal", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Sub-Optimal Season / Thermal Stress", "desc": "Early summer heat induces premature bolting and sunburned outer scales."},
        "whole year": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Staggered sequential plantings across three overlapping seasons."}
    },
    "sunflower": {
        "rabi": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Cool winter days and clear sunshine optimize capitulum diameter and seed oil content."},
        "kharif": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Monsoon rains during flowering impede honeybee pollination and induce head rot."},
        "summer": {"factor": 0.75, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Moderate Feasibility", "desc": "Requires timely irrigation; high solar radiation yields plump seeds if moisture is maintained."},
        "whole year": {"factor": 0.90, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Photo-insensitive day-neutral crop suitable for flexible year-round planting."}
    },
    "dry chillies": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Warm humid climate supports vigorous vegetative branching and continuous fruit flush."},
        "rabi": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Cool winter weather slows ripening and drying cycles."},
        "summer": {"factor": 0.55, "is_viable": True, "status": "Sub-Optimal", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Sub-Optimal Season / Thermal Stress", "desc": "High daytime heat (>38°C) triggers extensive flower and young fruit drop."},
        "whole year": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Multi-flush perennial or extended commercial crop."}
    },
    "moong(green gram)": {
        "summer": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Short duration (60-65 days) under warm summer sunshine with irrigation."},
        "kharif": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Continuous monsoon rains cause pod rot and yellow mosaic virus pressure."},
        "rabi": {"factor": 0.75, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Winter cold slows vegetative growth in northern zones."},
        "whole year": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Catch crop across multi-season rotations."}
    },
    "urad": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Warm humid monsoon weather supports rapid canopy spread."},
        "rabi": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Post-rice fallow rabi urad under residual moisture."},
        "summer": {"factor": 0.70, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Short-duration summer urad under assured irrigation."},
        "whole year": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Flexible rotation crop."}
    },

    # 4. PERENNIAL & ANNUAL CASH CROPS
    "sugarcane": {
        "whole year": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "10-14 month perennial crop achieving peak biomass and sucrose accumulation."},
        "kharif": {"factor": 0.95, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Monsoon planting (Adsali) produces massive vegetative tonnage."},
        "rabi": {"factor": 0.90, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Spring planting produces healthy tillers as temperatures warm up."},
        "summer": {"factor": 0.75, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Moderate Feasibility", "warning_key": "warning_seasonal_mismatch", "warning_message": "Late summer planting shortens effective vegetative elongation before winter crushing, lowering millable cane weight."}
    },
    "coconut": {
        "whole year": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Perennial tropical palm bearing continuous monthly nut spadices."},
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Monsoon replenishment boosts crown vigor and water nut yield."},
        "rabi": {"factor": 0.95, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Steady winter nut development in tropical latitudes."},
        "summer": {"factor": 0.90, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Requires regular basin irrigation to prevent summer button shedding."}
    },
    "arecanut": {
        "whole year": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Perennial tropical palm with continuous inflorescence emergence."},
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Humid monsoon conditions optimize nut expansion."},
        "rabi": {"factor": 0.95, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Optimal nut maturation and harvest."},
        "summer": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Moderate Feasibility", "desc": "Requires summer irrigation and mulch to avoid crown scorching."}
    },
    "black pepper": {
        "whole year": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Perennial rainforest vine with year-round canopy development."},
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Monsoon humidity stimulates heavy spike emergence and pollination."},
        "rabi": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Winter berry ripening and harvest phase."},
        "summer": {"factor": 0.60, "is_viable": True, "status": "Sub-Optimal", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Sub-Optimal Season / Thermal Stress", "desc": "High atmospheric aridity causes spike shedding without overhead shade."}
    },
    "apple": {
        "whole year": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Perennial alpine fruit tree cycling through winter chilling, spring bloom, and autumn harvest."},
        "rabi": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Winter chilling period fulfills critical dormancy break requirements."},
        "kharif": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_apple_season", "warning_message": "Unviable Sowing Window: Apple requires winter chilling and dormancy; kharif or summer sowing is biologically unviable."},
        "summer": {"factor": 0.00, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_apple_season", "warning_message": "Thermal Desiccation: Summer heat without prior winter chilling induces fatal vegetative desiccation."}
    },
    "tobacco": {
        "rabi": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Cool dry winter weather ensures broad, elastic leaves with high nicotine quality."},
        "kharif": {"factor": 0.70, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Moderate Feasibility", "desc": "Excessive rainfall during curing damages leaf grade."},
        "summer": {"factor": 0.45, "is_viable": False, "status": "Incompatible", "risk": "High Risk / Seasonal Incompatibility", "suitability": "Seasonally Incompatible", "warning_key": "warning_seasonal_mismatch", "warning_message": "Scorching summer heat causes premature curing, brittleness, and severe leaf necrosis."},
        "whole year": {"factor": 0.80, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Moderate Feasibility", "desc": "Requires careful scheduling around seasonal curing rains."}
    },
    "castor seed": {
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Monsoon sowing establishes deep taproot and heavy primary spike."},
        "rabi": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Secondary and tertiary spike maturation in winter."},
        "summer": {"factor": 0.55, "is_viable": True, "status": "Sub-Optimal", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Sub-Optimal Season / Thermal Stress", "desc": "High summer temperatures reduce capsule size."},
        "whole year": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Extended harvest across multiple pickings."}
    },
    "banana": {
        "whole year": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "11-13 month perennial giant herb with continuous shooting."},
        "kharif": {"factor": 1.00, "is_viable": True, "status": "Optimal", "risk": "Low Risk / Optimal Season", "suitability": "Optimal Season", "desc": "Monsoon moisture maximizes pseudostem girth."},
        "rabi": {"factor": 0.85, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk", "suitability": "Moderate Feasibility", "desc": "Cool winter temperatures extend bunch development period."},
        "summer": {"factor": 0.75, "is_viable": True, "status": "Moderate", "risk": "Moderate Risk / Seasonal Stress", "suitability": "Moderate Feasibility", "desc": "Requires frequent irrigation to prevent leaf scorch."}
    }
}

def evaluate_agro_climatic_feasibility(crop_raw: str, state_raw: str) -> Dict[str, Any]:
    st = state_raw.lower().strip()
    c_raw = crop_raw.lower().strip()
    if "rice" in c_raw or "paddy" in c_raw:
        c_key = "rice"
    elif "soya" in c_raw or "soybean" in c_raw:
        c_key = "soyabean"
    elif "cotton" in c_raw:
        c_key = "cotton"
    elif "sugarcane" in c_raw:
        c_key = "sugarcane"
    elif "coconut" in c_raw:
        c_key = "coconut"
    elif "apple" in c_raw:
        c_key = "apple"
    elif "banana" in c_raw:
        c_key = "banana"
    elif "wheat" in c_raw:
        c_key = "wheat"
    elif "arecanut" in c_raw:
        c_key = "arecanut"
    elif "cashew" in c_raw:
        c_key = "cashewnut"
    elif "jute" in c_raw:
        c_key = "jute"
    elif "pepper" in c_raw:
        c_key = "black pepper"
    elif "cardamom" in c_raw:
        c_key = "cardamom"
    elif "saffron" in c_raw:
        c_key = "saffron"
    elif "rubber" in c_raw:
        c_key = "rubber"
    elif "tapioca" in c_raw:
        c_key = "tapioca"
    elif "groundnut" in c_raw:
        c_key = "groundnut"
    else:
        c_key = c_raw
    state_rules = AGRO_CLIMATIC_MATRIX.get(st)
    if state_rules:
        unviable_set = state_rules.get("unviable", set())
        if c_key in unviable_set or c_raw in unviable_set:
            reasons = state_rules.get("reasons", {})
            reason_tuple = reasons.get(c_key, reasons.get("default", ("warning_default_mismatch", "Agro-climatic mismatch for this region.")))
            w_key, w_msg = reason_tuple
            return {
                "is_viable": False,
                "risk_level": "High Risk / Climate Mismatch",
                "climate_suitability": "Unviable",
                "warning_key": w_key,
                "warning_message": w_msg,
                "compatible_crops": state_rules.get("compatible", [])
            }
    compat = state_rules.get("compatible", []) if state_rules else []
    return {
        "is_viable": True,
        "risk_level": "Low Risk / Optimal Climate",
        "climate_suitability": "Optimal Climate",
        "warning_key": None,
        "warning_message": None,
        "compatible_crops": compat
    }

def evaluate_seasonal_feasibility(crop_raw: str, season_raw: str) -> Dict[str, Any]:
    crop_c = canonicalize_yield_crop(crop_raw).lower().strip()
    s_raw = str(season_raw or "Kharif").lower().strip()
    if "rabi" in s_raw or "winter" in s_raw:
        season_key = "rabi"
    elif "summer" in s_raw or "zaid" in s_raw:
        season_key = "summer"
    elif "whole" in s_raw or "year" in s_raw:
        season_key = "whole year"
    else:
        season_key = "kharif"

    rules = SEASON_CROP_AFFINITY_MATRIX.get(crop_c, None)
    if not rules:
        for k in SEASON_CROP_AFFINITY_MATRIX:
            if k in crop_c or crop_c in k:
                rules = SEASON_CROP_AFFINITY_MATRIX[k]
                break

    if rules and season_key in rules:
        entry = rules[season_key]
        return {
            "is_viable": entry.get("is_viable", True),
            "factor": entry.get("factor", 1.0),
            "season_status": entry.get("status", "Optimal"),
            "risk_level": entry.get("risk", "Low Risk / Optimal Season"),
            "climate_suitability": entry.get("suitability", "Optimal Season"),
            "warning_key": entry.get("warning_key"),
            "warning_message": entry.get("warning_message"),
            "reason": entry.get("desc", entry.get("warning_message", "Seasonal agronomic factor applied."))
        }

    # Agronomic fallback for crops not explicitly mapped
    if season_key == "kharif":
        return {"is_viable": True, "factor": 1.0, "season_status": "Optimal", "risk_level": "Low Risk / Optimal Season", "climate_suitability": "Optimal Season", "warning_key": None, "warning_message": None, "reason": "Standard monsoon cultivation."}
    elif season_key == "rabi":
        return {"is_viable": True, "factor": 0.85, "season_status": "Moderate", "risk_level": "Moderate Risk", "climate_suitability": "Moderate Feasibility", "warning_key": None, "warning_message": None, "reason": "Irrigated winter cultivation."}
    elif season_key == "summer":
        return {"is_viable": True, "factor": 0.60, "season_status": "Sub-Optimal", "risk_level": "Moderate Risk / Seasonal Stress", "climate_suitability": "Sub-Optimal Season / Thermal Stress", "warning_key": None, "warning_message": None, "reason": "High temperature and evaporative demand."}
    else:
        return {"is_viable": True, "factor": 0.90, "season_status": "Optimal", "risk_level": "Low Risk / Optimal Season", "climate_suitability": "Optimal Season", "warning_key": None, "warning_message": None, "reason": "Year-round cultivation."}

def get_compatible_crops_for_state(state: str) -> List[str]:
    st = state.lower().strip()
    if st in AGRO_CLIMATIC_MATRIX:
        return AGRO_CLIMATIC_MATRIX[st].get("compatible", [])
    return ["Rice", "Wheat", "Maize", "Cotton(lint)", "Sugarcane", "Groundnut", "Gram"]

def canonicalize_yield_crop(crop_name: str) -> str:
    if not crop_name:
        return "Rice"
    raw = str(crop_name).strip().lower()
    if "paddy" in raw or "rice" in raw:
        return "Rice"
    if "apple" in raw:
        return "Apple"
    if "barley" in raw:
        return "Barley"
    if "wheat" in raw:
        return "Wheat"
    if "maize" in raw or "corn" in raw:
        return "Maize"
    if "cotton" in raw:
        return "Cotton(lint)"
    if "sugarcane" in raw or "cane" in raw:
        return "Sugarcane"
    if "groundnut" in raw or "peanut" in raw:
        return "Groundnut"
    if "soya" in raw or "soybean" in raw:
        return "Soyabean"
    if "gram" in raw or "chickpea" in raw:
        if "arhar" in raw or "tur" in raw or "pigeon" in raw or "red" in raw:
            return "Arhar/Tur"
        return "Gram"
    if "arhar" in raw or "tur" in raw or "pigeon" in raw:
        return "Arhar/Tur"
    if "potato" in raw:
        return "Potato"
    if "onion" in raw:
        return "Onion"
    if "chilli" in raw or "chillies" in raw:
        return "Dry chillies"
    if "turmeric" in raw:
        return "Turmeric"
    if "sunflower" in raw:
        return "Sunflower"
    if "bajra" in raw or "pearl millet" in raw:
        return "Bajra"
    if "coconut" in raw:
        return "Coconut"
    if "jute" in raw:
        return "Jute"
    if "tobacco" in raw:
        return "Tobacco"
    _, cat_info = normalize_crop_name(crop_name)
    if cat_info and cat_info.get("yield_dataset_name"):
        return cat_info["yield_dataset_name"]
    return crop_name.strip()

def compute_agronomic_scaling(state: str, area_acres: float, user_rf: float, user_fert_per_acre: float, user_pest_per_acre: float) -> float:
    baseline = get_state_agri_baseline(state)
    base_rf = float(baseline.get("rainfall", 1000))
    base_fert_per_acre = float(baseline.get("fertilizer_per_ha", 120)) / 2.47105
    base_pest_per_acre = float(baseline.get("pesticide_per_ha", 0.30)) / 2.47105
    scaling = 1.0
    if user_rf > 0:
        rf_ratio = user_rf / base_rf
        if rf_ratio < 0.5:
            rf_factor = 0.75 + (rf_ratio / 0.5) * 0.15
        elif rf_ratio <= 1.2:
            rf_factor = 0.90 + ((rf_ratio - 0.5) / 0.7) * 0.18
        else:
            rf_factor = max(0.85, 1.08 - (rf_ratio - 1.2) * 0.15)
        scaling *= rf_factor
    if user_fert_per_acre > 0:
        fert_ratio = user_fert_per_acre / base_fert_per_acre
        if fert_ratio < 1.0:
            fert_factor = 0.80 + (fert_ratio * 0.20)
        else:
            fert_factor = min(1.15, 1.00 + (fert_ratio - 1.0) * 0.15)
        scaling *= fert_factor
    if user_pest_per_acre > 0:
        pest_ratio = user_pest_per_acre / base_pest_per_acre
        if pest_ratio < 1.0:
            pest_factor = 0.88 + (pest_ratio * 0.12)
        else:
            pest_factor = min(1.08, 1.00 + (pest_ratio - 1.0) * 0.08)
        scaling *= pest_factor
    return max(0.50, min(1.35, scaling))

def predict_yield(input_data: Dict[str, Any]) -> float:
    details = predict_yield_detailed(input_data)
    return details["predicted_yield_tonnes_ha"]

def predict_yield_detailed(input_data: Dict[str, Any]) -> Dict[str, Any]:
    model = load_yield_model()
    crop_raw = str(input_data.get("Crop", "Rice")).strip()
    season = str(input_data.get("Season", "Kharif")).strip()
    state = str(input_data.get("State", "Andhra Pradesh")).strip()
    crop_dataset_name = canonicalize_yield_crop(crop_raw)
    raw_year = input_data.get("Crop_Year") if input_data.get("Crop_Year") is not None else input_data.get("crop_year", 2020)
    try:
        crop_year = int(raw_year) if raw_year is not None and str(raw_year).strip() != "" else 2020
    except (ValueError, TypeError):
        crop_year = 2020
    area_unit = str(input_data.get("area_unit", "acres")).lower()
    try:
        area_raw = float(input_data.get("Area", 1.0))
        if area_raw <= 0:
            area_raw = 1.0
    except (ValueError, TypeError):
        area_raw = 1.0
    if area_unit in ("hectares", "ha"):
        area_ha = area_raw
        area_acres = area_ha / 0.404686
    else:
        area_acres = area_raw
        area_ha = area_acres * 0.404686

    baseline = get_state_agri_baseline(state)
    user_rf = float(input_data.get("Annual_Rainfall", 0) or 0)
    rainfall = user_rf if user_rf > 0 else float(baseline["rainfall"])
    user_fert = float(input_data.get("Fertilizer", 0) or 0)
    fertilizer = round(user_fert * area_acres, 2) if user_fert > 0 else round(baseline["fertilizer_per_ha"] * area_ha, 2)
    user_pest = float(input_data.get("Pesticide", 0) or 0)
    pesticide = round(user_pest * area_acres, 2) if user_pest > 0 else round(baseline["pesticide_per_ha"] * area_ha, 2)

    # 1. Agro-Climatic State Feasibility Gating
    feasibility = evaluate_agro_climatic_feasibility(crop_raw, state)
    if not feasibility["is_viable"]:
        pass
    else:
        feasibility = evaluate_agro_climatic_feasibility(crop_dataset_name, state)

    # 2. Season-Crop Agronomic Affinity Gating
    seasonal = evaluate_seasonal_feasibility(crop_dataset_name, season)

    season_mismatch = not seasonal["is_viable"]
    season_status = seasonal["season_status"]
    season_factor = seasonal["factor"]
    season_warning = seasonal.get("reason") or seasonal.get("warning_message")

    if not feasibility["is_viable"]:
        is_viable = False
        risk_level = feasibility["risk_level"]
        climate_suitability = feasibility["climate_suitability"]
        warning_key = feasibility["warning_key"]
        warning_message = feasibility["warning_message"]
    elif not seasonal["is_viable"]:
        is_viable = False
        risk_level = seasonal["risk_level"]
        climate_suitability = seasonal["climate_suitability"]
        warning_key = seasonal["warning_key"]
        warning_message = seasonal["warning_message"]
    else:
        is_viable = True
        if seasonal["factor"] < 0.75:
            risk_level = seasonal["risk_level"]
            climate_suitability = seasonal["climate_suitability"]
        else:
            risk_level = feasibility["risk_level"]
            climate_suitability = seasonal["climate_suitability"] if seasonal["factor"] < 1.0 else feasibility["climate_suitability"]
        warning_key = None
        warning_message = None

    is_coconut = "coconut" in crop_dataset_name.lower()
    yield_unit = "nuts/ha" if is_coconut else "tonnes/ha"
    acre_unit = "nuts/acre" if is_coconut else "quintals/acre"

    if not is_viable:
        yield_tonnes_ha = 0.00
        yield_per_acre = 0.00
        estimated_production = 0.00
        production_unit = "thousand nuts" if is_coconut else "tonnes"
        if not feasibility["is_viable"]:
            suggestions = [
                f"Strict Agro-Climatic Gating: {crop_raw} cannot be commercially cultivated in {state} due to fundamental bio-climatic incompatibility.",
                f"Agronomic Barrier: {warning_message}",
                f"Recommended Viable Alternatives: Shift to ICAR-adapted crops for {state} such as {', '.join(feasibility.get('compatible_crops', [])[:5])}.",
                "Capital Preservation Advisory: Do not invest capital or purchase chemical fertilizers/seeds for unviable crop-climate pairings as harvest output is zero."
            ]
        else:
            suggestions = [
                f"Strict Seasonal Incompatibility: {crop_dataset_name} cannot be commercially cultivated during the {season} season.",
                f"Seasonal Agronomic Barrier: {warning_message}",
                f"Recommended Agronomic Window: Shift cultivation of {crop_dataset_name} to its optimal season.",
                "Harvest Loss Mitigation: Do not invest in seed and chemical inputs for this season as extreme temperature, waterlogging, or photoperiod mismatch will cause complete crop failure."
            ]
    else:
        # Standardize season for ML model categorical encoding
        s_lower = season.lower().strip()
        if "rabi" in s_lower or "winter" in s_lower:
            ml_season = "Rabi"
        elif "summer" in s_lower or "zaid" in s_lower:
            ml_season = "Summer"
        elif "whole" in s_lower or "year" in s_lower:
            ml_season = "Whole Year"
        else:
            ml_season = "Kharif"

        inference_df = pd.DataFrame([{
            "Crop": crop_dataset_name,
            "Season": ml_season,
            "State": state,
            "Crop_Year": crop_year,
            "Area": area_ha,
            "Annual_Rainfall": rainfall,
            "Fertilizer": fertilizer,
            "Pesticide": pesticide
        }])
        raw_pred = model.predict(inference_df)
        pred_val = float(max(0.01, raw_pred[0]))
        if crop_dataset_name.lower() == "apple":
            st_lower = state.lower().strip()
            if "jammu" in st_lower or "kashmir" in st_lower:
                pred_val = round(max(pred_val, 9.85), 2)
            elif "himachal" in st_lower:
                pred_val = round(max(pred_val, 7.50), 2)
            elif "uttarakhand" in st_lower:
                pred_val = round(max(pred_val, 6.20), 2)
        scaling_factor = compute_agronomic_scaling(state, area_acres, user_rf, user_fert, user_pest)
        # Apply agronomic input scaling and seasonal affinity factor
        pred_val = round(pred_val * scaling_factor * season_factor, 2)
        if is_coconut:
            yield_tonnes_ha = pred_val
            yield_per_acre = round(yield_tonnes_ha * 0.404686, 1)
            estimated_production = round((yield_tonnes_ha * area_ha) / 1000.0, 1)
            production_unit = "thousand nuts"
        else:
            yield_tonnes_ha = round(pred_val, 2)
            yield_per_acre = round(yield_tonnes_ha * 4.04686, 2)
            estimated_production = round(yield_tonnes_ha * area_ha, 2)
            production_unit = "tonnes"

        suggestions = [
            f"Split Nitrogen Application: For {crop_dataset_name}, apply 50% nitrogen as basal dose, 25% at active tillering, and 25% at panicle initiation/flowering.",
            f"Critical Irrigation Timing: Avoid moisture stress during anthesis and grain/pod-filling; maintain field-capacity moisture for optimal test weight.",
            f"Micronutrient Foliar Spray: Spray 0.5% Zinc Sulphate + 1% Urea at 30 and 45 days after sowing to prevent hidden micronutrient hunger.",
            f"Integrated Pest Scouting: Inspect weekly for early borer/blight symptoms; deploy pheromone traps (5/acre) before applying targeted biocontrol.",
            f"Harvest Index Management: Drain field water 10-12 days before harvest; harvest when 80-85% of ears/pods turn straw golden to minimize grain shattering."
        ]

    return {
        "crop": crop_dataset_name,
        "state": state,
        "season": season,
        "crop_year": crop_year,
        "Crop_Year": crop_year,
        "area_acres": round(area_acres, 2),
        "area_ha": round(area_ha, 2),
        "predicted_yield": yield_tonnes_ha,
        "predicted_yield_tonnes_ha": yield_tonnes_ha,
        "predicted_yield_per_acre": yield_per_acre,
        "yield_unit": yield_unit,
        "acre_unit": acre_unit,
        "estimated_production": estimated_production,
        "production_unit": production_unit,
        "risk_level": risk_level,
        "climate_suitability": climate_suitability,
        "is_viable": is_viable,
        "season_mismatch": season_mismatch,
        "season_status": season_status,
        "season_factor": season_factor,
        "season_warning": season_warning,
        "warning_key": warning_key,
        "warning_message": warning_message,
        "actionable_suggestions": suggestions,
        "annual_rainfall_used": rainfall,
        "fertilizer_used": fertilizer,
        "pesticide_used": pesticide,
        "methodology": "Pre-harvest Random Forest Regression (DES Agricultural Statistics, ICAR Agro-Climatic Gating & Seasonal Affinity Model)",
        "limitations": "Estimates assume normal seasonal weather without severe unseasonal floods, extreme hailstorms, or major pest outbreaks."
    }


# ==============================================================================
# IN-MEMORY MODEL PRE-WARMING (Eliminates Disk I/O Latency)
# ==============================================================================
try:
    load_yield_model()
except Exception:
    pass
