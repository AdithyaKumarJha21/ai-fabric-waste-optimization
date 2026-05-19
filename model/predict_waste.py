from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "random_forest_waste_model.joblib"


def get_efficiency_level(waste_percentage):
    """Convert predicted waste percentage into a simple efficiency label."""
    if waste_percentage <= 10:
        return "Excellent"
    if waste_percentage <= 20:
        return "Good"
    if waste_percentage <= 30:
        return "Moderate"
    return "Poor"


def load_model():
    """Load the trained Random Forest model from disk."""
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "Trained model not found. Run: python model/train_model.py"
        )

    return joblib.load(MODEL_FILE)


def predict_waste(input_data):
    """Predict fabric waste percentage using the saved model."""
    model = load_model()
    input_frame = pd.DataFrame([input_data])
    predicted_waste = float(model.predict(input_frame)[0])
    predicted_waste = round(max(0, min(predicted_waste, 100)), 2)

    return {
        "predicted_waste_percentage": predicted_waste,
        "predicted_utilization_percentage": round(100 - predicted_waste, 2),
        "efficiency_level": get_efficiency_level(predicted_waste),
    }
