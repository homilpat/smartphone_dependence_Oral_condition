"""Cheer Up Clinic Streamlit entry point."""

import streamlit as st

from data_service import load_and_map_data, make_demo_data
from model_service import load_ml_assets
from views.care import solution_tab
from views.dashboard import dashboard_tab
from views.information import guide_tab, program_tab, smartphone_tab
from views.layout import render_header
from views.prediction import prediction_tab


st.set_page_config(
    page_title="Cheer up(치아 업) Clinic",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main() -> None:
    demo_mode = False
    try:
        dashboard_data = load_and_map_data()
    except FileNotFoundError:
        dashboard_data = make_demo_data()
        demo_mode = True
        st.info("공개 포트폴리오 버전입니다. 통계 화면은 개인정보 없는 합성 데이터입니다.")

    model, scaler, metadata = load_ml_assets()
    render_header(dashboard_data, demo_mode)
    tabs = st.tabs(["📱 스마트폰 과의존", "🎯 구강 예측하기", "💡 맞춤형 솔루션", "🏫 자료실"])

    with tabs[0]:
        smartphone_tab()
    with tabs[1]:
        prediction_tab(model, scaler, metadata)
    with tabs[2]:
        solution_tab()
    with tabs[3]:
        resource_tabs = st.tabs(["📊 통계 예측지도", "📘 관리 가이드", "프로그램 안내"])
        with resource_tabs[0]:
            dashboard_tab(dashboard_data)
        with resource_tabs[1]:
            guide_tab()
        with resource_tabs[2]:
            program_tab()


if __name__ == "__main__":
    main()
