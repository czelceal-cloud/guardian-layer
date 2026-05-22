"""Test AIInterruptEvaluator"""
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from tical_code.vigil.interrupt_evaluator import AIInterruptEvaluator, NewInstruction
from tical_code.vigil.ai_state_classifier import AIStateResult

def _st(s, d=30): return AIStateResult(state=s, confidence=0.9, evidence=[], duration_seconds=d)
class Test(unittest.TestCase):
    def setUp(self): self.e = AIInterruptEvaluator()
    def test_parallel_queue(self): self.assertEqual(self.e.evaluate_new_instruction(NewInstruction(content="顺便查天气"), _st("DEEP_WORK")).action, "queue")
    def test_hurry_reject(self): self.assertEqual(self.e.evaluate_new_instruction(NewInstruction(content="快点"), _st("REASONING")).action, "reject")
    def test_emergency_execute(self): self.assertEqual(self.e.evaluate_new_instruction(NewInstruction(content="着火了！"), _st("DEEP_WORK")).action, "execute_now")
    def test_waiting_execute(self): self.assertEqual(self.e.evaluate_new_instruction(NewInstruction(content="写个函数"), _st("WAITING")).action, "execute_now")
    def test_stuck_interrupt(self): self.assertEqual(self.e.evaluate_new_instruction(NewInstruction(content="新任务"), _st("STUCK")).action, "interrupt_current")

if __name__ == "__main__":
    unittest.main()
