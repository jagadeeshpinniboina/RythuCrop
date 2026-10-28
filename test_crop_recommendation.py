from app.models.predictor import recommend_crop_top3

# Test with different inputs
test_cases = [
    {'N': 90, 'P': 42, 'K': 43, 'temperature': 25, 'humidity': 80, 'ph': 6.5, 'rainfall': 200},
    {'N': 20, 'P': 35, 'K': 40, 'temperature': 20, 'humidity': 50, 'ph': 7.0, 'rainfall': 50},
    {'N': 120, 'P': 60, 'K': 80, 'temperature': 24, 'humidity': 75, 'ph': 6.5, 'rainfall': 150},
    {'N': 40, 'P': 35, 'K': 40, 'temperature': 28, 'humidity': 50, 'ph': 6.0, 'rainfall': 40},
]

print("Testing crop recommendations:")
print("=" * 80)
for i, test in enumerate(test_cases, 1):
    try:
        result = recommend_crop_top3(test)
        print("Test {}: {} -> {}".format(i, test, result))
    except Exception as e:
        print("Test {} ERROR: {}".format(i, str(e)))
