"""
RythuCrop Centralized Multilingual Translation Registry
Provides verified native agricultural terminology across 9 Indian languages:
1. English (en)
2. Telugu (te)
3. Hindi (hi)
4. Tamil (ta)
5. Kannada (kn)
6. Malayalam (ml)
7. Marathi (mr)
8. Bengali (bn)
9. Odia (od)
"""

import json
from pathlib import Path

LANGUAGES = ["en", "te", "hi", "ta", "kn", "ml", "mr", "bn", "od"]

LANGUAGE_NAMES = {
    "en": "English",
    "te": "తెలుగు",
    "hi": "हिन्दी",
    "ta": "தமிழ்",
    "kn": "ಕನ್ನಡ",
    "ml": "മലയാളം",
    "mr": "मराठी",
    "bn": "বাংলা",
    "od": "ଓଡ଼ିଆ"
}

TRANSLATIONS = {
    "en": {
        # Nav
        "nav_home": "Home",
        "nav_planning": "Farm Planning",
        "nav_crop": "Crop Recommendation",
        "nav_yield": "Yield Prediction",
        "nav_advisory": "Smart Advisory",
        "nav_catalogue": "Crop Catalogue",
        "nav_market": "Market Prices",
        "nav_storage": "Storage Finder",
        "nav_alerts": "Price Alerts",
        "nav_about": "About",
        "nav_login": "Login / Register",
        "nav_logout": "Logout",
        "user_welcome": "Farmer Profile",

        # Hero
        "hero_badge": "SMART AGRICULTURE • PRECISION AGRI-TECH",
        "hero_title1": "Smart Farming.",
        "hero_title2": "Better Decisions.",
        "hero_desc": "RythuCrop equips Indian farmers with location-aware crop recommendation, leakage-free yield estimation, Agmarknet wholesale mandi prices, and verified cold storage discovery.",
        "hero_btn1": "Start Farm Planning",
        "hero_btn2": "Explore Market Prices",
        "hero_card_title": "DECISION SUPPORT",
        "hero_card_main": "From Soil to Mandi",
        "hero_card_desc": "Make informed agricultural choices backed by verified data and machine learning.",

        # Location Bar
        "loc_state": "State",
        "loc_district": "District",
        "loc_mandal": "Mandal / Tehsil",
        "loc_season": "Season",
        "loc_year": "Crop Year",
        "loc_apply": "Set Farm Location",

        # Farm Planning
        "plan_eyebrow": "FARM PLANNING",
        "plan_title": "Tell us about your farm",
        "plan_desc": "Select simple farming conditions. RythuCrop converts your inputs into practical crop options with water, soil, and risk considerations.",
        "land": "Land area (acres)",
        "season": "Season",
        "soil": "Soil type",
        "irrigation": "Water Availability",
        "goal": "Main Farming Goal",
        "experience": "Farming Experience",
        "generate_plan": "Generate Farm Plan",
        "plan_result_label": "RECOMMENDED CROPS",
        "plan_result_title": "Your recommendations will appear here",
        "plan_result_desc": "Enter your farm parameters and click Generate Farm Plan.",

        # Crop Recommendation
        "crop_eyebrow": "CROP RECOMMENDATION",
        "crop_title": "Find the right crop for your soil",
        "crop_desc": "Enter laboratory soil nutrient and climate readings for multi-class machine learning classification.",
        "nitrogen": "Nitrogen (N) kg/ha",
        "phosphorus": "Phosphorus (P) kg/ha",
        "potassium": "Potassium (K) kg/ha",
        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "soil_ph": "Soil pH",
        "rainfall": "Rainfall (mm)",
        "recommend_btn": "Recommend Crops",
        "recommended": "TOP RECOMMENDATIONS",
        "crop_result_desc": "Classified using trained Random Forest model with 51 crop varieties.",
        "crop_rank_1": "#1 Crop",
        "crop_rank_2": "#2 Crop",
        "crop_rank_3": "#3 Crop",

        # Yield Prediction
        "yield_eyebrow": "YIELD PREDICTION",
        "yield_title": "Estimate your pre-harvest yield",
        "yield_desc": "Location, crop, and year sensitive estimation trained without circular production leakage.",
        "yield_crop": "Crop",
        "crop_year": "Crop Year",
        "yield_season": "Season",
        "state": "State",
        "area": "Cultivated Area",
        "area_unit_label": "Unit",
        "unit_acres": "Acres",
        "unit_hectares": "Hectares",
        "annual_rainfall": "Annual Rainfall (mm, optional)",
        "fertilizer": "Fertilizer (kg, optional)",
        "pesticide": "Pesticide (kg, optional)",
        "yield_btn": "Predict Pre-Harvest Yield",
        "predicted": "ESTIMATED CROP YIELD",
        "yield_result_desc": "Derived from Indian Directorate of Economics & Statistics agricultural records.",
        "estimated_production_label": "Total Estimated Production",

        # Smart Advisory
        "advisory_eyebrow": "SMART ADVISORY",
        "advisory_title": "Crop Care & Agronomic Checklist",
        "advisory_desc": "Actionable agronomic advice covering water conservation, fertilizer management, and disease prevention.",
        "advisory_crop": "Select Crop",
        "advisory_priority": "Primary Priority",
        "get_advice": "Get Advisory Checklist",
        "advice_label": "AGRONOMIC ADVICE",
        "advice_title": "Choose your priority to view guidance",

        # Crop Catalogue
        "catalogue_eyebrow": "CROP CATALOGUE",
        "catalogue_title": "Explore Verified Agricultural Crops",
        "catalogue_desc": "Comprehensive directory of cereals, pulses, oilseeds, commercial crops, vegetables, fruits, and plantation crops.",
        "cat_filter_category": "Category",
        "cat_filter_season": "Season",
        "cat_search_placeholder": "Search crop by name...",
        "cat_all": "All",
        "badge_ml": "ML Recommended",
        "badge_yield": "Yield Model",
        "badge_mandi": "Mandi Prices",
        "badge_storage": "Storage Support",

        # Mandi Market Prices
        "mandi_eyebrow": "AGRICULTURAL MARKET PRICES",
        "mandi_title": "Wholesale Mandi Prices & Selling Guidance",
        "mandi_desc": "Official wholesale APMC market arrivals, modal rates, and break-even post-harvest calculations.",
        "mandi_select_crop": "Select Crop",
        "mandi_select_state": "Select State",
        "mandi_select_district": "Select District",
        "mandi_search_btn": "Check Mandi Prices",
        "mandi_modal_price": "Modal Price",
        "mandi_min_max": "Min – Max Price",
        "mandi_market_name": "Market / Mandi Yard",
        "mandi_arrival_date": "Reported Date",
        "mandi_trend": "30-Day Trend",
        "selling_guidance_title": "Post-Harvest Economic Guidance",
        "calc_selling_btn": "Calculate Selling vs Holding",
        "distance_km": "Distance to Mandi (km)",
        "holding_days": "Planned Storage Duration (days)",

        # Storage Finder
        "storage_eyebrow": "STORAGE & COLD CHAIN FINDER",
        "storage_title": "Locate Nearby Warehouses & Cold Storages",
        "storage_desc": "Locate WDRA registered grain warehouses and accredited cold chains to protect your harvest from distress sale.",
        "storage_filter_type": "Storage Type",
        "storage_all_types": "All Storage Types",
        "storage_grain": "Grain Warehouse (Ambient)",
        "storage_cold": "Cold Storage (Chilled / Controlled)",
        "storage_search_btn": "Find Storage Facilities",
        "storage_capacity": "Capacity",
        "storage_status": "Status",
        "storage_contact": "Contact",

        # Price Alerts
        "alert_eyebrow": "PRICE ALERTS & NOTIFICATIONS",
        "alert_title": "Subscribe to Mandi Price Notifications",
        "alert_desc": "Get notified on your mobile number when market prices cross your target threshold.",
        "alert_mobile": "Mobile Number",
        "alert_target_price": "Target Price (₹/Quintal)",
        "alert_condition": "Notify when price is",
        "cond_above": "Equal to or Above",
        "cond_below": "Equal to or Below",
        "alert_subscribe_btn": "Subscribe to Alert",
        "alert_my_subscriptions": "My Active Subscriptions",
        "alert_no_active": "No active subscriptions found for this number.",

        # Auth Modal
        "auth_modal_title": "Farmer Mobile Login",
        "auth_modal_desc": "Login with your mobile number to save farm plans and subscribe to market alerts.",
        "auth_mobile_label": "10-Digit Mobile Number",
        "auth_request_otp": "Send OTP",
        "auth_otp_label": "Enter 6-Digit OTP",
        "auth_verify_btn": "Verify & Login",
        "auth_dev_notice": "Development Mode Active: OTP is shown directly in the prompt or console.",

        # About
        "about_eyebrow": "ABOUT RYTHUCROP",
        "about_title": "Transparent Technology for Indian Agriculture",
        "about_desc": "RythuCrop bridges open agricultural data, scientific agronomy, and machine learning to empower farmers with verifiable decisions.",
        "about_ml": "Machine Learning",
        "about_ml_desc": "Trained without target leakage using verified historical agricultural datasets.",
        "about_farmer": "Farmer Centric",
        "about_farmer_desc": "Simple native interfaces, clear units, and honest transparency without false claims.",
        "about_mobile": "Multi-Device & Multilingual",
        "about_mobile_desc": "Fully accessible across 9 Indian languages on mobile, tablet, and desktop.",
        "footer_desc": "RythuCrop — Precision Agricultural Decision Support for Indian Farmers.",

        # Dropdown Options
        "season_kharif": "Kharif (Monsoon)",
        "season_rabi": "Rabi (Winter)",
        "season_summer": "Summer (Zaid)",
        "season_whole_year": "Whole Year",
        "soil_loamy": "Loamy Soil",
        "soil_black": "Black Soil",
        "soil_red": "Red Soil",
        "soil_clay": "Clay Soil",
        "soil_sandy": "Sandy Soil",
        "soil_alluvial": "Alluvial Soil",
        "water_good": "Good water availability (Canal / Tube well)",
        "water_moderate": "Moderate water availability",
        "water_low": "Low water availability (Rainfed)",
        "water_rainfed": "Rainfed (No assured irrigation)",
        "goal_yield": "Higher yield",
        "goal_water": "Lower water use",
        "goal_cost": "Lower input cost",
        "goal_balanced": "Balanced farming",
        "exp_beginner": "Beginner (1-2 years)",
        "exp_some": "Some experience (3-5 years)",
        "exp_experienced": "Experienced (5+ years)",
        "priority_water": "Water saving & irrigation",
        "priority_fertilizer": "Fertilizer & nutrient management",
        "priority_pest": "Pest & disease prevention",
        "priority_harvest": "Harvesting & post-harvest care",

        # General
        "calculating": "Processing…",
        "prediction_failed": "Prediction failed",
        "server_error": "Server error. Please check your connection.",
        "unit_tonnes_ha": "tonnes/ha",
        "unit_quintals_acre": "quintals/acre",
        "reasons_label": "Key Reasons:",
        "soil_label": "Soil Guidance:",
        "water_label": "Water Scheduling:",
        "risks_label": "Assumptions & Risks:",
        "next_steps_label": "Recommended Actions:"
    },

    "te": {
        # Nav
        "nav_home": "హోమ్",
        "nav_planning": "వ్యవసాయ ప్రణాళిక",
        "nav_crop": "పంట సిఫార్సు",
        "nav_yield": "దిగుబడి అంచనా",
        "nav_advisory": "స్మార్ట్ సలహా",
        "nav_catalogue": "పంటల జాబితా",
        "nav_market": "మార్కెట్ ధరలు",
        "nav_storage": "గోదాముల సమాచారం",
        "nav_alerts": "ధర హెచ్చరికలు",
        "nav_about": "మా గురించి",
        "nav_login": "లాగిన్ / నమోదు",
        "nav_logout": "లాగౌట్",
        "user_welcome": "రైతు ప్రొఫైల్",

        # Hero
        "hero_badge": "స్మార్ట్ వ్యవసాయం • ప్రిసిషన్ అగ్రి-టెక్",
        "hero_title1": "స్మార్ట్ వ్యవసాయం.",
        "hero_title2": "మెరుగైన నిర్ణయాలు.",
        "hero_desc": "RythuCrop భారతీయ రైతులకు ప్రాంతీయ పంట సిఫార్సు, ఖచ్చితమైన దిగుబడి అంచనా, అగ్మార్క్‌నెట్ మార్కెట్ ధరలు మరియు శీతల గిడ్డంగుల సమాచారాన్ని అందిస్తుంది.",
        "hero_btn1": "వ్యవసాయ ప్రణాళిక ప్రారంభించండి",
        "hero_btn2": "మార్కెట్ ధరలను చూడండి",
        "hero_card_title": "నిర్ణయ సహాయం",
        "hero_card_main": "నేల నుండి మార్కెట్ వరకు",
        "hero_card_desc": "శాస్త్రీయ డేటా మరియు మెషిన్ లెర్నింగ్ ఆధారంగా సరైన నిర్ణయాలు తీసుకోండి.",

        # Location Bar
        "loc_state": "రాష్ట్రం",
        "loc_district": "జిల్లా",
        "loc_mandal": "మండలం / తాలూకా",
        "loc_season": "సీజన్",
        "loc_year": "పంట సంవత్సరం",
        "loc_apply": "ప్రాంతాన్ని ఎంచుకోండి",

        # Farm Planning
        "plan_eyebrow": "వ్యవసాయ ప్రణాళిక",
        "plan_title": "మీ పొలం గురించి చెప్పండి",
        "plan_desc": "మీ పొలం వివరాలను ఎంచుకోండి. RythuCrop నీరు, నేల మరియు ప్రమాదాల వివరాలతో ఆచరణాత్మక పంట ప్రణాళికను అందిస్తుంది.",
        "land": "భూమి విస్తీర్ణం (ఎకరాలు)",
        "season": "సీజన్",
        "soil": "నేల రకం",
        "irrigation": "నీటి లభ్యత",
        "goal": "ప్రధాన లక్ష్యం",
        "experience": "వ్యవసాయ అనుభవం",
        "generate_plan": "నా ప్రణాళిక తయారు చేయండి",
        "plan_result_label": "సిఫార్సు చేసిన పంటలు",
        "plan_result_title": "మీ సిఫార్సులు ఇక్కడ కనిపిస్తాయి",
        "plan_result_desc": "వివరాలను నమోదు చేసి ప్రణాళిక బటన్‌పై నొక్కండి.",

        # Crop Recommendation
        "crop_eyebrow": "పంట సిఫార్సు",
        "crop_title": "మీ నేలకు సరిపోయే పంటను కనుగొనండి",
        "crop_desc": "ఖచ్చితమైన పంట సిఫార్సు కోసం నేల పోషకాలు మరియు వాతావరణ విలువలను నమోదు చేయండి.",
        "nitrogen": "నత్రజని (N) kg/ha",
        "phosphorus": "భాస్వరం (P) kg/ha",
        "potassium": "పొటాషియం (K) kg/ha",
        "temperature": "ఉష్ణోగ్రత (°C)",
        "humidity": "తేమ శాతం (%)",
        "soil_ph": "నేల pH",
        "rainfall": "వర్షపాతం (mm)",
        "recommend_btn": "పంట సిఫార్సు పొందండి",
        "recommended": "అగ్ర సిఫార్సులు",
        "crop_result_desc": "శిక్షణ పొందిన 51 పంటల ర్యాండమ్ ఫారెస్ట్ మోడల్ ఆధారంగా రూపొందించబడింది.",
        "crop_rank_1": "#1 పంట",
        "crop_rank_2": "#2 పంట",
        "crop_rank_3": "#3 పంట",

        # Yield Prediction
        "yield_eyebrow": "దిగుబడి అంచనా",
        "yield_title": "కోతకు ముందే దిగుబడిని అంచనా వేయండి",
        "yield_desc": "రాష్ట్రం, పంట, విస్తీర్ణం మరియు వర్షపాతం ఆధారంగా నిజాయితీ గల దిగుబడి గణన.",
        "yield_crop": "పంట",
        "crop_year": "పంట సంవత్సరం",
        "yield_season": "సీజన్",
        "state": "రాష్ట్రం",
        "area": "సాగు విస్తీర్ణం",
        "area_unit_label": "యూనిట్",
        "unit_acres": "ఎకరాలు",
        "unit_hectares": "హెక్టార్లు",
        "annual_rainfall": "వార్షిక వర్షపాతం (mm, ఐచ్ఛికం)",
        "fertilizer": "ఎరువుల వినియోగం (kg, ఐచ్ఛికం)",
        "pesticide": "పురుగుమందు (kg, ఐచ్ఛికం)",
        "yield_btn": "దిగుబడిని అంచనా వేయండి",
        "predicted": "అంచనా పంట దిగుబడి",
        "yield_result_desc": "భారత ఆర్థిక మరియు గణాంకాల డైరెక్టరేట్ రికార్డుల ఆధారంగా.",
        "estimated_production_label": "మొత్తం అంచనా ఉత్పత్తి",

        # Smart Advisory
        "advisory_eyebrow": "స్మార్ట్ సలహా",
        "advisory_title": "పంట సంరక్షణ & వ్యవసాయ సూచనలు",
        "advisory_desc": "నీటి యాజమాన్యం, ఎరువుల సమతుల్యత మరియు తెగుళ్ళ నివారణపై ఆచరణాత్మక సలహాలు.",
        "advisory_crop": "పంటను ఎంచుకోండి",
        "advisory_priority": "ప్రధాన అవసరం",
        "get_advice": "సలహా జాబితాను పొందండి",
        "advice_label": "వ్యవసాయ సలహా",
        "advice_title": "మార్గదర్శకత్వం కోసం ప్రాధాన్యతను ఎంచుకోండి",

        # Crop Catalogue
        "catalogue_eyebrow": "పంటల జాబితా",
        "catalogue_title": "ధృవీకరించబడిన పంటల వివరాలు",
        "catalogue_desc": "ధాన్యాలు, పప్పుధాన్యాలు, నూనెగింజలు, వాణిజ్య పంటలు, కూరగాయలు మరియు పండ్ల సమగ్ర సమాచారం.",
        "cat_filter_category": "వర్గం",
        "cat_filter_season": "సీజన్",
        "cat_search_placeholder": "పంట పేరుతో వెతకండి...",
        "cat_all": "అన్నీ",
        "badge_ml": "ML సిఫార్సు కలదు",
        "badge_yield": "దిగుబడి మోడల్",
        "badge_mandi": "మార్కెట్ ధరలు",
        "badge_storage": "నిల్వ సమాచారం",

        # Mandi Market Prices
        "mandi_eyebrow": "వ్యవసాయ మార్కెట్ ధరలు",
        "mandi_title": "మార్కెట్ ధరలు & అమ్మకపు సలహాలు",
        "mandi_desc": "అధికారిక వ్యవసాయ మార్కెట్ ధరలు మరియు రవాణా, నిల్వ ఖర్చుల లెక్కింపు.",
        "mandi_select_crop": "పంటను ఎంచుకోండి",
        "mandi_select_state": "రాష్ట్రం",
        "mandi_select_district": "జిల్లా",
        "mandi_search_btn": "మార్కెట్ ధరలు చూడండి",
        "mandi_modal_price": "మోడల్ ధర",
        "mandi_min_max": "కనిష్ట – గరిష్ట ధర",
        "mandi_market_name": "మార్కెట్ యార్డ్",
        "mandi_arrival_date": "నివేదించిన తేదీ",
        "mandi_trend": "30 రోజుల ధోరణి",
        "selling_guidance_title": "అమ్మకం vs నిల్వ విశ్లేషణ",
        "calc_selling_btn": "అమ్మకపు లాభనష్టాలు లెక్కించండి",
        "distance_km": "మార్కెట్‌కు దూరం (కి.మీ)",
        "holding_days": "నిల్వ చేయాలనుకున్న రోజులు",

        # Storage Finder
        "storage_eyebrow": "గిడ్డంగులు & శీతల నిల్వ సమాచారం",
        "storage_title": "సమీప గోదాములు మరియు కోల్డ్ స్టోరేజీలు",
        "storage_desc": "ధాన్యం పాడవకుండా సరైన ధరకు అమ్ముకోవడానికి గుర్తింపు పొందిన గిడ్డంగులను కనుగొనండి.",
        "storage_filter_type": "నిల్వ రకం",
        "storage_all_types": "అన్ని రకాల నిల్వలు",
        "storage_grain": "ధాన్యం గిడ్డంగి (సాధారణ)",
        "storage_cold": "శీతల నిల్వ (కోల్డ్ స్టోరేజ్)",
        "storage_search_btn": "సౌకర్యాలను కనుగొనండి",
        "storage_capacity": "సామర్థ్యం",
        "storage_status": "పరిస్థితి",
        "storage_contact": "సంప్రదించండి",

        # Price Alerts
        "alert_eyebrow": "ధర హెచ్చరికలు",
        "alert_title": "మార్కెట్ ధరల అలర్ట్‌లను పొందండి",
        "alert_desc": "మీరు కోరుకున్న ధరకు మార్కెట్ చేరినప్పుడు మొబైల్ నోటిఫికేషన్ పొందండి.",
        "alert_mobile": "మొబైల్ నంబర్",
        "alert_target_price": "లక్ష్య ధర (₹/క్వింటాల్)",
        "alert_condition": "ధర ఇలా ఉన్నప్పుడు",
        "cond_above": "సమానంగా లేదా అంతకంటే ఎక్కువ",
        "cond_below": "సమానంగా లేదా అంతకంటే తక్కువ",
        "alert_subscribe_btn": "అలర్ట్‌ను నమోదు చేసుకోండి",
        "alert_my_subscriptions": "నా యాక్టివ్ అలర్ట్‌లు",
        "alert_no_active": "ఈ నంబర్‌కు ఎలాంటి అలర్ట్‌లు లేవు.",

        # Auth Modal
        "auth_modal_title": "రైతు మొబైల్ లాగిన్",
        "auth_modal_desc": "పంట ప్రణాళికలను భద్రపరచడానికి మరియు ధర హెచ్చరికలను పొందడానికి లాగిన్ అవ్వండి.",
        "auth_mobile_label": "10 అంకెల మొబైల్ నంబర్",
        "auth_request_otp": "OTP పంపండి",
        "auth_otp_label": "6 అంకెల OTP నమోదు చేయండి",
        "auth_verify_btn": "ధృవీకరించి లాగిన్ అవ్వండి",
        "auth_dev_notice": "డెవలప్‌మెంట్ మోడ్ యాక్టివ్‌గా ఉంది: OTP స్క్రీన్‌పై కనిపిస్తుంది.",

        # About
        "about_eyebrow": "RYTHUCROP గురించి",
        "about_title": "భారతీయ వ్యవసాయం కోసం పారదర్శక సాంకేతికత",
        "about_desc": "రైతులకు నమ్మకమైన నిర్ణయాలు అందించడానికి వ్యవసాయ డేటా మరియు శాస్త్రీయ మోడళ్లను కలుపుతుంది.",
        "about_ml": "మెషిన్ లెర్నింగ్",
        "about_ml_desc": "డేటా లీకేజ్ లేకుండా అధికారిక గణాంకాలతో శిక్షణ పొందిన మోడల్స్.",
        "about_farmer": "రైతే ప్రాధాన్యత",
        "about_farmer_desc": "సులభమైన స్థానిక భాష మరియు స్పష్టమైన మార్గదర్శకత్వం.",
        "about_mobile": "అన్ని పరికరాల్లో & బహుభాషా సౌలభ్యం",
        "about_mobile_desc": "మొబైల్, టాబ్లెట్ మరియు కంప్యూటర్లలో 9 భారతీయ భాషల్లో అందుబాటులో ఉంది.",
        "footer_desc": "RythuCrop — భారతీయ రైతుల కోసం స్మార్ట్ వ్యవసాయ నిర్ణయ వేదిక.",

        # Dropdown Options
        "season_kharif": "ఖరీఫ్ (వర్షాకాలం)",
        "season_rabi": "రబీ (శీతాకాలం)",
        "season_summer": "వేసవి (జాయెద్)",
        "season_whole_year": "సంవత్సరం పొడవునా",
        "soil_loamy": "ఒండ్రు నేల",
        "soil_black": "నల్లరేగడి నేల",
        "soil_red": "ఎర్ర నేల",
        "soil_clay": "బంకమట్టి నేల",
        "soil_sandy": "ఇసుక నేల",
        "soil_alluvial": "వరద ఒండ్రు నేల",
        "water_good": "మంచి నీటి సౌకర్యం (కాలువ / బోర్)",
        "water_moderate": "మధ్యస్థ నీటి సౌకర్యం",
        "water_low": "తక్కువ నీటి లభ్యత (వర్షాధారం)",
        "water_rainfed": "పూర్తి వర్షాధారం (నీటి పారుదల లేదు)",
        "goal_yield": "అధిక దిగుబడి",
        "goal_water": "తక్కువ నీటి వినియోగం",
        "goal_cost": "తక్కువ పెట్టుబడి ఖర్చు",
        "goal_balanced": "సమతుల్య వ్యవసాయం",
        "exp_beginner": "ప్రారంభ రైతు (1-2 సంవత్సరాలు)",
        "exp_some": "కొంత అనుభవం (3-5 సంవత్సరాలు)",
        "exp_experienced": "అనుభవజ్ఞుడు (5+ సంవత్సరాలు)",
        "priority_water": "నీటి పొదుపు & యాజమాన్యం",
        "priority_fertilizer": "ఎరువులు & పోషక నిర్వహణ",
        "priority_pest": "తెగుళ్ళు & పురుగుల నివారణ",
        "priority_harvest": "కోత & కోతానంతర సంరక్షణ",

        # General
        "calculating": "వివరాలు ప్రాసెస్ అవుతున్నాయి…",
        "prediction_failed": "అంచనా విఫలమైంది",
        "server_error": "సర్వర్ లోపం ఏర్పడింది. దయచేసి మళ్ళీ ప్రయత్నించండి.",
        "unit_tonnes_ha": "టన్నులు/హెక్టార్",
        "unit_quintals_acre": "క్వింటాళ్ళు/ఎకరం",
        "reasons_label": "ముఖ్య కారణాలు:",
        "soil_label": "నేల సలహా:",
        "water_label": "నీటి యాజమాన్యం:",
        "risks_label": "అనుమానాలు & ప్రమాదాలు:",
        "next_steps_label": "సిఫార్సు చేసిన చర్యలు:"
    },

    "hi": {
        # Nav
        "nav_home": "होम",
        "nav_planning": "कृषि योजना",
        "nav_crop": "फसल सुझाव",
        "nav_yield": "उपज अनुमान",
        "nav_advisory": "स्मार्ट सलाह",
        "nav_catalogue": "फसल सूची",
        "nav_market": "मंडी भाव",
        "nav_storage": "भंडारण खोजें",
        "nav_alerts": "मूल्य अलर्ट",
        "nav_about": "हमारे बारे में",
        "nav_login": "लॉगिन / पंजीकरण",
        "nav_logout": "लॉगआउट",
        "user_welcome": "किसान प्रोफ़ाइल",

        # Hero
        "hero_badge": "स्मार्ट कृषि • सटीक कृषि तकनीक",
        "hero_title1": "स्मार्ट खेती.",
        "hero_title2": "बेहतर फैसले.",
        "hero_desc": "RythuCrop भारतीय किसानों को स्थान-आधारित फसल सुझाव, सटीक उपज अनुमान, एगमार्कनेट थोक मंडी भाव और सत्यापित शीत भंडारण की जानकारी प्रदान करता है।",
        "hero_btn1": "कृषि योजना बनाएं",
        "hero_btn2": "मंडी भाव देखें",
        "hero_card_title": "निर्णय सहायता",
        "hero_card_main": "मिट्टी से मंडी तक",
        "hero_card_desc": "सत्यापित डेटा और मशीन लर्निंग के आधार पर सही निर्णय लें।",

        # Location Bar
        "loc_state": "राज्य",
        "loc_district": "ज़िला",
        "loc_mandal": "तहसील / मंडल",
        "loc_season": "मौसम",
        "loc_year": "फसल वर्ष",
        "loc_apply": "स्थान सेट करें",

        # Farm Planning
        "plan_eyebrow": "कृषि योजना",
        "plan_title": "अपने खेत के बारे में बताएं",
        "plan_desc": "सरल विकल्प चुनें। RythuCrop पानी, मिट्टी और जोखिम के विचारों के साथ व्यावहारिक फसल योजना तैयार करता है।",
        "land": "भूमि क्षेत्र (एकड़)",
        "season": "मौसम",
        "soil": "मिट्टी का प्रकार",
        "irrigation": "जल उपलब्धता",
        "goal": "मुख्य लक्ष्य",
        "experience": "कृषि अनुभव",
        "generate_plan": "मेरी योजना बनाएं",
        "plan_result_label": "सुझाई गई फसलें",
        "plan_result_title": "आपके सुझाव यहां दिखाई देंगे",
        "plan_result_desc": "आवश्यकताएं चुनकर योजना बनाएं पर क्लिक करें।",

        # Crop Recommendation
        "crop_eyebrow": "फसल सुझाव",
        "crop_title": "अपनी मिट्टी के लिए सही फसल खोजें",
        "crop_desc": "मशीन लर्निंग वर्गीकरण के लिए मिट्टी के पोषक तत्व और मौसम की जानकारी दर्ज करें।",
        "nitrogen": "नाइट्रोजन (N) kg/ha",
        "phosphorus": "फॉस्फोरस (P) kg/ha",
        "potassium": "पोटैशियम (K) kg/ha",
        "temperature": "तापमान (°C)",
        "humidity": "नमी (%)",
        "soil_ph": "मिट्टी pH",
        "rainfall": "वर्षा (mm)",
        "recommend_btn": "फसल सुझाएं",
        "recommended": "शीर्ष फसल सुझाव",
        "crop_result_desc": "51 फसलों पर प्रशिक्षित रैंडम फॉरेस्ट मॉडल द्वारा वर्गीकृत।",
        "crop_rank_1": "#1 फसल",
        "crop_rank_2": "#2 फसल",
        "crop_rank_3": "#3 फसल",

        # Yield Prediction
        "yield_eyebrow": "उपज अनुमान",
        "yield_title": "कटाई से पहले उपज का अनुमान लगाएं",
        "yield_desc": "राज्य, फसल, क्षेत्रफल और वर्षा पर आधारित सटीक उपज गणना।",
        "yield_crop": "फसल",
        "crop_year": "फसल वर्ष",
        "yield_season": "मौसम",
        "state": "राज्य",
        "area": "बुवाई क्षेत्र",
        "area_unit_label": "इकाई",
        "unit_acres": "एकड़",
        "unit_hectares": "हेक्टेयर",
        "annual_rainfall": "वार्षिक वर्षा (mm, वैकल्पिक)",
        "fertilizer": "उर्वरक उपयोग (kg, वैकल्पिक)",
        "pesticide": "कीटनाशक (kg, वैकल्पिक)",
        "yield_btn": "उपज का अनुमान लगाएं",
        "predicted": "अनुमानित फसल उपज",
        "yield_result_desc": "अर्थशास्त्र और सांख्यिकी निदेशालय के आधिकारिक आंकड़ों पर आधारित।",
        "estimated_production_label": "कुल अनुमानित उत्पादन",

        # Smart Advisory
        "advisory_eyebrow": "स्मार्ट सलाह",
        "advisory_title": "फसल देखभाल और कृषि कार्य सूची",
        "advisory_desc": "सिंचाई, पोषण प्रबंधन और कीट नियंत्रण पर व्यावहारिक दिशा-निर्देश।",
        "advisory_crop": "फसल चुनें",
        "advisory_priority": "प्राथमिकता",
        "get_advice": "सलाह सूची देखें",
        "advice_label": "कृषि सलाह",
        "advice_title": "मार्गदर्शन देखने के लिए प्राथमिकता चुनें",

        # Crop Catalogue
        "catalogue_eyebrow": "फसल सूची",
        "catalogue_title": "सत्यापित कृषि फसलों की सूची",
        "catalogue_desc": "अनाज, दलहन, तिलहन, वाणिज्यिक फसलें, सब्जियां और फलों की विस्तृत जानकारी।",
        "cat_filter_category": "श्रेणी",
        "cat_filter_season": "मौसम",
        "cat_search_placeholder": "फसल के नाम से खोजें...",
        "cat_all": "सभी",
        "badge_ml": "ML सिफारिश उपलब्ध",
        "badge_yield": "उपज मॉडल",
        "badge_mandi": "मंडी भाव",
        "badge_storage": "भंडारण सुविधा",

        # Mandi Market Prices
        "mandi_eyebrow": "कृषि मंडी भाव",
        "mandi_title": "थोक मंडी भाव और बिक्री मार्गदर्शन",
        "mandi_desc": "आधिकारिक एपीएमसी थोक भाव और कटाई के बाद बिक्री बनाम भंडारण का विश्लेषण।",
        "mandi_select_crop": "फसल चुनें",
        "mandi_select_state": "राज्य",
        "mandi_select_district": "ज़िला",
        "mandi_search_btn": "मंडी भाव देखें",
        "mandi_modal_price": "मॉडल भाव",
        "mandi_min_max": "न्यूनतम – अधिकतम भाव",
        "mandi_market_name": "मंडी यार्ड",
        "mandi_arrival_date": "रिपोर्टिंग तिथि",
        "mandi_trend": "30 दिन का रुझान",
        "selling_guidance_title": "बिक्री बनाम भंडारण विश्लेषण",
        "calc_selling_btn": "लाभ-हानि की गणना करें",
        "distance_km": "मंडी की दूरी (किमी)",
        "holding_days": "भंडारण की अवधि (दिन)",

        # Storage Finder
        "storage_eyebrow": "गोदाम और कोल्ड स्टोरेज खोजें",
        "storage_title": "निकटतम अनाज गोदाम और शीतगृह",
        "storage_desc": "फसल को खराब होने से बचाने और सही दाम पाने के लिए मान्यता प्राप्त गोदाम खोजें।",
        "storage_filter_type": "भंडारण प्रकार",
        "storage_all_types": "सभी प्रकार",
        "storage_grain": "अनाज गोदाम (सामान्य)",
        "storage_cold": "शीतगृह (कोल्ड स्टोरेज)",
        "storage_search_btn": "गोदाम खोजें",
        "storage_capacity": "क्षमता",
        "storage_status": "स्थिति",
        "storage_contact": "संपर्क",

        # Price Alerts
        "alert_eyebrow": "मूल्य अलर्ट",
        "alert_title": "मंडी मूल्य सूचना प्राप्त करें",
        "alert_desc": "जब मंडी का भाव आपके लक्षित मूल्य पर पहुंचे तो मोबाइल पर एसएमएस पाएं।",
        "alert_mobile": "मोबाइल नंबर",
        "alert_target_price": "लक्षित मूल्य (₹/क्विंटल)",
        "alert_condition": "जब मूल्य हो",
        "cond_above": "बराबर या अधिक",
        "cond_below": "बराबर या कम",
        "alert_subscribe_btn": "अलर्ट सब्सक्राइब करें",
        "alert_my_subscriptions": "मेरे सक्रिय अलर्ट",
        "alert_no_active": "इस नंबर के लिए कोई सक्रिय अलर्ट नहीं मिला।",

        # Auth Modal
        "auth_modal_title": "किसान मोबाइल लॉगिन",
        "auth_modal_desc": "कृषि योजनाएं सहेजने और मूल्य अलर्ट प्राप्त करने के लिए लॉगिन करें।",
        "auth_mobile_label": "10 अंकों का मोबाइल नंबर",
        "auth_request_otp": "ओटीपी भेजें",
        "auth_otp_label": "6 अंकों का ओटीपी दर्ज करें",
        "auth_verify_btn": "सत्यापित करें और लॉगिन करें",
        "auth_dev_notice": "डेवलपमेंट मोड सक्रिय: ओटीपी स्क्रीन पर प्रदर्शित है।",

        # About
        "about_eyebrow": "RYTHUCROP के बारे में",
        "about_title": "भारतीय कृषि के लिए पारदर्शी तकनीक",
        "about_desc": "किसानों को भरोसेमंद निर्णय लेने के लिए कृषि डेटा और एमएल मॉडल को जोड़ता है।",
        "about_ml": "मशीन लर्निंग",
        "about_ml_desc": "बिना डेटा लीकेज के आधिकारिक आंकड़ों से प्रशिक्षित मॉडल।",
        "about_farmer": "किसान प्रथम",
        "about_farmer_desc": "सरल स्थानीय भाषा और स्पष्ट मार्गदर्शन।",
        "about_mobile": "सभी उपकरणों पर और बहुभाषी",
        "about_mobile_desc": "मोबाइल, टैबलेट और कंप्यूटर पर 9 भारतीय भाषाओं में उपलब्ध।",
        "footer_desc": "RythuCrop — भारतीय किसानों के लिए सटीक कृषि निर्णय सहायता प्रणाली।",

        # Dropdown Options
        "season_kharif": "खरीफ (मानसून)",
        "season_rabi": "रबी (सर्दियां)",
        "season_summer": "जायद (गर्मी)",
        "season_whole_year": "पूरे साल",
        "soil_loamy": "दोमट मिट्टी",
        "soil_black": "काली मिट्टी",
        "soil_red": "लाल मिट्टी",
        "soil_clay": "चिकनी मिट्टी",
        "soil_sandy": "बलुई मिट्टी",
        "soil_alluvial": "जलोढ़ मिट्टी",
        "water_good": "अच्छी जल उपलब्धता (नहर / नलकूप)",
        "water_moderate": "मध्यम जल उपलब्धता",
        "water_low": "कम जल उपलब्धता (वर्षा आधारित)",
        "water_rainfed": "पूर्णतः वर्षा आधारित (सिंचाई नहीं)",
        "goal_yield": "अधिक उपज",
        "goal_water": "कम पानी का उपयोग",
        "goal_cost": "कम लागत",
        "goal_balanced": "संतुलित खेती",
        "exp_beginner": "शुरुआती किसान (1-2 वर्ष)",
        "exp_some": "कुछ अनुभव (3-5 वर्ष)",
        "exp_experienced": "अनुभवी किसान (5+ वर्ष)",
        "priority_water": "जल संरक्षण और सिंचाई",
        "priority_fertilizer": "उर्वरक एवं पोषण प्रबंधन",
        "priority_pest": "कीट एवं रोग नियंत्रण",
        "priority_harvest": "कटाई एवं कटाई उपरांत प्रबंधन",

        # General
        "calculating": "प्रक्रिया जारी है…",
        "prediction_failed": "अनुमान विफल हुआ",
        "server_error": "सर्वर त्रुटि हुई। कृपया पुनः प्रयास करें।",
        "unit_tonnes_ha": "टन/हेक्टेयर",
        "unit_quintals_acre": "क्विंटल/एकड़",
        "reasons_label": "मुख्य कारण:",
        "soil_label": "मिट्टी संबंधी सलाह:",
        "water_label": "सिंचाई प्रबंधन:",
        "risks_label": "मान्यताएं एवं जोखिम:",
        "next_steps_label": "सुझाए गए कदम:"
    }
}

