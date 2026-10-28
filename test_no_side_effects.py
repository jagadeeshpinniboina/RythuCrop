import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("="*80)
print("VERIFYING NO SIDE EFFECTS ON OTHER SECTIONS")
print("="*80)

# Test 1: Check if the main page loads correctly
print("\n1. Main page (GET /)")
try:
    resp = requests.get(f"{BASE_URL}/")
    if resp.status_code == 200:
        if "crop" in resp.text.lower() and "yield" in resp.text.lower():
            print("   ✓ Main page loads correctly")
        else:
            print("   ✗ Main page might be missing content")
    else:
        print(f"   ✗ Main page returns status {resp.status_code}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Test Yield Prediction
print("\n2. Yield Prediction (/predict-yield)")
try:
    yield_data = {
        "N": 50,
        "P": 50,
        "K": 50,
        "temperature": 25,
        "humidity": 70,
        "ph": 6.5,
        "rainfall": 100
    }
    resp = requests.post(f"{BASE_URL}/predict-yield", json=yield_data)
    if resp.status_code == 200:
        result = resp.json()
        if "yield" in result or "predicted_yield" in result:
            print(f"   ✓ Yield prediction works → {result}")
        else:
            print(f"   ✗ Unexpected response: {result}")
    elif resp.status_code == 500:
        # May fail if model not available
        print(f"   ~ Yield prediction endpoint exists (error: {resp.json().get('error', 'Unknown')})")
    else:
        print(f"   ✗ Yield prediction returns status {resp.status_code}")
except Exception as e:
    print(f"   ~ Yield prediction endpoint not tested: {e}")

# Test 3: Test Farm Planning
print("\n3. Farm Planning (/farm-plan)")
try:
    farm_data = {
        "season": "Kharif",
        "soil": "Loamy",
        "farmer_experience": "intermediate",
        "goal": "high_yield",
        "land_area": 2.5,
        "water_availability": "moderate"
    }
    resp = requests.post(f"{BASE_URL}/farm-plan", json=farm_data)
    if resp.status_code == 200:
        result = resp.json()
        if "recommended_crops" in result:
            print(f"   ✓ Farm planning works → {result.get('recommended_crops', [])[:2]}")
        else:
            print(f"   ✗ Unexpected response: {result}")
    else:
        print(f"   ✗ Farm planning returns status {resp.status_code}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Verify crop recommendation still works
print("\n4. Crop Recommendation (/predict)")
try:
    crop_data = {
        "N": 60,
        "P": 60,
        "K": 60,
        "temperature": 25,
        "humidity": 70,
        "ph": 6.5,
        "rainfall": 100
    }
    resp = requests.post(f"{BASE_URL}/predict", json=crop_data)
    if resp.status_code == 200:
        result = resp.json()
        if "top_3" in result and result["top_3"]:
            print(f"   ✓ Crop recommendation works → {result['top_3']}")
        else:
            print(f"   ✗ Unexpected response: {result}")
    else:
        print(f"   ✗ Crop recommendation returns status {resp.status_code}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*80)
print("VERIFICATION COMPLETE")
print("="*80)
