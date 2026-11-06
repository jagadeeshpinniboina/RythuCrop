import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["RYTHUCROP_DEV_AUTH"] = "true"

import unittest
from app import app
from app.models.yield_predictor import evaluate_seasonal_feasibility, predict_yield_detailed


class TestSeasonalYieldReactivity(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_rabi_strict_crops_in_wrong_seasons(self):
        """Wheat, Barley, Gram should fail in Kharif and Summer with 0 yield."""
        # Wheat in Kharif
        wheat_kharif = evaluate_seasonal_feasibility("Wheat", "Kharif (Monsoon)")
        self.assertFalse(wheat_kharif["is_viable"])
        self.assertEqual(wheat_kharif["factor"], 0.0)
        self.assertEqual(wheat_kharif["season_status"], "Incompatible")

        # Wheat in Summer
        wheat_summer = evaluate_seasonal_feasibility("Wheat", "Summer (Zaid)")
        self.assertFalse(wheat_summer["is_viable"])
        self.assertEqual(wheat_summer["factor"], 0.0)

        # Wheat in Rabi (Optimal)
        wheat_rabi = evaluate_seasonal_feasibility("Wheat", "Rabi (Winter)")
        self.assertTrue(wheat_rabi["is_viable"])
        self.assertEqual(wheat_rabi["factor"], 1.0)
        self.assertEqual(wheat_rabi["season_status"], "Optimal")

        # Gram in Kharif
        gram_kharif = evaluate_seasonal_feasibility("Gram", "Kharif")
        self.assertFalse(gram_kharif["is_viable"])
        self.assertEqual(gram_kharif["factor"], 0.0)

        # Gram in Rabi
        gram_rabi = evaluate_seasonal_feasibility("Gram", "Rabi")
        self.assertTrue(gram_rabi["is_viable"])
        self.assertEqual(gram_rabi["factor"], 1.0)

    def test_kharif_dominant_crops_reactivity(self):
        """Rice and Cotton should have optimal yields in Kharif and lower in Rabi/Summer."""
        rice_kharif = evaluate_seasonal_feasibility("Rice", "Kharif")
        self.assertTrue(rice_kharif["is_viable"])
        self.assertEqual(rice_kharif["factor"], 1.0)
        self.assertEqual(rice_kharif["season_status"], "Optimal")

        rice_rabi = evaluate_seasonal_feasibility("Rice", "Rabi")
        self.assertTrue(rice_rabi["is_viable"])
        self.assertEqual(rice_rabi["factor"], 0.88)
        self.assertEqual(rice_rabi["season_status"], "Moderate")

        rice_summer = evaluate_seasonal_feasibility("Rice", "Summer")
        self.assertTrue(rice_summer["is_viable"])
        self.assertEqual(rice_summer["factor"], 0.55)
        self.assertEqual(rice_summer["season_status"], "Sub-Optimal")

        # Cotton in Summer should be incompatible
        cotton_summer = evaluate_seasonal_feasibility("Cotton(lint)", "Summer")
        self.assertFalse(cotton_summer["is_viable"])
        self.assertEqual(cotton_summer["factor"], 0.0)

    def test_perennial_annual_crops(self):
        """Sugarcane and Coconut thrive across Whole Year."""
        sugarcane_year = evaluate_seasonal_feasibility("Sugarcane", "Whole Year")
        self.assertTrue(sugarcane_year["is_viable"])
        self.assertEqual(sugarcane_year["factor"], 1.0)

        coconut_kharif = evaluate_seasonal_feasibility("Coconut", "Kharif")
        self.assertTrue(coconut_kharif["is_viable"])
        self.assertEqual(coconut_kharif["factor"], 1.0)

    def test_predict_yield_detailed_seasonal_integration(self):
        """Detailed predictions include season_mismatch, season_status, season_factor."""
        # Viable case: Wheat in Rabi in Punjab
        res_rabi = predict_yield_detailed({
            "Crop": "Wheat", "State": "Punjab", "Season": "Rabi",
            "Area": 2.0, "Annual_Rainfall": 650.0, "Fertilizer": 140.0, "Pesticide": 20.0
        })
        self.assertTrue(res_rabi["is_viable"])
        self.assertFalse(res_rabi["season_mismatch"])
        self.assertEqual(res_rabi["season_status"], "Optimal")
        self.assertGreater(res_rabi["predicted_yield_tonnes_ha"], 1.0)

        # Incompatible season case: Wheat in Kharif in Punjab
        res_kharif = predict_yield_detailed({
            "Crop": "Wheat", "State": "Punjab", "Season": "Kharif",
            "Area": 2.0, "Annual_Rainfall": 650.0, "Fertilizer": 140.0, "Pesticide": 20.0
        })
        self.assertFalse(res_kharif["is_viable"])
        self.assertTrue(res_kharif["season_mismatch"])
        self.assertEqual(res_kharif["season_status"], "Incompatible")
        self.assertEqual(res_kharif["predicted_yield_tonnes_ha"], 0.0)
        self.assertEqual(res_kharif["estimated_production"], 0.0)
        self.assertEqual(res_kharif["warning_key"], "warning_wheat_kharif")

    def test_predict_yield_api_endpoint(self):
        """API response carries seasonal fields for reactive UI."""
        with self.app.session_transaction() as sess:
            sess["is_authenticated"] = True
            sess["mobile"] = "+919876543210"
            sess["user_id"] = "+919876543210"

        resp = self.app.post("/predict-yield", json={
            "Crop": "Wheat",
            "State": "Punjab",
            "Season": "Summer (Zaid)",
            "Area": 1.0,
            "Annual_Rainfall": 500.0,
            "Fertilizer": 100.0,
            "Pesticide": 10.0
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["is_viable"])
        self.assertTrue(data["season_mismatch"])
        self.assertEqual(data["season_status"], "Incompatible")
        self.assertEqual(data["predicted_yield"], 0.0)
        self.assertEqual(data["estimated_production"], 0.0)
        self.assertEqual(data["production_unit"], "tonnes")
        self.assertEqual(data["warning_key"], "warning_wheat_summer")


if __name__ == "__main__":
    unittest.main()
