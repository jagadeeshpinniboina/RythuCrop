import joblib
import os

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'ml', 'saved_models', 'crop_recommendation_model.pkl')

try:
    model = joblib.load(model_path)
    print("Model classes (crops it was trained on):")
    print(sorted(model.classes_.tolist()))
except Exception as e:
    print(f"Error loading model: {e}")
