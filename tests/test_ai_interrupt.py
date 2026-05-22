"""test_ai_interrupt.py — Tests for AIInterruptEvaluator"""
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tical_code.guardian.ai_interrupt_evaluator import AIInterruptEvaluator, NewInstruction
from tical_code.guardian.ai_state_classifier import AIStateResult

def _state(s, dur=30.0):
    return AIStateResult(state=s, confidence=0.9, evidence=[], duration_seconds=dur)
def _instr(text, urgency=0.0):
    return NewInstruction(content=text, urgency_hint=urgency)

class TestAIInterruptEvaluator(unittest.TestCase):
    def setUp(self):
        self.ev = AIInterruptEvaluator()
    def test_deep_work_parallel_queued(self):
        v = self.ev.evaluate_new_instruction(_instr("顺便帮我查一下天气"), _state("DEEP_WORK"))
        self.assertEqual(v.action, "queue")
    def test_reasoning_hurry_rejected(self):
        v = self.ev.evaluate_new_instruction(_instr("快点"), _state("REASONING"))
        self.assertEqual(v.action, "reject")
    def test_generating_redirect_interrupt(self):
        v = self.ev.evaluate_new_instruction(_instr("方向错了，停"), _state("GENERATING", dur=10))
        self.assertIn(v.action, ("interrupt_current", "queue"))
    def test_waiting_always_execute(self):
        v = self.ev.evaluate_new_instruction(_instr("帮我写个函数"), _state("WAITING"))
        self.assertEqual(v.action, "execute_now")
    def test_stuck_always_interrupt(self):
        v = self.ev.evaluate_new_instruction(_instr("新任务"), _state("STUCK"))
        self.assertEqual(v.action, "interrupt_current")
    def test_deep_work_emergency_execute(self):
        v = self.ev.evaluate_new_instruction(_instr("着火了！紧急！"), _state("DEEP_WORK"))
        self.assertEqual(v.action, "execute_now")
    def test_pure_hurry_english(self):
        v = self.ev.evaluate_new_instruction(_instr("hurry up"), _state("DEEP_WORK"))
        self.assertEqual(v.action, "reject")
    def test_high_urgency_hint_executes(self):
        v = self.ev.evaluate_new_instruction(_instr("看一下这个文件", urgency=0.9), _state("DEEP_WORK"))
        self.assertEqual(v.action, "execute_now")

if __name__ == "__main__":
    unittest.main()
