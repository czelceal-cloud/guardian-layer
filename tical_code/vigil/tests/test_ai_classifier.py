"""Test AIStateClassifier"""
import time, unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from tical_code.vigil.ai_state_classifier import AIStateClassifier
from tical_code.vigil.ai_signal_collector import AISignal

def _s(task="coding", dur=30, calls=0, reps=0, rate=0.0, length=0, unfinished=True, ago=5):
    return AISignal(current_task_type=task, task_duration_seconds=dur, tool_call_count=calls,
        tool_call_repeat_count=reps, token_consumption_rate=rate, output_length=length,
        has_unfinished_output=unfinished, last_progress_time=time.time()-ago)

class Test(unittest.TestCase):
    def setUp(self): self.c = AIStateClassifier()
    def test_deep_work(self): self.assertEqual(self.c.classify(_s(calls=4)).state, "DEEP_WORK")
    def test_reasoning(self): self.assertEqual(self.c.classify(_s(calls=0, rate=2.0, dur=30)).state, "REASONING")
    def test_generating(self): self.assertEqual(self.c.classify(_s(rate=15.0, length=500)).state, "GENERATING")
    def test_waiting(self): self.assertEqual(self.c.classify(_s(task="idle", unfinished=False)).state, "WAITING")
    def test_stuck_repeat(self): self.assertEqual(self.c.classify(_s(reps=3)).state, "STUCK")
    def test_stuck_noprogress(self): self.assertEqual(self.c.classify(_s(unfinished=True, ago=90)).state, "STUCK")

if __name__ == "__main__":
    unittest.main()
