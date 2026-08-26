import streamlit as st


def smartphone_tab() -> None:
    st.markdown('<div class="section-title">스마트폰 과의존 이해하기</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">스마트폰 과의존의 정의와 S-Scale 분류 기준을 확인해 보세요.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="card"><h4>스마트폰 과의존이란?</h4>
        <p class="muted">스마트폰 이용 조절력이 감소하고 일상생활에서 문제적 결과를 경험하는 상태입니다.</p>
        <div class="guide-card"><b>조절 실패</b><br>이용시간을 계획대로 조절하기 어렵습니다.</div>
        <div class="guide-card"><b>현저성</b><br>스마트폰 이용이 일상에서 가장 중요한 활동이 됩니다.</div>
        <div class="guide-card"><b>문제적 결과</b><br>건강, 학업 또는 관계에 부정적인 결과가 생깁니다.</div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="card"><h4>청소년 S-Scale 분류 기준</h4>
        <div class="info-card"><b>고위험군: 31점 이상</b><br>전문 상담기관과 상의해 보세요.</div>
        <div class="info-card"><b>잠재적 위험군: 23~30점</b><br>사용 시간을 점검하고 조절 계획을 세워보세요.</div>
        <div class="info-card"><b>일반군: 22점 이하</b><br>현재의 건강한 사용 습관을 유지하세요.</div></div>""",
        unsafe_allow_html=True,
    )
    st.info("'구강 예측하기' 탭에서 위험군 선별 검사를 진행할 수 있습니다.")


def guide_tab() -> None:
    st.markdown('<div class="section-title">관리 가이드</div>', unsafe_allow_html=True)
    lifestyle, oral = st.tabs(["생활습관 관리", "구강 관리"])
    with lifestyle:
        st.markdown(
            """<div class="card"><div class="guide-card"><b>스마트폰</b><br>취침 전 30분은 화면 노출을 줄이세요.</div>
            <div class="guide-card"><b>수면</b><br>기상과 취침 시간을 일정하게 유지하세요.</div>
            <div class="guide-card"><b>식습관</b><br>당류·탄산 섭취 후에는 물을 마시세요.</div></div>""",
            unsafe_allow_html=True,
        )
    with oral:
        st.markdown(
            """<div class="card"><div class="guide-card"><b>기본 관리</b><br>하루 2회 이상 양치하고 치실을 사용하세요.</div>
            <div class="guide-card"><b>증상 관찰</b><br>통증이나 출혈이 반복되면 기록해 두세요.</div>
            <div class="guide-card"><b>진료 안내</b><br>증상이 지속되면 치과 또는 의료진과 상담하세요.</div></div>""",
            unsafe_allow_html=True,
        )


def program_tab() -> None:
    st.markdown('<div class="section-title">예방 프로그램 안내</div>', unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        st.markdown(
            '<div class="card"><h4>가족·보호자 교육</h4><p class="muted">가족이 함께 스마트폰 사용 규칙과 구강 관리 습관을 정해보세요.</p></div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            '<div class="card"><h4>학교 예방교육</h4><p class="muted">학교와 지역 상담기관의 예방교육 프로그램을 확인해 보세요.</p></div>',
            unsafe_allow_html=True,
        )
