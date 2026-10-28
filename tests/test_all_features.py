import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app
from app.models.predictor import recommend_farm_plan, recommend_crop_top3, CropInputError
from app.models.yield_predictor import predict_yield, predict_yield_detailed
from app.data.translations import TRANSLATIONS, LANGUAGES
from app.data.agri_taxonomy import FARM_PLANNING_21_CROPS


def run_comprehensive_test_suite():
    print("=" * 80)
    print("RYTHUCROP COMPREHENSIVE REGRESSION & INTEGRATION TEST SUITE")
    print("=" * 80)

    client = app.test_client()
    with client.session_transaction() as sess:
        sess["is_authenticated"] = True
        sess["mobile"] = "+919876543210"
        sess["user_id"] = "+919876543210"
    passed_tests = 0
    total_tests = 0

    # Test 1: Application Startup & Home Page
    total_tests += 1
    resp = client.get("/")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    assert len(resp.data) > 1000, "Home page content empty"
    print("[PASS] Test 1: Flask app startup & GET / (Home page)")
    passed_tests += 1

    # Test 2: All 9 Languages Parity
    total_tests += 1
    for lang in LANGUAGES:
        assert lang in TRANSLATIONS, f"Language {lang} missing"
        assert len(TRANSLATIONS[lang]) == len(TRANSLATIONS["en"]), f"Key mismatch in {lang}"
    print(f"[PASS] Test 2: Multilingual parity confirmed across all {len(LANGUAGES)} languages")
    passed_tests += 1

    # Test 3: Farm Planning Preserved Contract (6 inputs)
    total_tests += 1
    farm_payload = {
        "land": 2.5,
        "season": "Kharif",
        "soil": "Sandy Soil",
        "irrigation": "Low water availability",
        "goal": "Balanced farming",
        "experience": "Beginner"
    }
    fp_resp = client.post("/farm-plan", json=farm_payload)
    assert fp_resp.status_code == 200
    fp_data = fp_resp.get_json()
    assert "recommended_crops" in fp_data
    assert len(fp_data["recommended_crops"]) >= 2
    # Ensure crops come from the 21-crop list
    for c in fp_data["recommended_crops"]:
        assert c in FARM_PLANNING_21_CROPS, f"Crop {c} not in 21-crop list"
    assert "plan_details" in fp_data
    print("[PASS] Test 3: Farm planning with 6 preserved inputs and 21-crop compatibility")
    passed_tests += 1

    # Test 4: Crop Recommendation Valid & Invalid Inputs
    total_tests += 1
    valid_crop_input = {
        "N": 90, "P": 42, "K": 43,
        "temperature": 25.0, "humidity": 80.0,
        "ph": 6.5, "rainfall": 200.0
    }
    rec_resp = client.post("/predict", json=valid_crop_input)
    assert rec_resp.status_code == 200
    rec_data = rec_resp.get_json()
    assert "top_3" in rec_data
    assert len(rec_data["top_3"]) == 3
    assert "top_3_detailed" in rec_data

    # Test negative rejection
    neg_resp = client.post("/predict", json={**valid_crop_input, "N": -10})
    assert neg_resp.status_code == 400
    assert "negative" in neg_resp.get_json()["error"].lower()

    # Test out of range rejection
    range_resp = client.post("/predict", json={**valid_crop_input, "temperature": 95})
    assert range_resp.status_code == 400
    print("[PASS] Test 4: Crop recommendation ML inference & strict input validation (400 on error)")
    passed_tests += 1

    # Test 5: Pre-Harvest Yield Prediction (Without Production Leakage)
    total_tests += 1
    punjab_rice = {
        "Crop": "Rice", "Crop_Year": 2019, "Season": "Kharif",
        "State": "Punjab", "Area": 2.5, "area_unit": "acres"
    }
    meghalaya_rice = {
        "Crop": "Rice", "Crop_Year": 2019, "Season": "Kharif",
        "State": "Meghalaya", "Area": 2.5, "area_unit": "acres"
    }

    py_punjab = client.post("/predict-yield", json=punjab_rice).get_json()
    py_meghalaya = client.post("/predict-yield", json=meghalaya_rice).get_json()

    assert "predicted_yield" in py_punjab
    assert "estimated_production" in py_punjab
    assert py_punjab["yield_unit"] == "tonnes/ha"
    assert py_punjab["acre_unit"] == "quintals/acre"

    # Regional sensitivity check: Punjab Rice historically yields more than Meghalaya Rice
    assert py_punjab["predicted_yield"] > py_meghalaya["predicted_yield"], (
        f"Expected Punjab ({py_punjab['predicted_yield']}) > Meghalaya ({py_meghalaya['predicted_yield']})"
    )
    print(f"[PASS] Test 5: Yield prediction learned regional difference (Punjab {py_punjab['predicted_yield']} > Meghalaya {py_meghalaya['predicted_yield']} t/ha)")
    passed_tests += 1

    # Test 6: Location Hierarchy API
    total_tests += 1
    states_resp = client.get("/api/states").get_json()
    assert "states" in states_resp
    assert len(states_resp["states"]) >= 25

    dist_resp = client.get("/api/districts?state=Andhra Pradesh").get_json()
    assert "districts" in dist_resp
    assert "Kurnool" in dist_resp["districts"]
    print("[PASS] Test 6: Location hierarchy APIs (States & Districts)")
    passed_tests += 1

    # Test 7: Crop Catalogue API
    total_tests += 1
    cat_resp = client.get("/api/crops").get_json()
    assert "crops" in cat_resp
    assert cat_resp["count"] >= 20
    assert "categories" in cat_resp
    print(f"[PASS] Test 7: Crop Catalogue API returned {cat_resp['count']} crops across {len(cat_resp['categories'])} categories")
    passed_tests += 1

    # Test 8: Agmarknet Mandi Prices API & Selling Guidance
    total_tests += 1
    mandi_resp = client.get("/api/mandi-prices?crop=Rice").get_json()
    assert mandi_resp["count"] > 0
    first_price = mandi_resp["prices"][0]
    assert "modal_price" in first_price
    assert "arrival_date" in first_price
    assert "source" in first_price

    guidance_resp = client.get("/api/selling-guidance?crop=Rice&modal_price=2200&distance_km=30&holding_days=45").get_json()
    assert "net_immediate_realization_rs_qtl" in guidance_resp
    assert "breakeven_future_price_rs_qtl" in guidance_resp
    assert "recommendation" in guidance_resp
    print("[PASS] Test 8: Wholesale Mandi prices and post-harvest economic selling guidance")
    passed_tests += 1

    # Test 9: Storage & Cold Storage Finder API
    total_tests += 1
    storage_resp = client.get("/api/storage?state=Andhra Pradesh").get_json()
    assert storage_resp["count"] > 0
    facility = storage_resp["facilities"][0]
    assert "capacity_mt" in facility
    assert "suitable_crops" in facility
    assert "source" in facility
    print("[PASS] Test 9: Storage finder returned verified warehouses and cold chains")
    passed_tests += 1

    # Test 10: Mobile OTP Auth & Session Lifecycle
    total_tests += 1
    req_otp = client.post("/api/auth/request-otp", json={"mobile": "9876543210"}).get_json()
    assert "data" in req_otp
    otp_code = req_otp["data"].get("dev_otp")
    assert otp_code is not None, "Dev OTP should be returned in development mode"

    # Verify OTP
    verify_resp = client.post("/api/auth/verify-otp", json={
        "mobile": "9876543210",
        "otp": otp_code,
        "preferred_lang": "te"
    })
    assert verify_resp.status_code == 200
    assert verify_resp.get_json()["user"]["mobile"] == "+919876543210"

    # Session check
    sess_resp = client.get("/api/auth/session").get_json()
    assert sess_resp["authenticated"] is True
    assert sess_resp["user"]["mobile"] == "+919876543210"

    # Logout
    logout_resp = client.post("/api/auth/logout").get_json()
    sess_after = client.get("/api/auth/session").get_json()
    assert sess_after["authenticated"] is False
    print("[PASS] Test 10: Mobile OTP auth, session state, dev mode fallback, and logout")
    passed_tests += 1

    # Test 11: Price Alerts Subscription & Management
    total_tests += 1
    alert_resp = client.post("/api/alerts/subscribe", json={
        "mobile": "9876543210",
        "crop": "Cotton",
        "market": "Warangal APMC Yard",
        "condition_type": "above",
        "target_price": 7500
    }).get_json()
    assert "alert_id" in alert_resp
    alert_id = alert_resp["alert_id"]

    my_alerts = client.get("/api/alerts/my-alerts?mobile=9876543210").get_json()
    assert my_alerts["count"] >= 1

    cancel_resp = client.post("/api/alerts/cancel", json={
        "alert_id": alert_id,
        "mobile": "9876543210"
    }).get_json()
    assert cancel_resp["success"] is True
    print("[PASS] Test 11: Price alert creation, retrieval, and cancellation")
    passed_tests += 1

    print("=" * 80)
    print(f"ALL {passed_tests}/{total_tests} COMPREHENSIVE TESTS PASSED WITH 100% SUCCESS RATE!")
    print("=" * 80)


if __name__ == "__main__":
    run_comprehensive_test_suite()
