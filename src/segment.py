"""
RetailMind: Customer RFM Segmentation Engine
Module: src/segment.py
Analyzes customer Recency, Frequency, and Monetary parameters to classify
profiles into behavioral cohorts and suggest data-driven retention campaigns.
"""

import os
import sys
import argparse
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

# Ensure local imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class CustomerSegmenter:
    """RFM behavioral customer segmentation engine."""

    def __init__(self, model_path: Optional[str] = None):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.model_path = model_path or os.path.join(base_dir, "models", "rfm_kmeans_model.pkl")
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            raise FileNotFoundError(f"RFM model not found at {self.model_path}. Run 'python src/train.py' first.")

    def segment_customer(self, recency: int, frequency: int, monetary: float) -> Dict[str, Any]:
        """
        Assigns customer profile to behavioral cluster and generates marketing actions.
        """
        input_df = pd.DataFrame([{
            "recency_days": float(recency),
            "frequency": float(frequency),
            "monetary_spend": float(monetary)
        }])

        cluster_id = int(self.pipeline.predict(input_df)[0])

        # Cluster interpretation based on RFM heuristics
        if monetary > 2000 and frequency >= 18 and recency <= 30:
            segment_name = "Champions / VIP"
            badge_color = "success"
            strategy = "Reward loyalty with exclusive early-access perks, concierge support, and premium invitations."
            offer = "Complimentary VIP gift & double reward loyalty points"
        elif monetary >= 900 and frequency >= 8:
            segment_name = "Loyal Customers"
            badge_color = "primary"
            strategy = "Upsell higher-margin products and cross-sell related categories based on past purchase history."
            offer = "15% off next order above $100"
        elif recency <= 90:
            segment_name = "Potential Loyalists"
            badge_color = "warning"
            strategy = "Engage with personalized recommendations to build habit and increase order frequency."
            offer = "Free expedited shipping on next 2 orders"
        else:
            segment_name = "At Risk / Inactive"
            badge_color = "danger"
            strategy = "Launch targeted win-back email campaign with aggressive discount incentives before complete churn."
            offer = "25% off reactivation discount voucher"

        return {
            "cluster_id": cluster_id,
            "segment_name": segment_name,
            "badge_color": badge_color,
            "marketing_strategy": strategy,
            "recommended_offer": offer,
            "rfm_scores": {
                "recency_days": recency,
                "frequency": frequency,
                "monetary_spend": round(monetary, 2)
            }
        }


# Singleton accessor
_segmenter = None

def segment_customer(recency: int, frequency: int, monetary: float) -> Dict[str, Any]:
    global _segmenter
    if _segmenter is None:
        _segmenter = CustomerSegmenter()
    return _segmenter.segment_customer(recency, frequency, monetary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify customer RFM segment")
    parser.add_argument("--recency", type=int, default=12, help="Days since last purchase")
    parser.add_argument("--frequency", type=int, default=24, help="Total transactions")
    parser.add_argument("--monetary", type=float, default=3200.0, help="Total spend in $")
    args = parser.parse_args()

    res = segment_customer(args.recency, args.frequency, args.monetary)
    print("\n--- RetailMind Customer RFM Analysis ---")
    print(f"Segment:             {res['segment_name']}")
    print(f"Recommended Offer:   {res['recommended_offer']}")
    print(f"Retention Strategy:  {res['marketing_strategy']}")
