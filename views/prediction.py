import streamlit as st

from config import SMARTPHONE_QUESTIONS, TIME_OPTIONS
from model_service import encode_answers, risk_colors, risk_label


def _basic_inputs():
    columns = st.columns(4)
    with columns[0]:
        gender = st.selectbox("성별", ["여학생", "남학생"])
    with columns[1]:
        school = st.selectbox("학교급", ["중학교", "고등학교"])
    with columns[2]:
        grade = st.selectbox("학업성적", ["상", "중", "하"])
    with columns[3]:
        income = st.selectbox("경제수준", ["상", "중", "하"])
    return gender, school, grade, income


def _smartphone_inputs() -> list[int]:
    st.markdown("#### 📱 스마트폰 과의존 척도 (S-Scale)")
    st.info("각 문항에 해당되는 정도를 선택해 주세요. 1점은 전혀 그렇지 않다, 4점은 매우 그렇다입니다.")
    scores, columns = [], st.columns(2)
    for index, question in enumerate(SMARTPHONE_QUESTIONS):
        with columns[index % 2]:
            scores.append(st.radio(
                f"{index + 1}. {question}", [1, 2, 3, 4], horizontal=True, key=f"q_{index}"
            ))
    return scores


def prediction_tab(model, scaler, metadata) -> None:
    st.markdown('<div class="section-title">구강 증상 위험군 선별</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">설문으로 위험군 선별 보조 점수를 계산합니다. 의료 진단은 아닙니다.</div>',
        unsafe_allow_html=True,
    )
    if model is None:
        st.error("모델 파일을 찾을 수 없습니다. 모델 학습 스크립트를 먼저 실행해 주세요.")
        return

    with st.form("comprehensive_screening"):
        st.markdown("#### 👤 기본 정보")
        gender, school, grade, income = _basic_inputs()
        st.divider()
        scores = _smartphone_inputs()
        st.divider()
        sleep_value = st.radio(
            "최근 7일의 수면이 피로회복에 충분했습니까?",
            [1, 2, 3, 4, 5],
            format_func=lambda value: {
                1: "매우 충분하다", 2: "충분하다", 3: "그저 그렇다",
                4: "충분하지 않다", 5: "전혀 충분하지 않다",
            }[value],
            horizontal=True,
        )
        columns = st.columns(2)
        with columns[0]:
            weekday = st.selectbox("주중 스마트폰 사용 시간", TIME_OPTIONS)
        with columns[1]:
            weekend = st.selectbox("주말 스마트폰 사용 시간", TIME_OPTIONS)
        submitted = st.form_submit_button("선별 결과 확인하기", type="primary", width="stretch")

    if not submitted:
        return
    total = sum(scores)
    smartphone_group = "위험군" if total >= 23 else "일반군"
    sleep_group = "부족" if sleep_value >= 3 else "충분"
    raw = encode_answers(
        gender, school, grade, income, weekday, weekend, smartphone_group, sleep_group,
    )
    score = float(model.predict_proba(scaler.transform(raw))[0, 1])
    threshold = metadata["screening_threshold"]
    risk = risk_label(score, threshold)
    st.session_state.update(diag_sp_group=smartphone_group, diag_oral_risk=risk)
    text_color, background, border = risk_colors(score, threshold)

    left, right = st.columns(2)
    with left:
        st.metric("스마트폰 의존 점수", f"{total}점", delta=smartphone_group, delta_color="inverse")
    with right:
        st.markdown(
            f'<div class="risk-box" style="text-align:center;background:{background};border:2px solid {border};">'
            f'<b style="color:{text_color};">구강 증상 위험군: {risk}</b><br>'
            f'<span style="color:{text_color};">위험군 선별 보조 점수: {score * 100:.1f}점</span></div>',
            unsafe_allow_html=True,
        )
    st.success("선별이 완료되었습니다. 증상이 지속되면 점수와 관계없이 치과 또는 의료진과 상담하세요.")
