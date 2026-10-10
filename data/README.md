# RetailMind Datasets Documentation

## Overview
The `RetailMind` data layer comprises two interconnected retail intelligence datasets engineered for predictive sales forecasting, demand planning, and customer lifetime value (CLV) behavioral segmentation.

---

## 1. Retail Sales & Demand Dataset: `retail_sales.csv`

Contains 1,000 retail transaction records across 10 commercial store locations and 5 high-volume product categories.

| Column Name | Type | Description | Range / Example |
| :--- | :--- | :--- | :--- |
| `transaction_id` | Integer | Unique identifier for weekly store record | `1` to `1000` |
| `store_id` | Integer | Retail branch identifier | `1` to `10` |
| `category` | String | Merchandise department | `Electronics`, `Apparel`, `Groceries`, etc. |
| `price` | Float | Unit price in USD ($) | `$12.50` – `$225.00` |
| `discount` | Float | Promotional markdown rate | `0.00` – `0.30` (0% to 30%) |
| `is_holiday` | Integer | Binary holiday indicator | `1` (Holiday), `0` (Standard) |
| `is_weekend` | Integer | Weekend shopping flag | `1` (Weekend), `0` (Weekday) |
| `advertising_spend` | Float | Marketing spend in USD ($) | `$200.00` – `$2,500.00` |
| `customer_footfall` | Integer | In-store foot traffic volume | `400` – `3,200` visitors |
| `month` | Integer | Calendar month | `1` (Jan) to `12` (Dec) |
| `weekly_sales_units`| Integer | **Target:** Total quantity of units sold | `90` – `1,500` units |
| `total_revenue` | Float | Total gross sales revenue ($) | `weekly_sales_units * price * (1 - discount)` |

---

## 2. Customer RFM Segmentation Dataset: `customer_rfm.csv`

Contains 600 customer profiles with Recency, Frequency, and Monetary (RFM) behavioral metrics for clustering and loyalty modeling.

| Column Name | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `customer_id` | Integer | Unique customer account ID | `1001` |
| `recency_days` | Integer | Days since last retail transaction | `1` to `365` days |
| `frequency` | Integer | Total order transactions in past 12 months | `1` to `48` orders |
| `monetary_spend`| Float | Cumulative spend in USD ($) | `$45.00` – `$5,400.00` |
| `segment_label` | String | Target behavioral cluster | `Champions / VIP`, `Loyal Customers`, `At Risk` |

---

## Usage in Models
1. **Sales Forecaster (`src/train.py`):** Trains regression models (Random Forest / Gradient Boosting) to forecast sales volume and gross revenue given price, discount, advertising, footfall, and seasonal indicators.
2. **Customer Segmentation (`src/segment.py`):** Trains K-Means clustering with standard feature scaling on normalized RFM scores to identify churn risk and high-value customer segments.
