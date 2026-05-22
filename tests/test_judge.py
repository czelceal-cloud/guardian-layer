"""test_judge.py — Tests for GuardianJudge"""
import time, unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tical_code.guardian.guardian_judge import GuardianJudge, InterventionRequest, GuardianVerdict
from tical_code.guardian.state_classifier import StateResult

def _req(urgency=0.3):
    return InterventionRequest(requester="test", reason="test", urgency=urgency, proposed_action="test")
def _state(s, conf=0.7, dur=10):
    return StateResult(state=s, confidence=conf, evidence=[], duration_minutes=dur)

class TestJudgeFatigue(unittest.TestCase):
    def setUp(self):
        self.judge = GuardianJudge()
    def test_fatigue_over_2h_interrupt(self):
        v = self.judge.evaluate_intervention(_req(0.3), _state("FATIGUE", dur=130))
        self.assertEqual(v.action, "interrupt")
    def test_fatigue_over_1h_prompt(self):
        v = self.judge.evaluate_intervention(_req(0.3), _state("FATIGUE", dur=70))
        self.assertEqual(v.action, "prompt")
    def test_fatigue_under_1h_notify(self):
        v = self.judge.evaluate_intervention(_req(0.3), _state("FATIGUE", dur=30))
        self.assertEqual(v.action, "notify")

class TestJudgeDistress(unittest.TestCase):
    def setUp(self):
        self.judge = GuardianJudge()
    def test_distress_high_conf_alert(self):
        v = self.judge.evaluate_intervention(_req(0.5), _state("DISTRESS", conf=0.7))
        self.assertEqual(v.action, "alert_emergency")
    def test_distress_low_conf_interrupt(self):
        v = self.judge.evaluate_intervention(_req(0.5), _state("DISTRESS", conf=0.4))
        self.assertEqual(v.action, "interrupt")

class TestJudgeProactive(unittest.TestCase):
    def setUp(self):
        self.judge = GuardianJudge()
    def test_proactive_focus_protect(self):
        v = self.judge.evaluate_proactive(_state("FOCUS"))
        self.assertEqual(v.action, "protect")
        self.assertFalse(v.overruled_request)
    def test_proactive_distress_alert(self):
        v = self.judge.evaluate_proactive(_state("DISTRESS", conf=0.75))
        self.assertEqual(v.action, "alert_emergency")

if __name__ == "__main__":
    unittest.main()
