"""
RetailMind: System Evaluation and Benchmarks
Module: src/evaluate.py
Evaluates predictive sales regression metrics and RFM clustering quality.
"""

import os
import sys
import argparse
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, silhouette_score, davies_bouldin_score

# Ensure local imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.preprocess import prepare_sales_features


def evaluate_system(
    sales_path: str = "data/retail_sales.csv",
    rfm_path: str = "data/customer_rfm.csv",
    sales_model_path: str = "models/sales_forecast_model.pkl",
    rfm_model_path: str = "models/rfm_kmeans_model.pkl"
):
    print("=" * 65)
    print("RetailMind: Machine Learning Performance Benchmarks")
    print("=" * 65)

    # 1. Sales Forecasting Evaluation
    print("1. Evaluating Sales Forecasting Engine:")
    if not os.path.exists(sales_model_path):
        raise FileNotFoundError(f"Sales model not found at {sales_model_path}")

    sales_df = pd.read_csv(sales_path)
    X_sales, y_sales = prepare_sales_features(sales_df)

    sales_pipeline = joblib.load(sales_model_path)
    y_pred = sales_pipeline.predict(X_sales)

    r2 = r2_score(y_sales, y_pred)
    mae = mean_absolute_error(y_sales, y_pred)
    rmse = np.sqrt(mean_squared_error(y_sales, y_pred))
    mape = np.mean(np.abs((y_sales - y_pred) / y_sales)) * 100

    print(f"  R² Goodness of Fit:      {r2 * 100:.2f}%")
    print(f"  Mean Absolute Error:     {mae:.2f} units")
    print(f"  Root Mean Squared Error: {rmse:.2f} units")
    print(f"  Mean Abs Percentage Err: {mape:.2f}%")

    # 2. RFM Segmentation Evaluation
    print("\n2. Evaluating Customer RFM Segmentation Engine:")
    if not os.path.exists(rfm_model_path):
        raise FileNotFoundError(f"RFM model not found at {rfm_model_path}")

    rfm_df = pd.read_csv(rfm_path)
    rfm_features = ["recency_days", "frequency", "monetary_spend"]
    X_rfm = rfm_df[rfm_features]

    rfm_pipeline = joblib.load(rfm_model_path)
    scaled_X = rfm_pipeline.named_steps["scaler"].transform(X_rfm)
    clusters = rfm_pipeline.named_steps["kmeans"].predict(scaled_X)

    sil = silhouette_score(scaled_X, clusters)
    db = davies_bouldin_score(scaled_X, clusters)

    print(f"  Clusters Formed (k):     {len(np.unique(clusters))}")
    print(f"  Silhouette Score:        {sil:.3f} (Values > 0.4 indicate robust separation)")
    print(f"  Davies-Bouldin Index:    {db:.3f} (Lower indicates tighter clustering)")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate RetailMind models")
    parser.add_argument("--sales_data", default="data/retail_sales.csv")
    parser.add_argument("--rfm_data", default="data/customer_rfm.csv")
    args = parser.parse_args()

    evaluate_system(args.sales_data, args.rfm_data)
