#!/usr/bin/env python
import sys
sys.path.insert(0, 'c:\\Crop-Yield-Prediction')

from app.models.predictor import recommend_farm_plan, FARM_PLANNING_CROPS

# 21 required crops
REQUIRED_CROPS = set(FARM_PLANNING_CROPS)

print("COMPREHENSIVE FARM PLANNING VERIFICATION")
print("=" * 80)
print(f"Total required crops: {len(REQUIRED_CROPS)}")
print(f"Crops: {sorted(REQUIRED_CROPS)}")
print()

# Test with all combinations of key parameters
seasons = ['Kharif', 'Rabi', 'Summer']
soils = ['Loamy', 'Black Soil', 'Red Soil', 'Clay Soil', 'Sandy Soil']
water_levels = ['Good water availability', 'Moderate water availability', 'Low water availability', 'Rainfed']
goals = ['Higher yield', 'Lower water use', 'Lower input cost', 'Balanced farming']
experiences = ['Beginner', 'Some experience', 'Experienced']

test_count = 0
invalid_count = 0
all_recommendations = set()

print("Testing all combinations...")
print()

for season in seasons:
    for soil in soils:
        for water in water_levels:
            for goal in goals:
                for experience in experiences:
                    test_count += 1
                    
                    try:
                        recs = recommend_farm_plan({
                            'land': 3,
                            'season': season,
                            'soil': soil,
                            'irrigation': water,
                            'goal': goal,
                            'experience': experience
                        })
                        
                        # Validate
                        if not recs:
                            print(f"  ❌ Empty recommendations for {season}/{soil}/{water}/{goal}/{experience}")
                            invalid_count += 1
                        else:
                            # Add to set of all recommendations
                            for crop in recs:
                                all_recommendations.add(crop)
                            
                            # Check for invalid crops
                            invalid_crops = [c for c in recs if c not in REQUIRED_CROPS]
                            if invalid_crops:
                                print(f"  ❌ Invalid crops: {invalid_crops} for {season}/{soil}/{water}/{goal}/{experience}")
                                invalid_count += 1
                    except Exception as e:
                        print(f"  ❌ ERROR: {e} for {season}/{soil}/{water}/{goal}/{experience}")
                        invalid_count += 1

print()
print("=" * 80)
print(f"Tests run: {test_count}")
print(f"Invalid tests: {invalid_count}")
print(f"Valid tests: {test_count - invalid_count}")
print()
print(f"Unique crops recommended across all tests: {len(all_recommendations)}")
print(f"Crops recommended: {sorted(all_recommendations)}")
print()

missing_crops = REQUIRED_CROPS - all_recommendations
if missing_crops:
    print(f"⚠️  Crops never recommended: {sorted(missing_crops)}")
else:
    print(f"✓ All 21 crops can be recommended in some scenario")

print()
print("=" * 80)
if invalid_count == 0 and len(all_recommendations) == len(REQUIRED_CROPS):
    print("✓ ALL TESTS PASSED")
else:
    print("❌ SOME TESTS FAILED")
