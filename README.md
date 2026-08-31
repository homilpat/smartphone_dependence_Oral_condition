[시연영상](https://youtu.be/bkxu6rmWbFw)
# Cheer Up Clinic

청소년의 생활·정신건강·스마트폰 사용 정보를 바탕으로 구강 증상 위험군 선별을 돕는 Streamlit 포트폴리오입니다. 의료 진단이나 질병 발생 확률을 제공하지 않습니다.

## 주요 기능

- 12개 설문 변수를 이용한 구강 증상 위험군 선별 보조 점수
- Validation에서 정한 단일 임계값에 따른 `낮음`·`주의` 안내
- 스마트폰 S-Scale 분류와 생활·구강 관리 안내
- 개인정보 없는 합성 데이터 기반 대시보드

## 데이터와 모델

- 원자료: 제16차 청소년건강행태조사(KYRBS 2020) 54,948명
- 분석 표본: 스마트폰 이용시간 결측 제거 후 52,627명
- 모델: 사전 지정 XGBoost
- 분할: Train 60% / Validation 20% / Test 20%
- 임계값: Validation 가중 Recall 0.85 이상을 만족하는 가장 높은 값

| 평가 데이터 | AUC | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| Validation | 0.6406 | 0.5734 | 0.5493 | 0.8503 | 0.6674 |
| Test | 0.6446 | 0.5727 | 0.5481 | 0.8548 | 0.6679 |

선별 임계값은 `0.385317`입니다. 외부 검증이 없고 Test AUC가 약 0.645이므로 개인의 질병 여부를 판정하는 용도로 사용할 수 없습니다. 실제 실행 결과와 환경은 `models/model_meta.json`에 기록했습니다.

## 실행

```bash
python -m pip install -r requirements-runtime.txt
streamlit run app.py
```

자동 검증은 다음 명령으로 실행합니다.

```bash
python -m unittest discover -s tests
```

공개 저장소에는 실행 가능한 비식별 모델 자산이 포함됩니다. 행 단위 조사 데이터는 포함하지 않으며, 데이터가 없을 때 앱은 고정 시드 합성 데모 데이터를 사용합니다.

학습을 재현하려면 이용 조건에 따라 KYRBS 2020 SAS 파일을 `data/raw/kyrbs2020.sas7bdat`에 직접 준비한 뒤 실행합니다.

```bash
python preprocess_data.py
python train.py
```

## 운영 파일

| 파일 | 설명 |
|---|---|
| `app.py` | Streamlit 페이지 조립과 실행 진입점 |
| `config.py` | 경로, 서비스 문구, 설문 선택지 설정 |
| `data_service.py` | 로컬·합성 데이터 로드와 가중 통계 |
| `model_service.py` | 모델 자산 로드, 입력 인코딩, 선별 단계 계산 |
| `views/prediction.py` | 설문 입력과 위험군 선별 결과 화면 |
| `views/care.py` | 맞춤 관리 및 주변 치과 검색 화면 |
| `views/dashboard.py` | 합성 데모 통계 시각화 화면 |
| `views/information.py` | S-Scale·관리 가이드·예방 프로그램 화면 |
| `views/layout.py` | 공통 스타일과 상단 요약 화면 |
| `tests/test_app.py` | 전체 화면 렌더링과 설문 제출 회귀 검사 |
| `tests/test_services.py` | 합성 데이터와 모델 예측 핵심 검사 |
| `models/xgboost_model.pkl` | 학습 행을 포함하지 않는 XGBoost 배포 모델 |
| `models/scaler.pkl` | Train의 집계 평균·표준편차를 담은 표준화 객체 |
| `models/model_meta.json` | 변수, 임계값, Validation·Test 성능, 실행환경 |
| `preprocess_data.py` | 원본 SAS를 비식별 분석 테이블로 변환 |
| `train.py` | 데이터 분할, 학습, 임계값 설정, 최종 평가 |
| `requirements-runtime.txt` | 앱 실행용 고정 의존성 |
| `requirements-analysis.txt` | 재학습·분석용 고정 의존성 |
| `DEVELOPMENT_ROADMAP.md` | 실제 변경·검증 결과와 다음 과제 |
| `SECURITY.md` | 공개 저장소의 민감정보 제외 원칙 |
| `analysis_archive/` | 운영 경로에서 제외한 과거 분석 코드 |

## 공개 범위

원본 SAS, 행 단위 파생 CSV, 논문·조사 지침 PDF, 비밀키, 개인 연락처와 사용자 절대경로는 Git에서 제외합니다. 자세한 원칙은 `SECURITY.md`를 참고하세요.
