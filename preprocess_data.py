"""Build the de-identified KYRBS 2020 modeling table."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
RAW_PATH = ROOT / "data" / "raw" / "kyrbs2020.sas7bdat"
OUTPUT_PATH = ROOT / "data" / "processed" / "kyrbs2020_clean_v1.csv"
SMARTPHONE_ITEMS = [f"INT_SP_OU_{i}" for i in range(1, 11)]
ANXIETY_ITEMS = [f"M_GAD_{i}" for i in range(1, 8)]
RAW_COLUMNS = [
    "SEX", "GRADE", "E_S_RCRD", "E_SES", "INT_SPWD_TM", "INT_SPWK_TM",
    *SMARTPHONE_ITEMS, *ANXIETY_ITEMS, "M_STR", "M_SAD", "M_SUI_CON",
    "O_SYMP1", "O_SYMP2", "O_SYMP3", "O_SYMP4", "M_SLP_EN", "W",
]
FINAL_COLUMNS = [
    "gender", "school", "grade", "income", "smartphone_use_day",
    "smartphone_use_weekend", "smartphone_dependence", "anxiety", "stress",
    "despair", "suicidal_thoughts", "oral_health", "sleep_quality", "W",
]


def categorize_time(minutes: float) -> str | float:
    if pd.isna(minutes):
        return np.nan
    hours = minutes / 60
    if hours <= 3:
        return "≤3"
    if hours <= 5:
        return "3 ~ 5"
    if hours <= 8:
        return "5 ~ 8"
    return "≥8"


def categorize_anxiety(score: float) -> str | float:
    if pd.isna(score):
        return np.nan
    if score <= 4:
        return "No"
    if score <= 9:
        return "Mild"
    if score <= 14:
        return "Moderate"
    return "Severe"


def build_table(raw_path: Path = RAW_PATH) -> pd.DataFrame:
    raw = pd.read_sas(raw_path, format="sas7bdat")
    missing = sorted(set(RAW_COLUMNS) - set(raw.columns))
    if missing:
        raise KeyError(f"KYRBS columns are missing: {missing}")
    df = raw[RAW_COLUMNS].copy()
    out = pd.DataFrame(index=df.index)
    out["gender"] = df["SEX"].map({1: "Male", 2: "Female"})
    out["school"] = df["GRADE"].map(
        {1: "Middle school", 2: "Middle school", 3: "Middle school",
         4: "High school", 5: "High school", 6: "High school"}
    )
    ordered_level = {1: "High", 2: "High", 3: "Middle", 4: "Low", 5: "Low"}
    out["grade"] = df["E_S_RCRD"].map(ordered_level)
    out["income"] = df["E_SES"].map(ordered_level)
    out["smartphone_use_day"] = df["INT_SPWD_TM"].map(categorize_time)
    out["smartphone_use_weekend"] = df["INT_SPWK_TM"].map(categorize_time)

    smartphone_score = df[SMARTPHONE_ITEMS].sum(axis=1, min_count=len(SMARTPHONE_ITEMS))
    out["smartphone_dependence"] = smartphone_score.map(
        lambda value: np.nan if pd.isna(value) else ("No" if value < 23 else "Risk")
    )
    anxiety_score = (df[ANXIETY_ITEMS] - 1).sum(axis=1, min_count=len(ANXIETY_ITEMS))
    out["anxiety"] = anxiety_score.map(categorize_anxiety)
    out["stress"] = df["M_STR"].map(ordered_level)
    out["despair"] = df["M_SAD"].map({1: "No", 2: "Yes"})
    out["suicidal_thoughts"] = df["M_SUI_CON"].map({1: "No", 2: "Yes"})
    oral_count = df[["O_SYMP1", "O_SYMP2", "O_SYMP3", "O_SYMP4"]].sum(axis=1)
    out["oral_health"] = oral_count.map(lambda value: "No" if value == 0 else "Yes")
    out["sleep_quality"] = df["M_SLP_EN"].map(
        {1: "No", 2: "No", 3: "Yes", 4: "Yes", 5: "Yes"}
    )
    out["W"] = df["W"]
    return out[FINAL_COLUMNS].dropna().reset_index(drop=True)


def main() -> None:
    clean = build_table()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"saved={OUTPUT_PATH.relative_to(ROOT)} rows={len(clean)} columns={len(clean.columns)}")
    print(clean["oral_health"].value_counts().to_string())


if __name__ == "__main__":
    main()
