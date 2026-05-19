# AI-Powered Fabric Waste Prediction & Cutting Optimization System

This project predicts fabric waste and helps optimize cutting layouts for textile factories and tailors.

## Project Structure

- `dataset/` - dataset generation and sample fabric waste data
- `logic/` - mathematical layout and cutting calculations
- `model/` - machine learning models for waste prediction
- `backend/` - API layer for connecting the UI, logic, and model
- `frontend/` - user interface for input and result display
- `docs/` - documentation and project notes

## Current Goal

Build a simple working system using Random Forest first. Advanced SNN integration can be added later.

## Prototype Run Order

1. Generate or refresh the dataset:

```bash
python dataset/generate_dataset.py
```

2. Train the Random Forest model:

```bash
python model/train_model.py
```

3. Start the Flask backend:

```bash
python backend/app.py
```

4. Open the frontend:

```text
frontend/index.html
```

## Current Prototype Status

- Dataset generator is available.
- Logic engine is implemented.
- Random Forest training and prediction modules are implemented.
- Flask backend is implemented.
- Simple frontend is implemented.
- SNN remains future scope.
