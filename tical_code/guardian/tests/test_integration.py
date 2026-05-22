"""Integration test"""
import asyncio, unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from tical_code.guardian import build_guardian, NewInstruction
from unittest.mock import MagicMock
from tical_code.guardian.state_classifier import StateResult

class Test(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.msgs = []
        async def cap(t): self.msgs.append(t)
        self.g = build_guardian(send_message=cap)
    async def test_patrol_focus_protect(self):
        self.g.state_classifier.classify = MagicMock(return_value=StateResult("FOCUS", 0.85, ["steady"], 15))
        before = len(self.msgs); await self.g.patrol()
        self.assertEqual(len(self.msgs), before)
    async def test_parallel_queued(self):
        self.g.ai_signal_collector.task_started("coding")
        self.g.ai_signal_collector.record_tool_call("bash")
        self.g.ai_signal_collector.record_tool_call("web_fetch")
        self.g.ai_signal_collector.record_tokens(20)
        self.assertEqual(self.g.evaluate_instruction(NewInstruction(content="顺便查天气")).action, "queue")
    async def test_hurry_rejected(self):
        self.g.ai_signal_collector.task_started("coding")
        self.g.ai_signal_collector.record_tool_call("bash")
        self.g.ai_signal_collector.record_tool_call("file_read")
        self.g.ai_signal_collector.record_tokens(10)
        self.assertEqual(self.g.evaluate_instruction(NewInstruction(content="快点")).action, "reject")

if __name__ == "__main__":
    asyncio.run(unittest.main())
