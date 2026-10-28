import sys
import importlib

# Force reload of the module
if 'app.models.predictor' in sys.modules:
    del sys.modules['app.models.predictor']
if 'app' in sys.modules:
    del sys.modules['app']

from app.models.predictor import recommend_crop_top3

# Test with negative value
test_data = {"N": -10, "P": 42, "K": 43, "temperature": 25, "humidity": 80, "ph": 6.5, "rainfall": 200}

print("Testing recommend_crop_top3 with negative N:")
print(f"Input: {test_data}")
print()

try:
    result = recommend_crop_top3(test_data)
    print(f"ERROR: Should have raised ValueError but got: {result}")
except ValueError as e:
    print(f"✓ Correctly raised ValueError: {e}")
except Exception as e:
    print(f"Raised different exception: {type(e).__name__}: {e}")
