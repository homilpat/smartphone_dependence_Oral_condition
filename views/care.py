from urllib.parse import quote_plus

import streamlit as st


CARE_TYPES = {
    1: (
        "🔴 집중 케어 솔루션", "#b42318",
        "스마트폰 사용과 구강 증상 모두 적극적인 관리가 필요합니다.",
        ["취침 1시간 전 스마트폰을 다른 곳에 두세요.", "식후 양치와 치실 사용을 지켜보세요.", "불편감이 지속되면 치과에 방문하세요."],
    ),
    2: (
        "🟡 구강 집중 솔루션", "#b26a00",
        "스마트폰 사용과 별개로 구강 관리 요인을 점검할 필요가 있습니다.",
        ["치실이나 치간칫솔을 사용하세요.", "당류와 탄산음료 섭취를 줄이세요.", "증상이 반복되면 구강 검진을 받으세요."],
    ),
    3: (
        "🔵 스마트폰 사용 관리", "#005a9e",
        "현재 구강 선별 결과는 낮지만 스마트폰 사용 습관을 관리해야 합니다.",
        ["앱 타이머로 사용 시간을 줄이세요.", "취침 전 스마트폰을 멀리 두세요.", "현재의 구강 관리 습관은 유지하세요."],
    ),
    4: (
        "🟢 건강 유지 솔루션", "#067647",
        "현재 생활습관과 구강 관리 상태를 꾸준히 유지하세요.",
        ["규칙적인 생활과 수면을 유지하세요.", "하루 2회 이상 양치하세요.", "예방 목적의 정기 검진을 고려하세요."],
    ),
}


def medical_tab(key_suffix: str = "main") -> None:
    st.markdown('<div class="section-title">의료기관 연계</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">증상이 지속되면 주변 치과를 확인하고 직접 연락해 진료를 예약하세요.</div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.06, 0.94], gap="large")
    with left:
        with st.container(border=True):
            st.markdown("#### 주변 치과 찾기")
            location = st.text_input("지역 또는 주소", placeholder="예: 서울 성동구", key=f"loc_{key_suffix}")
            category = st.selectbox(
                "검색 유형", ["치과", "청소년 치과", "예방 진료 치과", "야간 진료 치과"],
                key=f"kw_{key_suffix}",
            )
            query = quote_plus(f"{location} {category}".strip())
            st.link_button(
                "지도에서 주변 치과 검색", f"https://www.google.com/maps/search/?api=1&query={query}",
                width="stretch",
            )
    with right:
        st.markdown(
            """<div class="card"><h4>진료 연결 안내</h4>
            <div class="guide-card">통증, 출혈, 씹기 불편이 반복되면 치과 상담을 우선 고려하세요.</div>
            <div class="guide-card">증상 발생 시점과 불편한 부위를 정리하면 상담에 도움이 됩니다.</div>
            <div class="guide-card">이 앱은 예약을 저장하거나 의료기관으로 전송하지 않습니다.</div></div>""",
            unsafe_allow_html=True,
        )


def _care_type() -> int:
    smartphone = st.session_state.get("diag_sp_group")
    oral = st.session_state.get("diag_oral_risk")
    if not smartphone or not oral:
        return 0
    smartphone_risk, oral_risk = smartphone == "위험군", oral == "주의"
    if smartphone_risk and oral_risk:
        return 1
    if oral_risk:
        return 2
    if smartphone_risk:
        return 3
    return 4


def solution_tab() -> None:
    st.markdown('<div class="section-title">개인 맞춤형 솔루션</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">선별 결과에 맞는 생활습관과 구강 관리 가이드를 제안합니다.</div>',
        unsafe_allow_html=True,
    )
    care_type = _care_type()
    if not care_type:
        st.info("먼저 '구강 예측하기' 탭에서 선별 검사를 진행해 주세요.")
        return
    title, color, description, actions = CARE_TYPES[care_type]
    action_html = "".join(
        f'<div class="guide-card" style="flex:1;margin-bottom:0;"><b>{index}.</b> {action}</div>'
        for index, action in enumerate(actions, 1)
    )
    st.markdown(
        f'<div class="card" style="border:3px solid {color};"><h4 style="color:{color};">{title}</h4>'
        f'<p class="muted">{description}</p><div style="display:flex;gap:1rem;">{action_html}</div></div>',
        unsafe_allow_html=True,
    )
    if care_type in (1, 2):
        st.divider()
        medical_tab("solution_view")
