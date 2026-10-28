import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "saved_models",
    "crop_yield_model.pkl"
)


def load_yield_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Yield model not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def predict_yield(input_data):
    model = load_yield_model()

    df = pd.DataFrame([{
        "Crop": input_data["Crop"],
        "Crop_Year": input_data["Crop_Year"],
        "Season": input_data["Season"],
        "State": input_data["State"],
        "Area": input_data["Area"],
        "Production": input_data["Production"],
        "Annual_Rainfall": input_data["Annual_Rainfall"],
        "Fertilizer": input_data["Fertilizer"],
        "Pesticide": input_data["Pesticide"]
    }])
    for column in ["Crop", "Season", "State"]:
        df[column] = df[column].astype(str).str.strip()

    prediction = model.predict(df)

    return float(prediction[0])