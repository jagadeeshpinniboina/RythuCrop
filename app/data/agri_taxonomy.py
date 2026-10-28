"""
RythuCrop Agricultural Taxonomy and Crop Registry
Provides unified normalization, agronomic traits, and capability mappings across
catalogue, recommendation model, yield dataset, and mandi price systems.
"""

# Categorical taxonomy grouping
CROP_CATEGORIES = [
    "Cereals and Millets",
    "Pulses",
    "Oilseeds",
    "Commercial and Fibre Crops",
    "Vegetables",
    "Fruits",
    "Flowers",
    "Spices and Plantation Crops"
]

# Canonical crop definitions
CROP_CATALOGUE = {
    # Cereals and Millets
    "rice": {
        "id": "rice",
        "name": "Rice (Paddy)",
        "category": "Cereals and Millets",
        "yield_dataset_name": "Rice",
        "recommendation_class": "rice",
        "seasons": ["Kharif", "Rabi", "Summer"],
        "soils": ["Clay Soil", "Loamy", "Alluvial"],
        "water_req": "Good water availability",
        "duration_days": "110–145 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [2.0, 5.5],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 2200,
        "advisory_tips": {
            "irrigation": "Maintain 2-5 cm standing water during tillering and panicle initiation. Drain before harvest.",
            "nutrients": "Apply balanced N:P:K (100:50:50 kg/ha). Apply zinc sulphate in deficient soils.",
            "pest": "Monitor for yellow stem borer and leaf folder. Use Trichogramma cards and avoid excess urea."
        }
    },
    "wheat": {
        "id": "wheat",
        "name": "Wheat",
        "category": "Cereals and Millets",
        "yield_dataset_name": "Wheat",
        "recommendation_class": "wheat",
        "seasons": ["Rabi", "Winter"],
        "soils": ["Loamy", "Clay Soil", "Black Soil"],
        "water_req": "Moderate water availability",
        "duration_days": "115–135 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [2.2, 5.0],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 2275,
        "advisory_tips": {
            "irrigation": "First irrigation at Crown Root Initiation (20-25 DAS) is critical. 4-5 irrigations in total.",
            "nutrients": "Standard NPK 120:60:40 kg/ha. Apply half N and full P, K at sowing.",
            "pest": "Watch for yellow rust in northern plains and aphid buildup during grain filling."
        }
    },
    "maize": {
        "id": "maize",
        "name": "Maize",
        "category": "Cereals and Millets",
        "yield_dataset_name": "Maize",
        "recommendation_class": "maize",
        "seasons": ["Kharif", "Rabi", "Summer"],
        "soils": ["Black Soil", "Red Soil", "Loamy"],
        "water_req": "Moderate water availability",
        "duration_days": "85–110 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [2.0, 6.0],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 2090,
        "advisory_tips": {
            "irrigation": "Critical stages are tasseling and silking. Avoid waterlogging at seedling stage.",
            "nutrients": "NPK 120:60:40 kg/ha with micronutrient zinc sulphate at 25 kg/ha.",
            "pest": "Scout for Fall Armyworm (FAW); use pheromone traps and neem sprays early."
        }
    },
    "bajra": {
        "id": "bajra",
        "name": "Bajra (Pearl Millet)",
        "category": "Cereals and Millets",
        "yield_dataset_name": "Bajra",
        "recommendation_class": None,
        "seasons": ["Kharif", "Summer"],
        "soils": ["Sandy Soil", "Red Soil", "Loamy"],
        "water_req": "Low water availability",
        "duration_days": "75–90 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [1.0, 2.5],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 2500,
        "advisory_tips": {
            "irrigation": "Highly drought tolerant. Needs 1-2 supplemental irrigations if dry spell exceeds 20 days.",
            "nutrients": "NPK 60:30:20 kg/ha. Excellent choice for rainfed arid and semi-arid tracts.",
            "pest": "Watch for downy mildew and ergot. Use certified seed treated with metalaxyl."
        }
    },
    "jowar": {
        "id": "jowar",
        "name": "Jowar (Sorghum)",
        "category": "Cereals and Millets",
        "yield_dataset_name": "Jowar",
        "recommendation_class": "sorghum",
        "seasons": ["Kharif", "Rabi"],
        "soils": ["Black Soil", "Loamy", "Clay Soil"],
        "water_req": "Low water availability",
        "duration_days": "100–120 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [1.0, 3.0],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 3180,
        "advisory_tips": {
            "irrigation": "Tolerates dry spells; avoid moisture stress during flag leaf and grain filling.",
            "nutrients": "NPK 80:40:40 kg/ha for rainfed hybrids.",
            "pest": "Watch out for shoot fly in early 4 weeks. Sowing with first monsoon shower reduces risk."
        }
    },
    "ragi": {
        "id": "ragi",
        "name": "Ragi (Finger Millet)",
        "category": "Cereals and Millets",
        "yield_dataset_name": "Ragi",
        "recommendation_class": "ragi",
        "seasons": ["Kharif", "Rabi"],
        "soils": ["Red Soil", "Loamy", "Sandy Soil"],
        "water_req": "Low water availability",
        "duration_days": "95–115 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [1.2, 3.2],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 3846,
        "advisory_tips": {
            "irrigation": "Grows well under rainfed conditions; responds well to 2-3 protective irrigations.",
            "nutrients": "Apply farmyard manure and 60:30:30 kg NPK/ha.",
            "pest": "Blast disease is the key threat. Use resistant cultivars and tricyclazole if required."
        }
    },
    "barley": {
        "id": "barley",
        "name": "Barley",
        "category": "Cereals and Millets",
        "yield_dataset_name": "Barley",
        "recommendation_class": "barley",
        "seasons": ["Rabi", "Winter"],
        "soils": ["Loamy", "Sandy Soil", "Clay Soil"],
        "water_req": "Low water availability",
        "duration_days": "110–130 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [2.0, 4.2],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 1850,
        "advisory_tips": {
            "irrigation": "Tolerates salinity and moisture stress better than wheat.",
            "nutrients": "NPK 60:30:20 kg/ha.",
            "pest": "Check for loose smut and aphid infestations."
        }
    },

    # Pulses
    "arhar_tur": {
        "id": "arhar_tur",
        "name": "Red Gram (Arhar / Tur / Pigeonpea)",
        "category": "Pulses",
        "yield_dataset_name": "Arhar/Tur",
        "recommendation_class": "pigeonpeas",
        "seasons": ["Kharif", "Rabi"],
        "soils": ["Black Soil", "Red Soil", "Clay Soil", "Loamy"],
        "water_req": "Low water availability",
        "duration_days": "150–180 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [0.7, 1.8],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 7000,
        "advisory_tips": {
            "irrigation": "Deep rooted crop; water at flowering and pod development stages if rainfall ceases.",
            "nutrients": "Inoculate seeds with Rhizobium. Apply 20 kg N, 50 kg P2O5 per ha.",
            "pest": "Pod borer (Helicoverpa) management is essential at 50% flowering stage."
        }
    },
    "gram": {
        "id": "gram",
        "name": "Bengal Gram (Chickpea)",
        "category": "Pulses",
        "yield_dataset_name": "Gram",
        "recommendation_class": "chickpea",
        "seasons": ["Rabi", "Winter"],
        "soils": ["Black Soil", "Loamy", "Clay Soil"],
        "water_req": "Low water availability",
        "duration_days": "95–115 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [0.8, 2.2],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 5440,
        "advisory_tips": {
            "irrigation": "Needs residual soil moisture. Do not overwater; waterlogging causes collar rot.",
            "nutrients": "NPK 20:40:20 kg/ha with sulfur application.",
            "pest": "Watch for Helicoverpa pod borer and Fusarium wilt in wilt-prone soils."
        }
    },
    "moong": {
        "id": "moong",
        "name": "Green Gram (Moong)",
        "category": "Pulses",
        "yield_dataset_name": "Moong(Green Gram)",
        "recommendation_class": "mungbean",
        "seasons": ["Kharif", "Summer"],
        "soils": ["Loamy", "Red Soil", "Black Soil"],
        "water_req": "Low water availability",
        "duration_days": "60–75 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [0.5, 1.4],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 8558,
        "advisory_tips": {
            "irrigation": "Short duration catch crop. Ideal for intercropping and summer relay farming.",
            "nutrients": "20 kg N and 40 kg P2O5 per hectare.",
            "pest": "Control whitefly to prevent Yellow Mosaic Virus (YMV)."
        }
    },
    "urad": {
        "id": "urad",
        "name": "Black Gram (Urad)",
        "category": "Pulses",
        "yield_dataset_name": "Urad",
        "recommendation_class": "blackgram",
        "seasons": ["Kharif", "Rabi"],
        "soils": ["Black Soil", "Loamy", "Clay Soil"],
        "water_req": "Low water availability",
        "duration_days": "70–85 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [0.6, 1.5],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 6950,
        "advisory_tips": {
            "irrigation": "Water sensitive at flowering. Avoid standing water.",
            "nutrients": "NPK 20:40:20 kg/ha plus Rhizobium seed treatment.",
            "pest": "Spray neem oil at early stage for sucking pests."
        }
    },
    "lentil": {
        "id": "lentil",
        "name": "Lentil (Masoor)",
        "category": "Pulses",
        "yield_dataset_name": "Masoor",
        "recommendation_class": "lentil",
        "seasons": ["Rabi", "Winter"],
        "soils": ["Loamy", "Clay Soil", "Alluvial"],
        "water_req": "Low water availability",
        "duration_days": "100–120 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [0.7, 1.6],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 6425,
        "advisory_tips": {
            "irrigation": "Requires 1-2 irrigations if winter rains fail.",
            "nutrients": "20:40:20 kg NPK/ha.",
            "pest": "Watch for rust and collar rot."
        }
    },

    # Oilseeds
    "groundnut": {
        "id": "groundnut",
        "name": "Groundnut (Peanut)",
        "category": "Oilseeds",
        "yield_dataset_name": "Groundnut",
        "recommendation_class": None,
        "seasons": ["Kharif", "Summer"],
        "soils": ["Sandy Soil", "Red Soil", "Loamy"],
        "water_req": "Moderate water availability",
        "duration_days": "105–125 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [1.1, 2.8],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 6377,
        "advisory_tips": {
            "irrigation": "Pegging and pod development are critical moisture stages.",
            "nutrients": "Apply gypsum (200-400 kg/ha) at flowering to supply calcium and sulfur for pod filling.",
            "pest": "Manage collar rot and tikka leaf spot using carbendazim seed dressing."
        }
    },
    "soyabean": {
        "id": "soyabean",
        "name": "Soybean",
        "category": "Oilseeds",
        "yield_dataset_name": "Soyabean",
        "recommendation_class": "soybean",
        "seasons": ["Kharif"],
        "soils": ["Black Soil", "Loamy"],
        "water_req": "Moderate water availability",
        "duration_days": "90–105 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [1.0, 2.5],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 4600,
        "advisory_tips": {
            "irrigation": "Requires uniform moisture during pod formation; ensure good drainage during continuous rains.",
            "nutrients": "NPK 20:60:40 kg/ha. Inoculate with Bradyrhizobium japonicum.",
            "pest": "Scout for girdle beetle and stem fly. Harvest promptly when pods turn golden brown."
        }
    },
    "sunflower": {
        "id": "sunflower",
        "name": "Sunflower",
        "category": "Oilseeds",
        "yield_dataset_name": "Sunflower",
        "recommendation_class": "sunflower",
        "seasons": ["Kharif", "Rabi", "Summer"],
        "soils": ["Black Soil", "Red Soil", "Loamy"],
        "water_req": "Moderate water availability",
        "duration_days": "80–95 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [0.8, 2.0],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 6760,
        "advisory_tips": {
            "irrigation": "Water during buttoning, flowering, and seed development stages.",
            "nutrients": "Boron spray (0.2%) at ray floret stage improves seed setting significantly.",
            "pest": "Bird scaring during seed maturation is critical."
        }
    },
    "castor_seed": {
        "id": "castor_seed",
        "name": "Castor Seed",
        "category": "Oilseeds",
        "yield_dataset_name": "Castor seed",
        "recommendation_class": None,
        "seasons": ["Kharif", "Rabi"],
        "soils": ["Sandy Soil", "Red Soil", "Loamy"],
        "water_req": "Low water availability",
        "duration_days": "140–180 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [1.0, 2.2],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 5800,
        "advisory_tips": {
            "irrigation": "High drought resistance; 3-4 irrigations double the yield in dry zones.",
            "nutrients": "NPK 60:30:20 kg/ha.",
            "pest": "Semilooper caterpillar and capsule borer are major pests."
        }
    },

    # Commercial and Fibre Crops
    "cotton": {
        "id": "cotton",
        "name": "Cotton",
        "category": "Commercial and Fibre Crops",
        "yield_dataset_name": "Cotton(lint)",
        "recommendation_class": "cotton",
        "seasons": ["Kharif", "Summer"],
        "soils": ["Black Soil", "Red Soil", "Clay Soil"],
        "water_req": "Good water availability",
        "duration_days": "150–180 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [1.2, 3.5],
        "storage_type": "Dry grain warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 7020,
        "advisory_tips": {
            "irrigation": "Avoid excessive vegetative watering. Peak square and boll development need steady moisture.",
            "nutrients": "Apply 120:60:60 kg NPK/ha in split doses with magnesium sulphate foliar spray.",
            "pest": "Install pink bollworm pheromone traps. Sucking pest management needed in first 60 days."
        }
    },
    "sugarcane": {
        "id": "sugarcane",
        "name": "Sugarcane",
        "category": "Commercial and Fibre Crops",
        "yield_dataset_name": "Sugarcane",
        "recommendation_class": None,
        "seasons": ["Kharif", "Rabi", "Whole Year"],
        "soils": ["Black Soil", "Loamy", "Clay Soil"],
        "water_req": "Good water availability",
        "duration_days": "300–365 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [50.0, 110.0],
        "storage_type": "Direct sugar mill processing",
        "perishable": True,
        "base_mandi_modal_rs_qtl": 315,
        "advisory_tips": {
            "irrigation": "High water consumer (1500-2500 mm). Adopt drip irrigation for 40% water savings.",
            "nutrients": "Heavy feeder: 250:100:120 kg NPK/ha. Apply zinc and iron if chlorosis appears.",
            "pest": "Early shoot borer and red rot. Use disease-free sets treated with fungicide."
        }
    },
    "jute": {
        "id": "jute",
        "name": "Jute",
        "category": "Commercial and Fibre Crops",
        "yield_dataset_name": "Jute",
        "recommendation_class": "jute",
        "seasons": ["Kharif"],
        "soils": ["Loamy", "Clay Soil", "Alluvial"],
        "water_req": "Good water availability",
        "duration_days": "120–140 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [2.0, 3.8],
        "storage_type": "Dry warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 5050,
        "advisory_tips": {
            "irrigation": "Needs warm, humid monsoon climate and standing slow-moving water for retting.",
            "nutrients": "NPK 60:30:30 kg/ha.",
            "pest": "Yellow mite and hairy caterpillar control."
        }
    },
    "tobacco": {
        "id": "tobacco",
        "name": "Tobacco",
        "category": "Commercial and Fibre Crops",
        "yield_dataset_name": "Tobacco",
        "recommendation_class": None,
        "seasons": ["Rabi", "Winter"],
        "soils": ["Black Soil", "Red Soil", "Loamy"],
        "water_req": "Moderate water availability",
        "duration_days": "110–135 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [1.2, 2.8],
        "storage_type": "Curing barn & dry warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 14000,
        "advisory_tips": {
            "irrigation": "Regulated irrigation; avoid chloride-rich irrigation water to protect burning quality.",
            "nutrients": "Balanced nitrogen with high potassium sulfate.",
            "pest": "Tobacco caterpillar and damping-off in nursery."
        }
    },

    # Vegetables
    "potato": {
        "id": "potato",
        "name": "Potato",
        "category": "Vegetables",
        "yield_dataset_name": "Potato",
        "recommendation_class": "potato",
        "seasons": ["Rabi", "Winter"],
        "soils": ["Loamy", "Sandy Soil", "Alluvial"],
        "water_req": "Moderate water availability",
        "duration_days": "80–110 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [12.0, 28.0],
        "storage_type": "Cold storage (2-4°C, 90-95% RH)",
        "perishable": True,
        "base_mandi_modal_rs_qtl": 1350,
        "advisory_tips": {
            "irrigation": "Light and frequent irrigations; stop watering 10 days before harvest to harden skins.",
            "nutrients": "NPK 150:100:120 kg/ha. Earthing-up is critical to prevent greening of tubers.",
            "pest": "Late blight prevention using mancozeb; aphid control to prevent viral degeneration."
        }
    },
    "onion": {
        "id": "onion",
        "name": "Onion",
        "category": "Vegetables",
        "yield_dataset_name": "Onion",
        "recommendation_class": "onion",
        "seasons": ["Rabi", "Kharif", "Summer"],
        "soils": ["Black Soil", "Red Soil", "Loamy"],
        "water_req": "Moderate water availability",
        "duration_days": "120–140 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [10.0, 25.0],
        "storage_type": "Ventilated storage structure (Chawl)",
        "perishable": True,
        "base_mandi_modal_rs_qtl": 1700,
        "advisory_tips": {
            "irrigation": "Shallow root system; requires regular irrigation every 7-10 days. Stop 15 days pre-harvest.",
            "nutrients": "NPK 100:50:50 kg/ha plus sulfur at 30 kg/ha to improve pungency and storability.",
            "pest": "Thrips management and purple blotch prevention."
        }
    },
    "tomato": {
        "id": "tomato",
        "name": "Tomato",
        "category": "Vegetables",
        "yield_dataset_name": None,
        "recommendation_class": "tomato",
        "seasons": ["Kharif", "Rabi", "Summer"],
        "soils": ["Loamy", "Red Soil", "Black Soil"],
        "water_req": "Good water availability",
        "duration_days": "110–130 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [18.0, 45.0],
        "storage_type": "Cold storage (10-12°C)",
        "perishable": True,
        "base_mandi_modal_rs_qtl": 1800,
        "advisory_tips": {
            "irrigation": "Drip irrigation with fertigation gives best quality and reduces blossom end rot.",
            "nutrients": "NPK 150:100:100 kg/ha plus calcium nitrate foliar spray.",
            "pest": "Tuta absoluta and tomato leaf curl virus (whitefly vector)."
        }
    },

    # Fruits
    "banana": {
        "id": "banana",
        "name": "Banana",
        "category": "Fruits",
        "yield_dataset_name": "Banana",
        "recommendation_class": "banana",
        "seasons": ["Whole Year", "Kharif"],
        "soils": ["Clay Soil", "Loamy", "Alluvial"],
        "water_req": "Good water availability",
        "duration_days": "300–365 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [25.0, 60.0],
        "storage_type": "Cold storage (13-14°C, 90% RH)",
        "perishable": True,
        "base_mandi_modal_rs_qtl": 1900,
        "advisory_tips": {
            "irrigation": "High moisture requirement; avoid water deficit during shooting and fruit filling.",
            "nutrients": "200g N, 60g P, 300g K per plant in split applications.",
            "pest": "Sigatoka leaf spot and banana pseudostem weevil."
        }
    },
    "coconut": {
        "id": "coconut",
        "name": "Coconut",
        "category": "Fruits",
        "yield_dataset_name": "Coconut",
        "recommendation_class": "coconut",
        "seasons": ["Whole Year", "Kharif"],
        "soils": ["Sandy Soil", "Red Soil", "Loamy"],
        "water_req": "Good water availability",
        "duration_days": "Perennial (Continuous)",
        "yield_unit": "nuts/ha",
        "typical_yield_range": [5000, 12000],
        "storage_type": "Dry copra storage / shed",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 2800,
        "advisory_tips": {
            "irrigation": "Requires 40-50 liters/palm/day under basin or drip irrigation in dry months.",
            "nutrients": "Apply 500g N, 320g P2O5, 1200g K2O per bearing palm per year in two splits.",
            "pest": "Rhinoceros beetle and red palm weevil. Use pheromone traps."
        }
    },
    "mango": {
        "id": "mango",
        "name": "Mango",
        "category": "Fruits",
        "yield_dataset_name": None,
        "recommendation_class": "mango",
        "seasons": ["Summer", "Whole Year"],
        "soils": ["Loamy", "Red Soil", "Alluvial"],
        "water_req": "Moderate water availability",
        "duration_days": "Perennial (Seasonal harvest)",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [6.0, 15.0],
        "storage_type": "Cold storage (10-13°C)",
        "perishable": True,
        "base_mandi_modal_rs_qtl": 3800,
        "advisory_tips": {
            "irrigation": "Withhold water 2-3 months prior to flowering to promote floral bud differentiation.",
            "nutrients": "Apply FYM with NPK after harvest during monsoon.",
            "pest": "Mango hopper and anthracnose. Timely spray at panicle emergence."
        }
    },
    "apple": {
        "id": "apple",
        "name": "Apple",
        "category": "Fruits",
        "yield_dataset_name": None,
        "recommendation_class": "apple",
        "seasons": ["Autumn", "Whole Year"],
        "soils": ["Loamy", "Clay Soil"],
        "water_req": "Moderate water availability",
        "duration_days": "Perennial (Temperate)",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [8.0, 20.0],
        "storage_type": "Controlled atmosphere (CA) cold storage (0-2°C)",
        "perishable": True,
        "base_mandi_modal_rs_qtl": 7500,
        "advisory_tips": {
            "irrigation": "Critical during fruit sizing in temperate zones.",
            "nutrients": "Calcium sprays reduce bitter pit and storage breakdown.",
            "pest": "Apple scab and San Jose scale control."
        }
    },
    "grapes": {
        "id": "grapes",
        "name": "Grapes",
        "category": "Fruits",
        "yield_dataset_name": None,
        "recommendation_class": "grapes",
        "seasons": ["Winter", "Summer"],
        "soils": ["Sandy Soil", "Loamy", "Red Soil"],
        "water_req": "Good water availability",
        "duration_days": "Perennial (Trellis)",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [15.0, 35.0],
        "storage_type": "Cold storage (0°C, 95% RH with SO2 pads)",
        "perishable": True,
        "base_mandi_modal_rs_qtl": 4200,
        "advisory_tips": {
            "irrigation": "Regulated deficit irrigation post-veraison enhances brix and berry quality.",
            "nutrients": "Potassium application during berry development is vital.",
            "pest": "Downy mildew and powdery mildew prevention."
        }
    },

    # Spices and Plantation Crops
    "turmeric": {
        "id": "turmeric",
        "name": "Turmeric",
        "category": "Spices and Plantation Crops",
        "yield_dataset_name": "Turmeric",
        "recommendation_class": "turmeric",
        "seasons": ["Kharif"],
        "soils": ["Black Soil", "Red Soil", "Loamy"],
        "water_req": "Good water availability",
        "duration_days": "240–270 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [4.0, 9.0],
        "storage_type": "Dry polished warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 12500,
        "advisory_tips": {
            "irrigation": "Requires 15-20 irrigations in medium soils. Ridge and furrow planting prevents rhizome rot.",
            "nutrients": "Heavy FYM application (25-30 t/ha) with NPK 120:60:120 kg/ha.",
            "pest": "Rhizome rot and shoot borer. Seed treatment with metalaxyl is recommended."
        }
    },
    "dry_chillies": {
        "id": "dry_chillies",
        "name": "Dry Chillies",
        "category": "Spices and Plantation Crops",
        "yield_dataset_name": "Dry chillies",
        "recommendation_class": None,
        "seasons": ["Kharif", "Rabi", "Summer"],
        "soils": ["Black Soil", "Red Soil", "Loamy"],
        "water_req": "Moderate water availability",
        "duration_days": "150–180 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [1.5, 3.8],
        "storage_type": "Cold storage (4-6°C to retain red color)",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 18000,
        "advisory_tips": {
            "irrigation": "Irrigate at flowering and pod set. Avoid flooding which causes damping-off.",
            "nutrients": "NPK 120:60:60 kg/ha in splits.",
            "pest": "Thrips, mites, and anthracnose (die-back). Solar drying on clean polythene sheets preserves capsaicin."
        }
    },
    "black_pepper": {
        "id": "black_pepper",
        "name": "Black Pepper",
        "category": "Spices and Plantation Crops",
        "yield_dataset_name": "Black pepper",
        "recommendation_class": "blackpepper",
        "seasons": ["Kharif", "Whole Year"],
        "soils": ["Red Soil", "Loamy", "Clay Soil"],
        "water_req": "Good water availability",
        "duration_days": "Perennial (Vine)",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [0.6, 2.0],
        "storage_type": "Dry spice warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 58000,
        "advisory_tips": {
            "irrigation": "Requires humid tropical climate with summer irrigation under drip/micro-sprinkler.",
            "nutrients": "Apply 100g N, 40g P2O5, 140g K2O per vine per year.",
            "pest": "Phytophthora foot rot (quick wilt). Apply Trichoderma and Bordeaux mixture."
        }
    },
    "arecanut": {
        "id": "arecanut",
        "name": "Arecanut",
        "category": "Spices and Plantation Crops",
        "yield_dataset_name": "Arecanut",
        "recommendation_class": None,
        "seasons": ["Whole Year", "Kharif"],
        "soils": ["Black Soil", "Red Soil", "Loamy"],
        "water_req": "Good water availability",
        "duration_days": "Perennial (Palm)",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [1.2, 2.8],
        "storage_type": "Dry ventilated warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 42000,
        "advisory_tips": {
            "irrigation": "Requires regular irrigation during dry period; cannot withstand prolonged drought.",
            "nutrients": "Apply 100g N, 40g P, 140g K per palm with green leaf manure.",
            "pest": "Koleroga (fruit rot) caused by Phytophthora. Spray 1% Bordeaux mixture before monsoon."
        }
    },
    "garlic": {
        "id": "garlic",
        "name": "Garlic",
        "category": "Spices and Plantation Crops",
        "yield_dataset_name": "Garlic",
        "recommendation_class": "garlic",
        "seasons": ["Rabi", "Winter"],
        "soils": ["Loamy", "Black Soil"],
        "water_req": "Moderate water availability",
        "duration_days": "120–140 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [4.0, 10.0],
        "storage_type": "Cool ventilated warehouse",
        "perishable": False,
        "base_mandi_modal_rs_qtl": 8500,
        "advisory_tips": {
            "irrigation": "Irrigate immediately after planting cloves, then at 8-10 day intervals.",
            "nutrients": "100:50:50 kg NPK/ha plus sulfur at 30 kg/ha.",
            "pest": "Thrips and purple blotch."
        }
    },
    "ginger": {
        "id": "ginger",
        "name": "Ginger",
        "category": "Spices and Plantation Crops",
        "yield_dataset_name": "Ginger",
        "recommendation_class": None,
        "seasons": ["Kharif"],
        "soils": ["Loamy", "Red Soil"],
        "water_req": "Good water availability",
        "duration_days": "210–240 days",
        "yield_unit": "tonnes/ha",
        "typical_yield_range": [8.0, 18.0],
        "storage_type": "Cool storage / sand pits",
        "perishable": True,
        "base_mandi_modal_rs_qtl": 6500,
        "advisory_tips": {
            "irrigation": "Requires mulch to conserve moisture and frequent light watering.",
            "nutrients": "Heavy organic manure (25 t/ha) and balanced chemical fertilizer.",
            "pest": "Soft rot (rhizome rot). Ensure excellent drainage."
        }
    }
}

