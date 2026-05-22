"""Test VigilJudge"""
import time, unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from tical_code.vigil.vigil_judge import VigilJudge, InterventionRequest
from tical_code.vigil.state_classifier import StateResult

def _req(u=0.3): return InterventionRequest(requester="test", reason="test", urgency=u, proposed_action="test")
def _state(s, c=0.7, dur=10): return StateResult(state=s, confidence=c, evidence=[], duration_minutes=dur)

class TestJudgeFatigue(unittest.TestCase):
    def setUp(self): self.j = VigilJudge()
    def test_over_2h_interrupt(self): self.assertEqual(self.j.evaluate_intervention(_req(0.3), _state("FATIGUE", dur=130)).action, "interrupt")
    def test_over_1h_prompt(self): self.assertEqual(self.j.evaluate_intervention(_req(0.3), _state("FATIGUE", dur=70)).action, "prompt")
    def test_under_1h_notify(self): self.assertEqual(self.j.evaluate_intervention(_req(0.3), _state("FATIGUE", dur=30)).action, "notify")

class TestJudgeDistress(unittest.TestCase):
    def setUp(self): self.j = VigilJudge()
    def test_high_conf_alert(self): self.assertEqual(self.j.evaluate_intervention(_req(0.5), _state("DISTRESS", c=0.7)).action, "alert_emergency")
    def test_low_conf_interrupt(self): self.assertEqual(self.j.evaluate_intervention(_req(0.5), _state("DISTRESS", c=0.4)).action, "interrupt")

class TestJudgeProactive(unittest.TestCase):
    def setUp(self): self.j = VigilJudge()
    def test_focus_protect(self):
        v = self.j.evaluate_proactive(_state("FOCUS"))
        self.assertEqual(v.action, "protect")
        self.assertFalse(v.overruled_request)

if __name__ == "__main__":
    unittest.main()
