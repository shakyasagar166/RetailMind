"""
RetailMind: Sales Forecasting Inference Engine
Module: src/predict.py
Provides sales demand predictions and inventory restock calculations.
"""

import os
import sys
import argparse
import joblib
import pandas as pd
from typing import Dict, Any, Optional

# Ensure local imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.preprocess import encode_input_record, FEATURE_COLUMNS


class SalesForecaster:
    """Predictive sales and inventory intelligence engine."""

    def __init__(self, model_path: Optional[str] = None):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.model_path = model_path or os.path.join(base_dir, "models", "sales_forecast_model.pkl")
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            raise FileNotFoundError(f"Model not found at {self.model_path}. Run 'python src/train.py' first.")

    def forecast(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predicts weekly unit sales and estimated gross revenue.
        """
        clean_input = encode_input_record(input_data)
        input_df = pd.DataFrame([clean_input])[FEATURE_COLUMNS]

        # Predict units
        predicted_units = float(self.pipeline.predict(input_df)[0])
        predicted_units = max(10, round(predicted_units))

        price = clean_input["price"]
        discount = clean_input["discount"]
        effective_price = price * (1.0 - discount)
        projected_revenue = round(predicted_units * effective_price, 2)

        # Inventory guidance
        safety_stock = int(predicted_units * 1.25)
        reorder_point = int(predicted_units * 0.45)

        if predicted_units > 500:
            demand_status = "High Demand Surge"
            status_color = "danger"
        elif predicted_units > 250:
            demand_status = "Moderate Demand"
            status_color = "warning"
        else:
            demand_status = "Steady Baseline"
            status_color = "success"

        return {
            "predicted_units": predicted_units,
            "projected_revenue": projected_revenue,
            "demand_status": demand_status,
            "status_color": status_color,
            "recommended_safety_stock": safety_stock,
            "recommended_reorder_point": reorder_point,
            "effective_price": round(effective_price, 2),
            "inputs": clean_input
        }


# Singleton accessor
_forecaster = None

def forecast_sales(params: Dict[str, Any]) -> Dict[str, Any]:
    global _forecaster
    if _forecaster is None:
        _forecaster = SalesForecaster()
    return _forecaster.forecast(params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict retail sales")
    parser.add_argument("--category", default="Electronics")
    parser.add_argument("--price", type=float, default=199.99)
    parser.add_argument("--discount", type=float, default=0.15)
    parser.add_argument("--holiday", type=int, default=1)
    parser.add_argument("--footfall", type=int, default=2200)
    args = parser.parse_args()

    sample = {
        "store_id": 1,
        "category": args.category,
        "price": args.price,
        "discount": args.discount,
        "is_holiday": args.holiday,
        "is_weekend": 1,
        "advertising_spend": 1200.0,
        "customer_footfall": args.footfall,
        "month": 11
    }

    result = forecast_sales(sample)
    print("\n--- RetailMind Demand Forecast ---")
    print(f"Predicted Sales:       {result['predicted_units']} units")
    print(f"Projected Revenue:     ${result['projected_revenue']:,.2f}")
    print(f"Demand Status:         {result['demand_status']}")
    print(f"Safety Stock Target:   {result['recommended_safety_stock']} units")
    print(f"Reorder Point:         {result['recommended_reorder_point']} units")
