# Backend

This folder will contain the API layer for the fabric waste prediction system.

## Purpose

- Receive fabric and pattern input from the frontend.
- Call layout calculation functions from `logic/`.
- Call waste prediction models from `model/`.
- Return prediction and optimization results through API endpoints.

## Notes

- Keep API code separate from calculation and machine learning code.
- Flask or FastAPI can be added here later.

## Prototype File

- `app.py` - Flask API with:
  - `GET /health`
  - `POST /predict`

## Run Backend

```bash
python backend/app.py
```

The local API runs at:

```text
http://127.0.0.1:5000
```
