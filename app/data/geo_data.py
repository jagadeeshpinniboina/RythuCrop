"""
Indian Geographic Hierarchy and Regional Agricultural Baselines
Maps States, Districts, Mandals, and Agro-Climatic Baselines.
"""

INDIAN_STATES_DISTRICTS = {
    "Andhra Pradesh": [
        "Kurnool", "Guntur", "Krishna", "East Godavari", "West Godavari",
        "Anantapur", "Chittoor", "Prakasam", "Srikakulam", "Vizianagaram",
        "Visakhapatnam", "YSR Kadapa", "Nellore"
    ],
    "Telangana": [
        "Warangal", "Karimnagar", "Nalgonda", "Khammam", "Nizamabad",
        "Mahabubnagar", "Medak", "Adilabad", "Rangareddy", "Suryapet",
        "Siddipet", "Jagtial", "Mancherial"
    ],
    "Punjab": [
        "Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda",
        "Firozpur", "Sangrur", "Gurdaspur", "Hoshiarpur", "Moga", "Fazilka"
    ],
    "Haryana": [
        "Karnal", "Hisar", "Ambala", "Rohtak", "Sirsa", "Kurukshetra",
        "Sonipat", "Panipat", "Yamunanagar", "Fatehabad", "Bhiwani"
    ],
    "Uttar Pradesh": [
        "Varanasi", "Prayagraj", "Gorakhpur", "Meerut", "Bareilly",
        "Agra", "Aligarh", "Lucknow", "Ayodhya", "Budaun", "Bulandshahr",
        "Muzaffarnagar", "Saharanpur", "Moradabad"
    ],
    "Maharashtra": [
        "Nashik", "Pune", "Ahmednagar", "Solapur", "Kolhapur",
        "Chhatrapati Sambhajinagar", "Nagpur", "Jalgaon", "Amravati",
        "Yavatmal", "Nanded", "Satara", "Sangli"
    ],
    "Karnataka": [
        "Belagavi", "Mysuru", "Mandya", "Shivamogga", "Ballari",
        "Vijayapura", "Davanagere", "Hassan", "Tumakuru", "Bagalkote",
        "Dharwad", "Kalaburagi", "Udupi", "Chikkamagaluru"
    ],
    "Tamil Nadu": [
        "Thanjavur", "Madurai", "Coimbatore", "Salem", "Tiruchirappalli",
        "Tirunelveli", "Erode", "Dindigul", "Villupuram", "Cuddalore",
        "Tiruvarur", "Nagapattinam", "Tiruppur"
    ],
    "Kerala": [
        "Palakkad", "Wayanad", "Alappuzha", "Idukki", "Thrissur",
        "Kottayam", "Ernakulam", "Kozhikode", "Malappuram", "Kannur"
    ],
    "West Bengal": [
        "Purba Bardhaman", "Murshidabad", "Nadia", "Hooghly", "Paschim Medinipur",
        "North 24 Parganas", "South 24 Parganas", "Malda", "Birbhum", "Bankura"
    ],
    "Bihar": [
        "Patna", "Muzaffarpur", "Gaya", "Bhagalpur", "Samastipur",
        "Rohtas", "Purnia", "Darbhanga", "Begusarai", "Nalanda", "Siwan"
    ],
    "Madhya Pradesh": [
        "Indore", "Ujjain", "Bhopal", "Jabalpur", "Hoshangabad",
        "Sehore", "Dewas", "Dhar", "Khargone", "Sagar", "Vidisha"
    ],
    "Gujarat": [
        "Rajkot", "Junagadh", "Surat", "Vadodara", "Ahmedabad",
        "Bhavnagar", "Amreli", "Banaskantha", "Mehsana", "Kheda", "Bharuch"
    ],
    "Rajasthan": [
        "Sri Ganganagar", "Kota", "Hanumangarh", "Jaipur", "Alwar",
        "Barmer", "Bikaner", "Nagaur", "Jodhpur", "Bharatpur", "Chittorgarh"
    ],
    "Odisha": [
        "Bargarh", "Ganjam", "Sambalpur", "Cuttack", "Balasore",
        "Kalahandi", "Bolangir", "Puri", "Koraput", "Mayurbhanj"
    ],
    "Assam": [
        "Kamrup", "Nagaon", "Sonitpur", "Dibrugarh", "Barpeta",
        "Cachar", "Jorhat", "Golaghat", "Darrang", "Lakhimpur"
    ],
    "Meghalaya": [
        "East Khasi Hills", "West Garo Hills", "Ri-Bhoi", "West Khasi Hills",
        "East Jaintia Hills", "South Garo Hills"
    ],
    "Himachal Pradesh": [
        "Shimla", "Kullu", "Kangra", "Mandi", "Solan", "Chamba", "Sirmaur"
    ],
    "Uttarakhand": [
        "Dehradun", "Haridwar", "Udham Singh Nagar", "Nainital", "Almora", "Pauri Garhwal"
    ],
    "Chhattisgarh": [
        "Raipur", "Durg", "Rajnandgaon", "Bilaspur", "Janjgir-Champa", "Bastar", "Dhamtari"
    ],
    "Jharkhand": [
        "Ranchi", "Hazaribagh", "Palamu", "Giridih", "Deoghar", "East Singhbhum"
    ],
    "Goa": [
        "North Goa", "South Goa"
    ],
    "Tripura": [
        "West Tripura", "South Tripura", "Dhalai", "North Tripura"
    ],
    "Manipur": [
        "Imphal West", "Imphal East", "Thoubal", "Bishnupur"
    ],
    "Mizoram": [
        "Aizawl", "Lunglei", "Champhai", "Kolasib"
    ],
    "Nagaland": [
        "Kohima", "Dimapur", "Mokokchung", "Wokha"
    ],
    "Arunachal Pradesh": [
        "Papum Pare", "East Siang", "West Kameng", "Changlang"
    ],
    "Sikkim": [
        "East Sikkim", "West Sikkim", "South Sikkim", "North Sikkim"
    ],
    "Puducherry": [
        "Puducherry", "Karaikal", "Yanam", "Mahe"
    ],
    "Delhi": [
        "North Delhi", "South Delhi", "West Delhi", "North West Delhi"
    ],
    "Jammu and Kashmir": [
        "Srinagar", "Jammu", "Anantnag", "Baramulla", "Pulwama", "Kathua"
    ]
}