# Add Tamil, Kannada, Malayalam, Marathi, Bengali, Odia programmatically with full translations
TA_BASE = {
    "nav_home": "முகப்பு", "nav_planning": "விவசாய திட்டம்", "nav_crop": "பயிர் பரிந்துரை", "nav_yield": "மகசூல் கணிப்பு", "nav_advisory": "ஸ்மார்ட் ஆலோசனை", "nav_catalogue": "பயிர் பட்டியல்", "nav_market": "சந்தை விலைகள்", "nav_storage": "சேமிப்பு கிடங்குகள்", "nav_alerts": "விலை அறிவிப்புகள்", "nav_about": "பற்றி", "nav_login": "உள்நுழைக / பதிவு", "nav_logout": "வெளியேறு", "user_welcome": "விவசாயி சுயவிவரம்",
    "hero_badge": "ஸ்மார்ட் விவசாயம் • துல்லிய வேளாண் தொழில்நுட்பம்", "hero_title1": "ஸ்மார்ட் விவசாயம்.", "hero_title2": "சிறந்த முடிவுகள்.", "hero_desc": "RythuCrop இந்திய விவசாயிகளுக்கு வட்டார பயிர் பரிந்துரை, மகசூல் மதிப்பீடு, எக்மார்க்நெட் சந்தை விலைகள் மற்றும் குளிர்சாதன கிடங்கு தகவல்களை வழங்குகிறது.", "hero_btn1": "திட்டம் தொடங்குக", "hero_btn2": "சந்தை விலை பார்க்க", "hero_card_title": "முடிவு ஆதரவு", "hero_card_main": "மண்ணிலிருந்து சந்தை வரை", "hero_card_desc": "நிரூபிக்கப்பட்ட தரவு மற்றும் இயந்திர கற்றல் மூலம் சரியான முடிவுகளை எடுங்கள்.",
    "loc_state": "மாநிலம்", "loc_district": "மாவட்டம்", "loc_mandal": "வட்டம் / தாலுகா", "loc_season": "பருவம்", "loc_year": "பயிர் ஆண்டு", "loc_apply": "இருப்பிடத்தை அமைக்கவும்",
    "plan_eyebrow": "விவசாய திட்டம்", "plan_title": "உங்கள் பண்ணையைப் பற்றி கூறுங்கள்", "plan_desc": "எளிய விருப்பங்களைத் தேர்வு செய்யுங்கள். RythuCrop நீர், மண் மற்றும் இடர் காரணிகளுடன் நடைமுறை திட்டத்தை வழங்குகிறது.",
    "land": "நிலப்பரப்பு (ஏக்கர்)", "season": "பருவம்", "soil": "மண் வகை", "irrigation": "நீர் இருப்பு", "goal": "முக்கிய நோக்கம்", "experience": "விவசாய அனுபவம்", "generate_plan": "என் திட்டத்தை உருவாக்கு", "plan_result_label": "பரிந்துரைக்கப்பட்ட பயிர்கள்", "plan_result_title": "பரிந்துரைகள் இங்கே தோன்றும்", "plan_result_desc": "தேவைகளை உள்ளிட்டு திட்டத்தை உருவாக்குங்கள்.",
    "crop_eyebrow": "பயிர் பரிந்துரை", "crop_title": "உங்கள் மண்ணுக்கு ஏற்ற பயிரை கண்டறியுங்கள்", "crop_desc": "மண் சத்துக்கள் மற்றும் காலநிலை அளவீடுகளை உள்ளிட்டு பயிர் பரிந்துரையைப் பெறுங்கள்.",
    "nitrogen": "நைட்ரஜன் (N) kg/ha", "phosphorus": "பாஸ்பரஸ் (P) kg/ha", "potassium": "பொட்டாசியம் (K) kg/ha", "temperature": "வெப்பநிலை (°C)", "humidity": "ஈரப்பதம் (%)", "soil_ph": "மண் pH", "rainfall": "மழைப்பொழிவு (mm)", "recommend_btn": "பயிரை பரிந்துரைக்கவும்", "recommended": "முக்கிய பரிந்துரைகள்", "crop_result_desc": "51 பயிர்களுக்கான இயந்திர கற்றல் மாதிரியின் மூலம் கணிக்கப்பட்டது.", "crop_rank_1": "#1 பயிர்", "crop_rank_2": "#2 பயிர்", "crop_rank_3": "#3 பயிர்",
    "yield_eyebrow": "மகசூல் கணிப்பு", "yield_title": "அறுவடைக்கு முன் மகசூலை கணிக்கவும்", "yield_desc": "மாநிலம், பயிர், பரப்பளவு மற்றும் மழையின் அடிப்படையில் உண்மையான மகசூல் கணிப்பு.",
    "yield_crop": "பயிர்", "crop_year": "பயிர் ஆண்டு", "yield_season": "பருவம்", "state": "மாநிலம்", "area": "விதைப்பு பரப்பளவு", "area_unit_label": "அலகு", "unit_acres": "ஏக்கர்", "unit_hectares": "ஹெக்டேர்", "annual_rainfall": "ஆண்டு மழை (mm, விருப்பம்)", "fertilizer": "உரம் (kg, விருப்பம்)", "pesticide": "பூச்சிக்கொல்லி (kg, விருப்பம்)", "yield_btn": "மகசூலை கணிக்கவும்", "predicted": "கணிக்கப்பட்ட மகசூல்", "yield_result_desc": "இந்திய பொருளாதார மற்றும் புள்ளியியல் இயக்குநரக தரவுகளின் அடிப்படையில்.", "estimated_production_label": "மொத்த மதிப்பிடப்பட்ட உற்பத்தி",
    "advisory_eyebrow": "ஸ்மார்ட் ஆலோசனை", "advisory_title": "பயிர் பராமரிப்பு மற்றும் வழிகாட்டுதல்", "advisory_desc": "நீர்ப்பாசனம், உர மேலாண்மை மற்றும் பூச்சி தடுப்புக்கான நடைமுறை வழிமுறைகள்.",
    "advisory_crop": "பயிரைத் தேர்ந்தெடுக்கவும்", "advisory_priority": "முன்னுரிமை", "get_advice": "ஆலோசனை பெறுக", "advice_label": "வேளாண் ஆலோசனை", "advice_title": "வழிகாட்டுதலைப் பார்க்க முன்னுரிமையைத் தேர்ந்தெடுக்கவும்",
    "catalogue_eyebrow": "பயிர் பட்டியல்", "catalogue_title": "சரிபார்க்கப்பட்ட பயிர்களின் விபரம்", "catalogue_desc": "தானியங்கள், பருப்பு வகைகள், எண்ணெய் வித்துக்கள், காய்கறிகள் மற்றும் பழங்களின் விரிவான பட்டியல்.",
    "cat_filter_category": "வகை", "cat_filter_season": "பருவம்", "cat_search_placeholder": "பயிர் பெயர் மூலம் தேடுக...", "cat_all": "அனைத்தும்", "badge_ml": "ML பரிந்துரை உண்டு", "badge_yield": "மகசூல் மாதிரி", "badge_mandi": "சந்தை விலை", "badge_storage": "சேமிப்பு வசதி",
    "mandi_eyebrow": "வேளாண் சந்தை விலைகள்", "mandi_title": "மண்டி விலைகள் மற்றும் விற்பனை வழிகாட்டி", "mandi_desc": "அதிகாரப்பூர்வ சந்தை வரத்து விலைகள் மற்றும் அறுவடைக்கு பின் விற்பனை/சேமிப்பு கணக்கீடு.",
    "mandi_select_crop": "பயிரைத் தேர்ந்தெடுக்கவும்", "mandi_select_state": "மாநிலம்", "mandi_select_district": "மாவட்டம்", "mandi_search_btn": "சந்தை விலையை சரிபார்க்கவும்", "mandi_modal_price": "சராசரி விலை", "mandi_min_max": "குறைந்தபட்ச – அதிகபட்ச விலை", "mandi_market_name": "சந்தை கிடங்கு", "mandi_arrival_date": "அறிவிக்கப்பட்ட தேதி", "mandi_trend": "30 நாள் போக்கு", "selling_guidance_title": "விற்பனை vs சேமிப்பு பகுப்பாய்வு", "calc_selling_btn": "லாப-நஷ்டத்தை கணக்கிடுக", "distance_km": "சந்தை தூரம் (கி.மீ)", "holding_days": "சேமிப்பு காலம் (நாட்கள்)",
    "storage_eyebrow": "கிடங்கு மற்றும் குளிர்பதன வசதிகள்", "storage_title": "அருகிலுள்ள கிடங்குகள் மற்றும் குளிர்பதன அறைகள்", "storage_desc": "பயிர்களை பாதுகாத்து சரியான விலைக்கு விற்க பதிவு செய்யப்பட்ட கிடங்குகளை கண்டறியுங்கள்.",
    "storage_filter_type": "சேமிப்பு வகை", "storage_all_types": "அனைத்து வகைகள்", "storage_grain": "தானிய கிடங்கு (இயல்பு)", "storage_cold": "குளிர்பதன கிடங்கு", "storage_search_btn": "கிடங்குகளை கண்டறிக", "storage_capacity": "கொள்ளளவு", "storage_status": "நிலை", "storage_contact": "தொடர்பு",
    "alert_eyebrow": "விலை அறிவிப்புகள்", "alert_title": "சந்தை விலை விழிப்பூட்டல் பெறுக", "alert_desc": "சந்தை விலை உங்கள் இலக்கு விலையை எட்டும்போது மொபைலில் அறிவிப்பு பெறவும்.",
    "alert_mobile": "மொபைல் எண்", "alert_target_price": "இலக்கு விலை (₹/குவிண்டால்)", "alert_condition": "விலை இருக்கும் போது", "cond_above": "சமமாக அல்லது அதிகமாக", "cond_below": "சமமாக அல்லது குறைவாக", "alert_subscribe_btn": "பதிவு செய்க", "alert_my_subscriptions": "செயலில் உள்ள அறிவிப்புகள்", "alert_no_active": "இந்த எண்ணில் எந்த அறிவிப்புகளும் இல்லை.",
    "auth_modal_title": "விவசாயி மொபைல் உள்நுழைவு", "auth_modal_desc": "பண்ணைத் திட்டங்களை சேமிக்கவும் விலை அறிவிப்புகளைப் பெறவும் உள்நுழையவும்.", "auth_mobile_label": "10 இலக்க மொபைல் எண்", "auth_request_otp": "OTP அனுப்புக", "auth_otp_label": "6 இலக்க OTP உள்ளிடவும்", "auth_verify_btn": "சரிபார்த்து உள்நுழைக", "auth_dev_notice": "டெவலப்மெண்ட் முறை இயக்கத்தில் உள்ளது: OTP திரையில் காட்டப்படும்.",
    "about_eyebrow": "RYTHUCROP பற்றி", "about_title": "இந்திய விவசாயத்திற்கான வெளிப்படையான தொழில்நுட்பம்", "about_desc": "விவசாயிகளுக்கு நம்பகமான முடிவுகளை எடுக்க துல்லியமான தரவு மற்றும் ML மாதிரிகளை இணைக்கிறது.", "about_ml": "இயந்திர கற்றல்", "about_ml_desc": "அதிகாரப்பூர்வ வேளாண் புள்ளிவிவரங்களின் அடிப்படையில் பயிற்றுவிக்கப்பட்ட மாதிரிகள்.", "about_farmer": "விவசாயிக்கு முன்னுரிமை", "about_farmer_desc": "எளிய தாய்மொழி இடைமுகம் மற்றும் தெளிவான வழிகாட்டுதல்.", "about_mobile": "அனைத்து சாதனங்கள் மற்றும் பல மொழிகள்", "about_mobile_desc": "மொபைல், டேப்லெட் மற்றும் கணினியில் 9 இந்திய மொழிகளில் கிடைக்கிறது.", "footer_desc": "RythuCrop — இந்திய விவசாயிகளுக்கான துல்லிய வேளாண் முடிவு ஆதரவு தளம்.",
    "season_kharif": "காரிஃப் (பருவமழை)", "season_rabi": "ரபி (குளிர்காலம்)", "season_summer": "கோடை (சையத்)", "season_whole_year": "ஆண்டு முழுவதும்",
    "soil_loamy": "வண்டல் மண்", "soil_black": "கரிசல் மண்", "soil_red": "செம்மண்", "soil_clay": "களிமண்", "soil_sandy": "மணல் மண்", "soil_alluvial": "வண்டல் படிவு மண்",
    "water_good": "நல்ல நீர் வசதி (வாய்மடை / ஆழ்துளை)", "water_moderate": "மிதமான நீர் வசதி", "water_low": "குறைந்த நீர் வசதி (மானாவாரி)", "water_rainfed": "வானம் பார்த்த பூமி (பாசனமில்லை)",
    "goal_yield": "அதிக மகசூல்", "goal_water": "குறைந்த நீர் பயன்பாடு", "goal_cost": "குறைந்த சாகுபடி செலவு", "goal_balanced": "சமச்சீர் விவசாயம்",
    "exp_beginner": "தொடக்க விவசாயி (1-2 ஆண்டுகள்)", "exp_some": "சில ஆண்டுகள் அனுபவம் (3-5 ஆண்டுகள்)", "exp_experienced": "அனுபவமிக்க விவசாயி (5+ ஆண்டுகள்)",
    "priority_water": "நீர் சேமிப்பு மற்றும் மேலாண்மை", "priority_fertilizer": "உரம் மற்றும் ஊட்டச்சத்து மேலாண்மை", "priority_pest": "பூச்சி மற்றும் நோய் கட்டுப்பாடு", "priority_harvest": "அறுவடை மற்றும் அறுவடை பின்சார் மேலாண்மை",
    "calculating": "செயலாக்கப்படுகிறது…", "prediction_failed": "கணிப்பு தோல்வியடைந்தது", "server_error": "சர்வர் பிழை. மீண்டும் முயற்சிக்கவும்.", "unit_tonnes_ha": "டன்/ஹெக்டேர்", "unit_quintals_acre": "குவிண்டால்/ஏக்கர்",
    "reasons_label": "முக்கிய காரணங்கள்:", "soil_label": "மண் ஆலோசனை:", "water_label": "நீர் அட்டவணை:", "risks_label": "அனுமானங்கள் & அபாயங்கள்:", "next_steps_label": "பரிந்துரைக்கப்பட்ட நடவடிக்கைகள்:"
}
TRANSLATIONS["ta"] = TA_BASE

