import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory


PROJECT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"
sys.path.append(str(PROJECT_DIR))

from logic.layout_calculator import calculate_layout
from model.predict_waste import predict_waste


app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    """Allow the simple frontend page to call this local prototype API."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


def get_request_value(data, key, default=None):
    """Read a value from frontend data with a simple default."""
    value = data.get(key, default)
    if value == "":
        return default
    return value


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


@app.route("/", methods=["GET"])
def home():
    """Serve the prototype frontend from the Flask backend."""
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:file_name>", methods=["GET"])
def frontend_files(file_name):
    """Serve CSS and JavaScript files used by the frontend."""
    return send_from_directory(FRONTEND_DIR, file_name)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json() or {}

        # Step 1: Run mathematical cutting layout calculations.
        layout_result = calculate_layout(
            get_request_value(data, "Fabric_Length"),
            get_request_value(data, "Fabric_Width"),
            get_request_value(data, "Piece_Length"),
            get_request_value(data, "Piece_Width"),
        )

        # Step 2: Prepare the exact feature shape expected by the ML model.
        model_input = {
            "Fabric_Length": float(get_request_value(data, "Fabric_Length")),
            "Fabric_Width": float(get_request_value(data, "Fabric_Width")),
            "Piece_Length": float(get_request_value(data, "Piece_Length")),
            "Piece_Width": float(get_request_value(data, "Piece_Width")),
            "Fabric_Type": get_request_value(data, "Fabric_Type", "Cotton"),
            "GSM": int(float(get_request_value(data, "GSM", 180))),
            "Defect_Count": int(float(get_request_value(data, "Defect_Count", 0))),
            "Marker_Efficiency": float(get_request_value(data, "Marker_Efficiency", 85)),
            "Layout_Type": get_request_value(
                data,
                "Layout_Type",
                layout_result["selected_orientation"],
            ),
            "Pieces_Along_Length": layout_result["pieces_along_length"],
            "Pieces_Along_Width": layout_result["pieces_along_width"],
            "Pieces_Possible": layout_result["pieces_possible"],
        }

        # Step 3: Run AI prediction separately from layout calculations.
        prediction_result = predict_waste(model_input)

        return jsonify(
            {
                "layout": layout_result,
                "prediction": prediction_result,
            }
        )

    except Exception as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=False, port=5000)
