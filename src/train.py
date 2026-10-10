"""
RetailMind: Model Training and Serialization Pipeline
Module: src/train.py
Trains predictive sales regression model and customer RFM clustering pipeline,
saving serialized model artifacts in models/.
"""

import os
import sys
import argparse
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, silhouette_score

# Ensure local imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.preprocess import prepare_sales_features


def train_sales_model(data_path: str, models_dir: str):
    """Trains regression pipeline for weekly sales demand prediction."""
    print("Loading retail sales data:", data_path)
    df = pd.read_csv(data_path)
    X, y = prepare_sales_features(df)
    
    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Preprocessor
    categorical_features = ["category"]
    numeric_features = [
        "store_id", "price", "discount", "is_holiday",
        "is_weekend", "advertising_spend", "customer_footfall", "month"
    ]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
            ("num", StandardScaler(), numeric_features)
        ]
    )
    
    # Regression model
    model_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=120, max_depth=12, random_state=42))
    ])
    
    print("Fitting Random Forest Demand Forecaster...")
    model_pipeline.fit(X_train, y_train)
    
    # Evaluation
    y_pred = model_pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"Sales Model Test R² Score:   {r2 * 100:.2f}%")
    print(f"Sales Model Mean Abs Error: {mae:.2f} units")
    print(f"Sales Model Root MSE:       {rmse:.2f} units")
    
    # Save model
    sales_model_path = os.path.join(models_dir, "sales_forecast_model.pkl")
    joblib.dump(model_pipeline, sales_model_path)
    print(f"Saved Sales Pipeline to:    {sales_model_path}")
    
    return model_pipeline, {"r2": r2, "mae": mae, "rmse": rmse}


def train_rfm_model(data_path: str, models_dir: str):
    """Trains K-Means segmentation pipeline for customer RFM analysis."""
    print("\nLoading RFM customer data:", data_path)
    df = pd.read_csv(data_path)
    
    rfm_features = ["recency_days", "frequency", "monetary_spend"]
    X = df[rfm_features].copy()
    
    # Scaling + KMeans pipeline
    rfm_pipeline = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("kmeans", KMeans(n_clusters=4, random_state=42, n_init=10))
    ])
    
    print("Fitting K-Means Clustering Pipeline (k=4)...")
    rfm_pipeline.fit(X)
    
    # Evaluate silhouette score
    scaled_X = rfm_pipeline.named_steps["scaler"].transform(X)
    cluster_labels = rfm_pipeline.named_steps["kmeans"].labels_
    sil_score = silhouette_score(scaled_X, cluster_labels)
    
    print(f"RFM Clustering Silhouette Score: {sil_score:.3f}")
    
    # Save model
    rfm_model_path = os.path.join(models_dir, "rfm_kmeans_model.pkl")
    joblib.dump(rfm_pipeline, rfm_model_path)
    print(f"Saved RFM Pipeline to:           {rfm_model_path}")
    
    return rfm_pipeline, {"silhouette": sil_score}


def train_all(
    sales_path: str = "data/retail_sales.csv",
    rfm_path: str = "data/customer_rfm.csv",
    models_dir: str = "models"
):
    """Runs complete training workflow for both retail pipelines."""
    os.makedirs(models_dir, exist_ok=True)
    print("=" * 60)
    print("RetailMind: End-to-End Model Training Pipeline")
    print("=" * 60)
    
    train_sales_model(sales_path, models_dir)
    train_rfm_model(rfm_path, models_dir)
    
    print("=" * 60)
    print("All RetailMind models trained and saved successfully!")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train RetailMind models")
    parser.add_argument("--sales_data", default="data/retail_sales.csv")
    parser.add_argument("--rfm_data", default="data/customer_rfm.csv")
    parser.add_argument("--output", default="models")
    args = parser.parse_args()
    
    train_all(args.sales_data, args.rfm_data, args.output)
