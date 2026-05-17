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