# The 21 crops required for Farm Planning (preserving exact original list)
FARM_PLANNING_21_CROPS = [
    'Arecanut', 'Arhar/Tur', 'Castor seed', 'Coconut', 'Cotton(lint)',
    'Dry chillies', 'Gram', 'Jute', 'Maize', 'Onion', 'Potato', 'Rice',
    'Sugarcane', 'Sunflower', 'Tobacco', 'Turmeric', 'Wheat', 'Bajra',
    'Black pepper', 'Groundnut', 'Soyabean'
]

# Alias map: maps any representation (lowercase, spaces, dataset strings, model classes) to canonical id
CROP_ALIAS_MAP = {
    # Rice
    "rice": "rice", "paddy": "rice",
    # Wheat
    "wheat": "wheat",
    # Maize
    "maize": "maize", "corn": "maize",
    # Bajra
    "bajra": "bajra", "pearl millet": "bajra",
    # Jowar
    "jowar": "jowar", "sorghum": "jowar",
    # Ragi
    "ragi": "ragi", "finger millet": "ragi",
    # Barley
    "barley": "barley",
    # Arhar / Tur
    "arhar/tur": "arhar_tur", "pigeonpeas": "arhar_tur", "arhar": "arhar_tur", "tur": "arhar_tur", "red gram": "arhar_tur",
    # Gram
    "gram": "gram", "chickpea": "gram", "bengal gram": "gram",
    # Moong
    "moong(green gram)": "moong", "moong": "moong", "mungbean": "moong", "green gram": "moong",
    # Urad
    "urad": "urad", "blackgram": "urad", "black gram": "urad",
    # Lentil
    "masoor": "lentil", "lentil": "lentil",
    # Groundnut
    "groundnut": "groundnut", "peanut": "groundnut",
    # Soyabean
    "soyabean": "soyabean", "soybean": "soyabean",
    # Sunflower
    "sunflower": "sunflower",
    # Castor
    "castor seed": "castor_seed", "castor": "castor_seed",
    # Cotton
    "cotton(lint)": "cotton", "cotton": "cotton",
    # Sugarcane
    "sugarcane": "sugarcane",
    # Jute
    "jute": "jute",
    # Tobacco
    "tobacco": "tobacco",
    # Potato
    "potato": "potato",
    # Onion
    "onion": "onion",
    # Tomato
    "tomato": "tomato",
    # Banana
    "banana": "banana",
    # Coconut
    "coconut": "coconut",
    # Mango
    "mango": "mango",
    # Apple
    "apple": "apple",
    # Grapes
    "grapes": "grapes",
    # Turmeric
    "turmeric": "turmeric",
    # Dry chillies
    "dry chillies": "dry_chillies", "chilli": "dry_chillies", "dry chillis": "dry_chillies",
    # Black pepper
    "black pepper": "black_pepper", "blackpepper": "black_pepper", "pepper": "black_pepper",
    # Arecanut
    "arecanut": "arecanut", "betelnut": "arecanut",
    # Garlic
    "garlic": "garlic",
    # Ginger
    "ginger": "ginger"
}


