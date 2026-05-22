"""test_ai_classifier.py — Tests for AIStateClassifier"""
import time, unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tical_code.guardian.ai_state_classifier import AIStateClassifier
from tical_code.guardian.ai_signal_collector import AISignal

def _signal(task_type="coding", duration=30, tool_calls=0, tool_repeats=0, token_rate=0.0, output_len=0, unfinished=True, last_progress_ago=5, completion=0.5):
    return AISignal(current_task_type=task_type, task_duration_seconds=duration, tool_call_count=tool_calls, tool_call_repeat_count=tool_repeats, token_consumption_rate=token_rate, output_length=output_len, has_unfinished_output=unfinished, last_progress_time=time.time()-last_progress_ago, estimated_completion=completion)

class TestAIStateClassifier(unittest.TestCase):
    def setUp(self):
        self.clf = AIStateClassifier()
    def test_tool_calls_is_deep_work(self):
        r = self.clf.classify(_signal(tool_calls=4))
        self.assertEqual(r.state, "DEEP_WORK")
    def test_slow_token_no_tools_is_reasoning(self):
        r = self.clf.classify(_signal(tool_calls=0, token_rate=2.0, duration=30, unfinished=True))
        self.assertEqual(r.state, "REASONING")
    def test_high_token_rate_is_generating(self):
        r = self.clf.classify(_signal(token_rate=15.0, output_len=500, unfinished=True))
        self.assertEqual(r.state, "GENERATING")
    def test_idle_is_waiting(self):
        r = self.clf.classify(_signal(task_type="idle", unfinished=False))
        self.assertEqual(r.state, "WAITING")
    def test_waiting_task_type(self):
        r = self.clf.classify(_signal(task_type="waiting", unfinished=False))
        self.assertEqual(r.state, "WAITING")
    def test_tool_repeat_is_stuck(self):
        r = self.clf.classify(_signal(tool_repeats=3))
        self.assertEqual(r.state, "STUCK")
    def test_no_progress_is_stuck(self):
        r = self.clf.classify(_signal(unfinished=True, last_progress_ago=90))
        self.assertEqual(r.state, "STUCK")

if __name__ == "__main__":
    unittest.main()