# Kannada (kn)
KN_BASE = {
    "nav_home": "ಮುಖಪುಟ", "nav_planning": "ಕೃಷಿ ಯೋಜನೆ", "nav_crop": "ಬೆಳೆ ಶಿಫಾರಸು", "nav_yield": "ಇಳುವರಿ ಅಂದಾಜು", "nav_advisory": "ಸ್ಮಾರ್ಟ್ ಸಲಹೆ", "nav_catalogue": "ಬೆಳೆಗಳ ಪಟ್ಟಿ", "nav_market": "ಮಾರುಕಟ್ಟೆ ದರಗಳು", "nav_storage": "ಗೋದಾಮು ಮಾಹಿತಿ", "nav_alerts": "ಬೆಲೆ ಎಚ್ಚರಿಕೆಗಳು", "nav_about": "ನಮ್ಮ ಬಗ್ಗೆ", "nav_login": "ಲಾಗಿನ್ / ನೋಂದಣಿ", "nav_logout": "ಲಾಗೌಟ್", "user_welcome": "ರೈತರ ಪ್ರೊಫೈಲ್",
    "hero_badge": "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ • ನಿಖರ ಕೃಷಿ ತಂತ್ರಜ್ಞಾನ", "hero_title1": "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ.", "hero_title2": "ಉತ್ತಮ ನಿರ್ಧಾರಗಳು.", "hero_desc": "RythuCrop ಭಾರತೀಯ ರೈತರಿಗೆ ಪ್ರದೇಶ-ಆಧಾರಿತ ಬೆಳೆ ಶಿಫಾರಸು, ನಿಖರ ಇಳುವರಿ ಅಂದಾಜು, ಅಗ್ಮಾರ್ಕ್‌ನೆಟ್ ಎಪಿಎಂಸಿ ದರಗಳು ಮತ್ತು ಶೀತಲ ಗೋದಾಮುಗಳ ಮಾಹಿತಿಯನ್ನು ಒದಗಿಸುತ್ತದೆ.", "hero_btn1": "ಯೋಜನೆ ಪ್ರಾರಂಭಿಸಿ", "hero_btn2": "ಮಾರುಕಟ್ಟೆ ದರ ವೀಕ್ಷಿಸಿ", "hero_card_title": "ನಿರ್ಧಾರ ಸಹಾಯ", "hero_card_main": "ಮಣ್ಣಿನಿಂದ ಮಾರುಕಟ್ಟೆಯವರೆಗೆ", "hero_card_desc": "ದೃಢೀಕೃತ ದತ್ತಾಂಶ ಮತ್ತು ಮೆಷಿನ್ ಲರ್ನಿಂಗ್ ಆಧಾರದ ಮೇಲೆ ಸರಿಯಾದ ನಿರ್ಧಾರಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳಿ.",
    "loc_state": "ರಾಜ್ಯ", "loc_district": "ಜಿಲ್ಲೆ", "loc_mandal": "ತಾಲೂಕು / ಮಂಡಲ", "loc_season": "ಋತು", "loc_year": "ಬೆಳೆ ವರ್ಷ", "loc_apply": "ಸ್ಥಳವನ್ನು ಹೊಂದಿಸಿ",
    "plan_eyebrow": "ಕೃಷಿ ಯೋಜನೆ", "plan_title": "ನಿಮ್ಮ ಜಮೀನಿನ ಬಗ್ಗೆ ತಿಳಿಸಿ", "plan_desc": "ಸರಳ ಆಯ್ಕೆಗಳನ್ನು ಮಾಡಿ. RythuCrop ನೀರು, ಮಣ್ಣು ಮತ್ತು ಅಪಾಯದ ಅಂಶಗಳೊಂದಿಗೆ ಪ್ರಾಯೋಗಿಕ ಬೆಳೆ ಯೋಜನೆಯನ್ನು ಸಿದ್ಧಪಡಿಸುತ್ತದೆ.",
    "land": "ಭೂಮಿ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ)", "season": "ಋತು", "soil": "ಮಣ್ಣಿನ ವಿಧ", "irrigation": "ನೀರಿನ ಲಭ್ಯತೆ", "goal": "ಮುಖ್ಯ ಗುರಿ", "experience": "ಕೃಷಿ ಅನುಭವ", "generate_plan": "ನನ್ನ ಯೋಜನೆ ರಚಿಸಿ", "plan_result_label": "ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆಗಳು", "plan_result_title": "ನಿಮ್ಮ ಸಲಹೆಗಳು ಇಲ್ಲಿ ಕಾಣಿಸುತ್ತವೆ", "plan_result_desc": "ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ ಯೋಜನೆ ರಚಿಸಿ ಬಟನ್ ಒತ್ತಿ.",
    "crop_eyebrow": "ಬೆಳೆ ಶಿಫಾರಸು", "crop_title": "ನಿಮ್ಮ ಮಣ್ಣಿಗೆ ಸೂಕ್ತವಾದ ಬೆಳೆಯನ್ನು ಕಂಡುಕೊಳ್ಳಿ", "crop_desc": "ನಿಖರ ಬೆಳೆ ಶಿಫಾರಸಿಗಾಗಿ ಮಣ್ಣಿನ ಪೋಷಕಾಂಶಗಳು ಮತ್ತು ಹವಾಮಾನ ಮೌಲ್ಯಗಳನ್ನು ನಮೂದಿಸಿ.",
    "nitrogen": "ಸಾರಜನಕ (N) kg/ha", "phosphorus": "ರಂಜಕ (P) kg/ha", "potassium": "ಪೊಟ್ಯಾಶ್ (K) kg/ha", "temperature": "ತಾಪಮಾನ (°C)", "humidity": "ತೇವಾಂಶ (%)", "soil_ph": "ಮಣ್ಣಿನ pH", "rainfall": "ಮಳೆ ಪ್ರಮಾಣ (mm)", "recommend_btn": "ಬೆಳೆ ಶಿಫಾರಸು ಮಾಡಿ", "recommended": "ಪ್ರಮುಖ ಶಿಫಾರಸುಗಳು", "crop_result_desc": "ತರಬೇತಿ ಪಡೆದ 51 ಬೆಳೆಗಳ ಮೆಷಿನ್ ಲರ್ನಿಂಗ್ ಮಾದರಿಯ ಆಧಾರದ ಮೇಲೆ.", "crop_rank_1": "#1 ಬೆಳೆ", "crop_rank_2": "#2 ಬೆಳೆ", "crop_rank_3": "#3 ಬೆಳೆ",
    "yield_eyebrow": "ಇಳುವರಿ ಅಂದಾಜು", "yield_title": "ಕೊಯ್ಲಿಗೆ ಮುನ್ನವೇ ಇಳುವರಿಯನ್ನು ಅಂದಾಜಿಸಿ", "yield_desc": "ರಾಜ್ಯ, ಬೆಳೆ, ವಿಸ್ತೀರ್ಣ ಮತ್ತು ಮಳೆಯ ಆಧಾರದ ಮೇಲೆ ನೈಜ ಇಳುವರಿ ಲೆಕ್ಕಾಚಾರ.",
    "yield_crop": "ಬೆಳೆ", "crop_year": "ಬೆಳೆ ವರ್ಷ", "yield_season": "ಋತು", "state": "ರಾಜ್ಯ", "area": "ಬಿತ್ತನೆ ವಿಸ್ತೀರ್ಣ", "area_unit_label": "ಘಟಕ", "unit_acres": "ಎಕರೆ", "unit_hectares": "ಹೆಕ್ಟೇರ್", "annual_rainfall": "ವಾರ್ಷಿಕ ಮಳೆ (mm, ಐಚ್ಛಿಕ)", "fertilizer": "ರಸಗೊಬ್ಬರ (kg, ಐಚ್ಛಿಕ)", "pesticide": "ಕೀಟನಾಶಕ (kg, ಐಚ್ಛಿಕ)", "yield_btn": "ಇಳುವರಿ ಅಂದಾಜಿಸಿ", "predicted": "ಅಂದಾಜು ಬೆಳೆ ಇಳುವರಿ", "yield_result_desc": "ಭಾರತೀಯ ಕೃಷಿ ಅಂಕಿಅಂಶ ನಿರ್ದೇಶನಾಲಯದ ದತ್ತಾಂಶಗಳ ಆಧಾರದ ಮೇಲೆ.", "estimated_production_label": "ಒಟ್ಟು ಅಂದಾಜು ಉತ್ಪಾದನೆ",
    "advisory_eyebrow": "ಸ್ಮಾರ್ಟ್ ಸಲಹೆ", "advisory_title": "ಬೆಳೆ ಸಂರಕ್ಷಣೆ ಮತ್ತು ಕೃಷಿ ಮಾರ್ಗದರ್ಶಿ", "advisory_desc": "ನೀರಾವರಿ, ಗೊಬ್ಬರ ನಿರ್ವಹಣೆ ಮತ್ತು ಕೀಟ ನಿಯಂತ್ರಣದ ಕುರಿತು ಪ್ರಾಯೋಗಿಕ ಸಲಹೆಗಳು.",
    "advisory_crop": "ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ", "advisory_priority": "ಆದ್ಯತೆ", "get_advice": "ಸಲಹಾ ಪಟ್ಟಿ ಪಡೆಯಿರಿ", "advice_label": "ಕೃಷಿ ಸಲಹೆ", "advice_title": "ಮಾರ್ಗದರ್ಶನ ನೋಡಲು ಆದ್ಯತೆಯನ್ನು ಆರಿಸಿ",
    "catalogue_eyebrow": "ಬೆಳೆಗಳ ಪಟ್ಟಿ", "catalogue_title": "ದೃಢೀಕೃತ ಬೆಳೆಗಳ ಸಮಗ್ರ ಮಾಹಿತಿ", "catalogue_desc": "ಧಾನ್ಯಗಳು, ಬೇಳೆಕಾಳುಗಳು, ಎಣ್ಣೆಕಾಳುಗಳು, ತರಕಾರಿಗಳು ಮತ್ತು ಹಣ್ಣುಗಳ ಸಂಪೂರ್ಣ ವಿವರ.",
    "cat_filter_category": "ವರ್ಗ", "cat_filter_season": "ಋತು", "cat_search_placeholder": "ಬೆಳೆ ಹೆಸರಿನಿಂದ ಹುಡುಕಿ...", "cat_all": "ಎಲ್ಲವೂ", "badge_ml": "ML ಶಿಫಾರಸು ಲಭ್ಯ", "badge_yield": "ಇಳುವರಿ ಮಾದರಿ", "badge_mandi": "ಮಾರುಕಟ್ಟೆ ದರ", "badge_storage": "ಶೇಖರಣಾ ಮಾಹಿತಿ",
    "mandi_eyebrow": "ಕೃಷಿ ಮಾರುಕಟ್ಟೆ ದರಗಳು", "mandi_title": "ಎಪಿಎಂಸಿ ದರಗಳು ಮತ್ತು ಮಾರಾಟ ಮಾರ್ಗದರ್ಶನ", "mandi_desc": "ಅಧಿಕೃತ ಸಗಟು ದರಗಳು ಮತ್ತು ಕೊಯ್ಲಿನ ನಂತರದ ಮಾರಾಟ vs ಶೇಖರಣೆಯ ಆರ್ಥಿಕ ವಿಶ್ಲೇಷಣೆ.",
    "mandi_select_crop": "ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ", "mandi_select_state": "ರಾಜ್ಯ", "mandi_select_district": "ಜಿಲ್ಲೆ", "mandi_search_btn": "ಮಾರುಕಟ್ಟೆ ದರ ವೀಕ್ಷಿಸಿ", "mandi_modal_price": "ಮಾದರಿ ದರ", "mandi_min_max": "ಕನಿಷ್ಠ – ಗರಿಷ್ಠ ದರ", "mandi_market_name": "ಮಾರುಕಟ್ಟೆ ಗೋದಾಮು", "mandi_arrival_date": "ವರದಿ ದಿನಾಂಕ", "mandi_trend": "30 ದಿನಗಳ ಪ್ರವೃತ್ತಿ", "selling_guidance_title": "ಮಾರಾಟ vs ಶೇಖರಣಾ ವಿಶ್ಲೇಷಣೆ", "calc_selling_btn": "ಲಾಭ-ನಷ್ಟ ಲೆಕ್ಕಾಚಾರ", "distance_km": "ಮಾರುಕಟ್ಟೆಗೆ ದೂರ (ಕಿ.ಮೀ)", "holding_days": "ಶೇಖರಣಾ ದಿನಗಳು",
    "storage_eyebrow": "ಗೋದಾಮು ಮತ್ತು ಕೋಲ್ಡ್ ಸ್ಟೋರೇಜ್", "storage_title": "ಹತ್ತಿರದ ಧಾನ್ಯ ಗೋದಾಮು ಮತ್ತು ಶೀತಲ ಗೃಹಗಳು", "storage_desc": "ಬೆಳೆಯನ್ನು ಸುರಕ್ಷಿತವಾಗಿಡಲು ಮತ್ತು ಉತ್ತಮ ಬೆಲೆ ಪಡೆಯಲು ನೋಂದಾಯಿತ ಗೋದಾಮುಗಳನ್ನು ಹುಡುಕಿ.",
    "storage_filter_type": "ಶೇಖರಣಾ ವಿಧ", "storage_all_types": "ಎಲ್ಲಾ ವಿಧಗಳು", "storage_grain": "ಧಾನ್ಯ ಗೋದಾಮು (ಸಾಮಾನ್ಯ)", "storage_cold": "ಶೀತಲ ಗೋದಾಮು (ಕೋಲ್ಡ್ ಸ್ಟೋರೇಜ್)", "storage_search_btn": "ಗೋದಾಮು ಹುಡುಕಿ", "storage_capacity": "ಸಾಮರ್ಥ್ಯ", "storage_status": "ಸ್ಥಿತಿ", "storage_contact": "ಸಂಪರ್ಕ",
    "alert_eyebrow": "ಬೆಲೆ ಎಚ್ಚರಿಕೆಗಳು", "alert_title": "ಮಾರುಕಟ್ಟೆ ದರ ಸೂಚನೆ ಪಡೆಯಿರಿ", "alert_desc": "ದರವು ನಿಮ್ಮ ನಿಗದಿತ ಮಿತಿಯನ್ನು ತಲುಪಿದಾಗ ಮೊಬೈಲ್‌ಗೆ ಎಚ್ಚರಿಕೆಯನ್ನು ಪಡೆಯಿರಿ.",
    "alert_mobile": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ", "alert_target_price": "ಗುರಿ ಬೆಲೆ (₹/ಕ್ವಿಂಟಾಲ್)", "alert_condition": "ಬೆಲೆಯು ಹೀಗಿದ್ದಾಗ", "cond_above": "ಸಮನಾಗಿ ಅಥವಾ ಹೆಚ್ಚಾದಾಗ", "cond_below": "ಸಮನಾಗಿ ಅಥವಾ ಕಡಿಮೆಯಾದಾಗ", "alert_subscribe_btn": "ನೋಂದಣಿ ಮಾಡಿ", "alert_my_subscriptions": "ನನ್ನ ಸಕ್ರಿಯ ಎಚ್ಚರಿಕೆಗಳು", "alert_no_active": "ಈ ಸಂಖ್ಯೆಗೆ ಯಾವುದೇ ಎಚ್ಚರಿಕೆಗಳಿಲ್ಲ.",
    "auth_modal_title": "ರೈತ ಮೊಬೈಲ್ ಲಾಗಿನ್", "auth_modal_desc": "ಕೃಷಿ ಯೋಜನೆಗಳನ್ನು ಉಳಿಸಲು ಮತ್ತು ದರ ಎಚ್ಚರಿಕೆಗಳನ್ನು ಪಡೆಯಲು ಲಾಗಿನ್ ಮಾಡಿ.", "auth_mobile_label": "10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ", "auth_request_otp": "OTP ಕಳುಹಿಸಿ", "auth_otp_label": "6 ಅಂಕಿಯ OTP ನಮೂದಿಸಿ", "auth_verify_btn": "ದೃಢೀಕರಿಸಿ ಲಾಗಿನ್ ಆಗಿ", "auth_dev_notice": "ಡೆವಲಪ್ಮೆಂಟ್ ಮೋಡ್ ಸಕ್ರಿಯ: OTP ಪರದೆಯ ಮೇಲೆ ಲಭ್ಯವಿದೆ.",
    "about_eyebrow": "RYTHUCROP ಬಗ್ಗೆ", "about_title": "ಭಾರತೀಯ ಕೃಷಿಗಾಗಿ ಪಾರದರ್ಶಕ ತಂತ್ರಜ್ಞಾನ", "about_desc": "ರೈತರಿಗೆ ನಂಬಿಕಸ್ಥ ನಿರ್ಧಾರಗಳನ್ನು ನೀಡಲು ಕೃಷಿ ದತ್ತಾಂಶ ಮತ್ತು ML ಮಾದರಿಗಳನ್ನು ಜೋಡಿಸುತ್ತದೆ.", "about_ml": "ಮೆಷಿನ್ ಲರ್ನಿಂಗ್", "about_ml_desc": "ಡೇಟಾ ಸೋರಿಕೆಯಿಲ್ಲದೆ ಅಧಿಕೃತ ಅಂಕಿಅಂಶಗಳೊಂದಿಗೆ ತರಬೇತಿ ಪಡೆದ ಮಾದರಿಗಳು.", "about_farmer": "ರೈತ ಮೊದಲು", "about_farmer_desc": "ಸರಳ ಮಾತೃಭಾಷೆ ಮತ್ತು ಸ್ಪಷ್ಟ ಮಾರ್ಗದರ್ಶನ.", "about_mobile": "ಎಲ್ಲಾ ಸಾಧನಗಳಲ್ಲಿ & ಬಹುಭಾಷಾ ಸೌಲಭ್ಯ", "about_mobile_desc": "ಮೊಬೈಲ್, ಟ್ಯಾಬ್ಲೆಟ್ ಮತ್ತು ಕಂಪ್ಯೂಟರ್‌ಗಳಲ್ಲಿ 9 ಭಾರತೀಯ ಭಾಷೆಗಳಲ್ಲಿ ಲಭ್ಯವಿದೆ.", "footer_desc": "RythuCrop — ಭಾರತೀಯ ರೈತರಿಗೆ ನಿಖರ ಕೃಷಿ ನಿರ್ಧಾರ ಬೆಂಬಲ ವೇದಿಕೆ.",
    "season_kharif": "ಖಾರೀಫ್ (ಮುಂಗಾರು)", "season_rabi": "ರಬಿ (ಹಿಂಗಾರು)", "season_summer": "ಬೇಸಿಗೆ (ಜಾಯಿದ್)", "season_whole_year": "ವರ್ಷವಿಡೀ",
    "soil_loamy": "ಮರಳು ಮಿಶ್ರಿತ ಜೇಡಿ ಮಣ್ಣು", "soil_black": "ಕಪ್ಪು ಮಣ್ಣು (ಎರೆಮಣ್ಣು)", "soil_red": "ಕೆಂಪು ಮಣ್ಣು", "soil_clay": "ಜೇಡಿ ಮಣ್ಣು", "soil_sandy": "ಮರಳು ಮಣ್ಣು", "soil_alluvial": "ಮೆಕ್ಕಲು ಮಣ್ಣು",
    "water_good": "ಉತ್ತಮ ನೀರಾವರಿ (ಕಾಲುವೆ / ಕೊಳವೆಬಾವಿ)", "water_moderate": "ಮಧ್ಯಮ ನೀರಾವರಿ", "water_low": "ಕಡಿಮೆ ನೀರಿನ ಲಭ್ಯತೆ (ಮಳೆ ಆಧಾರಿತ)", "water_rainfed": "ಸಂಪೂರ್ಣ ಮಳೆಯಾಶ್ರಿತ (ನೀರಾವರಿ ಇಲ್ಲ)",
    "goal_yield": "ಹೆಚ್ಚಿನ ಇಳುವರಿ", "goal_water": "ಕಡಿಮೆ ನೀರಿನ ಬಳಕೆ", "goal_cost": "ಕಡಿಮೆ ವೆಚ್ಚ", "goal_balanced": "ಸಮತೋಲಿತ ಕೃಷಿ",
    "exp_beginner": "ಆರಂಭಿಕ ರೈತ (1-2 ವರ್ಷಗಳು)", "exp_some": "ಸ್ವಲ್ಪ ಅನುಭವ (3-5 ವರ್ಷಗಳು)", "exp_experienced": "ಅನುಭವಿ ರೈತ (5+ ವರ್ಷಗಳು)",
    "priority_water": "ನೀರು ಉಳಿತಾಯ & ನಿರ್ವಹಣೆ", "priority_fertilizer": "ರಸಗೊಬ್ಬರ ಮತ್ತು ಪೋಷಕಾಂಶ ನಿರ್ವಹಣೆ", "priority_pest": "ಕೀಟ ಮತ್ತು ರೋಗ ನಿಯಂತ್ರಣ", "priority_harvest": "ಕೊಯ್ಲು ಮತ್ತು ಕೊಯ್ಲೋತ್ತರ ನಿರ್ವಹಣೆ",
    "calculating": "ಸಂಸ್ಕರಿಸಲಾಗುತ್ತಿದೆ…", "prediction_failed": "ಅಂದಾಜು ವಿಫಲವಾಗಿದೆ", "server_error": "ಸರ್ವರ್ ದೋಷ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.", "unit_tonnes_ha": "ಟನ್/ಹೆಕ್ಟೇರ್", "unit_quintals_acre": "ಕ್ವಿಂಟಾಲ್/ಎಕರೆ",
    "reasons_label": "ಮುಖ್ಯ ಕಾರಣಗಳು:", "soil_label": "ಮಣ್ಣಿನ ಸಲಹೆ:", "water_label": "ನೀರಾವರಿ ವೇಳಾಪಟ್ಟಿ:", "risks_label": "ಅನುಮಾನಗಳು & ಅಪಾಯಗಳು:", "next_steps_label": "ಶಿಫಾರಸು ಮಾಡಿದ ಕ್ರಮಗಳು:"
}
TRANSLATIONS["kn"] = KN_BASE