# Subdistricts / Mandals for key agricultural zones
DISTRICT_MANDALS = {
    "Kurnool": ["Adoni", "Alur", "Banaganapalle", "Dhone", "Koilkuntla", "Nandyal", "Pattikonda", "Yemmiganur"],
    "Guntur": ["Tenali", "Bapatla", "Narasaraopet", "Sattenapalle", "Mangalagiri", "Ponnur", "Vinukonda"],
    "Warangal": ["Narsampet", "Parkal", "Wardhannapet", "Geesugonda", "Atmakur", "Dharmasagar"],
    "Ludhiana": ["Jagraon", "Khanna", "Samrala", "Payal", "Raikot"],
    "Nashik": ["Niphad", "Dindori", "Malegaon", "Sinnar", "Yeola", "Kalwan"],
    "Belagavi": ["Athani", "Bailhongal", "Chikkodi", "Gokak", "Hukkeri", "Raybag"],
    "Thanjavur": ["Kumbakonam", "Papanasam", "Pattukkottai", "Orathanadu", "Thiruvaiyaru"],
    "Palakkad": ["Alathur", "Chittur", "Mannarkkad", "Ottappalam", "Pattambi"],
    "Burdwan": ["Kalna", "Katwa", "Memari", "Galsi", "Bhatar"],
    "East Khasi Hills": ["Mawkynrew", "Mylliem", "Shella Bholaganj", "Pynursla", "Sohra"]
}

# State-level historical averages for climate and fertilizer baseline
STATE_AGRI_BASELINES = {
    "Andhra Pradesh": {"rainfall": 916, "fertilizer_per_ha": 155, "pesticide_per_ha": 0.35},
    "Telangana": {"rainfall": 940, "fertilizer_per_ha": 160, "pesticide_per_ha": 0.38},
    "Punjab": {"rainfall": 649, "fertilizer_per_ha": 245, "pesticide_per_ha": 0.75},
    "Haryana": {"rainfall": 560, "fertilizer_per_ha": 220, "pesticide_per_ha": 0.65},
    "Uttar Pradesh": {"rainfall": 980, "fertilizer_per_ha": 175, "pesticide_per_ha": 0.45},
    "Maharashtra": {"rainfall": 1150, "fertilizer_per_ha": 135, "pesticide_per_ha": 0.40},
    "Karnataka": {"rainfall": 1180, "fertilizer_per_ha": 140, "pesticide_per_ha": 0.35},
    "Tamil Nadu": {"rainfall": 998, "fertilizer_per_ha": 185, "pesticide_per_ha": 0.42},
    "Kerala": {"rainfall": 2850, "fertilizer_per_ha": 95, "pesticide_per_ha": 0.25},
    "West Bengal": {"rainfall": 1750, "fertilizer_per_ha": 165, "pesticide_per_ha": 0.48},
    "Bihar": {"rainfall": 1163, "fertilizer_per_ha": 145, "pesticide_per_ha": 0.30},
    "Madhya Pradesh": {"rainfall": 1050, "fertilizer_per_ha": 95, "pesticide_per_ha": 0.22},
    "Gujarat": {"rainfall": 820, "fertilizer_per_ha": 145, "pesticide_per_ha": 0.40},
    "Rajasthan": {"rainfall": 530, "fertilizer_per_ha": 65, "pesticide_per_ha": 0.18},
    "Odisha": {"rainfall": 1450, "fertilizer_per_ha": 70, "pesticide_per_ha": 0.20},
    "Assam": {"rainfall": 2100, "fertilizer_per_ha": 75, "pesticide_per_ha": 0.15},
    "Meghalaya": {"rainfall": 2600, "fertilizer_per_ha": 25, "pesticide_per_ha": 0.08},
    "Himachal Pradesh": {"rainfall": 1250, "fertilizer_per_ha": 60, "pesticide_per_ha": 0.20},
    "Uttarakhand": {"rainfall": 1550, "fertilizer_per_ha": 130, "pesticide_per_ha": 0.25},
    "Chhattisgarh": {"rainfall": 1267, "fertilizer_per_ha": 90, "pesticide_per_ha": 0.20},
    "Jharkhand": {"rainfall": 1280, "fertilizer_per_ha": 65, "pesticide_per_ha": 0.15}
}


def get_states_list():
    return sorted(list(INDIAN_STATES_DISTRICTS.keys()))


def get_districts_for_state(state: str):
    return INDIAN_STATES_DISTRICTS.get(state, ["All Districts"])


def get_mandals_for_district(district: str):
    return DISTRICT_MANDALS.get(district, ["Central Mandal", "North Mandal", "South Mandal", "East Mandal", "West Mandal"])


def get_state_agri_baseline(state: str):
    return STATE_AGRI_BASELINES.get(
        state,
        {"rainfall": 1000, "fertilizer_per_ha": 120, "pesticide_per_ha": 0.30}
    )