def normalize_crop_name(name: str):
    """Normalize any crop name or alias to canonical ID and catalogue entry."""
    if not name:
        return None, None
    key = str(name).strip().lower()
    canonical_id = CROP_ALIAS_MAP.get(key)
    if not canonical_id:
        # Try direct match in catalogue
        if key in CROP_CATALOGUE:
            canonical_id = key
    if canonical_id and canonical_id in CROP_CATALOGUE:
        return canonical_id, CROP_CATALOGUE[canonical_id]
    return None, None


def get_all_catalogue_crops():
    """Returns all catalogue crops structured with capability badges."""
    results = []
    for cid, info in CROP_CATALOGUE.items():
        results.append({
            "id": cid,
            "name": info["name"],
            "category": info["category"],
            "seasons": info["seasons"],
            "soils": info["soils"],
            "water_req": info["water_req"],
            "duration": info["duration_days"],
            "yield_unit": info["yield_unit"],
            "typical_yield_range": info["typical_yield_range"],
            "storage_type": info["storage_type"],
            "perishable": info["perishable"],
            "base_mandi_modal_rs_qtl": info["base_mandi_modal_rs_qtl"],
            "has_recommendation_model": info["recommendation_class"] is not None,
            "has_yield_model": info["yield_dataset_name"] is not None,
            "has_mandi_prices": True,
            "advisory_tips": info["advisory_tips"]
        })
    return results
