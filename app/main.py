"""
RetailMind: Flask Web Application
Module: app/main.py
Serves the retail intelligence dashboard and predictive REST API endpoints.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify

# Ensure local imports work
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from src.predict import SalesForecaster
from src.segment import CustomerSegmenter

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static")
)

forecaster = SalesForecaster()
segmenter = CustomerSegmenter()

# Pre-packaged retail operational scenarios for 1-click testing
RETAIL_SCENARIOS = {
    "holiday_surge": {
        "title": "🎉 Holiday Super Sale",
        "category": "Electronics",
        "price": 179.99,
        "discount": 0.20,
        "is_holiday": 1,
        "is_weekend": 1,
        "advertising_spend": 1800.0,
        "customer_footfall": 2600,
        "month": 12
    },
    "weekend_promo": {
        "title": "🛍️ Weekend Apparel Promo",
        "category": "Apparel",
        "price": 42.00,
        "discount": 0.15,
        "is_holiday": 0,
        "is_weekend": 1,
        "advertising_spend": 950.0,
        "customer_footfall": 1750,
        "month": 7
    },
    "grocery_rush": {
        "title": "🛒 Midweek Grocery Restock",
        "category": "Groceries",
        "price": 14.50,
        "discount": 0.05,
        "is_holiday": 0,
        "is_weekend": 0,
        "advertising_spend": 400.0,
        "customer_footfall": 1400,
        "month": 5
    }
}


@app.route("/")
def index():
    """Renders main dashboard."""
    return render_template("index.html", scenarios=RETAIL_SCENARIOS)


@app.route("/forecast", methods=["POST"])
def forecast():
    """Endpoint for demand forecasting."""
    try:
        data = request.get_json(silent=True) or request.form
        result = forecaster.forecast(data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/segment", methods=["POST"])
def segment():
    """Endpoint for customer RFM segmentation."""
    try:
        data = request.get_json(silent=True) or request.form
        recency = int(data.get("recency", 30))
        frequency = int(data.get("frequency", 5))
        monetary = float(data.get("monetary", 500.0))

        result = segmenter.segment_customer(recency, frequency, monetary)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/scenarios", methods=["GET"])
def get_scenarios():
    """Returns curated operational scenarios."""
    return jsonify({"success": True, "scenarios": RETAIL_SCENARIOS})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "RetailMind"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    print(f"Starting RetailMind on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
