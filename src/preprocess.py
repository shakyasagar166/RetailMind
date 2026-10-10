"""
RetailMind: Data Preprocessing and Feature Engineering
Module: src/preprocess.py
Prepares retail sales transaction features and RFM customer data for modeling.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any

CATEGORIES = ["Electronics", "Apparel", "Home & Kitchen", "Groceries", "Beauty & Health"]

FEATURE_COLUMNS = [
    "store_id", "category", "price", "discount", "is_holiday",
    "is_weekend", "advertising_spend", "customer_footfall", "month"
]


def prepare_sales_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Extracts features and target variable from sales dataset.
    """
    X = df[FEATURE_COLUMNS].copy()
    y = df["weekly_sales_units"].copy()
    return X, y


def encode_input_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and normalizes single inference input dictionary.
    """
    return {
        "store_id": int(record.get("store_id", 1)),
        "category": str(record.get("category", "Electronics")),
        "price": float(record.get("price", 50.0)),
        "discount": float(record.get("discount", 0.0)),
        "is_holiday": int(record.get("is_holiday", 0)),
        "is_weekend": int(record.get("is_weekend", 0)),
        "advertising_spend": float(record.get("advertising_spend", 500.0)),
        "customer_footfall": int(record.get("customer_footfall", 1200)),
        "month": int(record.get("month", 6))
    }