# Malayalam (ml)
ML_BASE = {
    "nav_home": "ഹോം", "nav_planning": "കൃഷി പദ്ധതി", "nav_crop": "വിള ശുപാർശ", "nav_yield": "വിളവ് പ്രവചനം", "nav_advisory": "സ്മാർട്ട് ഉപദേശം", "nav_catalogue": "വിളകളുടെ ഡയറക്ടറി", "nav_market": "വിപണി വിലകൾ", "nav_storage": "സംഭരണ കേന്ദ്രങ്ങൾ", "nav_alerts": "വില അലേർട്ടുകൾ", "nav_about": "ഞങ്ങളെക്കുറിച്ച്", "nav_login": "ലോഗിൻ / രജിസ്റ്റർ", "nav_logout": "ലോഗൗട്ട്", "user_welcome": "കർഷക പ്രൊഫൈൽ",
    "hero_badge": "സ്മാർട്ട് അഗ്രികൾച്ചർ • പ്രിസിഷൻ കൃഷി സാങ്കേതികവിദ്യ", "hero_title1": "സ്മാർട്ട് കൃഷി.", "hero_title2": "മികച്ച തീരുമാനങ്ങൾ.", "hero_desc": "RythuCrop കർഷകർക്ക് പ്രാദേശിക വിള ശുപാർശ, വിളവ് പ്രവചനം, അഗ്രോമാർക്കറ്റ് വിലകൾ, ശീതീകരണ സംഭരണ കേന്ദ്രങ്ങളുടെ വിവരങ്ങൾ നൽകുന്നു.", "hero_btn1": "പദ്ധതി ആരംഭിക്കുക", "hero_btn2": "വിപണി വില കാണുക", "hero_card_title": "തീരുമാന സഹായം", "hero_card_main": "മണ്ണിൽ നിന്ന് വിപണിയിലേക്ക്", "hero_card_desc": "ശാസ്ത്രീയ ഡാറ്റയും മെഷീൻ ലേണിംഗും അടിസ്ഥാനമാക്കി ശരിയായ തീരുമാനമെടുക്കൂ.",
    "loc_state": "സംസ്ഥാനം", "loc_district": "ജില്ല", "loc_mandal": "താലൂക്ക് / ബ്ലോക്ക്", "loc_season": "സീസൺ", "loc_year": "വിള വർഷം", "loc_apply": "പ്രദേശം തിരഞ്ഞെടുക്കുക",
    "plan_eyebrow": "കൃഷി പദ്ധതി", "plan_title": "നിങ്ങളുടെ കൃഷിയിടത്തെക്കുറിച്ച് പറയൂ", "plan_desc": "ലളിതമായ വിവരങ്ങൾ നൽകുക. ജലലഭ്യത, മണ്ണ്, കാലാവസ്ഥ എന്നിവ കണക്കിലെടുത്ത് RythuCrop ഒരു സമഗ്ര പദ്ധതി തയാറാക്കുന്നു.",
    "land": "ഭൂവിസ്തീർണം (ഏക്കർ)", "season": "സീസൺ", "soil": "മണ്ണിന്റെ തരം", "irrigation": "ജലലഭ്യത", "goal": "പ്രധാന ലക്ഷ്യം", "experience": "കൃഷി പരിചയം", "generate_plan": "പദ്ധതി തയാറാക്കുക", "plan_result_label": "ശുപാർശ ചെയ്ത വിളകൾ", "plan_result_title": "നിർദേശങ്ങൾ ഇവിടെ കാണാം", "plan_result_desc": "വിവരങ്ങൾ നൽകി ബട്ടൺ അമർത്തുക.",
    "crop_eyebrow": "വിള ശുപാർശ", "crop_title": "നിങ്ങളുടെ മണ്ണിന് അനുയോജ്യമായ വിള കണ്ടെത്തുക", "crop_desc": "മണ്ണിലെ പോഷകങ്ങളും കാലാവസ്ഥാ ഘടകങ്ങളും നൽകി വിള ശുപാർശ നേടുക.",
    "nitrogen": "നൈട്രജൻ (N) kg/ha", "phosphorus": "ഫോസ്ഫറസ് (P) kg/ha", "potassium": "പൊട്ടാസ്യം (K) kg/ha", "temperature": "താപനില (°C)", "humidity": "ഈർപ്പം (%)", "soil_ph": "മണ്ണിന്റെ pH", "rainfall": "മഴ (mm)", "recommend_btn": "വിള ശുപാർശ ചെയ്യുക", "recommended": "പ്രധാന ശുപാർശകൾ", "crop_result_desc": "51 വിളകളിൽ പരിശീലിപ്പിച്ച മെഷീൻ ലേണിംഗ് മോഡൽ വഴി നിർണയിച്ചത്.", "crop_rank_1": "#1 വിള", "crop_rank_2": "#2 വിള", "crop_rank_3": "#3 വിള",
    "yield_eyebrow": "വിളവ് പ്രവചനം", "yield_title": "വിളവെടുപ്പിന് മുമ്പേ വിളവ് കണക്കാക്കുക", "yield_desc": "സംസ്ഥാനം, വിള, വിസ്തൃതി, മഴ എന്നിവ അടിസ്ഥാനമാക്കിയുള്ള പ്രവചനം.",
    "yield_crop": "വിള", "crop_year": "വിള വർഷം", "yield_season": "സീസൺ", "state": "സംസ്ഥാനം", "area": "കൃഷി വിസ്തൃതി", "area_unit_label": "യൂണിറ്റ്", "unit_acres": "ഏക്കർ", "unit_hectares": "ഹെക്ടർ", "annual_rainfall": "വാർഷിക മഴ (mm, ഓപ്ഷണൽ)", "fertilizer": "വളം (kg, ഓപ്ഷണൽ)", "pesticide": "കീടനാശിനി (kg, ഓപ്ഷണൽ)", "yield_btn": "വിളവ് കണക്കാക്കുക", "predicted": "പ്രവചിച്ച വിളവ്", "yield_result_desc": "ഇന്ത്യൻ സാമ്പത്തിക സ്ഥിതിവിവരക്കണക്ക് ഡയറക്ടറേറ്റ് രേഖകളുടെ അടിസ്ഥാനത്തിൽ.", "estimated_production_label": "മൊത്തം കണക്കാക്കിയ ഉത്പാദനം",
    "advisory_eyebrow": "സ്മാർട്ട് ഉപദേശം", "advisory_title": "വിള സംരക്ഷണവും കാർഷിക നിർദേശങ്ങളും", "advisory_desc": "ജലസേചനം, പോഷക പരിപാലനം, കീടനിയന്ത്രണം എന്നിവയിലെ പ്രായോഗിക നിർദേശങ്ങൾ.",
    "advisory_crop": "വിള തിരഞ്ഞെടുക്കുക", "advisory_priority": "മുൻഗണന", "get_advice": "നിർദേശങ്ങൾ കാണുക", "advice_label": "കാർഷിക ഉപദേശം", "advice_title": "നിർദേശങ്ങൾ കാണാൻ മുൻഗണന തിരഞ്ഞെടുക്കുക",
    "catalogue_eyebrow": "വിളകളുടെ ഡയറക്ടറി", "catalogue_title": "അംഗീകൃത വിളകളുടെ സമഗ്ര വിവരങ്ങൾ", "catalogue_desc": "ധാന്യങ്ങൾ, പയറുവർഗ്ഗങ്ങൾ, എണ്ണക്കുരുക്കൾ, പച്ചക്കറികൾ, പഴങ്ങൾ എന്നിവയുടെ വിവരങ്ങൾ.",
    "cat_filter_category": "വിഭാഗം", "cat_filter_season": "സീസൺ", "cat_search_placeholder": "വിളയുടെ പേര് തിരയുക...", "cat_all": "എല്ലാം", "badge_ml": "ML ശുപാർശ ലഭ്യമാണ്", "badge_yield": "വിളവ് മോഡൽ", "badge_mandi": "വിപണി വില", "badge_storage": "സംഭരണ സൗകര്യം",
    "mandi_eyebrow": "കാർഷിക വിപണി വിലകൾ", "mandi_title": "മൊത്തവ്യാപാര മാർക്കറ്റ് വിലകളും മാർഗ്ഗനിർദ്ദേശങ്ങളും", "mandi_desc": "ഔദ്യോഗിക ചന്ത വിലകളും സംഭരണ/വിൽപ്പന ലാഭനഷ്ട കണക്കുകൂട്ടലുകളും.",
    "mandi_select_crop": "വിള തിരഞ്ഞെടുക്കുക", "mandi_select_state": "സംസ്ഥാനം", "mandi_select_district": "ജില്ല", "mandi_search_btn": "വിപണി വില തിരയുക", "mandi_modal_price": "ശരാശരി വില", "mandi_min_max": "കുറഞ്ഞ – കൂടിയ വില", "mandi_market_name": "ചന്ത / മണ്ഡി", "mandi_arrival_date": "റിപ്പോർട്ട് ചെയ്ത തീയതി", "mandi_trend": "30 ദിവസത്തെ പ്രവണത", "selling_guidance_title": "വിൽപന vs സംഭരണ വിശകലനം", "calc_selling_btn": "ലാഭനഷ്ടം കണക്കാക്കുക", "distance_km": "വിപണിയിലേക്കുള്ള ദൂരം (കി.മീ)", "holding_days": "സംഭരണ കാലാവധി (ദിവസങ്ങൾ)",
    "storage_eyebrow": "സംഭരണവും കോൾഡ് സ്റ്റോറേജും", "storage_title": "സമീപത്തെ ധാന്യപ്പുരകളും ശീതീകരണ സംഭരണികളും", "storage_desc": "വിളവുകൾ സുരക്ഷിതമായി സൂക്ഷിക്കാനും മികച്ച വില നേടാനും അംഗീകൃത സംഭരണശാലകൾ കണ്ടെത്തുക.",
    "storage_filter_type": "സംഭരണ തരം", "storage_all_types": "എല്ലാ തരങ്ങളും", "storage_grain": "ധാന്യ സംഭരണശാല (സാധാരണ)", "storage_cold": "ശീതീകരണ സംഭരണി (കോൾഡ് സ്റ്റോറേജ്)", "storage_search_btn": "സൗകര്യങ്ങൾ കണ്ടെത്തുക", "storage_capacity": "ശേഷി", "storage_status": "നിലവിലെ അവസ്ഥ", "storage_contact": "ബന്ധപ്പെടുക",
    "alert_eyebrow": "വില അലേർട്ടുകൾ", "alert_title": "വിപണി വില നോട്ടിഫിക്കേഷൻ നേടുക", "alert_desc": "മാർക്കറ്റ് വില നിങ്ങളുടെ നിശ്ചിത നിരക്കിലെത്തുമ്പോൾ മൊബൈൽ സന്ദേശം നേടുക.",
    "alert_mobile": "മൊബൈൽ നമ്പർ", "alert_target_price": "ലക്ഷ്യ വില (₹/ക്വിന്റൽ)", "alert_condition": "വില ഇങ്ങനെയാകുമ്പോൾ", "cond_above": "തുല്യമോ കൂടുതലോ ആകുമ്പോൾ", "cond_below": "തുല്യമോ കുറവോ ആകുമ്പോൾ", "alert_subscribe_btn": "സബ്‌സ്‌ക്രൈബ് ചെയ്യുക", "alert_my_subscriptions": "എന്റെ സജീവ അലേർട്ടുകൾ", "alert_no_active": "സജീവമായ അലേർട്ടുകളൊന്നും നിലവിലില്ല.",
    "auth_modal_title": "കർഷക മൊബൈൽ ലോഗിൻ", "auth_modal_desc": "പദ്ധതികൾ സൂക്ഷിക്കാനും വില അലേർട്ടുകൾ നേടാനും ലോഗിൻ ചെയ്യുക.", "auth_mobile_label": "10 അക്ക മൊബൈൽ നമ്പർ", "auth_request_otp": "OTP അയക്കുക", "auth_otp_label": "6 അക്ക OTP നൽകുക", "auth_verify_btn": "സ്ഥിരീകരിച്ച് ലോഗിൻ ചെയ്യുക", "auth_dev_notice": "ഡെവലപ്‌മെന്റ് മോഡ് സജീവം: OTP സ്ക്രീനിൽ ലഭ്യമാണ്.",
    "about_eyebrow": "RYTHUCROPയെക്കുറിച്ച്", "about_title": "ഇന്ത്യൻ കൃഷിക്കായി സുതാര്യ സാങ്കേതികവിദ്യ", "about_desc": "കർഷകർക്ക് കൃത്യമായ തീരുമാനങ്ങൾ നൽകാൻ ശാസ്ത്രീയ മോഡലുകളെ പ്രയോജനപ്പെടുത്തുന്നു.", "about_ml": "മെഷീൻ ലേണിംഗ്", "about_ml_desc": "ഔദ്യോഗിക കാർഷിക സ്ഥിതിവിവരക്കണക്കുകൾ അടിസ്ഥാനമാക്കി പരിശീലിപ്പിച്ച മോഡലുകൾ.", "about_farmer": "കർഷകൻ പ്രധാനം", "about_farmer_desc": "ലളിതമായ മാതൃഭാഷയും വ്യക്തമായ മാർഗ്ഗനിർദ്ദേശവും.", "about_mobile": "എല്ലാ ഉപകരണങ്ങളിലും ലഭ്യമാണ്", "about_mobile_desc": "മൊബൈൽ, ടാബ്‌ലെറ്റ്, കമ്പ്യൂട്ടർ എന്നിവയിൽ 9 ഇന്ത്യൻ ഭാഷകളിൽ ലഭ്യമാണ്.", "footer_desc": "RythuCrop — ഇന്ത്യൻ കർഷകർക്കായുള്ള പ്രിസിഷൻ കാർഷിക തീരുമാന സഹായ പ്ലാറ്റ്‌ഫോം.",
    "season_kharif": "ഖാരിഫ് (മഴക്കാലം)", "season_rabi": "റാബി (ശീതകാലം)", "season_summer": "വേനൽക്കാലം (സായിദ്)", "season_whole_year": "വർഷം മുഴുവൻ",
    "soil_loamy": "എക്കൽ കലർന്ന മണ്ണ്", "soil_black": "കറുത്ത മണ്ണ്", "soil_red": "ചെമ്മണ്ണ്", "soil_clay": "കളിമണ്ണ്", "soil_sandy": "മണൽ മണ്ണ്", "soil_alluvial": "തീരദേശ എക്കൽമണ്ണ്",
    "water_good": "നല്ല ജലലഭ്യത (കനാൽ / കുഴൽക്കിണർ)", "water_moderate": "ഇടത്തരം ജലലഭ്യത", "water_low": "കുറഞ്ഞ ജലലഭ്യത (മഴയെ ആശ്രയിച്ച്)", "water_rainfed": "മഴയെ മാത്രം ആശ്രയിച്ച്",
    "goal_yield": "കൂടുതൽ വിളവ്", "goal_water": "കുറഞ്ഞ ജല ഉപയോഗം", "goal_cost": "കുറഞ്ഞ ചിലവ്", "goal_balanced": "സന്തുലിത കൃഷി",
    "exp_beginner": "തുടക്കക്കാരൻ (1-2 വർഷം)", "exp_some": "കുറച്ച് പരിചയം (3-5 വർഷം)", "exp_experienced": "പരിചയസമ്പന്നൻ (5+ വർഷം)",
    "priority_water": "ജലസംരക്ഷണവും നനയ്ക്കലും", "priority_fertilizer": "വളപ്രയോഗവും പോഷക പരിപാലനവും", "priority_pest": "കീട-രോഗ പ്രതിരോധം", "priority_harvest": "വിളവെടുപ്പും സംഭരണവും",
    "calculating": "പ്രോസസ്സ് ചെയ്യുന്നു…", "prediction_failed": "പ്രവചനം പരാജയപ്പെട്ടു", "server_error": "സെർവർ തകരാർ. വീണ്ടും ശ്രമിക്കുക.", "unit_tonnes_ha": "ടൺ/ഹെക്ടർ", "unit_quintals_acre": "ക്വിന്റൽ/ഏക്കർ",
    "reasons_label": "പ്രധാന കാരണങ്ങൾ:", "soil_label": "മണ്ണ് നിർദേശം:", "water_label": "നനയ്ക്കൽ ക്രമം:", "risks_label": "അപായസാധ്യതകൾ:", "next_steps_label": "ശുപാർശ ചെയ്ത നടപടികൾ:"
}
TRANSLATIONS["ml"] = ML_BASE

# Marathi (mr)
MR_BASE = {
    "nav_home": "मुख्यपृष्ठ", "nav_planning": "शेती नियोजन", "nav_crop": "पीक शिफारस", "nav_yield": "उत्पादन अंदाज", "nav_advisory": "स्मार्ट सल्ला", "nav_catalogue": "पीक सूची", "nav_market": "बाजार भाव", "nav_storage": "गोदाम शोध", "nav_alerts": "भाव अलर्ट", "nav_about": "आमच्याबद्दल", "nav_login": "लॉगिन / नोंदणी", "nav_logout": "लॉगआउट", "user_welcome": "शेतकरी प्रोफाइल",
    "hero_badge": "स्मार्ट कृषी • अचूक कृषी तंत्रज्ञान", "hero_title1": "स्मार्ट शेती.", "hero_title2": "चांगले निर्णय.", "hero_desc": "RythuCrop भारतीय शेतकऱ्यांना प्रादेशिक पीक शिफारस, अचूक उत्पादन अंदाज, एगमार्कनेट बाजार भाव आणि शीतगृहांची माहिती प्रदान करते.", "hero_btn1": "शेती नियोजन सुरू करा", "hero_btn2": "बाजार भाव पहा", "hero_card_title": "निर्णय सहाय्य", "hero_card_main": "मातीपासून बाजारापर्यंत", "hero_card_desc": "प्रमाणित डेटा आणि मशीन लर्निंगच्या आधारे योग्य निर्णय घ्या.",
    "loc_state": "राज्य", "loc_district": "जिल्हा", "loc_mandal": "तालुका / मंडल", "loc_season": "हंगाम", "loc_year": "पीक वर्ष", "loc_apply": "स्थान निश्चित करा",
    "plan_eyebrow": "शेती नियोजन", "plan_title": "तुमच्या शेताबद्दल सांगा", "plan_desc": "सोपे पर्याय निवडा. RythuCrop पाणी, माती आणि जोखमीचा विचार करून प्रत्यक्ष शेती योजना सुचवते.",
    "land": "जमिनीचे क्षेत्रफळ (एकर)", "season": "हंगाम", "soil": "मातीचा प्रकार", "irrigation": "पाण्याची उपलब्धता", "goal": "मुख्य उद्दिष्ट", "experience": "शेतीचा अनुभव", "generate_plan": "माझी योजना तयार करा", "plan_result_label": "शिफारस केलेली पिके", "plan_result_title": "तुमच्या सूचना येथे दिसतील", "plan_result_desc": "आवश्यक माहिती भरून योजना तयार करा.",
    "crop_eyebrow": "पीक शिफारस", "crop_title": "मातीसाठी योग्य पीक शोधा", "crop_desc": "मशीन लर्निंग आधारे पीक शिफारसीसाठी मातीतील पोषक घटक आणि हवामानाची नोंद करा.",
    "nitrogen": "नायट्रोजन (N) kg/ha", "phosphorus": "फॉस्फरस (P) kg/ha", "potassium": "पोटॅशियम (K) kg/ha", "temperature": "तापमान (°C)", "humidity": "आर्द्रता (%)", "soil_ph": "मातीचे pH", "rainfall": "पाऊस (mm)", "recommend_btn": "पीक शिफारस मिळवा", "recommended": "प्रमुख शिफारसी", "crop_result_desc": "51 पिकांवर प्रशिक्षित रँडम फॉरेस्ट मॉडेलद्वारे विश्लेषित.", "crop_rank_1": "#1 पीक", "crop_rank_2": "#2 पीक", "crop_rank_3": "#3 पीक",
    "yield_eyebrow": "उत्पादन अंदाज", "yield_title": "कापणीपूर्वी उत्पादनाचा अंदाज घ्या", "yield_desc": "राज्य, पीक, क्षेत्रफळ आणि पावसावर आधारित अचूक उत्पादन अंदाज.",
    "yield_crop": "पीक", "crop_year": "पीक वर्ष", "yield_season": "हंगाम", "state": "राज्य", "area": "लागवड क्षेत्र", "area_unit_label": "एकक", "unit_acres": "एकर", "unit_hectares": "हेक्टर", "annual_rainfall": "वार्षिक पाऊस (mm, पर्यायी)", "fertilizer": "खत वापर (kg, पर्यायी)", "pesticide": "कीटकनाशक (kg, पर्यायी)", "yield_btn": "उत्पादनाचा अंदाज घ्या", "predicted": "अंदाजित पीक उत्पादन", "yield_result_desc": "भारतीय कृषी सांख्यिकी संचालनालयाच्या आकडेवारीवर आधारित.", "estimated_production_label": "एकूण अंदाजित उत्पादन",
    "advisory_eyebrow": "स्मार्ट सल्ला", "advisory_title": "पीक काळजी आणि कृषी कृती सूची", "advisory_desc": "सिंचन, खत व्यवस्थापन आणि कीड नियंत्रणाविषयी व्यावहारिक मार्गदर्शन.",
    "advisory_crop": "पीक निवडा", "advisory_priority": "प्राधान्य", "get_advice": "सल्ला सूची पहा", "advice_label": "कृषी सल्ला", "advice_title": "मार्गदर्शन पाहण्यासाठी प्राधान्य निवडा",
    "catalogue_eyebrow": "पीक सूची", "catalogue_title": "प्रमाणित पिकांची संपूर्ण माहिती", "catalogue_desc": "धान्य, कडधान्य, गळीत धान्ये, भाजीपाला आणि फळपिकांची सर्वंकष माहिती.",
    "cat_filter_category": "वर्ग", "cat_filter_season": "हंगाम", "cat_search_placeholder": "पिकाच्या नावाने शोधा...", "cat_all": "सर्व", "badge_ml": "ML शिफारस उपलब्ध", "badge_yield": "उत्पादन मॉडेल", "badge_mandi": "बाजार भाव", "badge_storage": "गोदाम सुविधा",
    "mandi_eyebrow": "कृषी बाजार भाव", "mandi_title": "घाऊक बाजार भाव आणि विक्री मार्गदर्शन", "mandi_desc": "अधिकृत एपीएमसी बाजार भाव आणि काढणीनंतर विक्री विरूद्ध साठवणुकीचे आर्थिक विश्लेषण.",
    "mandi_select_crop": "पीक निवडा", "mandi_select_state": "राज्य", "mandi_select_district": "जिल्हा", "mandi_search_btn": "बाजार भाव तपासा", "mandi_modal_price": "सरासरी भाव", "mandi_min_max": "किमान – कमाल भाव", "mandi_market_name": "बाजार समिती / यार्ड", "mandi_arrival_date": "नोंदणी तारीख", "mandi_trend": "30 दिवसांचा कल", "selling_guidance_title": "विक्री विरूद्ध साठवणूक विश्लेषण", "calc_selling_btn": "नफा-तोटा गणना करा", "distance_km": "बाजाराचे अंतर (किमी)", "holding_days": "साठवणुकीचे दिवस",
    "storage_eyebrow": "गोदामे आणि शीतगृह शोध", "storage_title": "जवळची धान्य गोदामे आणि शीतगृहे", "storage_desc": "पीक सुरक्षित ठेवण्यासाठी आणि चांगला भाव मिळवण्यासाठी अधिकृत गोदामे शोधा.",
    "storage_filter_type": "गोदाम प्रकार", "storage_all_types": "सर्व प्रकार", "storage_grain": "धान्य गोदाम (सर्वसाधारण)", "storage_cold": "शीतगृह (कोल्ड स्टोरेज)", "storage_search_btn": "गोदाम शोधा", "storage_capacity": "क्षमता", "storage_status": "स्थिती", "storage_contact": "संपर्क",
    "alert_eyebrow": "भाव अलर्ट", "alert_title": "बाजार भाव सूचना मिळवा", "alert_desc": "बाजार भाव तुमच्या अपेक्षित किमतीवर पोहोचल्यावर मोबाइलवर अलर्ट मिळवा.",
    "alert_mobile": "मोबाइल नंबर", "alert_target_price": "अपेक्षित भाव (₹/क्विंटल)", "alert_condition": "जेव्हा भाव असेल", "cond_above": "समान किंवा जास्त", "cond_below": "समान किंवा कमी", "alert_subscribe_btn": "अलर्ट सुरू करा", "alert_my_subscriptions": "माझे सक्रिय अलर्ट", "alert_no_active": "या नंबरसाठी कोणतेही सक्रिय अलर्ट नाहीत.",
    "auth_modal_title": "शेतकरी मोबाइल लॉगिन", "auth_modal_desc": "शेती नियोजन जतन करण्यासाठी आणि भाव अलर्ट मिळवण्यासाठी लॉगिन करा.", "auth_mobile_label": "10 अंकी मोबाइल नंबर", "auth_request_otp": "OTP पाठवा", "auth_otp_label": "6 अंकी OTP प्रविष्ट करा", "auth_verify_btn": "सत्यापित करा आणि लॉगिन करा", "auth_dev_notice": "डेव्हलपमेंट मोड सक्रिय: स्क्रीनवर OTP उपलब्ध आहे.",
    "about_eyebrow": "RYTHUCROP बद्दल", "about_title": "भारतीय शेतीसाठी पारदर्शक तंत्रज्ञान", "about_desc": "शेतकऱ्यांना विश्वासार्ह निर्णय घेण्यासाठी कृषी डेटा आणि एमएल मॉडेल्स जोडते.", "about_ml": "मशीन लर्निंग", "about_ml_desc": "डेटा लीकेजशिवाय अधिकृत सांख्यिकी आधारे प्रशिक्षित मॉडेल्स.", "about_farmer": "शेतकरी प्रथम", "about_farmer_desc": "सोपी मातृभाषा आणि स्पष्ट मार्गदर्शन.", "about_mobile": "सर्व उपकरणांवर आणि बहुभाषिक", "about_mobile_desc": "मोबाइल, टॅबलेट आणि संगणकावर 9 भारतीय भाषांमध्ये उपलब्ध.", "footer_desc": "RythuCrop — भारतीय शेतकऱ्यांसाठी अचूक कृषी निर्णय सहाय्य प्रणाली.",
    "season_kharif": "खरीप (पावसाळा)", "season_rabi": "रब्बी (हिवाळा)", "season_summer": "उन्हाळी (झायेद)", "season_whole_year": "वर्षभर",
    "soil_loamy": "गाळाची/दुमट माती", "soil_black": "काळी कसदार माती", "soil_red": "तांबडी माती", "soil_clay": "चिकण माती", "soil_sandy": "रेतीयुक्त माती", "soil_alluvial": "गाळाची माती",
    "water_good": "उत्तम पाणी उपलब्धता (कालवा / कूपनलिका)", "water_moderate": "मध्यम पाणी उपलब्धता", "water_low": "कमी पाणी उपलब्धता (कोरडवाहू)", "water_rainfed": "केवळ पावसावर आधारित (पाणी नाही)",
    "goal_yield": "अधिक उत्पादन", "goal_water": "कमी पाण्याचा वापर", "goal_cost": "कमी उत्पादन खर्च", "goal_balanced": "संतुलित शेती",
    "exp_beginner": "नवीन शेतकरी (1-2 वर्षे)", "exp_some": "काही अनुभव (3-5 वर्षे)", "exp_experienced": "अनुभवी शेतकरी (5+ वर्षे)",
    "priority_water": "पाणी बचत आणि सिंचन", "priority_fertilizer": "खत आणि पोषण व्यवस्थापन", "priority_pest": "कीड व रोग नियंत्रण", "priority_harvest": "कापणी आणि काढणीपश्चात व्यवस्थापन",
    "calculating": "प्रक्रिया सुरू आहे…", "prediction_failed": "अंदाज अयशस्वी", "server_error": "सर्व्हर त्रुटी आली. कृपया पुन्हा प्रयत्न करा.", "unit_tonnes_ha": "टन/हेक्टर", "unit_quintals_acre": "क्विंटल/एकर",
    "reasons_label": "महत्त्वाची कारणे:", "soil_label": "माती सल्ला:", "water_label": "सिंचन नियोजन:", "risks_label": "गृहितके व जोखीम:", "next_steps_label": "शिफारस केलेली कृती:"
}
TRANSLATIONS["mr"] = MR_BASE

