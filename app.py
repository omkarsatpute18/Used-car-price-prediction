from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

FRONTEND_DIR = BASE_DIR / "frontend"

MODEL_PATH = BASE_DIR / "used_car_price_model.pkl"


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=""
)


# ============================================================
# LOAD MACHINE LEARNING MODEL
# ============================================================

try:

    model = joblib.load(MODEL_PATH)

    print("Model loaded successfully.")

except Exception as error:

    model = None

    print("ERROR: Model could not be loaded.")
    print(error)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    if model is None:

        return jsonify({
            "status": "error",
            "model_loaded": False
        }), 500

    return jsonify({
        "status": "ok",
        "model_loaded": True,
        "message": "Used Car Price Prediction API is running"
    })


# ============================================================
# PREDICTION API
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ----------------------------------------------------
        # Check model
        # ----------------------------------------------------

        if model is None:

            return jsonify({
                "success": False,
                "error": "Machine learning model is not available."
            }), 500


        # ----------------------------------------------------
        # Read request
        # ----------------------------------------------------

        data = request.get_json(silent=True)


        if not data:

            return jsonify({
                "success": False,
                "error": "No input data was received."
            }), 400


        # ----------------------------------------------------
        # Extract values
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

        values = {
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

            for field, value in values.items()

            if value is None or str(value).strip() == ""

        ]


        if missing_fields:

            return jsonify({

                "success": False,

                "error":
                    "Missing fields: "
                    + ", ".join(missing_fields)

            }), 400


        # ----------------------------------------------------
        # Convert numeric values
        # ----------------------------------------------------

        try:

            year = int(year)

            km_driven = int(km_driven)

        except (ValueError, TypeError):

            return jsonify({

                "success": False,

                "error":
                    "Year and kilometers driven "
                    "must be valid numbers."

            }), 400


        # ----------------------------------------------------
        # Validate values
        # ----------------------------------------------------

        if year < 1990 or year > 2026:

            return jsonify({

                "success": False,

                "error":
                    "Please enter a valid manufacturing year."

            }), 400


        if km_driven < 0:

            return jsonify({

                "success": False,

                "error":
                    "Kilometers driven cannot be negative."

            }), 400


        # ----------------------------------------------------
        # Create DataFrame
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
        # Safety check
        # ----------------------------------------------------

        if prediction < 0:

            prediction = 0


        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "predicted_price":
                round(float(prediction), 2)

        })


    except Exception as error:

        print("Prediction error:")
        print(error)


        return jsonify({

            "success": False,

            "error":
                "An error occurred while predicting "
                "the car price."

        }), 500


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 50)
    print("USED CAR PRICE PREDICTION")
    print("=" * 50)
    print()
    print("Website:")
    print("http://127.0.0.1:5000/")
    print()
    print("Health:")
    print("http://127.0.0.1:5000/health")
    print()
    print("Prediction API:")
    print("http://127.0.0.1:5000/predict")
    print()
    print("=" * 50)


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )