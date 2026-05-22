"""test_collector.py — Unit tests for SignalCollector"""
import time, unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tical_code.guardian.signal_collector import SignalCollector

class TestSignalCollector(unittest.TestCase):
    def test_empty_collector_returns_signal(self):
        c = SignalCollector()
        sig = c.get_interaction_signal()
        self.assertIsNotNone(sig)
    def test_records_input_and_updates_last_input_time(self):
        c = SignalCollector()
        before = time.time()
        c.record_input()
        sig = c.get_interaction_signal()
        self.assertGreaterEqual(sig.last_input_time, before)
    def test_error_rate_computed(self):
        c = SignalCollector()
        for _ in range(8):
            c.record_input(had_error=False)
        for _ in range(2):
            c.record_input(had_error=True)
        sig = c.get_interaction_signal()
        self.assertAlmostEqual(sig.input_error_rate, 0.2, delta=0.05)
    def test_response_length_trend_increasing(self):
        c = SignalCollector()
        for length in [10, 12, 11, 13, 15]:
            c.record_response(length)
        for length in [80, 90, 85, 95, 100]:
            c.record_response(length)
        sig = c.get_interaction_signal()
        self.assertEqual(sig.response_length_trend, "increasing")
    def test_response_length_trend_decreasing(self):
        c = SignalCollector()
        for length in [100, 90, 95, 85, 80]:
            c.record_response(length)
        for length in [10, 12, 11, 9, 8]:
            c.record_response(length)
        sig = c.get_interaction_signal()
        self.assertEqual(sig.response_length_trend, "decreasing")
    def test_task_switch_frequency_counted(self):
        c = SignalCollector()
        for _ in range(3):
            c.record_task_switch()
        sig = c.get_interaction_signal()
        self.assertEqual(sig.task_switch_frequency, 3)
    def test_no_physio_returns_none(self):
        c = SignalCollector()
        self.assertIsNone(c.get_physio_signal())
    def test_combined_signal_contains_interaction(self):
        c = SignalCollector()
        c.record_input()
        combined = c.collect()
        self.assertIsNotNone(combined.interaction)

if __name__ == "__main__":
    unittest.main()