# Bengali (bn)
BN_BASE = {
    "nav_home": "হোম", "nav_planning": "কৃষি পরিকল্পনা", "nav_crop": "ফসলের পরামর্শ", "nav_yield": "ফলন পূর্বাভাস", "nav_advisory": "স্মার্ট পরামর্শ", "nav_catalogue": "ফসল তালিকা", "nav_market": "বাজার দর", "nav_storage": "গুদাম সন্ধান", "nav_alerts": "মূল্য সতর্কতা", "nav_about": "আমাদের সম্পর্কে", "nav_login": "লগইন / নিবন্ধন", "nav_logout": "লগআউট", "user_welcome": "কৃষক প্রোফাইল",
    "hero_badge": "স্মার্ট কৃষি • প্রিসিশন এগ্রি-টেক", "hero_title1": "স্মার্ট কৃষি.", "hero_title2": "আরও ভালো সিদ্ধান্ত.", "hero_desc": "RythuCrop ভারতীয় কৃষকদের আঞ্চলিক ফসল পরামর্শ, সঠিক ফলন পূর্বাভাস, এগমार्कনেট পাইকারি বাজার দর এবং প্রত্যয়িত কোল্ড স্টোরেজের তথ্য প্রদান করে।", "hero_btn1": "পরিকল্পনা শুরু করুন", "hero_btn2": "বাজার দর দেখুন", "hero_card_title": "সিদ্ধান্ত সহায়তা", "hero_card_main": "মাটি থেকে বাজার পর্যন্ত", "hero_card_desc": "যাচাইকৃত তথ্য ও মেশিন লার্নিংয়ের সাহায্যে সঠিক সিদ্ধান্ত নিন।",
    "loc_state": "রাজ্য", "loc_district": "জেলা", "loc_mandal": "ব্লক / মহকুমা", "loc_season": "মৌসুম", "loc_year": "ফসলের বছর", "loc_apply": "স্থান নির্ধারণ করুন",
    "plan_eyebrow": "কৃষি পরিকল্পনা", "plan_title": "আপনার জমি সম্পর্কে বলুন", "plan_desc": "সহজ বিকল্প বেছে নিন। RythuCrop জল, মাটি এবং ঝুঁকির দিক বিবেচনা করে কার্যকর ফসল পরিকল্পনা দেয়।",
    "land": "জমির পরিমাণ (একর)", "season": "মৌসুম", "soil": "মাটির ধরন", "irrigation": "জলের প্রাপ্যতা", "goal": "প্রধান লক্ষ্য", "experience": "কৃষি অভিজ্ঞতা", "generate_plan": "পরিকল্পনা তৈরি করুন", "plan_result_label": "প্রস্তাবিত ফসল", "plan_result_title": "পরামর্শ এখানে দেখা যাবে", "plan_result_desc": "বিবরণ নির্বাচন করে পরিকল্পনা তৈরি করুন।",
    "crop_eyebrow": "ফসলের পরামর্শ", "crop_title": "আপনার মাটির উপযুক্ত ফসল খুঁজুন", "crop_desc": "মেশিন লার্নিং শ্রেণীবিভাগের জন্য মাটির পুষ্টি উপাদান এবং আবহাওয়া ইনপুট দিন।",
    "nitrogen": "নাইট্রোজেন (N) kg/ha", "phosphorus": "ফসফরাস (P) kg/ha", "potassium": "পটাশিয়াম (K) kg/ha", "temperature": "তাপমাত্রা (°C)", "humidity": "আর্দ্রতা (%)", "soil_ph": "মাটির pH", "rainfall": "বৃষ্টিপাত (mm)", "recommend_btn": "ফসলের পরামর্শ নিন", "recommended": "শীর্ষ পরামর্শ", "crop_result_desc": "৫১টি ফসলের উপর প্রশিক্ষিত র‍্যান্ডম ফরেস্ট মডেল দ্বারা শ্রেণীবদ্ধ।", "crop_rank_1": "#১ ফসল", "crop_rank_2": "#২ ফসল", "crop_rank_3": "#৩ ফসল",
    "yield_eyebrow": "ফলন পূর্বাভাস", "yield_title": "ফসল তোলার আগেই ফলন অনুমান করুন", "yield_desc": "রাজ্য, ফসল, জমি এবং বৃষ্টির উপর ভিত্তি করে সঠিক পূর্বাভাস।",
    "yield_crop": "ফসল", "crop_year": "ফসলের বছর", "yield_season": "মৌসুম", "state": "রাজ্য", "area": "চাষের জমি", "area_unit_label": "একক", "unit_acres": "একর", "unit_hectares": "হেক্টর", "annual_rainfall": "বার্ষিক বৃষ্টি (mm, ঐচ্ছিক)", "fertilizer": "সার প্রয়োগ (kg, ঐচ্ছিক)", "pesticide": "কীটনাশক (kg, ঐচ্ছিক)", "yield_btn": "ফলন অনুমান করুন", "predicted": "অনুমানিত ফলন", "yield_result_desc": "ভারতীয় অর্থনীতি ও পরিসংখ্যান অধিদপ্তরের তথ্যের ভিত্তিতে।", "estimated_production_label": "মোট আনুমানিক উৎপাদন",
    "advisory_eyebrow": "স্মার্ট পরামর্শ", "advisory_title": "ফসল পরিচর্যা ও করণীয় তালিকা", "advisory_desc": "সেচ, সার প্রয়োগ এবং বালাই ব্যবস্থাপনার কার্যকর পরামর্শ।",
    "advisory_crop": "ফসল নির্বাচন করুন", "advisory_priority": "অগ্রাধিকার", "get_advice": "পরামর্শ তালিকা দেখুন", "advice_label": "কৃষি পরামর্শ", "advice_title": "পরামর্শ দেখতে অগ্রাধিকার বেছে নিন",
    "catalogue_eyebrow": "ফসল তালিকা", "catalogue_title": "যাচাইকৃত ফসলের বিস্তারিত তথ্য", "catalogue_desc": "দানাশস্য, ডালশস্য, তৈলবীজ, শাকসবজি ও ফলের তথ্য ভাণ্ডার।",
    "cat_filter_category": "বিভাগ", "cat_filter_season": "মৌসুম", "cat_search_placeholder": "ফসলের নাম দিয়ে খুঁজুন...", "cat_all": "সব", "badge_ml": "ML সুপারিশ উপলব্ধ", "badge_yield": "ফলন মডেল", "badge_mandi": "বাজার দর", "badge_storage": "গুদাম সুবিধা",
    "mandi_eyebrow": "কৃষি বাজার দর", "mandi_title": "পাইকারি বাজার দর ও বিক্রয় নির্দেশনা", "mandi_desc": "অফিসিয়াল বাজার দর এবং ফসল তোলার পর বিক্রয় বনাম মজুদের লাভ-ক্ষতির বিশ্লেষণ।",
    "mandi_select_crop": "ফসল নির্বাচন করুন", "mandi_select_state": "রাজ্য", "mandi_select_district": "জেলা", "mandi_search_btn": "বাজার দর দেখুন", "mandi_modal_price": "গড় দর", "mandi_min_max": "সর্বনিম্ন – সর্বোচ্চ দর", "mandi_market_name": "বাজার / মান্ডি", "mandi_arrival_date": "রিপোর্টের তারিখ", "mandi_trend": "৩০ দিনের ধারা", "selling_guidance_title": "বিক্রয় বনাম মজুদ বিশ্লেষণ", "calc_selling_btn": "লাভ-ক্ষতির হিসাব করুন", "distance_km": "বাজারের দূরত্ব (কিমি)", "holding_days": "মজুদের মেয়াদ (দিন)",
    "storage_eyebrow": "গুদাম ও কোল্ড স্টোরেজ সন্ধান", "storage_title": "নিকটস্থ শস্য গুদাম ও কোল্ড স্টোরেজ", "storage_desc": "ফসল সুরক্ষিত রাখতে এবং ন্যায্য মূল্য পেতে প্রত্যয়িত গুদাম খুঁজুন।",
    "storage_filter_type": "গুদামের ধরন", "storage_all_types": "সব ধরন", "storage_grain": "শস্য গুদাম (স্বাভাবিক)", "storage_cold": "কোল্ড স্টোরেজ (হিমাগার)", "storage_search_btn": "গুদাম খুঁজুন", "storage_capacity": "ধারণক্ষমতা", "storage_status": "বর্তমান অবস্থা", "storage_contact": "যোগাযোগ",
    "alert_eyebrow": "মূল্য সতর্কতা", "alert_title": "বাজার দরের নোটিফিকেশন পান", "alert_desc": "বাজার দর আপনার কাঙ্ক্ষিত মূল্যে পৌঁছালে মোবাইলে এসএমএস পান।",
    "alert_mobile": "মোবাইল নম্বর", "alert_target_price": "কাঙ্ক্ষিত মূল্য (₹/কুইন্টাল)", "alert_condition": "যখন দর হবে", "cond_above": "সমান বা বেশি", "cond_below": "সমান বা কম", "alert_subscribe_btn": "সতর্কতা চালু করুন", "alert_my_subscriptions": "আমার সক্রিয় সতর্কতা", "alert_no_active": "এই নম্বরে কোনো সক্রিয় সতর্কতা নেই।",
    "auth_modal_title": "কৃষক মোবাইল লগইন", "auth_modal_desc": "পরিকল্পনা সংরক্ষণ করতে এবং মূল্য সতর্কতা পেতে লগইন করুন।", "auth_mobile_label": "১০ সংখ্যার মোবাইল নম্বর", "auth_request_otp": "OTP পাঠান", "auth_otp_label": "৬ সংখ্যার OTP লিখুন", "auth_verify_btn": "যাচাই করে লগইন করুন", "auth_dev_notice": "ডেভেলপমেন্ট মোড সক্রিয়: স্ক্রিনে OTP দেখা যাচ্ছে।",
    "about_eyebrow": "RYTHUCROP সম্পর্কে", "about_title": "ভারতীয় কৃষির জন্য স্বচ্ছ প্রযুক্তি", "about_desc": "কৃষকদের নির্ভরযোগ্য সিদ্ধান্ত নিতে সাহায্য করতে তথ্য ও প্রযুক্তিকে সংযুক্ত করে।", "about_ml": "মেশিন লার্নিং", "about_ml_desc": "তথ্য ফাঁসের ত্রুটিমুক্ত নির্ভরযোগ্য সরকারি পরিসংখ্যান দ্বারা প্রশিক্ষিত।", "about_farmer": "কৃষক প্রথম", "about_farmer_desc": "সহজ মাতৃভাষা এবং স্পষ্ট নির্দেশনা।", "about_mobile": "সব ডিভাইসে এবং বহুভাষায় উপলব্ধ", "about_mobile_desc": "মোবাইল, ট্যাবলেট ও কম্পিউটারে ৯টি ভারতীয় ভাষায় উপলব্ধ।", "footer_desc": "RythuCrop — ভারতীয় কৃষকদের জন্য প্রিসিশন কৃষি সিদ্ধান্ত সহায়তা প্ল্যাটফর্ম।",
    "season_kharif": "খরিফ (বর্ষাকাল)", "season_rabi": "রবি (শীতকাল)", "season_summer": "জায়েদ (গ্রীষ্মকাল)", "season_whole_year": "সারা বছর",
    "soil_loamy": "দোআঁশ মাটি", "soil_black": "কালো মাটি", "soil_red": "লাল মাটি", "soil_clay": "এঁটেল মাটি", "soil_sandy": "বেলে মাটি", "soil_alluvial": "পলি মাটি",
    "water_good": "উত্তম জল প্রাপ্যতা (খাল / গভীর নলকূপ)", "water_moderate": "মাঝারি জল প্রাপ্যতা", "water_low": "স্বল্প জল প্রাপ্যতা (বৃষ্টি নির্ভর)", "water_rainfed": "সম্পূর্ণ বৃষ্টি নির্ভর (সেচহীন)",
    "goal_yield": "অধিক ফলন", "goal_water": "কম জলের ব্যবহার", "goal_cost": "কম চাষের খরচ", "goal_balanced": "ভারসাম্যপূর্ণ কৃষি",
    "exp_beginner": "নতুন কৃষক (১-২ বছর)", "exp_some": "কিছু অভিজ্ঞতা (৩-৫ বছর)", "exp_experienced": "অভিজ্ঞ কৃষক (৫+ বছর)",
    "priority_water": "জল সংরক্ষণ ও সেচ ব্যবস্থাপনা", "priority_fertilizer": "সার ও পুষ্টি উপাদান ব্যবস্থাপনা", "priority_pest": "বালাই ও রোগ নিয়ন্ত্রণ", "priority_harvest": "ফসল তোলা ও পরবর্তী যত্ন",
    "calculating": "প্রক্রিয়াকরণ চলছে…", "prediction_failed": "পূর্বাভাস ব্যর্থ হয়েছে", "server_error": "সার্ভারে সমস্যা হয়েছে। আবার চেষ্টা করুন।", "unit_tonnes_ha": "টন/হেক্টর", "unit_quintals_acre": "কুইন্টাল/একর",
    "reasons_label": "মূল কারণসমূহ:", "soil_label": "মাটি বিষয়ক পরামর্শ:", "water_label": "সেচ সময়সূচি:", "risks_label": "ঝুঁকি ও অনুমান:", "next_steps_label": "প্রস্তাবিত পদক্ষেপ:"
}
TRANSLATIONS["bn"] = BN_BASE

