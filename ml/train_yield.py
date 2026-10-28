import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "data" / "ml" / "data" / "crop_yield.csv"
MODEL_DIR = BASE_DIR / "saved_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "crop_yield_model.pkl"
METRICS_PATH = MODEL_DIR / "yield_model_metrics.json"

CATEGORICAL_COLS = ["Crop", "Season", "State"]
NUMERICAL_COLS = ["Crop_Year", "Area", "Annual_Rainfall", "Fertilizer", "Pesticide"]
FEATURE_COLS = CATEGORICAL_COLS + NUMERICAL_COLS


def train_yield_model():
    print(f"Loading yield dataset from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)

    for col in CATEGORICAL_COLS:
        df[col] = df[col].astype(str).str.strip()

    for col in NUMERICAL_COLS + ["Yield"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=FEATURE_COLS + ["Yield"])
    # Filter out invalid negative yields or zero/negative area
    df = df[(df["Yield"] >= 0) & (df["Area"] > 0)]

    X = df[FEATURE_COLS]
    y = df["Yield"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLS),
            ("num", "passthrough", NUMERICAL_COLS),
        ]
    )

    rf = RandomForestRegressor(
        n_estimators=150,
        max_depth=25,
        random_state=42,
        n_jobs=-1
    )

    pipeline = TransformedTargetRegressor(
        regressor=RandomForestRegressor(n_estimators=150, max_depth=25, random_state=42, n_jobs=-1),
        transformer=None,
        func=np.log1p,
        inverse_func=np.expm1
    )

    # Wrap preprocessor and model into a single pipeline
    from sklearn.pipeline import Pipeline
    full_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", pipeline)
    ])

    print("Fitting pre-harvest yield model (No Production target leakage)...")
    full_pipeline.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = full_pipeline.predict(X_test)
    y_pred = np.clip(y_pred, a_min=0, a_max=None)

    mae = float(mean_absolute_error(y_test, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = float(r2_score(y_test, y_pred))

    test_df = X_test.copy()
    test_df["y_true"] = y_test
    test_df["y_pred"] = y_pred

    crop_metrics = {}
    key_crops = ["Rice", "Wheat", "Maize", "Sugarcane", "Cotton(lint)", "Groundnut", "Gram", "Potato", "Onion"]
    for crop in key_crops:
        sub = test_df[test_df["Crop"] == crop]
        if len(sub) > 0:
            c_mae = float(mean_absolute_error(sub["y_true"], sub["y_pred"]))
            c_rmse = float(np.sqrt(mean_squared_error(sub["y_true"], sub["y_pred"])))
            c_r2 = float(r2_score(sub["y_true"], sub["y_pred"]))
            crop_metrics[crop] = {
                "sample_count": len(sub),
                "mean_actual": float(sub["y_true"].mean()),
                "mae": round(c_mae, 4),
                "rmse": round(c_rmse, 4),
                "r2": round(c_r2, 4),
                "unit": "tonnes/ha"
            }

    metrics = {
        "dataset_records": len(df),
        "training_records": len(X_train),
        "test_records": len(X_test),
        "features": FEATURE_COLS,
        "overall_mae": round(mae, 4),
        "overall_rmse": round(rmse, 4),
        "overall_r2": round(r2, 4),
        "target_leakage_free": True,
        "crop_specific_metrics": crop_metrics
    }

    print(f"Overall MAE: {mae:.4f}")
    print(f"Overall RMSE: {rmse:.4f}")
    print(f"Overall R2: {r2:.4f}")

    joblib.dump(full_pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to {METRICS_PATH}")


if __name__ == "__main__":
    train_yield_model()
