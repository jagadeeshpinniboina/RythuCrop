import pandas as pd

df = pd.read_csv('ml/data/Crop_recommendation.csv')
cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

print("Training data ranges:")
print("=" * 60)
for col in cols:
    print("{}: min={}, max={}, mean={}".format(
        col, 
        round(df[col].min(), 2),
        round(df[col].max(), 2),
        round(df[col].mean(), 2)
    ))
print()
print("Unique crops in training data:", sorted(df['label'].unique().tolist()))
print("Number of crops:", len(df['label'].unique()))
