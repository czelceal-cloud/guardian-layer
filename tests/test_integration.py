"""test_integration.py — End-to-end integration test"""
import asyncio, time, unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tical_code.guardian import build_guardian, NewInstruction
from tical_code.guardian.state_classifier import StateResult
from unittest.mock import MagicMock

class TestIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.messages = []
        async def capture(text):
            self.messages.append(text)
        self.guardian = build_guardian(send_message=capture)
        self.g = self.guardian
    def _focus_state(self):
        return StateResult("FOCUS", 0.85, ["steady_input"], 15.0)
    def _fatigue_state(self, dur=90):
        return StateResult("FATIGUE", 0.75, ["work_5h", "error_rate_20%"], dur)
    async def test_focus_patrol_produces_protect(self):
        before = len(self.messages)
        self.g.state_classifier.classify = MagicMock(return_value=self._focus_state())
        await self.g.patrol()
        self.assertEqual(before, len(self.messages))
    async def test_parallel_instruction_queued_during_deep_work(self):
        self.g.ai_signal_collector.task_started("coding")
        for _ in range(3):
            self.g.ai_signal_collector.record_tool_call("read_file")
        self.g.ai_signal_collector.record_tokens(20)
        verdict = self.g.evaluate_instruction(NewInstruction(content="顺便帮我查个天气"))
        self.assertEqual(verdict.action, "queue")
    async def test_hurry_rejected_during_deep_work(self):
        self.g.ai_signal_collector.task_started("coding")
        for _ in range(3):
            self.g.ai_signal_collector.record_tool_call("write_file")
        verdict = self.g.evaluate_instruction(NewInstruction(content="快点"))
        self.assertEqual(verdict.action, "reject")
    async def test_emergency_executes_during_deep_work(self):
        self.g.ai_signal_collector.task_started("coding")
        for _ in range(3):
            self.g.ai_signal_collector.record_tool_call("run_tests")
        verdict = self.g.evaluate_instruction(NewInstruction(content="着火了！紧急！"))
        self.assertEqual(verdict.action, "execute_now")
    async def test_waiting_ai_executes_immediately(self):
        self.g.ai_signal_collector.set_waiting()
        verdict = self.g.evaluate_instruction(NewInstruction(content="帮我写一个函数"))
        self.assertEqual(verdict.action, "execute_now")
    async def test_fatigue_patrol_sends_prompt(self):
        self.g.state_classifier.classify = MagicMock(return_value=self._fatigue_state(dur=70))
        before = len(self.messages)
        await self.g.patrol()
        self.assertGreater(len(self.messages), before)
    async def test_queue_drains_after_task_complete(self):
        self.g.ai_signal_collector.task_started("coding")
        for _ in range(3):
            self.g.ai_signal_collector.record_tool_call("bash")
        for content in ["顺便查个天气", "顺便帮我翻译一段话"]:
            v = self.g.evaluate_instruction(NewInstruction(content=content))
            if v.action == "queue":
                self.g.instruction_queue.enqueue(NewInstruction(content=content), v.queue_priority, v)
        self.assertEqual(self.g.instruction_queue.size(), 2)
        self.g.ai_signal_collector.task_completed()
        first = self.g.instruction_queue.dequeue()
        self.assertIsNotNone(first)

if __name__ == "__main__":
    asyncio.run(unittest.main())
