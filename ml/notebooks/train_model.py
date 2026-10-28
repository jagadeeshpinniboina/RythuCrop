import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load dataset
data_path = "data/ml/data/crop_yield.csv"
df = pd.read_csv(data_path)
for column in ["Crop", "Season", "State"]:
    df[column] = df[column].astype(str).str.strip()

# Input features and target
X = df.drop("Yield", axis=1)
y = df["Yield"]

# Categorical and numerical columns
categorical_cols = ["Crop", "Season", "State"]
numerical_cols = [
    "Crop_Year",
    "Area",
    "Production",
    "Annual_Rainfall",
    "Fertilizer",
    "Pesticide"
]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("numerical", "passthrough", numerical_cols)
    ]
)

# Model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

# Pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
pipeline.fit(X_train, y_train)

# Evaluate
predictions = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Model Training Completed!")
print("Mean Absolute Error:", mae)
print("R2 Score:", r2)

# Save model
model_path = "ml/saved_models/crop_yield_model.pkl"
joblib.dump(pipeline, model_path)

print("Model saved successfully!")
print(model_path)