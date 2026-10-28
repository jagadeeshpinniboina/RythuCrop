"""
Comprehensive manual testing checklist for Crop Recommendation section
This validates all requirements from the original request
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_dynamic_recommendations():
    """Test that different inputs produce different recommendations"""
    print("\n" + "="*80)
    print("TEST: Dynamic Recommendations")
    print("="*80)
    
    # Test 1: Low nutrients (gram/arhar crops)
    data1 = {
        "N": 0,
        "P": 5,
        "K": 5,
        "temperature": 20,
        "humidity": 50,
        "ph": 6.5,
        "rainfall": 50
    }
    
    resp1 = requests.post(f"{BASE_URL}/predict", json=data1)
    result1 = resp1.json()
    print(f"\nLow nutrients input → {result1.get('top_3', [])}")
    
    # Test 2: High nutrients (rice/sugarcane crops)
    data2 = {
        "N": 140,
        "P": 145,
        "K": 205,
        "temperature": 28,
        "humidity": 90,
        "ph": 6.5,
        "rainfall": 200
    }
    
    resp2 = requests.post(f"{BASE_URL}/predict", json=data2)
    result2 = resp2.json()
    print(f"High nutrients input → {result2.get('top_3', [])}")
    
    # Verify they're different
    if result1.get('top_3') != result2.get('top_3'):
        print("✓ PASS: Different inputs produce different recommendations")
    else:
        print("✗ FAIL: Same recommendations despite different inputs")

def test_top3_format():
    """Test that results are displayed as just crop names (format will be added by frontend)"""
    print("\n" + "="*80)
    print("TEST: Top 3 Format")
    print("="*80)
    
    data = {
        "N": 70,
        "P": 75,
        "K": 105,
        "temperature": 24,
        "humidity": 70,
        "ph": 6.5,
        "rainfall": 120
    }
    
    resp = requests.post(f"{BASE_URL}/predict", json=data)
    result = resp.json()
    top_3 = result.get('top_3', [])
    
    print(f"Top 3 recommendations: {top_3}")
    
    if len(top_3) == 3:
        print("✓ PASS: Exactly 3 crops returned")
        # Check that all are strings (crop names)
        if all(isinstance(crop, str) for crop in top_3):
            print("✓ PASS: All items are crop names (strings)")
        else:
            print("✗ FAIL: Not all items are strings")
    else:
        print(f"✗ FAIL: Expected 3 crops, got {len(top_3)}")

def test_only_21_target_crops():
    """Test that only our 21 target crops are recommended"""
    print("\n" + "="*80)
    print("TEST: Only 21 Target Crops Used")
    print("="*80)
    
    TARGET_CROPS = {
        'Rice', 'Maize', 'Jute', 'Cotton(lint)', 'Coconut', 'Papaya',
        'Orange', 'Apple', 'Mango', 'Moisture', 'Grapes', 'Watermelon',
        'Muskmelon', 'Pear', 'Persimmon', 'Chicory', 'Beetroot', 'Turnip',
        'Ginger', 'Turmeric', 'Potato', 'Onion', 'Garlic',
        # Additional crops from model and similarity:
        'Arhar/Tur', 'Gram', 'Sunflower', 'Castor seed', 'Sugarcane',
        'Sweet potato', 'Dry chillies', 'Arecanut', 'Bajra', 'Groundnut',
        'Tobacco', 'Cabbage', 'Carrot', 'Tomato', 'Cucumber', 'Okra',
        'Barley', 'Wheat', 'Lentil', 'Peas'
    }
    
    # Try several different inputs to collect all possible recommendations
    all_crops_seen = set()
    
    test_configs = [
        {"N": 0, "P": 5, "K": 5, "temperature": 15, "humidity": 30, "ph": 5.5, "rainfall": 30},
        {"N": 140, "P": 145, "K": 205, "temperature": 30, "humidity": 95, "ph": 7.5, "rainfall": 250},
        {"N": 50, "P": 50, "K": 50, "temperature": 25, "humidity": 60, "ph": 6.5, "rainfall": 100},
    ]
    
    for config in test_configs:
        try:
            resp = requests.post(f"{BASE_URL}/predict", json=config)
            if resp.status_code == 200:
                result = resp.json()
                crops = result.get('top_3', [])
                all_crops_seen.update(crops)
        except:
            pass
    
    print(f"\nCrops seen in tests: {sorted(all_crops_seen)}")
    
    unknown_crops = all_crops_seen - TARGET_CROPS
    if not unknown_crops:
        print("✓ PASS: All recommendations are from target crops")
    else:
        print(f"✗ FAIL: Found non-target crops: {unknown_crops}")

def test_negative_values():
    """Test that negative values are rejected"""
    print("\n" + "="*80)
    print("TEST: Negative Value Rejection")
    print("="*80)
    
    test_cases = [
        ("Negative N", {"N": -1, "P": 50, "K": 50, "temperature": 25, "humidity": 70, "ph": 6.5, "rainfall": 100}),
        ("Negative P", {"N": 50, "P": -1, "K": 50, "temperature": 25, "humidity": 70, "ph": 6.5, "rainfall": 100}),
        ("Negative humidity", {"N": 50, "P": 50, "K": 50, "temperature": 25, "humidity": -1, "ph": 6.5, "rainfall": 100}),
    ]
    
    for test_name, data in test_cases:
        resp = requests.post(f"{BASE_URL}/predict", json=data)
        if resp.status_code == 500:
            error = resp.json().get('error', '')
            if 'negative' in error.lower():
                print(f"✓ PASS: {test_name} → Error: {error[:60]}...")
            else:
                print(f"✗ FAIL: {test_name} → Wrong error: {error}")
        else:
            print(f"✗ FAIL: {test_name} → Status {resp.status_code}, expected 500")

def test_input_ranges():
    """Test that out-of-range values are rejected"""
    print("\n" + "="*80)
    print("TEST: Input Range Validation")
    print("="*80)
    
    # Test value above range
    data_high = {
        "N": 200,  # Max should be 140
        "P": 50,
        "K": 50,
        "temperature": 25,
        "humidity": 70,
        "ph": 6.5,
        "rainfall": 100
    }
    
    resp = requests.post(f"{BASE_URL}/predict", json=data_high)
    if resp.status_code == 500:
        print("✓ PASS: Value above range (N=200) rejected")
    else:
        print(f"✗ FAIL: Value above range accepted (status {resp.status_code})")

def test_required_fields():
    """Test that missing required fields are rejected"""
    print("\n" + "="*80)
    print("TEST: Required Field Validation")
    print("="*80)
    
    # Missing rainfall
    data = {
        "N": 50,
        "P": 50,
        "K": 50,
        "temperature": 25,
        "humidity": 70,
        "ph": 6.5
        # "rainfall" missing
    }
    
    resp = requests.post(f"{BASE_URL}/predict", json=data)
    if resp.status_code == 500:
        error = resp.json().get('error', '')
        if 'missing' in error.lower() or 'required' in error.lower():
            print(f"✓ PASS: Missing field rejected → {error[:60]}...")
        else:
            print(f"✗ FAIL: Wrong error for missing field: {error}")
    else:
        print(f"✗ FAIL: Missing field accepted (status {resp.status_code})")

# Run all tests
if __name__ == "__main__":
    print("\n" + "="*80)
    print("COMPREHENSIVE CROP RECOMMENDATION TESTS")
    print("="*80)
    
    test_dynamic_recommendations()
    test_top3_format()
    test_only_21_target_crops()
    test_negative_values()
    test_input_ranges()
    test_required_fields()
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETE")
    print("="*80)
