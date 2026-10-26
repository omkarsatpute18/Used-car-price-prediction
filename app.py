from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"
MODEL_PATH = BASE_DIR / "used_car_price_model.pkl"


# ============================================================
# FLASK APP
# ============================================================

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=""
)

CORS(app)


# ============================================================
# LOAD MODEL
# ============================================================

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
    print(f"Model path: {MODEL_PATH}")

except Exception as error:
    model = None
    print("ERROR: Could not load the model.")
    print(error)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


# ============================================================
# PREDICTION API
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Check whether model is available
        if model is None:
            return jsonify({
                "success": False,
                "error": "Machine learning model could not be loaded."
            }), 500


        # Get JSON data
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400


        # ----------------------------------------------------
        # Get input values
        # ----------------------------------------------------

        brand = data.get("brand")
        year = data.get("year")
        km_driven = data.get("km_driven")
        fuel = data.get("fuel")
        seller_type = data.get("seller_type")
        transmission = data.get("transmission")
        owner = data.get("owner")


        # ----------------------------------------------------
        # Validate required fields
        # ----------------------------------------------------

        required_fields = {
            "brand": brand,
            "year": year,
            "km_driven": km_driven,
            "fuel": fuel,
            "seller_type": seller_type,
            "transmission": transmission,
            "owner": owner
        }

        missing_fields = [
            field
            for field, value in required_fields.items()
            if value is None or value == ""
        ]

        if missing_fields:

            return jsonify({
                "success": False,
                "error": (
                    "Missing fields: "
                    + ", ".join(missing_fields)
                )
            }), 400


        # ----------------------------------------------------
        # Convert numeric values
        # ----------------------------------------------------

        try:

            year = int(year)
            km_driven = int(km_driven)

        except ValueError:

            return jsonify({
                "success": False,
                "error": "Year and kilometers must be numbers."
            }), 400


        # ----------------------------------------------------
        # Create input DataFrame
        # ----------------------------------------------------

        input_data = pd.DataFrame({

            "year": [year],

            "km_driven": [km_driven],

            "fuel": [fuel],

            "seller_type": [seller_type],

            "transmission": [transmission],

            "owner": [owner],

            "brand": [brand]

        })


        # ----------------------------------------------------
        # Make prediction
        # ----------------------------------------------------

        prediction = model.predict(input_data)[0]


        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "predicted_price": round(
                float(prediction),
                2
            )

        })


    except Exception as error:

        print("Prediction error:")
        print(error)

        return jsonify({

            "success": False,

            "error": str(error)

        }), 400


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("---------------------------------------------")
    print("Used Car Price Prediction")
    print("---------------------------------------------")
    print("Frontend: http://127.0.0.1:5000/")
    print("API:      http://127.0.0.1:5000/predict")
    print("---------------------------------------------")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )