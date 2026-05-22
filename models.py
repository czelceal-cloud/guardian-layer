
from dataclasses import dataclass, field
from typing import Optional, List
import time

@dataclass
class InteractionSignal:
    input_interval_avg: float = 0.0
    input_interval_variance: float = 0.0
    session_duration: float = 0.0
    consecutive_work_hours: float = 0.0
    input_error_rate: float = 0.0
    response_length_trend: str = "stable"
    task_switch_frequency: float = 0.0
    input_gap_minutes: float = 0.0

@dataclass
class StateResult:
    state: str
    confidence: float
    evidence: List[str]
    duration_minutes: float = 0.0

@dataclass
class InterventionRequest:
    requester:str
    reason:str
    urgency:float
    proposed_action:str
    timestamp:float=time.time()

@dataclass
class GuardianVerdict:
    action:str
    target:str
    confidence:float
    reason:str
    overruled_request:bool
    evidence:List[str]=field(default_factory=list)
    cooldown_minutes:float=30.0
    timestamp:float=time.time()

@dataclass
class AISignal:
    current_task_type:str="idle"
    task_duration_seconds:float=0
    tool_call_repeat_count:int=0
    token_consumption_rate:float=0
    has_unfinished_output:bool=False
    estimated_completion:float=0.0

@dataclass
class NewInstruction:
    content:str
    source:str="human"
    urgency_hint:float=0.0
    timestamp:float=time.time()
