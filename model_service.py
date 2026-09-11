from __future__ import annotations

import json

import joblib
import numpy as np
import streamlit as st

from config import MODELS_DIR


@st.cache_resource(show_spinner=False)
def load_ml_assets():
    paths = [
        MODELS_DIR / "xgboost_model.pkl",
        MODELS_DIR / "scaler.pkl",
        MODELS_DIR / "model_meta.json",
    ]
    if not all(path.exists() for path in paths):
        return None, None, None
    model = joblib.load(paths[0])
    scaler = joblib.load(paths[1])
    metadata = json.loads(paths[2].read_text(encoding="utf-8"))
    return model, scaler, metadata


def encode_answers(
    gender: str,
    school: str,
    grade: str,
    income: str,
    weekday: str,
    weekend: str,
    smartphone_group: str,
    sleep_group: str,
) -> np.ndarray:
    values = [
        {"여학생": 0, "남학생": 1}[gender],
        {"중학교": 0, "고등학교": 1}[school],
        {"하": 0, "중": 1, "상": 2}[grade],
        {"하": 0, "중": 1, "상": 2}[income],
        {"3시간 이하": 0, "3~5시간": 1, "5~8시간": 2, "8시간 이상": 3}[weekday],
        {"3시간 이하": 0, "3~5시간": 1, "5~8시간": 2, "8시간 이상": 3}[weekend],
        int(smartphone_group == "위험군"),
        int(sleep_group == "부족"),
    ]
    return np.asarray([values], dtype=float)


def risk_label(score: float, threshold: float) -> str:
    return "주의" if score >= threshold else "낮음"


def risk_colors(score: float, threshold: float) -> tuple[str, str, str]:
    if score >= threshold:
        return "#b42318", "#fbeae9", "#b42318"
    return "#067647", "#e5f5ed", "#067647"