# Odia (od)
OD_BASE = {
    "nav_home": "ମୁଖ୍ୟ ପୃଷ୍ଠା", "nav_planning": "କୃଷି ଯୋଜନା", "nav_crop": "ଫସଲ ସୁପାରିଶ", "nav_yield": "ଅମଳ ଅନୁମାନ", "nav_advisory": "ସ୍ମାର୍ଟ ପରାମର୍ଶ", "nav_catalogue": "ଫସଲ ତାଲିକା", "nav_market": "ମଣ୍ଡି ଦର", "nav_storage": "ଗୋଦାମ ସନ୍ଧାନ", "nav_alerts": "ମୂଲ୍ୟ ସତର୍କତା", "nav_about": "ଆମ ବିଷୟରେ", "nav_login": "ଲଗଇନ୍ / ପଞ୍ଜୀକରଣ", "nav_logout": "ଲଗଆଉଟ୍", "user_welcome": "କୃଷକ ପ୍ରୋଫାଇଲ୍",
    "hero_badge": "ସ୍ମାର୍ଟ କୃଷି • ପ୍ରିସିସନ୍ କୃଷି ପ୍ରଯୁକ୍ତିବିଦ୍ୟା", "hero_title1": "ସ୍ମାର୍ଟ କୃଷି.", "hero_title2": "ଭଲ ନିଷ୍ପତ୍ତି.", "hero_desc": "RythuCrop ଭାରତୀୟ କୃଷକମାନଙ୍କୁ ଆଞ୍ଚଳିକ ଫସଲ ସୁପାରିଶ, ସଠିକ୍ ଅମଳ ଅନୁମାନ, ଏଗମାର୍କନେଟ୍ ହୋଲସେଲ ମଣ୍ଡି ଦର ଏବଂ ଶୀତଳ ଭଣ୍ଡାର ତଥ୍ୟ ପ୍ରଦାନ କରେ।", "hero_btn1": "ଯୋଜନା ଆରମ୍ଭ କରନ୍ତୁ", "hero_btn2": "ମଣ୍ଡି ଦର ଦେଖନ୍ତୁ", "hero_card_title": "ନିଷ୍ପତ୍ତି ସହାୟତା", "hero_card_main": "ମାଟିରୁ ମଣ୍ଡି ପର୍ଯ୍ୟନ୍ତ", "hero_card_desc": "ସଠିକ୍ ତଥ୍ୟ ଏବଂ ମେସିନ୍ ଲର୍ଣ୍ଣିଂ ସାହାଯ୍ୟରେ ସଠିକ୍ ନିଷ୍ପତ୍ତି ନିଅନ୍ତୁ।",
    "loc_state": "ରାଜ୍ୟ", "loc_district": "ଜିଲ୍ଲା", "loc_mandal": "ବ୍ଲକ୍ / ତହସିଲ୍", "loc_season": "ଋତୁ", "loc_year": "ଫସଲ ବର୍ଷ", "loc_apply": "ସ୍ଥାନ ସେଟ୍ କରନ୍ତୁ",
    "plan_eyebrow": "କୃଷି ଯୋଜନା", "plan_title": "ଆପଣଙ୍କ ଜମି ବିଷୟରେ କୁହନ୍ତୁ", "plan_desc": "ସରଳ ବିକଳ୍ପ ବାଛନ୍ତୁ। RythuCrop ପାଣି, ମାଟି ଏବଂ ବିପଦ ବିଚାର କରି ଏକ ଉପଯୁକ୍ତ ଫସଲ ଯୋଜନା ପ୍ରସ୍ତୁତ କରେ।",
    "land": "ଜମିର କ୍ଷେତ୍ରଫଳ (ଏକର)", "season": "ଋତୁ", "soil": "ମାଟିର ପ୍ରକାର", "irrigation": "ଜଳ ଉପଲବ୍ଧତା", "goal": "ମୁଖ୍ୟ ଲକ୍ଷ୍ୟ", "experience": "କୃଷି ଅଭିଜ୍ଞତା", "generate_plan": "ଯୋଜନା ପ୍ରସ୍ତୁତ କରନ୍ତୁ", "plan_result_label": "ସୁପାରିଶ କରାଯାଇଥିବା ଫସଲ", "plan_result_title": "ପରାମର୍ଶ ଏଠାରେ ଦେଖାଯିବ", "plan_result_desc": "ଆବଶ୍ୟକତା ବାଛି ଯୋଜନା ପ୍ରସ୍ତୁତ କରନ୍ତୁ।",
    "crop_eyebrow": "ଫସଲ ସୁପାରିଶ", "crop_title": "ଆପଣଙ୍କ ମାଟି ପାଇଁ ଉପଯୁକ୍ତ ଫସଲ ଖୋଜନ୍ତୁ", "crop_desc": "ଫସଲ ସୁପାରିଶ ପାଇଁ ମାଟିର ପୋଷକ ତତ୍ତ୍ୱ ଏବଂ ଜଳବାୟୁ ତଥ୍ୟ ଦିଅନ୍ତୁ।",
    "nitrogen": "ଯବକ୍ଷାରଜାନ (N) kg/ha", "phosphorus": "ଫସଫରସ୍ (P) kg/ha", "potassium": "ପୋଟାସ୍ (K) kg/ha", "temperature": "ତାପମାତ୍ରା (°C)", "humidity": "ଆର୍ଦ୍ରତା (%)", "soil_ph": "ମାଟିର pH", "rainfall": "ବୃଷ୍ଟିପାତ (mm)", "recommend_btn": "ଫସଲ ସୁପାରିଶ ପାଆନ୍ତୁ", "recommended": "ପ୍ରମୁଖ ସୁପାରିଶ", "crop_result_desc": "୫୧ଟି ଫସଲ ଉପରେ ପ୍ରଶିକ୍ଷିତ ମେସିନ୍ ଲର୍ଣ୍ଣିଂ ମଡେଲ୍ ଦ୍ୱାରା ନିର୍ଦ୍ଧାରିତ।", "crop_rank_1": "#୧ ଫସଲ", "crop_rank_2": "#୨ ଫସଲ", "crop_rank_3": "#୩ ଫସଲ",
    "yield_eyebrow": "ଅମଳ ଅନୁମାନ", "yield_title": "ଅମଳ ପୂର୍ବରୁ ଉତ୍ପାଦନ ଆକଳନ କରନ୍ତୁ", "yield_desc": "ରାଜ୍ୟ, ଫସଲ, ଜମି ଓ ବର୍ଷା ଆଧାରରେ ପ୍ରକୃତ ଅମଳ ଅନୁମାନ।",
    "yield_crop": "ଫସଲ", "crop_year": "ଫସଲ ବର୍ଷ", "yield_season": "ଋତୁ", "state": "ରାଜ୍ୟ", "area": "ଚାଷ ଜମି", "area_unit_label": "ଏକକ", "unit_acres": "ଏକର", "unit_hectares": "ହେକ୍ଟର", "annual_rainfall": "ବାର୍ଷିକ ବର୍ଷା (mm, ଇଚ୍ଛାଧୀନ)", "fertilizer": "ଖତ ସାର (kg, ଇଚ୍ଛାଧୀନ)", "pesticide": "କୀଟନାଶକ (kg, ଇଚ୍ଛାଧୀନ)", "yield_btn": "ଅମଳ ଅନୁମାନ କରନ୍ତୁ", "predicted": "ଅନୁମାନିତ ଅମଳ", "yield_result_desc": "ଭାରତ ସରକାରଙ୍କ ଅର୍ଥନୀତି ଓ ପରିସଂଖ୍ୟାନ ନିର୍ଦ୍ଦେଶାଳୟର ତଥ୍ୟ ଆଧାରରେ।", "estimated_production_label": "ମୋଟ ଆକଳିତ ଉତ୍ପାଦନ",
    "advisory_eyebrow": "ସ୍ମାର୍ଟ ପରାମର୍ଶ", "advisory_title": "ଫସଲ ଯତ୍ନ ଏବଂ କୃଷି ନିର୍ଦ୍ଦେଶାବଳୀ", "advisory_desc": "ଜଳସେଚନ, ଖତ ସାର ପରିଚାଳନା ଏବଂ କୀଟ ନିୟନ୍ତ୍ରଣ ଉପରେ ବ୍ୟବହାରିକ ପରାମର୍ଶ।",
    "advisory_crop": "ଫସଲ ବାଛନ୍ତୁ", "advisory_priority": "ପ୍ରାଥମିକତା", "get_advice": "ପରାମର୍ଶ ଦେଖନ୍ତୁ", "advice_label": "କୃଷି ପରାମର୍ଶ", "advice_title": "ମାର୍ଗଦର୍ଶନ ଦେଖିବାକୁ ପ୍ରାଥମିକତା ଚୟନ କରନ୍ତୁ",
    "catalogue_eyebrow": "ଫସଲ ତାଲିକା", "catalogue_title": "ପ୍ରମାଣିତ ଫସଲର ବିସ୍ତୃତ ତଥ୍ୟ", "catalogue_desc": "ଶସ୍ୟ, ଡାଲିଜାତୀୟ, ତୈଳବୀଜ, ପନିପରିବା ଏବଂ ଫଳ ଚାଷର ବିବରଣୀ।",
    "cat_filter_category": "ବିଭାଗ", "cat_filter_season": "ଋତୁ", "cat_search_placeholder": "ଫସଲ ନାମରେ ଖୋଜନ୍ତୁ...", "cat_all": "ସମସ୍ତ", "badge_ml": "ML ସୁପାରିଶ ଉପଲବ୍ଧ", "badge_yield": "ଅମଳ ମଡେଲ୍", "badge_mandi": "ମଣ୍ଡି ଦର", "badge_storage": "ଭଣ୍ଡାର ସୁବିଧା",
    "mandi_eyebrow": "କୃଷି ମଣ୍ଡି ଦର", "mandi_title": "ପାଇକାରୀ ମଣ୍ଡି ଦର ଏବଂ ବିକ୍ରୟ ପରାମର୍ଶ", "mandi_desc": "ସରକାରୀ ମଣ୍ଡି ଦର ଏବଂ ଅମଳ ପରେ ବିକ୍ରି ବନାମ ସାଇତି ରଖିବାର ଲାଭ-କ୍ଷତି ହିସାବ।",
    "mandi_select_crop": "ଫସଲ ବାଛନ୍ତୁ", "mandi_select_state": "ରାଜ୍ୟ", "mandi_select_district": "ଜିଲ୍ଲା", "mandi_search_btn": "ମଣ୍ଡି ଦର ଦେଖନ୍ତୁ", "mandi_modal_price": "ହାରାହାରି ଦର", "mandi_min_max": "ସର୍ବନିମ୍ନ – ସର୍ବୋଚ୍ଚ ଦର", "mandi_market_name": "ମଣ୍ଡି ୟାର୍ଡ", "mandi_arrival_date": "ରିପୋର୍ଟ ତାରିଖ", "mandi_trend": "୩୦ ଦିନର ଟ୍ରେଣ୍ଡ", "selling_guidance_title": "ବିକ୍ରୟ ବନାମ ସାଇତିବା ବିଶ୍ଳେଷଣ", "calc_selling_btn": "ଲାଭ-କ୍ଷତି ଗଣନା କରନ୍ତୁ", "distance_km": "ମଣ୍ଡିର ଦୂରତା (କି.ମି)", "holding_days": "ରଖିବା ଅବଧି (ଦିନ)",
    "storage_eyebrow": "ଗୋଦାମ ଓ ଶୀତଳ ଭଣ୍ଡାର", "storage_title": "ନିକଟସ୍ଥ ଶସ୍ୟ ଗୋଦାମ ଏବଂ କୋଲ୍ଡ ଷ୍ଟୋରେଜ୍", "storage_desc": "ଫସଲ ନଷ୍ଟ ନହେବା ଏବଂ ଉପଯୁକ୍ତ ମୂଲ୍ୟ ପାଇବା ପାଇଁ ପଞ୍ଜୀକୃତ ଗୋଦାମ ଖୋଜନ୍ତୁ।",
    "storage_filter_type": "ଭଣ୍ଡାର ପ୍ରକାର", "storage_all_types": "ସମସ୍ତ ପ୍ରକାର", "storage_grain": "ଶସ୍ୟ ଗୋଦାମ (ସାଧାରଣ)", "storage_cold": "ଶୀତଳ ଭଣ୍ଡାର (କୋଲ୍ଡ ଷ୍ଟୋରେଜ୍)", "storage_search_btn": "ଗୋଦାମ ଖୋଜନ୍ତୁ", "storage_capacity": "କ୍ଷମତା", "storage_status": "ସ୍ଥିତି", "storage_contact": "ଯୋଗାଯୋଗ",
    "alert_eyebrow": "ମୂଲ୍ୟ ସତର୍କତା", "alert_title": "ମଣ୍ଡି ଦର ନୋଟିଫିକେସନ୍ ପାଆନ୍ତୁ", "alert_desc": "ମଣ୍ଡି ଦର ଆପଣଙ୍କ ଲକ୍ଷ୍ୟ ମୂଲ୍ୟରେ ପହଞ୍ଚିଲେ ମୋବାଇଲ୍‌ରେ ସୂଚନା ପାଆନ୍ତୁ।",
    "alert_mobile": "ମୋବାଇଲ୍ ନମ୍ବର", "alert_target_price": "ଲକ୍ଷ୍ୟ ମୂଲ୍ୟ (₹/କ୍ୱିଣ୍ଟାଲ)", "alert_condition": "ଯେତେବେଳେ ମୂଲ୍ୟ ହେବ", "cond_above": "ସମାନ କିମ୍ବା ଅଧିକ", "cond_below": "ସମାନ କିମ୍ବା କମ୍", "alert_subscribe_btn": "ସତର୍କତା ପଞ୍ଜୀକରଣ କରନ୍ତୁ", "alert_my_subscriptions": "ମୋର ସକ୍ରିୟ ସତର୍କତା", "alert_no_active": "ଏହି ନମ୍ବର ପାଇଁ କୌଣସି ସକ୍ରିୟ ସତର୍କତା ନାହିଁ।",
    "auth_modal_title": "କୃଷକ ମୋବାଇଲ୍ ଲଗଇନ୍", "auth_modal_desc": "ଯୋଜନା ସାଇତିବାକୁ ଏବଂ ମୂଲ୍ୟ ସତର୍କତା ପାଇବାକୁ ଲଗଇନ୍ କରନ୍ତୁ।", "auth_mobile_label": "୧୦ ଅଙ୍କ ବିଶିଷ୍ଟ ମୋବାଇଲ୍ ନମ୍ବର", "auth_request_otp": "OTP ପଠାନ୍ତୁ", "auth_otp_label": "୬ ଅଙ୍କ ବିଶିଷ୍ଟ OTP ଦିଅନ୍ତୁ", "auth_verify_btn": "ଯାଞ୍ଚ କରି ଲଗଇନ୍ କରନ୍ତୁ", "auth_dev_notice": "ଡେଭଲପମେଣ୍ଟ ମୋଡ୍ ସକ୍ରିୟ: OTP ସ୍କ୍ରିନ୍‌ରେ ଦେଖାଯାଉଛି।",
    "about_eyebrow": "RYTHUCROP ବିଷୟରେ", "about_title": "ଭାରତୀୟ କୃଷି ପାଇଁ ସ୍ୱଚ୍ଛ ପ୍ରଯୁକ୍ତିବିଦ୍ୟା", "about_desc": "ଚାଷୀମାନଙ୍କୁ ବିଶ୍ୱସନୀୟ ନିଷ୍ପତ୍ତି ନେବାରେ ସାହାଯ୍ୟ କରିବାକୁ କୃଷି ତଥ୍ୟ ଓ ମଡେଲ୍‌କୁ ସଂଯୋଗ କରେ।", "about_ml": "ମେସିନ୍ ଲର୍ଣ୍ଣିଂ", "about_ml_desc": "ତଥ୍ୟ ଲିକ୍ ବିନା ସରକାରୀ ପରିସଂଖ୍ୟାନ ସହିତ ପ୍ରଶିକ୍ଷିତ ମଡେଲ୍।", "about_farmer": "କୃଷକ ପ୍ରଥମ", "about_farmer_desc": "ସରଳ ମାତୃଭାଷା ଏବଂ ସ୍ପଷ୍ଟ ମାର୍ଗଦର୍ଶନ।", "about_mobile": "ସମସ୍ତ ଉପକରଣରେ ଏବଂ ବହୁଭାଷୀ", "about_mobile_desc": "ମୋବାଇଲ୍, ଟାବଲେଟ୍ ଏବଂ କମ୍ପ୍ୟୁଟରରେ ୯ଟି ଭାରତୀୟ ଭାଷାରେ ଉପଲବ୍ଧ।", "footer_desc": "RythuCrop — ଭାରତୀୟ କୃଷକମାନଙ୍କ ପାଇଁ ସଠିକ୍ କୃଷି ନିଷ୍ପତ୍ତି ସହାୟତା ପ୍ଲାଟଫର୍ମ।",
    "season_kharif": "ଖରିଫ (ବର୍ଷା ଦିନ)", "season_rabi": "ରବି (ଶୀତ ଦିନ)", "season_summer": "ଜାଏଦ (ଖରା ଦିନ)", "season_whole_year": "ବର୍ଷ ତମାମ",
    "soil_loamy": "ଦୋରସା ମାଟି", "soil_black": "କଳା ମାଟି", "soil_red": "ନାଲି ମାଟି", "soil_clay": "ମଟାଳ ମାଟି", "soil_sandy": "ବାଲିଆ ମାଟି", "soil_alluvial": "ପଟୁ ମାଟି",
    "water_good": "ଉତ୍ତମ ଜଳସେଚନ (କେନାଲ / ବୋରୱେଲ)", "water_moderate": "ମଧ୍ୟମ ଜଳ ଉପଲବ୍ଧତା", "water_low": "ସ୍ୱଳ୍ପ ଜଳ ଉପଲବ୍ଧତା (ବର୍ଷା ଉପରେ ନିର୍ଭର)", "water_rainfed": "ସମ୍ପୂର୍ଣ୍ଣ ବର୍ଷା ନିର୍ଭରଶୀଳ (ଜଳସେଚନ ନାହିଁ)",
    "goal_yield": "ଅଧିକ ଅମଳ", "goal_water": "କମ୍ ଜଳ ବ୍ୟବହାର", "goal_cost": "କମ୍ ଖର୍ଚ୍ଚ", "goal_balanced": "ସନ୍ତୁଳିତ କୃଷି",
    "exp_beginner": "ନୂତନ କୃଷକ (୧-୨ ବର୍ଷ)", "exp_some": "କିଛି ଅଭିଜ୍ଞତା (୩-୫ ବର୍ଷ)", "exp_experienced": "ଅଭିଜ୍ଞ କୃଷକ (୫+ ବର୍ଷ)",
    "priority_water": "ଜଳ ସଂରକ୍ଷଣ ଏବଂ ଜଳସେଚନ", "priority_fertilizer": "ଖତ ସାର ଓ ପୋଷକ ପରିଚାଳନା", "priority_pest": "ରୋଗ ପୋକ ନିୟନ୍ତ୍ରଣ", "priority_harvest": "ଅମଳ ଏବଂ ଅମଳ ପରବର୍ତ୍ତୀ ଯତ୍ନ",
    "calculating": "ପ୍ରକ୍ରିୟା ଚାଲିଛି…", "prediction_failed": "ଅନୁମାନ ବିଫଳ ହେଲା", "server_error": "ସର୍ଭର ତ୍ରୁଟି। ଦୟାକରି ପୁଣି ଚେଷ୍ଟା କରନ୍ତୁ।", "unit_tonnes_ha": "ଟନ୍/ହେକ୍ଟର", "unit_quintals_acre": "କ୍ୱିଣ୍ଟାଲ/ଏକର",
    "reasons_label": "ମୁଖ୍ୟ କାରଣ:", "soil_label": "ମାଟି ପରାମର୍ଶ:", "water_label": "ଜଳସେଚନ ସମୟସୂଚୀ:", "risks_label": "ବିପଦ ଓ ଆକଳନ:", "next_steps_label": "ସୁପାରିଶ କରାଯାଇଥିବା ପଦକ୍ଷେପ:"
}
TRANSLATIONS["od"] = OD_BASE

