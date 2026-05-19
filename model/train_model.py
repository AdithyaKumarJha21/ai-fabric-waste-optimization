from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
DATASET_FILE = PROJECT_DIR / "dataset" / "fabric_waste_dataset.csv"
MODEL_FILE = BASE_DIR / "random_forest_waste_model.joblib"

FEATURE_COLUMNS = [
    "Fabric_Length",
    "Fabric_Width",
    "Piece_Length",
    "Piece_Width",
    "Fabric_Type",
    "GSM",
    "Defect_Count",
    "Marker_Efficiency",
    "Layout_Type",
    "Pieces_Along_Length",
    "Pieces_Along_Width",
    "Pieces_Possible",
]

TARGET_COLUMN = "Waste_Percentage"


def build_training_pipeline():
    """Build a beginner-friendly Random Forest training pipeline."""
    categorical_features = ["Fabric_Type", "Layout_Type"]
    numeric_features = [
        column for column in FEATURE_COLUMNS if column not in categorical_features
    ]

    # OneHotEncoder converts text columns into numeric columns for the model.
    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("numeric", "passthrough", numeric_features),
        ]
    )

    model = RandomForestRegressor(
        n_estimators=120,
        random_state=42,
        max_depth=12,
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def train_model():
    """Train the Random Forest model and save it for backend predictions."""
    dataset = pd.read_csv(DATASET_FILE)

    x = dataset[FEATURE_COLUMNS]
    y = dataset[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
    )

    pipeline = build_training_pipeline()
    pipeline.fit(x_train, y_train)

    predictions = pipeline.predict(x_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    joblib.dump(pipeline, MODEL_FILE)

    print("Random Forest training completed")
    print(f"Model saved to: {MODEL_FILE}")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"R2 Score: {r2:.2f}")

    return {
        "model_file": str(MODEL_FILE),
        "mean_absolute_error": round(mae, 2),
        "r2_score": round(r2, 2),
    }


if __name__ == "__main__":
    train_model()
