import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from data_utils import validate_customer_features


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

MODEL_PATH = DATA_DIR / "kmeans_model.pkl"
SCALER_PATH = DATA_DIR / "scaler.pkl"
FEATURES_PATH = DATA_DIR / "features.json"
CLUSTER_LABELS_PATH = DATA_DIR / "cluster_labels.json"
DEMO_DATA_PATH = DATA_DIR / "customer_segments_with_ml.csv"


def load_demo_data():
    return pd.read_csv(DEMO_DATA_PATH)


def load_feature_names():
    with open(FEATURES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    features = load_feature_names()

    with open(CLUSTER_LABELS_PATH, "r", encoding="utf-8") as f:
        cluster_labels = json.load(f)

    cluster_labels = {int(k): v for k, v in cluster_labels.items()}
    return model, scaler, features, cluster_labels


def segment_customer_features(feature_df):
    model, scaler, features, cluster_labels = load_artifacts()
    result_df = validate_customer_features(feature_df, features)
    X = result_df[features].copy()

    log_features = [
        "frequency",
        "monetary",
        "avg_order_value",
        "unique_products",
        "total_quantity",
        "customer_lifetime_days",
    ]

    available_log_features = [col for col in log_features if col in X.columns]
    X[available_log_features] = np.log1p(X[available_log_features])

    X_scaled = scaler.transform(X)
    result_df["ml_cluster"] = model.predict(X_scaled)
    result_df["ml_segment"] = result_df["ml_cluster"].map(cluster_labels)
    return result_df
