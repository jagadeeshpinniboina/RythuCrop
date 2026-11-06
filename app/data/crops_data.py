"""
RythuCrop Agronomic Crop Database and Characteristics
Comprehensive ICAR-calibrated agronomic profiles for crop planning, seasonal compatibility,
soil-water affinity matrices, and cultivation economics.
"""

from typing import Dict, List, Any

# Detailed agronomic characteristics for Farm Planning crops
CROP_DATA: Dict[str, Dict[str, Any]] = {
    "Cotton(lint)": {
        "id": "cotton",
        "name": "Cotton(lint)",
        "category": "Commercial and Fibre Crops",
        "crop_type": "seasonal",
        "seasons": ["Kharif"],
        "soils": {
            "Black Soil": 30,
            "Clay Soil": 26,
            "Loamy": 22,
            "Alluvial": 20,
            "Red Soil": 18,
            "Sandy Soil": 4
        },
        "water_req": "Good water availability",
        "water_affinity": {
            "Good water availability": 26,
            "Moderate water availability": 26,
            "Low water availability": 8,
            "Rainfed": 5
        },
        "experience": ["Some experience", "Experienced"],
        "land_suitability": ["Medium", "Large"],
        "goals": ["Higher yield", "Balanced farming"],
        "rotation_group": "fibre_cash",
        "soil_depletion": "medium",
        "economics": {
            "estimated_cost_per_acre": "₹24,000 - ₹30,000",
            "estimated_gross_return": "₹55,000 - ₹75,000",
            "estimated_profit_per_acre": "₹28,000 - ₹45,000",
            "market_demand": "High commercial mandi liquidity with active CCI procurement"
        },
        "soil_guidance": "Deep black cotton soils (Vertisols) provide optimal moisture retention. Ensure drainage channels to avoid seedling waterlogging.",
        "water_scheduling": "Key irrigation stages: Square formation (45-50 DAS), flowering (70-75 DAS), and boll development (90-100 DAS). Avoid moisture stress during boll filling.",
        "risks": "Susceptible to pink bollworm, sucking pests during vegetative growth, and boll rotting under unseasonal late rains.",
        "next_steps": "Use certified Bt cotton hybrids, apply pre-emergence weed control, and install yellow sticky traps with pheromone lures."
    },
    "Soyabean": {
        "id": "soyabean",
        "name": "Soyabean",
        "category": "Oilseeds",
        "crop_type": "seasonal",
        "seasons": ["Kharif"],
        "soils": {
            "Black Soil": 30,
            "Loamy": 26,
            "Alluvial": 22,
            "Clay Soil": 20,
            "Red Soil": 16,
            "Sandy Soil": 6
        },
        "water_req": "Moderate water availability",
        "water_affinity": {
            "Moderate water availability": 26,
            "Good water availability": 22,
            "Low water availability": 18,
            "Rainfed": 16
        },
        "experience": ["Beginner", "Some experience", "Experienced"],
        "land_suitability": ["Small", "Medium", "Large"],
        "goals": ["Lower input cost", "Balanced farming", "Higher yield"],
        "rotation_group": "legume_oilseed",
        "soil_depletion": "restorative",
        "economics": {
            "estimated_cost_per_acre": "₹14,000 - ₹18,000",
            "estimated_gross_return": "₹36,000 - ₹48,000",
            "estimated_profit_per_acre": "₹20,000 - ₹30,000",
            "market_demand": "High domestic oil extraction demand and defatted soya meal exports"
        },
        "soil_guidance": "Fertile, well-drained loams and black soils with pH 6.5-7.5. Rhizobium nodulation fixes 35-40 kg atmospheric Nitrogen per hectare.",
        "water_scheduling": "Critical moisture stages: Flowering (35-40 DAS) and pod filling (60-70 DAS). Tolerates short dry spells; ensure surface drainage.",
        "risks": "Susceptible to yellow mosaic virus, stem fly, and pod borer under prolonged cloudy conditions.",
        "next_steps": "Treat seed with Rhizobium and PSB biofertilizers, maintain 45 cm row spacing, and monitor for semilooper."
    },
    "Arhar/Tur": {
        "id": "arhar_tur",
        "name": "Arhar/Tur",
        "category": "Pulses",
        "crop_type": "seasonal",
        "seasons": ["Kharif"],
        "soils": {
            "Black Soil": 28,
            "Red Soil": 28,
            "Loamy": 26,
            "Alluvial": 22,
            "Clay Soil": 18,
            "Sandy Soil": 16
        },
        "water_req": "Low water availability",
        "water_affinity": {
            "Low water availability": 28,
            "Rainfed": 28,
            "Moderate water availability": 20,
            "Good water availability": 18
        },
        "experience": ["Beginner", "Some experience", "Experienced"],
        "land_suitability": ["Small", "Medium", "Large"],
        "goals": ["Lower water use", "Lower input cost", "Balanced farming"],
        "rotation_group": "legume_pulse",
        "soil_depletion": "restorative",
        "economics": {
            "estimated_cost_per_acre": "₹12,000 - ₹16,000",
            "estimated_gross_return": "₹38,000 - ₹52,000",
            "estimated_profit_per_acre": "₹24,000 - ₹36,000",
            "market_demand": "High domestic pulse consumption; stable market price well above MSP"
        },
        "soil_guidance": "Deep, well-drained soils allow deep taproot development up to 2 meters. Breaks subsoil hardpans and enriches residual soil nitrogen.",
        "water_scheduling": "Exceptional drought tolerance. 1-2 protective irrigations at flower initiation and pod formation significantly increase grain weight.",
        "risks": "Susceptible to pod borer (Helicoverpa armigera) and Phytophthora stem blight in waterlogged fields.",
        "next_steps": "Inoculate seeds with Rhizobium culture, apply 50 kg SSP per acre at sowing, and practice border row nipping."
    },
    "Rice": {
        "id": "rice",
        "name": "Rice",
        "category": "Cereals and Millets",
        "crop_type": "seasonal",
        "seasons": ["Kharif", "Summer"],
        "soils": {
            "Clay Soil": 30,
            "Alluvial": 28,
            "Loamy": 22,
            "Black Soil": 20,
            "Red Soil": 10,
            "Sandy Soil": -40
        },
        "water_req": "Good water availability",
        "water_affinity": {
            "Good water availability": 30,
            "Moderate water availability": 6,
            "Low water availability": -80,
            "Rainfed": -80
        },
        "experience": ["Beginner", "Some experience", "Experienced"],
        "land_suitability": ["Medium", "Large"],
        "goals": ["Higher yield", "Balanced farming"],
        "rotation_group": "staple_cereal",
        "soil_depletion": "high",
        "economics": {
            "estimated_cost_per_acre": "₹22,000 - ₹28,000",
            "estimated_gross_return": "₹50,000 - ₹68,000",
            "estimated_profit_per_acre": "₹26,000 - ₹40,000",
            "market_demand": "Guaranteed government procurement and steady national food staple demand"
        },
        "soil_guidance": "Heavy clay and alluvial soils with low percolation rate. Puddling forms an impermeable subsurface layer to conserve standing water.",
        "water_scheduling": "Maintain 2-5 cm standing water from tillering to panicle development. Drain field 10-12 days before anticipated harvest.",
        "risks": "Susceptible to blast, bacterial leaf blight, and brown planthopper under dense canopy and excess nitrogen.",
        "next_steps": "Adopt alternate wetting and drying (AWD) to save 25% water, apply zinc sulphate, and monitor light traps."
    },
    "Maize": {
        "id": "maize",
        "name": "Maize",
        "category": "Cereals and Millets",
        "crop_type": "seasonal",
        "seasons": ["Kharif"],
        "soils": {
            "Black Soil": 24,
            "Loamy": 24,
            "Alluvial": 22,
            "Red Soil": 18,
            "Clay Soil": 10,
            "Sandy Soil": 8
        },
        "water_req": "Good water availability",
        "water_affinity": {
            "Good water availability": 25,
            "Moderate water availability": 22,
            "Low water availability": -40,
            "Rainfed": -40
        },
        "experience": ["Beginner", "Some experience", "Experienced"],
        "land_suitability": ["Medium", "Large"],
        "goals": ["Higher yield", "Balanced farming"],
        "rotation_group": "cereal",
        "soil_depletion": "exhaustive",
        "economics": {
            "estimated_cost_per_acre": "₹16,000 - ₹20,000",
            "estimated_gross_return": "₹40,000 - ₹54,000",
            "estimated_profit_per_acre": "₹22,000 - ₹34,000",
            "market_demand": "Very high industrial demand across feed mills, starch manufacturing, and silage"
        },
        "soil_guidance": "Deep, fertile loam to black soils rich in organic matter. Sensitive to water stagnation; ridge planting ensures optimal aeration.",
        "water_scheduling": "Critical moisture periods: Knee-high stage (30-35 DAS), tasseling, and silking. Moisture deficit at pollination causes barren ears.",
        "risks": "High vulnerability to fall armyworm (Spodoptera frugiperda) and stem borer.",
        "next_steps": "Apply whorl application of bio-agents or neem formulation at 15-20 DAS and maintain split nitrogen fertigation."
    },
    "Groundnut": {
        "id": "groundnut",
        "name": "Groundnut",
        "category": "Oilseeds",
        "crop_type": "seasonal",
        "seasons": ["Kharif", "Summer"],
        "soils": {
            "Sandy Soil": 30,
            "Red Soil": 28,
            "Loamy": 26,
            "Alluvial": 18,
            "Black Soil": 12,
            "Clay Soil": -25
        },
        "water_req": "Moderate water availability",
        "water_affinity": {
            "Moderate water availability": 26,
            "Low water availability": 22,
            "Rainfed": 20,
            "Good water availability": 18
        },
        "experience": ["Beginner", "Some experience"],
        "land_suitability": ["Small", "Medium"],
        "goals": ["Balanced farming", "Lower input cost", "Lower water use"],
        "rotation_group": "legume_oilseed",
        "soil_depletion": "restorative",
        "economics": {
            "estimated_cost_per_acre": "₹18,000 - ₹22,000",
            "estimated_gross_return": "₹45,000 - ₹62,000",
            "estimated_profit_per_acre": "₹25,000 - ₹40,000",
            "market_demand": "High edible oil demand and confectionery export premiums"
        },
        "soil_guidance": "Light-textured sandy loams and red sandy soils with loose surface crumb. Enables easy gynophore (peg) penetration and clean harvest.",
        "water_scheduling": "Critical periods: Flowering (25-30 DAS) and peg penetration/pod swelling (45-65 DAS). Avoid excessive irrigation near maturity.",
        "risks": "Susceptible to tikka leaf spot, collar rot in waterlogged soils, and white grub attack on pods.",
        "next_steps": "Apply gypsum @ 200 kg/acre at flowering to ensure calcium for pod filling, and practice seed treatment with Trichoderma."
    },
    "Bajra": {
        "id": "bajra",
        "name": "Bajra",
        "category": "Cereals and Millets",
        "crop_type": "seasonal",
        "seasons": ["Kharif", "Summer"],
        "soils": {
            "Sandy Soil": 30,
            "Red Soil": 28,
            "Loamy": 20,
            "Alluvial": 16,
            "Black Soil": 12,
            "Clay Soil": -20
        },
        "water_req": "Low water availability",
        "water_affinity": {
            "Low water availability": 30,
            "Rainfed": 30,
            "Moderate water availability": 18,
            "Good water availability": 10
        },
        "experience": ["Beginner", "Some experience"],
        "land_suitability": ["Small", "Medium"],
        "goals": ["Lower water use", "Lower input cost"],
        "rotation_group": "millet",
        "soil_depletion": "low",
        "economics": {
            "estimated_cost_per_acre": "₹8,000 - ₹12,000",
            "estimated_gross_return": "₹24,000 - ₹34,000",
            "estimated_profit_per_acre": "₹15,000 - ₹22,000",
            "market_demand": "Growing superfood millet demand and valuable nutritious livestock fodder"
        },
        "soil_guidance": "Unmatched tolerance for sandy, low-fertility, and marginal soils. Performs reliably under high heat and erratic monsoons.",
        "water_scheduling": "Needs only 250-350 mm moisture during crop duration. Light protective irrigations during dry spells enhance earhead size.",
        "risks": "Vulnerable to downy mildew (green ear disease) and ergot under high atmospheric humidity.",
        "next_steps": "Use metalaxyl treated hybrid seed, thin out excess seedlings within 15 DAS, and harvest before earhead shattering."
    },
    "Castor seed": {
        "id": "castor_seed",
        "name": "Castor seed",
        "category": "Oilseeds",
        "crop_type": "seasonal",
        "seasons": ["Kharif"],
        "soils": {
            "Red Soil": 28,
            "Sandy Soil": 26,
            "Loamy": 22,
            "Black Soil": 18,
            "Alluvial": 16,
            "Clay Soil": -10
        },
        "water_req": "Low water availability",
        "water_affinity": {
            "Low water availability": 28,
            "Rainfed": 28,
            "Moderate water availability": 20,
            "Good water availability": 12
        },
        "experience": ["Beginner", "Some experience"],
        "land_suitability": ["Small", "Medium"],
        "goals": ["Lower water use", "Lower input cost", "Balanced farming"],
        "rotation_group": "oilseed_industrial",
        "soil_depletion": "medium",
        "economics": {
            "estimated_cost_per_acre": "₹10,000 - ₹14,000",
            "estimated_gross_return": "₹32,000 - ₹46,000",
            "estimated_profit_per_acre": "₹20,000 - ₹32,000",
            "market_demand": "High industrial and medicinal castor oil demand with strong export prices"
        },
        "soil_guidance": "Well-drained red sandy soils and light loams. Deep taproot system accesses water and nutrients from lower subsoil strata.",
        "water_scheduling": "High drought resilience. 1-2 supplementary irrigations at primary and secondary spike formation optimize capsule filling.",
        "risks": "Susceptible to semilooper and capsule borer (Dichocrocis punctiferalis).",
        "next_steps": "Maintain wide 90x60 cm plant spacing, adopt intercropping with pulses, and handpick semilooper larvae."
    },
    "Jute": {
        "id": "jute",
        "name": "Jute",
        "category": "Commercial and Fibre Crops",
        "crop_type": "seasonal",
        "seasons": ["Kharif"],
        "soils": {
            "Alluvial": 30,
            "Loamy": 26,
            "Clay Soil": 24,
            "Black Soil": 12,
            "Red Soil": 8,
            "Sandy Soil": -30
        },
        "water_req": "Good water availability",
        "water_affinity": {
            "Good water availability": 30,
            "Moderate water availability": 14,
            "Low water availability": -80,
            "Rainfed": -60
        },
        "experience": ["Some experience", "Beginner"],
        "land_suitability": ["Medium", "Large"],
        "goals": ["Higher yield"],
        "rotation_group": "fibre",
        "soil_depletion": "medium",
        "economics": {
            "estimated_cost_per_acre": "₹15,000 - ₹19,000",
            "estimated_gross_return": "₹38,000 - ₹50,000",
            "estimated_profit_per_acre": "₹22,000 - ₹31,000",
            "market_demand": "Steady government packaging procurement under Jute Packaging Materials Act"
        },
        "soil_guidance": "New alluvial soils along river basins rich in silt and organic matter. Neutral pH 6.2-7.2 promotes long, flexible bast fibers.",
        "water_scheduling": "Demands abundant rainfall or frequent standing moisture during stem elongation, plus clean water for ribbon retting.",
        "risks": "Yellow mite and stem rot (Macrophomina phaseolina) during humid spells.",
        "next_steps": "Harvest at 50% flowering for optimum fiber tensile strength and ensure clean retting."
    },
    "Wheat": {
        "id": "wheat",
        "name": "Wheat",
        "category": "Cereals and Millets",
        "crop_type": "seasonal",
        "seasons": ["Rabi"],
        "soils": {
            "Alluvial": 30,
            "Loamy": 28,
            "Black Soil": 25,
            "Clay Soil": 20,
            "Red Soil": 10,
            "Sandy Soil": -20
        },
        "water_req": "Good water availability",
        "water_affinity": {
            "Good water availability": 28,
            "Moderate water availability": 24,
            "Low water availability": -60,
            "Rainfed": -60
        },
        "experience": ["Beginner", "Some experience", "Experienced"],
        "land_suitability": ["Medium", "Large"],
        "goals": ["Higher yield", "Balanced farming"],
        "rotation_group": "staple_cereal",
        "soil_depletion": "medium_high",
        "economics": {
            "estimated_cost_per_acre": "₹16,000 - ₹20,000",
            "estimated_gross_return": "₹42,000 - ₹58,000",
            "estimated_profit_per_acre": "₹24,000 - ₹38,000",
            "market_demand": "Core national winter staple with guaranteed FCI MSP procurement"
        },
        "soil_guidance": "Fertile alluvial and clay loam soils with neutral pH. Requires a well-pulverized, firm seedbed for uniform germination.",
        "water_scheduling": "Needs 4-5 irrigations. Crown Root Initiation (CRI at 20-22 DAS) is critical; subsequent irrigations at tillering, flowering, and grain filling.",
        "risks": "Yellow and brown rust in northern belt; terminal heat stress during grain filling stage.",
        "next_steps": "Sow timely before Nov 20, use certified rust-resistant varieties, and apply zinc sulphate."
    },
    "Gram": {
        "id": "gram",
        "name": "Gram",
        "category": "Pulses",
        "crop_type": "seasonal",
        "seasons": ["Rabi"],
        "soils": {
            "Black Soil": 30,
            "Alluvial": 28,
            "Loamy": 26,
            "Clay Soil": 20,
            "Red Soil": 16,
            "Sandy Soil": 10
        },
        "water_req": "Low water availability",
        "water_affinity": {
            "Low water availability": 28,
            "Rainfed": 28,
            "Moderate water availability": 24,
            "Good water availability": 18
        },
        "experience": ["Beginner", "Some experience", "Experienced"],
        "land_suitability": ["Small", "Medium"],
        "goals": ["Lower water use", "Lower input cost", "Balanced farming"],
        "rotation_group": "legume_pulse",
        "soil_depletion": "restorative",
        "economics": {
            "estimated_cost_per_acre": "₹11,000 - ₹15,000",
            "estimated_gross_return": "₹35,000 - ₹48,000",
            "estimated_profit_per_acre": "₹22,000 - ₹33,000",
            "market_demand": "Consistently high demand for whole gram, besan flour, and split dal"
        },
        "soil_guidance": "Medium to heavy black cotton soils and alluvial loams. Cloddy seedbed prevents soil crusting and facilitates root aeration.",
        "water_scheduling": "Grown predominantly on conserved residual soil moisture. If irrigated, apply at pre-flowering and pod development. Excess water triggers vegetative wilt.",
        "risks": "Susceptible to Fusarium wilt, dry root rot, and pod borer (Helicoverpa).",
        "next_steps": "Treat seed with Trichoderma harzianum, apply sulfur, and avoid excess nitrogen fertilizer."
    },
    "Potato": {
        "id": "potato",
        "name": "Potato",
        "category": "Vegetables",
        "crop_type": "seasonal",
        "seasons": ["Rabi"],
        "soils": {
            "Alluvial": 30,
            "Loamy": 28,
            "Sandy Soil": 22,
            "Black Soil": 12,
            "Red Soil": 10,
            "Clay Soil": -30
        },
        "water_req": "Good water availability",
        "water_affinity": {
            "Good water availability": 28,
            "Moderate water availability": 22,
            "Low water availability": -60,
            "Rainfed": -60
        },
        "experience": ["Some experience", "Experienced"],
        "land_suitability": ["Small", "Medium"],
        "goals": ["Higher yield"],
        "rotation_group": "tuber_cash",
        "soil_depletion": "exhaustive",
        "economics": {
            "estimated_cost_per_acre": "₹32,000 - ₹42,000",
            "estimated_gross_return": "₹80,000 - ₹115,000",
            "estimated_profit_per_acre": "₹45,000 - ₹75,000",
            "market_demand": "Massive everyday vegetable demand and processing chips contract buying"
        },
        "soil_guidance": "Loose, friable sandy loams and rich alluvial soils with pH 5.2-6.5. Free of stones to allow uniform tuber bulking.",
        "water_scheduling": "Shallow root system requires 6-8 light irrigations at 8-10 day intervals. Stop watering 10 days before dehaulming.",
        "risks": "High vulnerability to late blight (Phytophthora infestans) during foggy winter mornings.",
        "next_steps": "Use certified disease-free seed tubers, practice timely earthing-up, and spray preventive mancozeb."
    },
    "Onion": {
        "id": "onion",
        "name": "Onion",
        "category": "Vegetables",
        "crop_type": "seasonal",
        "seasons": ["Rabi", "Summer"],
        "soils": {
            "Loamy": 28,
            "Alluvial": 26,
            "Red Soil": 24,
            "Black Soil": 22,
            "Sandy Soil": 16,
            "Clay Soil": -10
        },
        "water_req": "Moderate water availability",
        "water_affinity": {
            "Moderate water availability": 26,
            "Good water availability": 24,
            "Low water availability": -30,
            "Rainfed": -50
        },
        "experience": ["Some experience", "Experienced"],
        "land_suitability": ["Small", "Medium"],
        "goals": ["Higher yield", "Balanced farming"],
        "rotation_group": "bulb_vegetable",
        "soil_depletion": "medium",
        "economics": {
            "estimated_cost_per_acre": "₹22,000 - ₹28,000",
            "estimated_gross_return": "₹60,000 - ₹95,000",
            "estimated_profit_per_acre": "₹35,000 - ₹67,000",
            "market_demand": "Essential kitchen staple with frequent seasonal price surges in mandis"
        },
        "soil_guidance": "Deep, friable loams rich in decomposed organic matter with pH 6.0-7.0. Heavy soils impede bulb sizing.",
        "water_scheduling": "Requires 10-14 frequent light irrigations. Critical at bulb expansion (60-80 DAT). Withhold water 15 days before harvest for proper field curing.",
        "risks": "Susceptible to thrips, purple blotch, and basal rot during warm humid weather.",
        "next_steps": "Transplant 40-45 day old sturdy seedlings, apply sulfur for pungency, and cure bulbs under shade."
    },
    "Sunflower": {
        "id": "sunflower",
        "name": "Sunflower",
        "category": "Oilseeds",
        "crop_type": "seasonal",
        "seasons": ["Rabi", "Summer", "Kharif"],
        "soils": {
            "Loamy": 26,
            "Black Soil": 26,
            "Red Soil": 24,
            "Alluvial": 22,
            "Sandy Soil": 18,
            "Clay Soil": 14
        },
        "water_req": "Moderate water availability",
        "water_affinity": {
            "Moderate water availability": 25,
            "Low water availability": 20,
            "Good water availability": 18,
            "Rainfed": 16
        },
        "experience": ["Beginner", "Some experience"],
        "land_suitability": ["Small", "Medium"],
        "goals": ["Balanced farming", "Lower water use", "Lower input cost"],
        "rotation_group": "oilseed",
        "soil_depletion": "medium",
        "economics": {
            "estimated_cost_per_acre": "₹13,000 - ₹17,000",
            "estimated_gross_return": "₹36,000 - ₹50,000",
            "estimated_profit_per_acre": "₹21,000 - ₹33,000",
            "market_demand": "High demand for premium edible sunflower oil and bird feed export"
        },
        "soil_guidance": "Wide adaptability across deep black, red, and alluvial soils. Requires neutral pH and boron sufficiency for complete seed filling.",
        "water_scheduling": "Critical stages: Bud initiation (30-35 DAS), flowering (50-55 DAS), and seed filling (65-75 DAS). Tolerates heat well in summer.",
        "risks": "Vulnerable to parakeet damage near harvest, necrosis virus, and alternaria leaf spot.",
        "next_steps": "Spray boron @ 2g/L at ray floret opening to enhance seed setting, and install bird scarers."
    },
    "Dry chillies": {
        "id": "dry_chillies",
        "name": "Dry chillies",
        "category": "Spices and Plantation Crops",
        "crop_type": "seasonal",
        "seasons": ["Rabi", "Summer"],
        "soils": {
            "Black Soil": 28,
            "Red Soil": 26,
            "Loamy": 26,
            "Alluvial": 16,
            "Sandy Soil": 12,
            "Clay Soil": -10
        },
        "water_req": "Moderate water availability",
        "water_affinity": {
            "Moderate water availability": 26,
            "Good water availability": 22,
            "Low water availability": 12,
            "Rainfed": -20
        },
        "experience": ["Some experience", "Experienced"],
        "land_suitability": ["Small", "Medium"],
        "goals": ["Higher yield", "Balanced farming"],
        "rotation_group": "solanaceous_spice",
        "soil_depletion": "medium",
        "economics": {
            "estimated_cost_per_acre": "₹28,000 - ₹38,000",
            "estimated_gross_return": "₹75,000 - ₹120,000",
            "estimated_profit_per_acre": "₹45,000 - ₹82,000",
            "market_demand": "Major export commodity (Guntur/Byadgi mandis) with high spice value"
        },
        "soil_guidance": "Fertile, well-aerated black and red loamy soils. Susceptible to water stagnation which triggers root rot.",
        "water_scheduling": "Requires light, frequent irrigations. Avoid excess water during flowering to prevent flower drop.",
        "risks": "Chilli thrips, yellow mites, and anthracnose (die-back/fruit rot).",
        "next_steps": "Install blue sticky traps for thrips, spray neem oil early, and dry ripe pods on clean polythene sheets."
    },
    "Tobacco": {
        "id": "tobacco",
        "name": "Tobacco",
        "category": "Commercial and Fibre Crops",
        "crop_type": "seasonal",
        "seasons": ["Rabi"],
        "soils": {
            "Black Soil": 26,
            "Loamy": 26,
            "Alluvial": 24,
            "Red Soil": 22,
            "Sandy Soil": 12,
            "Clay Soil": 10
        },
        "water_req": "Moderate water availability",
        "water_affinity": {
            "Moderate water availability": 25,
            "Good water availability": 20,
            "Low water availability": 10,
            "Rainfed": -20
        },
        "experience": ["Some experience", "Experienced"],
        "land_suitability": ["Medium", "Large"],
        "goals": ["Higher yield", "Balanced farming"],
        "rotation_group": "commercial",
        "soil_depletion": "high",
        "economics": {
            "estimated_cost_per_acre": "₹24,000 - ₹32,000",
            "estimated_gross_return": "₹65,000 - ₹90,000",
            "estimated_profit_per_acre": "₹38,000 - ₹58,000",
            "market_demand": "Direct Tobacco Board regulated auction settlement with assured payment"
        },
        "soil_guidance": "Light to medium loams and black soils with low chloride content (< 50 ppm) to ensure good leaf burn quality.",
        "water_scheduling": "Needs controlled moisture up to topping stage. Over-irrigation ruins leaf aroma and curing color.",
        "risks": "Tobacco caterpillar (Spodoptera litura) and black shank disease.",
        "next_steps": "Practice timely topping and desuckering, and adhere to Tobacco Board authorized nursery seedlings."
    },
    "Turmeric": {
        "id": "turmeric",
        "name": "Turmeric",
        "category": "Spices and Plantation Crops",
        "crop_type": "perennial",
        "seasons": ["Whole Year"],
        "soils": {
            "Loamy": 30,
            "Red Soil": 28,
            "Black Soil": 26,
            "Alluvial": 24,
            "Clay Soil": 10,
            "Sandy Soil": 8
        },
        "water_req": "Good water availability",
        "water_affinity": {
            "Good water availability": 28,
            "Moderate water availability": 24,
            "Low water availability": -40,
            "Rainfed": -60
        },
        "experience": ["Some experience", "Experienced"],
        "land_suitability": ["Small", "Medium"],
        "goals": ["Higher yield", "Balanced farming"],
        "rotation_group": "rhizome_spice",
        "soil_depletion": "high",
        "economics": {
            "estimated_cost_per_acre": "₹35,000 - ₹48,000",
            "estimated_gross_return": "₹90,000 - ₹145,000",
            "estimated_profit_per_acre": "₹52,000 - ₹97,000",
            "market_demand": "High domestic spice and international pharmaceutical curcumin demand"
        },
        "soil_guidance": "Deep, loose, fertile loams and red loams rich in organic matter. Raised bed cultivation prevents water stagnation.",
        "water_scheduling": "Demands 15-20 irrigations over its 8-9 month life cycle. Drip irrigation under organic mulch yields maximum finger rhizomes.",
        "risks": "Rhizome rot (Pythium) and shoot borer during monsoon.",
        "next_steps": "Use mother rhizome seed material treated with mancozeb, apply green leaf mulch, and earth up twice."
    },
    "Sugarcane": {
        "id": "sugarcane",
        "name": "Sugarcane",
        "category": "Commercial and Fibre Crops",
        "crop_type": "perennial",
        "seasons": ["Whole Year"],
        "soils": {
            "Black Soil": 30,
            "Clay Soil": 28,
            "Alluvial": 28,
            "Loamy": 26,
            "Red Soil": 16,
            "Sandy Soil": -40
        },
        "water_req": "Good water availability",
        "water_affinity": {
            "Good water availability": 30,
            "Moderate water availability": 10,
            "Low water availability": -80,
            "Rainfed": -90
        },
        "experience": ["Some experience", "Experienced"],
        "land_suitability": ["Large", "Medium"],
        "goals": ["Higher yield"],
        "rotation_group": "perennial_cash",
        "soil_depletion": "exhaustive",
        "economics": {
            "estimated_cost_per_acre": "₹38,000 - ₹50,000",
            "estimated_gross_return": "₹100,000 - ₹150,000",
            "estimated_profit_per_acre": "₹58,000 - ₹100,000",
            "market_demand": "Statutory Fair & Remunerative Price (FRP) with direct sugar mill tie-ups"
        },
        "soil_guidance": "Deep, fertile black clay and alluvial loams with pH 6.5-7.5. Deep trench planting improves lodging resistance and ratoon yield.",
        "water_scheduling": "Heavy water consumer (1800-2200 mm). Drip fertigation saves 45% water while improving cane girth and sucrose recovery.",
        "risks": "Early shoot borer, red rot, and woolly aphid in humid tracts.",
        "next_steps": "Plant dual-bud setts treated with carbendazim, apply trash mulching in inter-rows, and wrap canes to prevent lodging."
    },
    "Coconut": {
        "id": "coconut",
        "name": "Coconut",
        "category": "Spices and Plantation Crops",
        "crop_type": "plantation",
        "seasons": ["Whole Year"],
        "soils": {
            "Sandy Soil": 30,
            "Red Soil": 28,
            "Loamy": 26,
            "Alluvial": 24,
            "Clay Soil": 10,
            "Black Soil": 12
        },
        "water_req": "Good water availability",
        "water_affinity": {
            "Good water availability": 28,
            "Moderate water availability": 22,
            "Low water availability": -50,
            "Rainfed": -60
        },
        "experience": ["Some experience", "Experienced"],
        "land_suitability": ["Large", "Medium"],
        "goals": ["Higher yield", "Balanced farming"],
        "rotation_group": "plantation",
        "soil_depletion": "perennial",
        "economics": {
            "estimated_cost_per_acre": "₹20,000 - ₹28,000/yr",
            "estimated_gross_return": "₹60,000 - ₹95,000/yr",
            "estimated_profit_per_acre": "₹38,000 - ₹67,000/yr",
            "market_demand": "Continuous bi-monthly harvesting with high demand for fresh nuts, copra, and coir"
        },
        "soil_guidance": "Coastal sands, alluvial loams, and red laterites with deep water table. Requires well-aerated root zone.",
        "water_scheduling": "Mature palms need 40-50 liters/palm/day. Drip ring irrigation around basin maintains steady nut production.",
        "risks": "Rhinoceros beetle, red palm weevil, and stem bleeding disease.",
        "next_steps": "Place naphthalene balls in leaf axils to deter beetles, install root feeding micronutrient kits, and intercrop with cocoa or pepper."
    },
    "Arecanut": {
        "id": "arecanut",
        "name": "Arecanut",
        "category": "Spices and Plantation Crops",
        "crop_type": "plantation",
        "seasons": ["Whole Year"],
        "soils": {
            "Red Soil": 28,
            "Loamy": 28,
            "Black Soil": 20,
            "Alluvial": 20,
            "Clay Soil": 10,
            "Sandy Soil": 10
        },
        "water_req": "Good water availability",
        "water_affinity": {
            "Good water availability": 28,
            "Moderate water availability": 20,
            "Low water availability": -60,
            "Rainfed": -70
        },
        "experience": ["Experienced"],
        "land_suitability": ["Large", "Medium"],
        "goals": ["Higher yield"],
        "rotation_group": "plantation",
        "soil_depletion": "perennial",
        "economics": {
            "estimated_cost_per_acre": "₹30,000 - ₹42,000/yr",
            "estimated_gross_return": "₹90,000 - ₹160,000/yr",
            "estimated_profit_per_acre": "₹55,000 - ₹118,000/yr",
            "market_demand": "High-value commercial supari trade with established cooperative auction platforms"
        },
        "soil_guidance": "Deep, well-drained laterite and red loamy soils with adequate organic matter. Unsuited for waterlogged clay or drought-prone tracts.",
        "water_scheduling": "High moisture requirement during flowering and nut expansion. Basin irrigation or overhead misting needed during dry months.",
        "risks": "Koleroga (fruit rot / Mahali) during heavy monsoon and yellow leaf disease.",
        "next_steps": "Spray 1% Bordeaux mixture before monsoon onset, tie poly-cover protectors over bunches, and apply bio-digester slurry."
    },
    "Black pepper": {
        "id": "black_pepper",
        "name": "Black pepper",
        "category": "Spices and Plantation Crops",
        "crop_type": "plantation",
        "seasons": ["Whole Year"],
        "soils": {
            "Red Soil": 28,
            "Loamy": 28,
            "Clay Soil": 18,
            "Alluvial": 20,
            "Black Soil": 16,
            "Sandy Soil": 8
        },
        "water_req": "Good water availability",
        "water_affinity": {
            "Good water availability": 28,
            "Moderate water availability": 20,
            "Low water availability": -60,
            "Rainfed": -70
        },
        "experience": ["Experienced"],
        "land_suitability": ["Small", "Medium", "Large"],
        "goals": ["Higher yield"],
        "rotation_group": "plantation",
        "soil_depletion": "perennial",
        "economics": {
            "estimated_cost_per_acre": "₹22,000 - ₹32,000/yr",
            "estimated_gross_return": "₹70,000 - ₹120,000/yr",
            "estimated_profit_per_acre": "₹45,000 - ₹88,000/yr",
            "market_demand": "Premium domestic spice value and international commodity export demand"
        },
        "soil_guidance": "Humus-rich virgin red laterites and forest loams with pH 5.5-6.5. Excellent subsoil drainage essential.",
        "water_scheduling": "Thrives in high humidity with 1500-2500 mm rainfall. Supplementary irrigation during winter/summer dry spells preserves spike count.",
        "risks": "Quick wilt (Phytophthora capsici) and pollu beetle.",
        "next_steps": "Drench vine basins with potassium phosphonate or Trichoderma, and prune shade trees before monsoon."
    }
}
