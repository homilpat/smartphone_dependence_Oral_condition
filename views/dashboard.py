import pandas as pd
import plotly.express as px
import streamlit as st

from config import TIME_OPTIONS
from data_service import weighted_distribution, weighted_rate


def _kpi(label: str, value: str, note: str) -> None:
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-sub">{note}</div></div>',
        unsafe_allow_html=True,
    )


def _time_chart(df: pd.DataFrame, column: str, title: str):
    grouped = df.groupby([column, "구강 증상"])["가중치"].sum().reset_index()
    grouped["비율(%)"] = grouped["가중치"] / grouped.groupby(column)["가중치"].transform("sum") * 100
    grouped[column] = pd.Categorical(grouped[column], categories=TIME_OPTIONS, ordered=True)
    figure = px.bar(
        grouped.sort_values(column), x=column, y="비율(%)", color="구강 증상", title=title,
        color_discrete_map={"없음": "#133F52", "있음": "#27770F"},
    )
    figure.update_layout(barmode="stack", height=380, xaxis_title="", yaxis_title="비율 (%)")
    return figure


def dashboard_tab(df: pd.DataFrame) -> None:
    st.markdown('<div class="section-title">통계 예측지도</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">합성 데모 데이터로 화면 구성을 보여줍니다. 실제 연구 통계가 아닙니다.</div>',
        unsafe_allow_html=True,
    )
    columns = st.columns(4)
    values = [
        ("스마트폰 의존 위험군", weighted_rate(df["스마트폰 의존"], df["가중치"], "위험군") * 100),
        ("수면 부족군", weighted_rate(df["수면 상태"], df["가중치"], "부족") * 100),
        ("구강 증상 경험", weighted_rate(df["구강 증상"], df["가중치"], "있음") * 100),
    ]
    for column, (label, value) in zip(columns[:3], values):
        with column:
            _kpi(label, f"{value:.1f}%", "합성 데모")
    with columns[3]:
        _kpi("선정 모델", "XGBoost", "위험군 선별 보조")

    left, right = st.columns(2)
    with left:
        st.plotly_chart(_time_chart(df, "주중 스마트폰 사용", "주중 사용시간과 구강 증상"), width="stretch")
    with right:
        st.plotly_chart(_time_chart(df, "주말 스마트폰 사용", "주말 사용시간과 구강 증상"), width="stretch")

    left, right = st.columns(2)
    with left:
        distribution = weighted_distribution(df, "스마트폰 의존")
        figure = px.pie(
            distribution, names="스마트폰 의존", values="비율", hole=0.45,
            color="스마트폰 의존", color_discrete_map={"일반군": "#64B5F6", "위험군": "#E57373"},
        )
        st.plotly_chart(figure, width="stretch")
    with right:
        combined = []
        for dependence in ("일반군", "위험군"):
            for sleep in ("충분", "부족"):
                subset = df[(df["스마트폰 의존"] == dependence) & (df["수면 상태"] == sleep)]
                combined.append({
                    "의존도": dependence,
                    "수면": sleep,
                    "구강증상 경험률(%)": weighted_rate(subset["구강 증상"], subset["가중치"], "있음") * 100,
                })
        figure = px.bar(
            pd.DataFrame(combined), x="의존도", y="구강증상 경험률(%)", color="수면", barmode="group",
            color_discrete_map={"충분": "#81C784", "부족": "#F06292"},
        )
        st.plotly_chart(figure, width="stretch")
