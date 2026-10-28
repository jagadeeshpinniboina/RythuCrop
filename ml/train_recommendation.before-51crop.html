import os
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


REQUIRED_CROPS = [
    'Arecanut', 'Arhar/Tur', 'Castor seed', 'Coconut', 'Cotton(lint)',
    'Dry chillies', 'Gram', 'Jute', 'Maize', 'Onion', 'Potato', 'Rice',
    'Sugarcane', 'Sunflower', 'Tobacco', 'Turmeric', 'Wheat', 'Bajra',
    'Black pepper', 'Groundnut', 'Soyabean'
]

FEATURE_COLUMNS = [
    "N", "P", "K",
    "temperature", "humidity", "ph", "rainfall"
]

LABEL_ALIASES = {
    "rice": "Rice",
    "maize": "Maize",
    "maize corn": "Maize",
    "jute": "Jute",
    "coconut": "Coconut",
    "coconut nariyal": "Coconut",
    "cotton": "Cotton(lint)",
    "cotton kapash": "Cotton(lint)",
    "wheat": "Wheat",
    "wheat gehun": "Wheat",
    "potato": "Potato",
    "potato aloo": "Potato",
    "onion": "Onion",
    "onion pyaaz": "Onion",
    "sunflower": "Sunflower",
    "sunflower surajmukhi": "Sunflower",
    "turmeric": "Turmeric",
    "turmeric haldi": "Turmeric",
    "black pepper": "Black pepper",
    "black pepper kali mirch": "Black pepper",
    "pepper": "Black pepper",
    "soybean": "Soyabean",
    "soyabean": "Soyabean",
    "soybean soyabean": "Soyabean",
    "groundnut": "Groundnut",
    "bajra": "Bajra",
    "arecanut": "Arecanut",
    "chickpea": "Gram",
    "chickpea gram": "Gram",
    "gram": "Gram",
    "pigeon peas": "Arhar/Tur",
    "pigeon peas tur arhar": "Arhar/Tur",
    "arhar": "Arhar/Tur",
    "arhar tur": "Arhar/Tur",
    "tur arhar": "Arhar/Tur",
    "castor seed": "Castor seed",
    "castor": "Castor seed",
    "sugarcane": "Sugarcane",
    "tobacco": "Tobacco",
    "dry chillies": "Dry chillies",
    "dry chillies chilli": "Dry chillies",
    "dry chilli": "Dry chillies",
}


def canonicalize_label(value):
    if pd.isna(value):
        return None
    label = str(value).strip()
    if not label:
        return None
    normalized = label.lower().replace("-", " ").replace("_", " ").replace("(", " ").replace(")", " ").replace("/", " ")
    normalized = " ".join(normalized.split())
    mapped = LABEL_ALIASES.get(normalized)
    if mapped:
        return mapped
    return label if label in REQUIRED_CROPS else None


def load_and_merge_datasets():
    base_dir = Path(__file__).resolve().parent
    primary_path = base_dir / "data" / "Crop_recommendation.csv"
    secondary_candidates = [
        Path("C:/Users/pinni/Downloads/archive (2)/standardized_crops.csv"),
        Path("C:/Users/pinni/Downloads/archive (2)/merged_crop_dataset.csv"),
        Path("C:/Users/pinni/Downloads/archive (1)/Crop_recommendation.csv"),
        Path("C:/Crop-Yield-Prediction-Backup/ml/data/Crop_recommendation.csv"),
        Path("C:/Users/pinni/Crop-Yield-Prediction/ml/data/Crop_recommendation.csv"),
    ]

    dataset_frames = []
    primary_labels = set()

    for path in [primary_path, *secondary_candidates]:
        if not path.exists():
            continue
        try:
            df = pd.read_csv(path)
        except Exception:
            continue
        if not set(FEATURE_COLUMNS).issubset(df.columns):
            continue
        if "label" not in df.columns:
            continue

        subset = df.loc[:, FEATURE_COLUMNS + ["label"]].copy()
        subset["label"] = subset["label"].map(canonicalize_label)
        subset = subset.dropna(subset=["label"]).copy()
        subset = subset[subset["label"].isin(REQUIRED_CROPS)].copy()

        if subset.empty:
            continue

        if path == primary_path:
            dataset_frames.append(subset)
            primary_labels |= set(subset["label"].unique())
        else:
            missing = subset[~subset["label"].isin(primary_labels)].copy()
            if not missing.empty:
                dataset_frames.append(missing)
                primary_labels |= set(missing["label"].unique())

    if not dataset_frames:
        fallback = pd.read_csv(primary_path)
        fallback = fallback.loc[:, FEATURE_COLUMNS + ["label"]].copy()
        fallback["label"] = fallback["label"].map(canonicalize_label)
        fallback = fallback.dropna(subset=["label"]).copy()
        fallback = fallback[fallback["label"].isin(REQUIRED_CROPS)].copy()
        if fallback.empty:
            raise ValueError(
                "No crop recommendation dataset with the required 7 features and crop labels was found. "
                "Add the valid second crop dataset before retraining."
            )
        dataset_frames.append(fallback)

    merged = pd.concat(dataset_frames, ignore_index=True)
    merged = merged.drop_duplicates().reset_index(drop=True)
    return merged


# Load filtered dataset
final_data = load_and_merge_datasets()

print("Dataset loaded successfully!")
print("Dataset shape:", final_data.shape)
print("Columns:", final_data.columns.tolist())
print("Unique crops:", sorted(final_data['label'].unique().tolist()))
print("Required crop count:", len(final_data['label'].unique()))

X = final_data[FEATURE_COLUMNS]
y = final_data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model Training Completed!")
print("Accuracy:", accuracy)
print("Model crop classes:", sorted(model.classes_.tolist()))

output_dir = Path(__file__).resolve().parent / "saved_models"
output_dir.mkdir(parents=True, exist_ok=True)
joblib.dump(model, output_dir / "crop_recommendation_model.pkl")

print("Recommendation model saved successfully!")
print("Allowed crop classes:", REQUIRED_CROPS)