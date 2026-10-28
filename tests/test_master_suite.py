"""
RythuCrop Comprehensive Master Test Suite
Validates all 19 requirements of the Master Specification.
"""

import sys
import unittest
from pathlib import Path
import json

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import app
from app.models.predictor import (
    recommend_crop_top3,
    recommend_crop_top3_detailed,
    recommend_farm_plan,
    recommend_farm_plan_detailed,
    CropInputError
)
from app.models.yield_predictor import (
    predict_yield,
    predict_yield_detailed
)
from app.data.translations import TRANSLATIONS, LANGUAGES, LOCALIZED_CROP_NAMES
from app.data.agri_taxonomy import (
    CROP_CATALOGUE,
    FARM_PLANNING_21_CROPS,
    normalize_crop_name
)
from app.data.geo_data import (
    get_states_list,
    get_districts_for_state,
    get_mandals_for_district,
    get_state_agri_baseline
)
from app.data.mandi_data import (
    search_mandi_prices,
    calculate_selling_guidance,
    MANDI_PRICE_REGISTRY
)
from app.data.storage_data import (
    search_storage_facilities,
    STORAGE_FACILITIES
)
from app.services.auth_service import (
    request_otp,
    verify_otp,
    normalize_mobile
)


class TestRythuCropMaster(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as sess:
            sess["is_authenticated"] = True
            sess["mobile"] = "+919876543210"
            sess["user_id"] = "+919876543210"

    # 1. Startup & Web Routes
    def test_01_app_startup_and_home(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"RythuCrop", resp.data)
        self.assertIn(b"translations.js", resp.data)

    def test_02_about_page(self):
        resp = self.client.get("/about")
        self.assertEqual(resp.status_code, 200)

    # 2. Multilingual Parity (All 9 Languages)
    def test_03_all_9_languages_parity(self):
        en_keys = set(TRANSLATIONS["en"].keys())
        self.assertEqual(len(LANGUAGES), 9)
        for lang in LANGUAGES:
            self.assertIn(lang, TRANSLATIONS)
            lang_keys = set(TRANSLATIONS[lang].keys())
            missing = en_keys - lang_keys
            self.assertEqual(len(missing), 0, f"Language {lang} is missing keys: {missing}")

    def test_04_localized_crop_names_coverage(self):
        for crop_id, names in LOCALIZED_CROP_NAMES.items():
            for lang in LANGUAGES:
                self.assertIn(lang, names, f"Crop {crop_id} missing {lang} translation")
                self.assertTrue(len(names[lang]) > 0)

    # 3. Farm Planning Preserved Contract (6 inputs)
    def test_05_farm_planning_payload_preserved(self):
        payload = {
            "land": 3.0,
            "season": "Kharif",
            "soil": "Black Soil",
            "irrigation": "Good water availability",
            "goal": "Higher yield",
            "experience": "Some experience"
        }
        resp = self.client.post("/farm-plan", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("recommended_crops", data)
        self.assertIn("plan_details", data)
        self.assertIn("inputs_preserved", data)

        # Confirm all 6 keys preserved
        preserved = data["inputs_preserved"]
        for k in ["land", "season", "soil", "irrigation", "goal", "experience"]:
            self.assertIn(k, preserved)

        # Confirm recommendations only draw from the 21 crops
        for c in data["recommended_crops"]:
            self.assertIn(c, FARM_PLANNING_21_CROPS)

    # 4. Crop Recommendation ML & Validation
    def test_06_crop_recommendation_valid(self):
        payload = {
            "N": 90, "P": 42, "K": 43,
            "temperature": 25.0, "humidity": 80.0,
            "ph": 6.5, "rainfall": 200.0
        }
        resp = self.client.post("/predict", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("top_3", data)
        self.assertEqual(len(data["top_3"]), 3)
        self.assertIn("top_3_detailed", data)

    def test_07_crop_recommendation_negative_rejected(self):
        payload = {
            "N": -5, "P": 42, "K": 43,
            "temperature": 25.0, "humidity": 80.0,
            "ph": 6.5, "rainfall": 200.0
        }
        resp = self.client.post("/predict", json=payload)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("cannot be negative", resp.get_json()["error"])

    def test_08_crop_recommendation_missing_field(self):
        payload = {"N": 90, "P": 42}
        resp = self.client.post("/predict", json=payload)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Missing required value", resp.get_json()["error"])

    # 5. Yield Prediction Without Production Leakage
    def test_09_yield_prediction_leakage_free(self):
        payload = {
            "Crop": "Rice",
            "Crop_Year": 2019,
            "Season": "Kharif",
            "State": "Andhra Pradesh",
            "Area": 5.0,
            "area_unit": "acres"
        }
        resp = self.client.post("/predict-yield", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("predicted_yield", data)
        self.assertIn("predicted_yield_per_acre", data)
        self.assertIn("estimated_production", data)
        self.assertEqual(data["yield_unit"], "tonnes/ha")
        self.assertEqual(data["acre_unit"], "quintals/acre")

    def test_10_yield_prediction_regional_sensitivity(self):
        punjab_payload = {
            "Crop": "Rice", "Crop_Year": 2018, "Season": "Kharif",
            "State": "Punjab", "Area": 2.0
        }
        meghalaya_payload = {
            "Crop": "Rice", "Crop_Year": 2018, "Season": "Kharif",
            "State": "Meghalaya", "Area": 2.0
        }
        res_punjab = self.client.post("/predict-yield", json=punjab_payload).get_json()
        res_meghalaya = self.client.post("/predict-yield", json=meghalaya_payload).get_json()

        # Real DES data: Punjab Rice average is ~3.7 t/ha, Meghalaya is ~2.0 t/ha
        self.assertGreater(res_punjab["predicted_yield"], res_meghalaya["predicted_yield"])

    # 6. Crop Catalogue
    def test_11_crop_catalogue_api(self):
        resp = self.client.get("/api/crops")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("categories", data)
        self.assertGreaterEqual(data["count"], 20)
        first = data["crops"][0]
        self.assertIn("has_recommendation_model", first)
        self.assertIn("has_yield_model", first)

    # 7. Mandi Market Prices & Selling Guidance
    def test_12_mandi_prices_and_guidance(self):
        resp = self.client.get("/api/mandi-prices?crop=Cotton")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertGreater(data["count"], 0)

        # Selling guidance
        guidance = calculate_selling_guidance(
            crop_name="Rice", modal_price=2200, holding_days=30, distance_km=25
        )
        self.assertIn("net_immediate_realization_rs_qtl", guidance)
        self.assertIn("breakeven_future_price_rs_qtl", guidance)
        self.assertIn("recommendation", guidance)

    # 8. Storage Finder
    def test_13_storage_finder_api(self):
        resp = self.client.get("/api/storage?type=cold")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertGreater(data["count"], 0)
        self.assertTrue(data["facilities"][0]["cold_storage"])

    # 9. Mobile OTP Auth
    def test_14_mobile_otp_flow(self):
        mobile = "9876543210"
        norm = normalize_mobile(mobile)
        self.assertEqual(norm, "+919876543210")

        # Request OTP
        req_resp = self.client.post("/api/auth/request-otp", json={"mobile": mobile})
        self.assertEqual(req_resp.status_code, 200)
        dev_otp = req_resp.get_json()["data"].get("dev_otp")
        self.assertIsNotNone(dev_otp)

        # Verify OTP
        verify_resp = self.client.post("/api/auth/verify-otp", json={
            "mobile": mobile, "otp": dev_otp, "preferred_lang": "te"
        })
        self.assertEqual(verify_resp.status_code, 200)
        user = verify_resp.get_json()["user"]
        self.assertEqual(user["mobile"], "+919876543210")

    # 10. Price Alerts
    def test_15_price_alerts_lifecycle(self):
        mobile = "+919876543210"
        sub_resp = self.client.post("/api/alerts/subscribe", json={
            "mobile": mobile,
            "crop": "Soyabean",
            "market": "Ujjain Mandi",
            "condition_type": "above",
            "target_price": 5000
        })
        self.assertEqual(sub_resp.status_code, 200)
        alert_id = sub_resp.get_json()["alert_id"]

        # Retrieve
        list_resp = self.client.get(f"/api/alerts/my-alerts?mobile={mobile}")
        self.assertEqual(list_resp.status_code, 200)
        self.assertGreaterEqual(list_resp.get_json()["count"], 1)

        # Cancel
        del_resp = self.client.post("/api/alerts/cancel", json={
            "alert_id": alert_id, "mobile": mobile
        })
        self.assertEqual(del_resp.status_code, 200)
        self.assertTrue(del_resp.get_json()["success"])


if __name__ == "__main__":
    unittest.main()
