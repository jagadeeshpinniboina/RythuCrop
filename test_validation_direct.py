from app.models.predictor import validate_crop_input

# Test validation directly
test_data = {"N": -10, "P": 42, "K": 43, "temperature": 25, "humidity": 80, "ph": 6.5, "rainfall": 200}

print("Testing validation function directly:")
print(f"Input: {test_data}")
print()

is_valid, error_msg, validated = validate_crop_input(test_data)
print(f"is_valid: {is_valid}")
print(f"error_msg: {error_msg}")
print(f"validated: {validated}")
