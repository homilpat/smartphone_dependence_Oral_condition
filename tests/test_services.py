import unittest

from data_service import make_demo_data
from model_service import encode_answers, load_ml_assets, risk_label


class ServiceTest(unittest.TestCase):
    def test_demo_data_has_no_missing_values(self):
        data = make_demo_data()
        self.assertEqual(len(data), 1200)
        self.assertEqual(int(data.isna().sum().sum()), 0)

    def test_model_assets_predict_valid_score(self):
        model, scaler, metadata = load_ml_assets()
        self.assertIsNotNone(model)
        values = encode_answers(
            "남학생", "고등학교", "중", "중", "보통", "중간", "아니오", "아니오",
            "3~5시간", "5~8시간", "일반군", "충분",
        )
        score = float(model.predict_proba(scaler.transform(values))[0, 1])
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        self.assertIn(risk_label(score, metadata["screening_threshold"]), {"낮음", "주의"})


if __name__ == "__main__":
    unittest.main()
