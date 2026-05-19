# Frontend

This folder will contain the user interface for the fabric waste prediction system.

## Purpose

- Collect fabric size and pattern details from users.
- Show predicted waste, utilization, and efficiency.
- Display cutting layout guidance in a clear visual format.

## Notes

- Keep UI code separate from backend and model code.
- Build simple screens first before adding advanced visualization.

## Prototype Files

- `index.html` - input form and result area.
- `style.css` - simple responsive styling.
- `script.js` - calls the Flask `/predict` API.

## Run Frontend

Start the backend first:

```bash
python backend/app.py
```

Then open:

```text
frontend/index.html
```
