import requests
import json

base_url = "http://127.0.0.1:5000"

# Test cases
test_cases = [
    {
        "name": "Test 1: Valid input (high N, P, K - rice-like)",
        "data": {"N": 90, "P": 42, "K": 43, "temperature": 25, "humidity": 80, "ph": 6.5, "rainfall": 200},
        "expect_success": True
    },
    {
        "name": "Test 2: Low nutrients (gram-like)",
        "data": {"N": 20, "P": 35, "K": 40, "temperature": 20, "humidity": 50, "ph": 7.0, "rainfall": 50},
        "expect_success": True
    },
    {
        "name": "Test 3: High nutrients (sugarcane-like)",
        "data": {"N": 120, "P": 60, "K": 80, "temperature": 24, "humidity": 75, "ph": 6.5, "rainfall": 150},
        "expect_success": True
    },
    {
        "name": "Test 4: Low rainfall (bajra-like)",
        "data": {"N": 40, "P": 35, "K": 40, "temperature": 28, "humidity": 50, "ph": 6.0, "rainfall": 40},
        "expect_success": True
    },
    {
        "name": "Test 5: Negative N (should fail)",
        "data": {"N": -10, "P": 42, "K": 43, "temperature": 25, "humidity": 80, "ph": 6.5, "rainfall": 200},
        "expect_success": False
    },
    {
        "name": "Test 6: Missing value (should fail)",
        "data": {"N": 90, "P": 42, "temperature": 25, "humidity": 80, "ph": 6.5, "rainfall": 200},
        "expect_success": False
    },
]

print("Testing Crop Recommendation API")
print("=" * 80)

for test in test_cases:
    print(f"\n{test['name']}")
    print("-" * 80)
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            json=test['data'],
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if "top_3" in result:
                print(f"✓ SUCCESS: Top 3 crops: {result['top_3']}")
                if not test['expect_success']:
                    print(f"  ⚠ WARNING: Expected to fail but got success")
            else:
                print(f"✗ FAILED: {result}")
        else:
            result = response.json()
            if "error" in result:
                print(f"✗ ERROR: {result['error']}")
                if test['expect_success']:
                    print(f"  ⚠ WARNING: Expected to succeed but got error")
            else:
                print(f"✗ FAILED with status {response.status_code}: {result}")
                
    except Exception as e:
        print(f"✗ EXCEPTION: {str(e)}")

print("\n" + "=" * 80)
print("Testing complete")
