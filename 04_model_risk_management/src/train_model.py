"""
Module 4: Model Risk Management
train_model.py — trains a proxy XGBoost credit scoring model on synthetic
UGRO MSME data, mimicking GRO Score 3.0 at a structural level.

IMPORTANT: This is a proxy model built on synthetic data for independent
governance assessment purposes. It does not reflect UGRO Capital's actual
GRO Score 3.0 model, architecture, or feature weights.
"""

import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, classification_report,
    confusion_matrix, average_precision_score
)
import xgboost as xgb

# ---- Constants ----

DATA_PATH = "01_data_quality/data/raw/ugro_msme_clean.csv"
MODEL_DIR = "04_model_risk_management/models"
DATA_OUT_DIR = "04_model_risk_management/data"
REPORTS_DIR = "04_model_risk_management/reports"

EXCLUDE_COLS = [
    "applicant_id", "application_date", "pan_number", "gstin",
    "gst_registration_date", "loan_status", "default_flag",
    "approved_loan_amount"
]

CATEGORICAL_COLS = ["state", "sector", "entity_type", "proprietor_gender"]
TARGET_COL = "default_flag"

# class imbalance ratio: ~5928 / 1635
SCALE_POS_WEIGHT = 3.6


# ---- Step 1: Load and filter data ----

def load_and_filter_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Full dataset shape: {df.shape}")
    print(f"loan_status value counts:\n{df['loan_status'].value_counts()}\n")

    disbursed = df[df["loan_status"] == "Disbursed"].copy()
    print(f"Disbursed-only shape: {disbursed.shape}")

    default_rate = disbursed["default_flag"].mean()
    print(f"Default rate among Disbursed loans: {default_rate:.4f}")
    print(f"Default counts:\n{disbursed['default_flag'].value_counts()}\n")

    return disbursed


# ---- Step 2: Feature engineering and split ----

def prepare_features(df: pd.DataFrame):
    """
    One-hot encode categoricals explicitly before splitting.
    This avoids silent category-code mismatches between train/test
    that occur with XGBoost's native enable_categorical on split data.
    Returns X (DataFrame, fully numeric), y (Series), feature_names (list).
    """
    feature_cols = [c for c in df.columns if c not in EXCLUDE_COLS]
    X_raw = df[feature_cols].copy()
    y = df[TARGET_COL].astype(int)

    # One-hot encode — drop_first=False so all categories are visible to SHAP
    X = pd.get_dummies(X_raw, columns=CATEGORICAL_COLS, drop_first=False)
    feature_names = list(X.columns)

    print(f"Feature matrix shape after encoding: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}\n")
    return X, y, feature_names


def split_data(X: pd.DataFrame, y: pd.Series, test_size=0.2, seed=42):
    """
    Stratified 80/20 split — preserves default rate in both splits.
    Seed fixed to 42 for reproducibility across all modules.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y
    )
    print(f"Train shape: {X_train.shape} | Default rate: {y_train.mean():.4f}")
    print(f"Test shape:  {X_test.shape} | Default rate: {y_test.mean():.4f}\n")
    return X_train, X_test, y_train, y_test


# ---- Step 3: Train XGBoost model ----

def train_model(X_train, y_train):
    """
    Train proxy XGBoost classifier.
    Deliberately moderate hyperparameters — not tuned for maximum AUC.
    scale_pos_weight corrects for 21.6% minority class imbalance.
    """
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=SCALE_POS_WEIGHT,
        eval_metric="auc",
        random_state=42,
        verbosity=1
    )

    print("Training XGBoost model...")
    model.fit(X_train, y_train)
    print("Training complete.\n")
    return model


# ---- Step 4: Evaluate model ----

def evaluate_model(model, X_test, y_test):
    """
    Compute AUC-ROC, Average Precision, confusion matrix,
    and classification report. Returns metrics dict.
    """
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = model.predict(X_test)

    auc = roc_auc_score(y_test, y_pred_proba)
    avg_precision = average_precision_score(y_test, y_pred_proba)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred,
                                   target_names=["No Default", "Default"])

    print("=" * 50)
    print(f"AUC-ROC:           {auc:.4f}")
    print(f"Average Precision: {avg_precision:.4f}")
    print("=" * 50)
    print(f"\nConfusion Matrix:\n{cm}")
    print(f"\nClassification Report:\n{report}")

    tn, fp, fn, tp = cm.ravel()
    metrics = {
        "auc_roc": round(auc, 4),
        "average_precision": round(avg_precision, 4),
        "true_positives": int(tp),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "precision_default": round(tp / (tp + fp), 4) if (tp + fp) > 0 else 0,
        "recall_default": round(tp / (tp + fn), 4) if (tp + fn) > 0 else 0,
        "n_test": int(len(y_test)),
        "n_train": int(len(y_test) * 4),
        "feature_count": int(X_test.shape[1])
    }
    return metrics


# ---- Step 5: Save model and artifacts ----

def save_artifacts(model, X_test, y_test, metrics, feature_names):
    """
    Save trained model, test set, and metrics JSON.
    These are consumed by psi_monitor.py and the dashboard.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(DATA_OUT_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Save model
    model_path = os.path.join(MODEL_DIR, "gro_score_proxy_v1.json")
    model.save_model(model_path)
    print(f"Model saved: {model_path}")

    # Save feature names list for downstream use
    feature_path = os.path.join(MODEL_DIR, "feature_names.json")
    with open(feature_path, "w") as f:
        json.dump(feature_names, f, indent=2)
    print(f"Feature names saved: {feature_path}")

    # Save test set with predictions for downstream modules
    # Also reload original categorical columns from clean dataset
    # so Module 5 bias audit has access to pre-encoded protected attributes
    full_df = pd.read_csv(DATA_PATH)
    disbursed_df = full_df[full_df["loan_status"] == "Disbursed"].copy()

    # Match test set rows using index alignment from split
    original_cats = disbursed_df[CATEGORICAL_COLS].loc[X_test.index].reset_index(drop=True)

    X_test_save = X_test.copy().reset_index(drop=True)
    X_test_save["default_flag"] = y_test.values
    X_test_save["predicted_proba"] = model.predict_proba(X_test)[:, 1]

    # Prepend original categorical columns for bias audit
    for col in CATEGORICAL_COLS:
        X_test_save[col] = original_cats[col].values

    test_path = os.path.join(DATA_OUT_DIR, "test_set_with_predictions.csv")
    X_test_save.to_csv(test_path, index=False)
    print(f"Test set saved: {test_path}")

    # Save metrics
    metrics_path = os.path.join(REPORTS_DIR, "model_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved: {metrics_path}")


# ---- Entry point ----

if __name__ == "__main__":
    disbursed_df = load_and_filter_data(DATA_PATH)
    X, y, feature_names = prepare_features(disbursed_df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    model = train_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    save_artifacts(model, X_test, y_test, metrics, feature_names)
    print(f"\nFeatures after encoding: {len(feature_names)}")
    print("Module 4 training pipeline complete.")
