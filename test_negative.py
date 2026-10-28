import requests
import json

# Test negative value
test_data = {
    "N": -10,
    "P": 42,
    "K": 43,
    "temperature": 25,
    "humidity": 80,
    "ph": 6.5,
    "rainfall": 200
}

print("Testing API with negative N value:")
print(f"Input: {test_data}")
print()

response = requests.post(
    "http://127.0.0.1:5000/predict",
    json=test_data,
    headers={"Content-Type": "application/json"}
)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
