# Model

This folder contains machine learning code for waste prediction.

## Purpose

- Train the Random Forest model.
- Predict fabric waste percentage and efficiency level.
- Save and load trained model files.

## Notes

- Do not place layout calculation logic here.
- The first working version should use Random Forest.
- SNN integration can be added later.

## Prototype Files

- `train_model.py` - trains and saves the Random Forest model.
- `predict_waste.py` - loads the saved model and predicts waste percentage.
- `random_forest_waste_model.joblib` - generated trained model file.

## Train Model

```bash
python model/train_model.py
```

Current prototype target:

- Predict `Waste_Percentage`.
- Keep SNN as future scope.
