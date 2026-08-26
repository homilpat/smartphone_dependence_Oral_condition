import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class AppSmokeTest(unittest.TestCase):
    def test_app_renders_and_prediction_submits(self):
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(app_path, default_timeout=30).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.tabs), 9)

        app.button[0].click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.success), 1)
        self.assertIn(app.session_state["diag_sp_group"], {"일반군", "위험군"})
        self.assertIn(app.session_state["diag_oral_risk"], {"낮음", "주의"})


if __name__ == "__main__":
    unittest.main()
