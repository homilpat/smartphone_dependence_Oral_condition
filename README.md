[시연영상](https://youtu.be/bkxu6rmWbFw)
# Cheer Up Clinic

청소년의 인구학·수면·스마트폰 사용 정보를 바탕으로 구강 증상 위험군 선별을 돕는 Streamlit 포트폴리오입니다. 의료 진단이나 질병 발생 확률을 제공하지 않습니다.

## 프로젝트 개요

| 구분 | 내용 |
|---|---|
| 진행 기간 | 2026.03.03 ~ 2026.04.01 (종료 후 2026.08~09 재검증) |
| 진행 인원 | 6인 (폰잠치아라팀 · AA 2 / DA 2 / TA 2) |
| 담당 역할 | DA — 데이터 수집·전처리, 변수 재구성, 가중 기술통계·Rao–Scott 교차분석. 종료 후 복합표본 위계적 로지스틱 회귀·설계보정 VIF 재현과 학습 코드 재검증 (예측 모델링·Streamlit 구현은 TA 담당) |

## 주요 기능

- 앱에서 입력받는 8개 설문 변수를 이용한 구강 증상 위험군 선별 보조 점수
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
| Validation | 0.6133 | 0.5534 | 0.5356 | 0.8500 | 0.6571 |
| Test | 0.6224 | 0.5562 | 0.5365 | 0.8599 | 0.6607 |

선별 임계값은 `0.399846`입니다. 기존 모델은 앱이 묻지 않는 정신건강 4개 변수를 포함해 앱에서 최저 기본값으로 채워지던 불일치가 있었습니다. 이를 해소하기 위해 앱이 실제 수집하는 8개 입력으로 재학습했습니다. 외부 검증이 없고 Test AUC가 약 0.622이므로 개인의 질병 여부를 판정하는 용도로 사용할 수 없습니다. 실제 실행 결과와 환경은 `models/model_meta.json`에 기록했습니다.

프로젝트 당시에는 5개 모델(LR·RF·XGBoost·LightGBM·CatBoost)을 튜닝한 뒤 Test 성능을 비교해 최종 모델을 골랐습니다(Test AUC 0.649). Test를 모델 선택에 쓰면 성능이 낙관적으로 추정될 수 있어, 종료 후 XGBoost를 사전 지정하고 하이퍼파라미터와 임계값은 Validation에서만 정한 뒤 Test는 마지막에 한 번만 평가하도록 다시 구성했습니다. 재학습 모델의 Train–Test AUC 차이는 0.023입니다.

## 가중 연관성 분석

선별 모델과 별도로, 복합표본 설계(`W`·`STRATA`·`CLUSTER`)를 반영해 요인과 구강 증상 경험의 연관성을 분석했습니다. 분석 표본 52,627명, 가중 모집단 2,521,215명입니다.

| 요인 | 비교 집단 | 구강 증상 경험률 (가중) | Rao–Scott 보정 F | p |
|---|---|---|---:|---|
| 스마트폰 과의존 | 위험군 vs 일반군 | 64.7% vs 45.3% | 1235.554 | < 0.001 |
| 수면의 질 | 부족 vs 충분 | 53.9% vs 42.1% | 533.269 | < 0.001 |
| 주말 사용시간 | 8시간 이상 vs 3시간 이하 | 55.6% vs 44.9% | 87.336 | < 0.001 |
| 주중 사용시간 | 8시간 이상 vs 3시간 이하 | 56.1% vs 46.7% | 67.506 | < 0.001 |

통제변수 → 스마트폰 변수 → 수면의 질 순으로 투입한 Taylor 선형화 위계적 로지스틱 회귀의 최종 모형에서 스마트폰 과의존 위험군은 OR 1.79 (95% CI 1.70–1.88), 수면 문제는 OR 1.25 (95% CI 1.20–1.31)였고 설계보정 VIF 최댓값은 2.465였습니다. 이 통계분석 재현 코드와 전체 결과는 원자료 이용 조건 때문에 저장소 밖 로컬 환경에 보관하며, 요약 기록은 `DEVELOPMENT_ROADMAP.md`에 있습니다.

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
| `models/model_meta.json` | 변수, 임계값, Train·Validation·Test 성능, 실행환경 |
| `preprocess_data.py` | 원본 SAS를 비식별 분석 테이블로 변환 |
| `train.py` | 데이터 분할, 학습, 임계값 설정, 최종 평가 |
| `requirements-runtime.txt` | 앱 실행용 고정 의존성 |
| `requirements-analysis.txt` | 재학습·분석용 고정 의존성 |
| `DEVELOPMENT_ROADMAP.md` | 실제 변경·검증 결과와 다음 과제 |
| `SECURITY.md` | 공개 저장소의 민감정보 제외 원칙 |
| `analysis_archive/` | 운영 경로에서 제외한 과거 분석 코드 |

## 공개 범위

원본 SAS, 행 단위 파생 CSV, 논문·조사 지침 PDF, 비밀키, 개인 연락처와 사용자 절대경로는 Git에서 제외합니다. 자세한 원칙은 `SECURITY.md`를 참고하세요.
