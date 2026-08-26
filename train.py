"""Train one predefined screening model and evaluate the untouched test set once."""

from __future__ import annotations

import json
import platform
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
import xgboost
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "processed" / "kyrbs2020_clean_v1.csv"
MODEL_DIR = ROOT / "models"
FEATURES = [
    "gender", "school", "grade", "income", "anxiety", "stress", "despair",
    "suicidal_thoughts", "smartphone_use_day", "smartphone_use_weekend",
    "smartphone_dependence", "sleep_quality",
]
ENCODE_MAP = {
    "gender": {"Female": 0, "Male": 1},
    "school": {"Middle school": 0, "High school": 1},
    "grade": {"Low": 0, "Middle": 1, "High": 2},
    "income": {"Low": 0, "Middle": 1, "High": 2},
    "anxiety": {"No": 0, "Mild": 1, "Moderate": 2, "Severe": 3},
    "stress": {"Low": 0, "Middle": 1, "High": 2},
    "despair": {"No": 0, "Yes": 1},
    "suicidal_thoughts": {"No": 0, "Yes": 1},
    "smartphone_use_day": {"≤3": 0, "3 ~ 5": 1, "5 ~ 8": 2, "≥8": 3},
    "smartphone_use_weekend": {"≤3": 0, "3 ~ 5": 1, "5 ~ 8": 2, "≥8": 3},
    "smartphone_dependence": {"No": 0, "Risk": 1},
    "sleep_quality": {"No": 0, "Yes": 1},
}
TARGET_RECALL = 0.85
SEED = 42


def encode(df: pd.DataFrame) -> pd.DataFrame:
    encoded = df[FEATURES].copy()
    for column, mapping in ENCODE_MAP.items():
        encoded[column] = encoded[column].map(mapping)
    if encoded.isna().any().any():
        raise ValueError("Unknown category found during feature encoding")
    return encoded


def threshold_for_recall(y_true: np.ndarray, probability: np.ndarray, weight: np.ndarray) -> float:
    _, tpr, thresholds = roc_curve(y_true, probability, sample_weight=weight)
    valid = np.flatnonzero(tpr >= TARGET_RECALL)
    return float(thresholds[valid[np.argmax(thresholds[valid])]]) if len(valid) else 0.5


def metrics(y_true: np.ndarray, probability: np.ndarray, weight: np.ndarray, threshold: float) -> dict:
    predicted = (probability >= threshold).astype(int)
    return {
        "auc": float(roc_auc_score(y_true, probability, sample_weight=weight)),
        "accuracy": float(accuracy_score(y_true, predicted, sample_weight=weight)),
        "precision": float(precision_score(y_true, predicted, sample_weight=weight, zero_division=0)),
        "recall": float(recall_score(y_true, predicted, sample_weight=weight, zero_division=0)),
        "f1": float(f1_score(y_true, predicted, sample_weight=weight, zero_division=0)),
    }


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    x = encode(df).to_numpy(dtype=float)
    y = (df["oral_health"] == "Yes").astype(int).to_numpy()
    weight = df["W"].to_numpy(dtype=float)
    x_tv, x_test, y_tv, y_test, w_tv, w_test = train_test_split(
        x, y, weight, test_size=0.2, stratify=y, random_state=SEED
    )
    x_train, x_val, y_train, y_val, w_train, w_val = train_test_split(
        x_tv, y_tv, w_tv, test_size=0.25, stratify=y_tv, random_state=SEED
    )
    scaler = StandardScaler().fit(x_train, sample_weight=w_train)
    x_train_s, x_val_s, x_test_s = map(scaler.transform, (x_train, x_val, x_test))
    model = XGBClassifier(
        n_estimators=250, max_depth=5, learning_rate=0.05, subsample=0.8,
        colsample_bytree=0.8, min_child_weight=20, eval_metric="logloss",
        random_state=SEED, n_jobs=-1,
    )
    model.fit(x_train_s, y_train, sample_weight=w_train, verbose=False)
    threshold = threshold_for_recall(y_val, model.predict_proba(x_val_s)[:, 1], w_val)
    validation = metrics(y_val, model.predict_proba(x_val_s)[:, 1], w_val, threshold)
    test = metrics(y_test, model.predict_proba(x_test_s)[:, 1], w_test, threshold)
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "xgboost_model.pkl")
    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
    report = {
        "model_name": "XGBoost predefined deployment model",
        "purpose": "oral symptom risk-group screening support; not diagnosis",
        "features": FEATURES,
        "target": "oral_health",
        "threshold_rule": "highest validation threshold with weighted recall >= 0.85",
        "screening_threshold": threshold,
        "validation_metrics": validation,
        "test_metrics": test,
        "split": {"train": len(y_train), "validation": len(y_val), "test": len(y_test), "seed": SEED},
        "encode_map": ENCODE_MAP,
        "runtime": {"python": platform.python_version(), "scikit_learn": sklearn.__version__, "xgboost": xgboost.__version__},
    }
    (MODEL_DIR / "model_meta.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
