import pandas as pd
import streamlit as st

from config import APP_SUBTITLE, APP_TITLE
from data_service import weighted_rate

CUSTOM_CSS = """
<style>
    #MainMenu, footer, header {visibility:hidden;}
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {display:none!important;}
    .block-container {padding-top:.8rem;padding-bottom:2.5rem;max-width:1480px;}
    .stTabs [data-baseweb="tab-list"] {gap:.85rem;width:100%;margin:.7rem 0 1.15rem;}
    .stTabs [data-baseweb="tab"] {flex:1 1 0;min-height:82px;font-size:1.2rem;font-weight:800;
        border-radius:20px;border:1px solid #ddd6c8;background:#f7f2e8;color:#403830;}
    .stTabs [aria-selected="true"] {background:#efe3d2!important;color:#9b5450!important;}
    .hero-wrap {background:linear-gradient(135deg,#fbf7ef,#efe2d1);border:1px solid #ddd2bf;
        border-radius:32px;padding:34px 40px;box-shadow:0 18px 36px rgba(52,33,14,.07);margin-bottom:1rem;}
    .hero-grid {display:grid;grid-template-columns:1.5fr 1fr;gap:1.35rem;align-items:stretch;}
    .hero-title {font-size:3.2rem;line-height:1.05;font-weight:900;color:#b55a5b;margin:0 0 .7rem;}
    .hero-subtitle {font-size:1.1rem;line-height:1.7;color:#4a4039;}
    .hero-panel {background:rgba(255,255,255,.72);border:1px solid #e8ddcd;border-radius:24px;padding:1.1rem;}
    .mini-stat-grid {display:grid;grid-template-columns:1fr 1fr;gap:.8rem;}
    .mini-stat {border-radius:18px;background:#fffdf8;border:1px solid #ede2d3;padding:1rem;}
    .mini-stat-value {font-size:1.4rem;font-weight:900;color:#312a26;}
    .section-title {margin:.1rem 0 .8rem;font-size:1.42rem;font-weight:900;color:#2d2724;}
    .section-desc {color:#72665d;margin:-.2rem 0 1rem;line-height:1.7;}
    .card {border-radius:22px;border:1px solid #e8dfd2;background:#fffdf9;padding:1.2rem;height:100%;}
    .kpi-card {border-radius:20px;border:1px solid #eee4d6;background:#faf5ed;padding:1rem;}
    .kpi-label,.kpi-sub,.muted {color:#7a685d;line-height:1.65;}
    .kpi-value {color:#302925;font-size:1.7rem;font-weight:900;}
    .guide-card,.info-card {background:#fffdfa;border:1px solid #efe4d6;border-radius:16px;
        padding:1rem;margin-bottom:.7rem;line-height:1.65;}
    .risk-box {border-radius:24px;padding:1.25rem;border:1px solid #ebe1d2;background:#fffdf9;}
</style>
"""


def render_header(df: pd.DataFrame, demo_mode: bool) -> None:
    oral = weighted_rate(df["구강 증상"], df["가중치"], "있음") * 100
    dependence = weighted_rate(df["스마트폰 의존"], df["가중치"], "위험군") * 100
    data_label = "합성 데모" if demo_mode else "로컬 분석 데이터"
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        f"""<div class="hero-wrap"><div class="hero-grid"><div>
        <h1 class="hero-title">{APP_TITLE}</h1><p class="hero-subtitle">{APP_SUBTITLE}</p>
        <p class="muted">의료 진단이 아닌 구강 증상 위험군 선별 보조 서비스입니다.</p></div>
        <div class="hero-panel"><b>대시보드 표시 자료: {data_label}</b><div class="mini-stat-grid">
        <div class="mini-stat">스마트폰 의존<div class="mini-stat-value">{dependence:.1f}%</div></div>
        <div class="mini-stat">구강 증상<div class="mini-stat-value">{oral:.1f}%</div></div>
        <div class="mini-stat">표시 행 수<div class="mini-stat-value">{len(df):,}</div></div>
        </div></div></div></div>""",
        unsafe_allow_html=True,
    )
