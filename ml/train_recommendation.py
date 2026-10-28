from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

FEATURE_COLUMNS = [
    "N", "P", "K",
    "temperature", "humidity", "ph", "rainfall"
]

DATASET_PATH = Path(r"C:\Users\pinni\Downloads\archive (2)\merged_crop_dataset.csv")


def load_dataset():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)

    required_columns = FEATURE_COLUMNS + ["label"]
    missing = [c for c in required_columns if c not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[required_columns].copy()
    df["label"] = df["label"].astype(str).str.strip()

    for column in FEATURE_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=required_columns)
    df = df[(df[FEATURE_COLUMNS] >= 0).all(axis=1)]
    df = df.drop_duplicates().reset_index(drop=True)

    if df["label"].nunique() < 2:
        raise ValueError("Dataset must contain at least two crop classes.")

    return df


final_data = load_dataset()

print("Dataset loaded successfully!")
print("Dataset shape:", final_data.shape)
print("Feature columns:", FEATURE_COLUMNS)
print("Total crops:", final_data["label"].nunique())
print("Crops:", sorted(final_data["label"].unique().tolist()))

X = final_data[FEATURE_COLUMNS]
y = final_data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model training completed!")
print("Accuracy:", round(accuracy, 4))
print("Model crop classes:", len(model.classes_))

output_dir = Path(__file__).resolve().parent / "saved_models"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "crop_recommendation_model.pkl"
joblib.dump(model, output_path)

print("Recommendation model saved successfully!")
print("Model path:", output_path)
