"""AI execution state signal collector."""
import time
from dataclasses import dataclass, field
from typing import List

@dataclass
class AISignal:
    current_task_type: str = "idle"
    task_duration_seconds: float = 0.0
    tool_call_count: int = 0
    tool_call_repeat_count: int = 0
    token_consumption_rate: float = 0.0
    output_length: int = 0
    has_unfinished_output: bool = False
    last_progress_time: float = field(default_factory=time.time)
    estimated_completion: float = 0.0

@dataclass
class _ToolCallEvent:
    tool_name: str; timestamp: float

@dataclass
class _TokenEvent:
    count: int; timestamp: float

class AISignalCollector:
    _STUCK_REPEAT_THRESHOLD = 3
    _STUCK_NO_PROGRESS_SECONDS = 60
    def __init__(self):
        self._task_type = "idle"; self._task_start = 0.0
        self._tool_calls: List[_ToolCallEvent] = []
        self._token_events: List[_TokenEvent] = []
        self._output_length = 0; self._has_unfinished = False
        self._last_progress = time.time(); self._estimated_completion = 0.0
        self._is_active = False
    def task_started(self, task_type: str):
        self._task_type = task_type; self._task_start = time.time()
        self._tool_calls.clear(); self._token_events.clear()
        self._output_length = 0; self._has_unfinished = True
        self._last_progress = time.time(); self._estimated_completion = 0.0
        self._is_active = True
    def task_completed(self):
        self._has_unfinished = False; self._is_active = False
        self._task_type = "idle"; self._estimated_completion = 1.0
    def set_waiting(self):
        self._task_type = "waiting"; self._has_unfinished = False; self._is_active = False
    def record_tool_call(self, tool_name: str):
        self._tool_calls.append(_ToolCallEvent(tool_name, time.time()))
        self._last_progress = time.time()
    def record_tokens(self, count: int):
        self._token_events.append(_TokenEvent(count, time.time()))
        if count > 0: self._last_progress = time.time()
    def record_output_length(self, length: int): self._output_length = length
    def set_estimated_completion(self, value: float): self._estimated_completion = max(0.0, min(1.0, value))
    def collect(self) -> AISignal:
        now = time.time(); duration = (now - self._task_start) if self._task_start else 0.0
        cutoff = now - 10
        recent_tokens = [e for e in self._token_events if e.timestamp >= cutoff]
        rate = sum(e.count for e in recent_tokens) / 10.0 if recent_tokens else 0.0
        return AISignal(current_task_type=self._task_type, task_duration_seconds=duration,
            tool_call_count=len(self._tool_calls), tool_call_repeat_count=self._count_tool_repeats(),
            token_consumption_rate=rate, output_length=self._output_length,
            has_unfinished_output=self._has_unfinished, last_progress_time=self._last_progress,
            estimated_completion=self._estimated_completion)
    def _count_tool_repeats(self) -> int:
        if len(self._tool_calls) < 2: return 0
        last = self._tool_calls[-1].tool_name; count = 0
        for ev in reversed(self._tool_calls):
            if ev.tool_name == last: count += 1
            else: break
        return count if count > 1 else 0
    def is_stuck(self) -> bool:
        sig = self.collect()
        no_progress = (time.time() - sig.last_progress_time) > self._STUCK_NO_PROGRESS_SECONDS
        repeat_stuck = sig.tool_call_repeat_count >= self._STUCK_REPEAT_THRESHOLD
        return self._is_active and (no_progress or repeat_stuck)
