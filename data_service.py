from __future__ import annotations

import io

import numpy as np
import pandas as pd
import streamlit as st

from config import DATA_PATH


def weighted_rate(series: pd.Series, weights: pd.Series, positive: str) -> float:
    mask = series.notna() & weights.notna()
    if mask.sum() == 0:
        return np.nan
    values, valid_weights = series[mask], weights[mask]
    total = valid_weights.sum()
    return float(valid_weights[values == positive].sum() / total) if total else np.nan


def weighted_distribution(
    df: pd.DataFrame, column: str, weight_column: str = "가중치"
) -> pd.DataFrame:
    grouped = df[[column, weight_column]].dropna().groupby(column, as_index=False)[weight_column].sum()
    grouped = grouped.rename(columns={weight_column: "가중치합"})
    grouped["비율"] = grouped["가중치합"] / grouped["가중치합"].sum()
    return grouped.sort_values("비율", ascending=False)


@st.cache_data(show_spinner=False)
def load_and_map_data(source=None) -> pd.DataFrame:
    df = pd.read_csv(source if source is not None else DATA_PATH)
    mapped = df.copy()
    mapped["스마트폰 의존"] = mapped["smartphone_dependence"].map({"No": "일반군", "Risk": "위험군"})
    mapped["구강 증상"] = mapped["oral_health"].map({"No": "없음", "Yes": "있음"})
    mapped["수면 상태"] = mapped["sleep_quality"].map({"No": "충분", "Yes": "부족"})
    time_map = {"≤3": "3시간 이하", "3 ~ 5": "3~5시간", "5 ~ 8": "5~8시간", "≥8": "8시간 이상"}
    mapped["주중 스마트폰 사용"] = mapped["smartphone_use_day"].map(time_map)
    mapped["주말 스마트폰 사용"] = mapped["smartphone_use_weekend"].map(time_map)
    mapped["가중치"] = mapped["W"]
    return mapped


@st.cache_data(show_spinner=False)
def make_demo_data(rows: int = 1200) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    demo = pd.DataFrame({
        "smartphone_dependence": rng.choice(["No", "Risk"], rows, p=[0.77, 0.23]),
        "oral_health": rng.choice(["No", "Yes"], rows, p=[0.50, 0.50]),
        "sleep_quality": rng.choice(["No", "Yes"], rows, p=[0.42, 0.58]),
        "smartphone_use_day": rng.choice(["≤3", "3 ~ 5", "5 ~ 8", "≥8"], rows),
        "smartphone_use_weekend": rng.choice(["≤3", "3 ~ 5", "5 ~ 8", "≥8"], rows),
        "W": np.ones(rows),
    })
    return load_and_map_data(io.BytesIO(demo.to_csv(index=False).encode("utf-8")))