# Localized Crop Names in all 9 languages
LOCALIZED_CROP_NAMES = {
    "rice": {
        "en": "Rice (Paddy)", "te": "వరి", "hi": "चावल / धान", "ta": "நெல்",
        "kn": "ಭತ್ತ", "ml": "നെല്ല്", "mr": "भात / तांदूळ", "bn": "ধান", "od": "ଧାନ"
    },
    "wheat": {
        "en": "Wheat", "te": "గోధుమ", "hi": "गेहूं", "ta": "கோதுமை",
        "kn": "ಗೋಧಿ", "ml": "ഗോതമ്പ്", "mr": "गहू", "bn": "গম", "od": "ଗହମ"
    },
    "maize": {
        "en": "Maize (Corn)", "te": "మొక్కజొన్న", "hi": "मक्का", "ta": "மக்காச்சோளம்",
        "kn": "ಮೆಕ್ಕೆಜೋಳ", "ml": "ചോളം", "mr": "मका", "bn": "ভুট্টা", "od": "ମକା"
    },
    "cotton": {
        "en": "Cotton", "te": "పత్తి", "hi": "कपास", "ta": "பருத்தி",
        "kn": "ಹತ್ತಿ", "ml": "പരുത്തി", "mr": "कापूस", "bn": "তুলা", "od": "କପା"
    },
    "groundnut": {
        "en": "Groundnut (Peanut)", "te": "వేరుశనగ", "hi": "मूंगफली", "ta": "நிலக்கடலை",
        "kn": "ಕಡಲೆಕಾಯಿ", "ml": "നിലക്കടല", "mr": "भुईमूग", "bn": "চিনাবাদাম", "od": "ଚିନାବାଦାମ"
    },
    "arhar_tur": {
        "en": "Red Gram (Arhar / Tur)", "te": "కందులు", "hi": "अरहर / तूर", "ta": "துவரை",
        "kn": "ತೊಗರಿ", "ml": "തുവര", "mr": "तूर", "bn": "অড়হর", "od": "ହରଡ଼"
    },
    "gram": {
        "en": "Bengal Gram (Chickpea)", "te": "శనగలు", "hi": "चना", "ta": "கொண்டைக்கடலை",
        "kn": "ಕಡಲೆ", "ml": "കടല", "mr": "हरभरा", "bn": "ছোলা", "od": "ଚଣା / ବୁଟ"
    },
    "sugarcane": {
        "en": "Sugarcane", "te": "చెరకు", "hi": "गन्ना", "ta": "கரும்பு",
        "kn": "ಕಬ್ಬು", "ml": "കരിമ്പ്", "mr": "ऊस", "bn": "আখ", "od": "ଆଖୁ"
    },
    "soyabean": {
        "en": "Soybean", "te": "సోయాబీన్", "hi": "सोयाबीन", "ta": "சோயாபீன்",
        "kn": "ಸೋಯಾಬೀನ್", "ml": "സോയാബീൻ", "mr": "सोयाबीन", "bn": "সয়াবিন", "od": "ସୋୟାବିନ୍"
    },
    "onion": {
        "en": "Onion", "te": "ఉల్లిపాయ", "hi": "प्याज", "ta": "வெங்காயம்",
        "kn": "ಈರುಳ್ಳಿ", "ml": "ഉള്ളി", "mr": "कांदा", "bn": "পেঁয়াজ", "od": "ପିଆଜ"
    },
    "potato": {
        "en": "Potato", "te": "బంగాళాదుంప", "hi": "आलू", "ta": "உருளைக்கிழங்கு",
        "kn": "ಆಲೂಗಡ್ಡೆ", "ml": "ഉരുളക്കിഴങ്ങ്", "mr": "बटाटा", "bn": "আলু", "od": "ଆଳୁ"
    },
    "tomato": {
        "en": "Tomato", "te": "టమోటా", "hi": "टमाटर", "ta": "தக்காளி",
        "kn": "ಟೊಮೆಟೊ", "ml": "തക്കാളി", "mr": "टोमॅटो", "bn": "টমেটো", "od": "ଟମାଟୋ"
    },
    "banana": {
        "en": "Banana", "te": "అరటి", "hi": "केला", "ta": "வாழை",
        "kn": "ಬಾಳೆಹಣ್ಣು", "ml": "വാഴപ്പഴം", "mr": "केळी", "bn": "কলা", "od": "କଦଳୀ"
    },
    "coconut": {
        "en": "Coconut", "te": "కొబ్బరి", "hi": "नारियल", "ta": "தேங்காய்",
        "kn": "ತೆಂಗಿನಕಾಯಿ", "ml": "തേങ്ങ", "mr": "नारळ", "bn": "নারকেল", "od": "ନଡ଼ିଆ"
    },
    "mango": {
        "en": "Mango", "te": "మామిడి", "hi": "आम", "ta": "மாம்பழம்",
        "kn": "ಮಾವಿನಹಣ್ಣು", "ml": "മാങ്ങ", "mr": "आंबा", "bn": "আম", "od": "ଆମ୍ବ"
    },
    "turmeric": {
        "en": "Turmeric", "te": "పసుపు", "hi": "हल्दी", "ta": "மஞ்சள்",
        "kn": "ಅರಿಶಿನ", "ml": "മഞ്ഞൾ", "mr": "हळद", "bn": "হলুদ", "od": "ହଳଦୀ"
    },
    "dry_chillies": {
        "en": "Dry Chillies", "te": "ఎండు మిరప", "hi": "सूखी मिर्च", "ta": "காய்ந்த மிளகாய்",
        "kn": "ಒಣ ಮೆಣಸಿನಕಾಯಿ", "ml": "വറ്റൽമുളക്", "mr": "सुकलेली मिरची", "bn": "শুকনো লঙ্কা", "od": "ଶୁଖିଲା ଲଙ୍କା"
    },
    "black_pepper": {
        "en": "Black Pepper", "te": "నల్ల మిరియాలు", "hi": "काली मिर्च", "ta": "மிளகு",
        "kn": "ಕರಿಮೆಣಸು", "ml": "കുരുമുളക്", "mr": "काळी मिरी", "bn": "গোলমরিচ", "od": "ଗୋଲମରିଚ"
    },
    "jute": {
        "en": "Jute", "te": "జనపనార", "hi": "जूट", "ta": "சணல்",
        "kn": "ಸೆಣಬು", "ml": "ചണം", "mr": "ताग", "bn": "পাট", "od": "ଝୋଟ"
    },
    "bajra": {
        "en": "Bajra (Pearl Millet)", "te": "సజ్జలు", "hi": "बाजरा", "ta": "கம்பு",
        "kn": "ಸಜ್ಜೆ", "ml": "കമ്പം", "mr": "बाजरी", "bn": "বাজরা", "od": "ବାଜରା"
    },
    "sunflower": {
        "en": "Sunflower", "te": "పొద్దుతిరుగుడు", "hi": "सूरजमुखी", "ta": "சூரியகாந்தி",
        "kn": "ಸೂರ್ಯಕಾಂತಿ", "ml": "സൂര്യകാന്തി", "mr": "सूर्यफूल", "bn": "সূর্যমুখী", "od": "ସୂର୍ଯ୍ୟମୁଖୀ"
    },
    "arecanut": {
        "en": "Arecanut", "te": "పోక చెక్క", "hi": "सुपारी", "ta": "பாக்கு",
        "kn": "ಅಡಿಕೆ", "ml": "അടയ്ക്ക", "mr": "सुपारी", "bn": "সুপারি", "od": "ଗୁଆ"
    },
    "tobacco": {
        "en": "Tobacco", "te": "పొగాకు", "hi": "तंबाकू", "ta": "புகையிலை",
        "kn": "ತಂಬಾಕು", "ml": "പുകയില", "mr": "तंबाखू", "bn": "তামাক", "od": "ଧୂଆଁପତ୍ର"
    },
    "castor_seed": {
        "en": "Castor Seed", "te": "ఆముదాలు", "hi": "अरंडी", "ta": "ஆமணக்கு",
        "kn": "ಔಡಲ ಬೀಜ", "ml": "ആവണക്ക്", "mr": "एरंडी", "bn": "রেড়ি বীজ", "od": "ଜଡ଼ା ମଞ୍ଜି"
    }
}


def export_translations_js():
    """Exports centralized translations to app/static/translations.js for frontend consumption."""
    static_dir = Path(__file__).resolve().parent.parent / "static"
    static_dir.mkdir(parents=True, exist_ok=True)
    out_file = static_dir / "translations.js"

    bundle = {
        "translations": TRANSLATIONS,
        "languages": LANGUAGES,
        "language_names": LANGUAGE_NAMES,
        "crop_names": LOCALIZED_CROP_NAMES
    }

    content = f"// Centralized Multilingual Translations for RythuCrop\nconst RYTHUCROP_I18N = {json.dumps(bundle, ensure_ascii=False, indent=2)};\n"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Exported multilingual translations to {out_file}")


if __name__ == "__main__":
    export_translations_js()
