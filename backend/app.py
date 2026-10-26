from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load trained ML model
model = joblib.load("used_car_price_model.pkl")


@app.route("/")
def home():
    return jsonify({
        "message": "Used Car Price Prediction API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        input_data = pd.DataFrame({
            "year": [int(data["year"])],
            "km_driven": [int(data["km_driven"])],
            "fuel": [data["fuel"]],
            "seller_type": [data["seller_type"]],
            "transmission": [data["transmission"]],
            "owner": [data["owner"]],
            "brand": [data["brand"]]
        })

        prediction = model.predict(input_data)[0]

        return jsonify({
            "success": True,
            "predicted_price": round(float(prediction), 2)
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)