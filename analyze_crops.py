import pandas as pd

# Load the yield dataset
d = pd.read_csv('data/ml/data/crop_yield.csv')

# Define the 21 required crops
required_crops = [
    'Arecanut', 'Arhar/Tur', 'Castor seed', 'Coconut', 'Cotton(lint)', 
    'Dry chillies', 'Gram', 'Jute', 'Maize', 'Onion', 'Potato', 'Rice', 
    'Sugarcane', 'Sunflower', 'Tobacco', 'Turmeric', 'Wheat', 'Bajra', 
    'Black pepper', 'Groundnut', 'Soyabean'
]

# Check which crops are in the dataset
available = []
missing = []
for crop in required_crops:
    if crop in d['Crop'].values:
        available.append(crop)
    else:
        # Check with different variations
        matches = d[d['Crop'].str.strip() == crop]['Crop'].unique()
        if len(matches) > 0:
            available.append(crop)
        else:
            missing.append(crop)

print("Available crops from the 21-crop list:", len(available))
print("Missing crops:", missing)
print("\nAnalyzing crop characteristics...")

# Get a sample of crops by season
for crop in required_crops[:5]:
    crop_data = d[d['Crop'].str.strip() == crop]
    if len(crop_data) > 0:
        print(f"\n{crop}:")
        print(f"  Seasons: {crop_data['Season'].unique()}")
        print(f"  States: {len(crop_data['State'].unique())} states")
        print(f"  Avg Yield: {crop_data['Yield'].mean():.1f}")

# Analyze all 21 crops by season
print("\n\n=== ALL 21 CROPS BY SEASON ===")
for crop in sorted(required_crops):
    crop_data = d[d['Crop'].str.strip() == crop]
    if len(crop_data) > 0:
        seasons = sorted(crop_data['Season'].unique())
        print(f"{crop:20} -> {', '.join(seasons)}")
