"""Test state classifier"""
import time, unittest, sys, os
from unittest.mock import patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from tical_code.vigil.state_classifier import StateClassifier, ClassifierConfig
from tical_code.vigil.signal_collector import CombinedSignal, InteractionSignal, PhysioSignal

def _sig(seconds_ago=5, avg=10, var=2, work_hours=1, err=0.0, trend="stable", switches=0, hrv=60, hr=70, spo2=98, eda=3, physio=True):
    ia = InteractionSignal(last_input_time=time.time()-seconds_ago, input_interval_avg=avg, input_interval_variance=var,
        session_duration=work_hours*60, consecutive_work_hours=work_hours, input_error_rate=err,
        response_length_trend=trend, task_switch_frequency=switches)
    ph = PhysioSignal(heart_rate=hr, hrv=hrv, spo2=spo2, eda=eda, source="test") if physio else None
    return CombinedSignal(interaction=ia, physio=ph)

class TestFocus(unittest.TestCase):
    def test_steady_is_focus(self):
        r = StateClassifier().classify(_sig(var=5, err=0.02, switches=0), [])
        self.assertEqual(r.state, "FOCUS")
    def test_focus_too_long_fatigue(self):
        cfg = ClassifierConfig(focus_max_hours=2)
        r = StateClassifier(cfg).classify(_sig(work_hours=2.5, var=5, err=0.02, switches=0), [])
        self.assertEqual(r.state, "FATIGUE")

class TestInspiration(unittest.TestCase):
    def test_bursty_inspiration(self):
        r = StateClassifier().classify(_sig(seconds_ago=120, var=200, trend="increasing", switches=0), [])
        self.assertEqual(r.state, "INSPIRATION")

class TestRest(unittest.TestCase):
    @patch("tical_code.vigil.state_classifier.StateClassifier._looks_like_rest_time", return_value=True)
    def test_rest_hours(self, _):
        r = StateClassifier().classify(_sig(seconds_ago=1500, var=1), [])
        self.assertEqual(r.state, "REST")

if __name__ == "__main__":
    unittest.main()
