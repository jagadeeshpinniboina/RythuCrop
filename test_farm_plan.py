#!/usr/bin/env python
import sys
sys.path.insert(0, 'c:\\Crop-Yield-Prediction')

from app.models.predictor import recommend_farm_plan

# Test cases with different combinations
test_cases = [
    # Test 1: Kharif, Low water (should recommend drought-tolerant crops)
    {
        'name': 'Test 1: Kharif, Low water availability, Beginner',
        'params': {'land': 2, 'season': 'Kharif', 'soil': 'Sandy Soil', 'irrigation': 'Low water availability', 'goal': 'Balanced farming', 'experience': 'Beginner'}
    },
    # Test 2: Rabi, Good water (should recommend high-yield crops)
    {
        'name': 'Test 2: Rabi, Good water, Higher yield goal',
        'params': {'land': 5, 'season': 'Rabi', 'soil': 'Black Soil', 'irrigation': 'Good water availability', 'goal': 'Higher yield', 'experience': 'Some experience'}
    },
    # Test 3: Summer, Rainfed (should recommend dry crops)
    {
        'name': 'Test 3: Summer, Rainfed, Lower water use',
        'params': {'land': 1, 'season': 'Summer', 'soil': 'Red Soil', 'irrigation': 'Rainfed', 'goal': 'Lower water use', 'experience': 'Beginner'}
    },
    # Test 4: Kharif, Black Soil, Good water (should work well)
    {
        'name': 'Test 4: Kharif, Black Soil, Good water, Experienced',
        'params': {'land': 10, 'season': 'Kharif', 'soil': 'Black Soil', 'irrigation': 'Good water availability', 'goal': 'Higher yield', 'experience': 'Experienced'}
    },
    # Test 5: Rabi, Loamy soil, Lower cost
    {
        'name': 'Test 5: Rabi, Loamy soil, Lower input cost',
        'params': {'land': 3, 'season': 'Rabi', 'soil': 'Loamy', 'irrigation': 'Moderate water availability', 'goal': 'Lower input cost', 'experience': 'Some experience'}
    },
]

# 21 required crops for validation
REQUIRED_CROPS = [
    'Arecanut', 'Arhar/Tur', 'Castor seed', 'Coconut', 'Cotton(lint)',
    'Dry chillies', 'Gram', 'Jute', 'Maize', 'Onion', 'Potato', 'Rice',
    'Sugarcane', 'Sunflower', 'Tobacco', 'Turmeric', 'Wheat', 'Bajra',
    'Black pepper', 'Groundnut', 'Soyabean'
]

print("=" * 80)
print("FARM PLANNING RECOMMENDATION TESTS")
print("=" * 80)

all_valid = True
for test in test_cases:
    print(f"\n{test['name']}")
    print(f"  Parameters: {test['params']}")
    
    recommendations = recommend_farm_plan(test['params'])
    print(f"  Recommended crops ({len(recommendations)}): {', '.join(recommendations)}")
    
    # Validate all crops are from the 21-crop list
    invalid_crops = [c for c in recommendations if c not in REQUIRED_CROPS]
    if invalid_crops:
        print(f"  ❌ ERROR: Invalid crops recommended: {invalid_crops}")
        all_valid = False
    else:
        print(f"  ✓ All crops from the 21-crop list")

print("\n" + "=" * 80)
if all_valid:
    print("✓ ALL TESTS PASSED - All recommendations use only the 21-crop list")
else:
    print("❌ SOME TESTS FAILED - Invalid crops were recommended")
print("=" * 80)
