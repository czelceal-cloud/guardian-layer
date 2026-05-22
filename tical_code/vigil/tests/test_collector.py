"""Test SignalCollector"""
import time, unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from tical_code.vigil.signal_collector import SignalCollector

class TestSignalCollector(unittest.TestCase):
    def test_empty_returns_signal(self):
        c = SignalCollector()
        self.assertIsNotNone(c.get_interaction_signal())
    def test_records_input(self):
        c = SignalCollector(); before = time.time()
        c.record_input()
        self.assertGreaterEqual(c.get_interaction_signal().last_input_time, before)
    def test_error_rate(self):
        c = SignalCollector()
        for _ in range(8): c.record_input(had_error=False)
        for _ in range(2): c.record_input(had_error=True)
        self.assertAlmostEqual(c.get_interaction_signal().input_error_rate, 0.2, delta=0.05)
    def test_trend_increasing(self):
        c = SignalCollector()
        for l in [10,12,11,13,15]: c.record_response(l)
        for l in [80,90,85,95,100]: c.record_response(l)
        self.assertEqual(c.get_interaction_signal().response_length_trend, "increasing")
    def test_trend_decreasing(self):
        c = SignalCollector()
        for l in [100,90,95,85,80]: c.record_response(l)
        for l in [10,12,11,9,8]: c.record_response(l)
        self.assertEqual(c.get_interaction_signal().response_length_trend, "decreasing")
    def test_task_switches(self):
        c = SignalCollector()
        for _ in range(3): c.record_task_switch()
        self.assertEqual(c.get_interaction_signal().task_switch_frequency, 3)

if __name__ == "__main__":
    unittest.main()
