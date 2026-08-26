from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "processed" / "kyrbs2020_clean_v1.csv"
MODELS_DIR = ROOT / "models"

APP_TITLE = "Cheer up(치아 업)Clinic"
APP_SUBTITLE = "청소년 생활습관 기반 구강 증상 위험군 선별과 개인 맞춤형 관리 안내"
TIME_OPTIONS = ["3시간 이하", "3~5시간", "5~8시간", "8시간 이상"]

SMARTPHONE_QUESTIONS = [
    "스마트폰 이용시간을 조절하는 것이 어렵다.",
    "스마트폰 이용시간을 줄이려고 시도해보았지만 실패한다.",
    "스마트폰 이용시간을 조절하는 것이 내 마음대로 안 된다.",
    "스마트폰 이용시간이 점점 늘어난다.",
    "스마트폰이 옆에 없으면 안절부절못하고 초조해진다.",
    "스마트폰이 생각나서 다른 일에 집중하기 힘들다.",
    "스마트폰이 없으면 일상생활이 힘들 것 같다는 생각이 든다.",
    "스마트폰 이용 때문에 건강에 문제가 생긴 적이 있다.",
    "스마트폰 이용 때문에 가족(친구)과 다툰 적이 있다.",
    "스마트폰 이용 때문에 해야 할 일(공부 등)에 지장을 받는다.",
]
