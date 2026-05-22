# Guardian Layer — AI Safety Runtime

A modular guardian layer for `tical-code` that protects both human focus and AI execution depth.

## Architecture

```
tical_code/guardian/
├── __init__.py              # Guardian factory + patrol/evaluate_instruction entry points
├── guardian_config.py/yaml  # YAML config with sane defaults
├── signal_collector.py      # Human interaction signal collection + PhysioAdapter plugin
├── ai_signal_collector.py   # AI execution state tracking + stuck detection
├── state_classifier.py      # 5-state human classifier (FOCUS/INSPIRATION/REST/FATIGUE/DISTRESS)
├── ai_state_classifier.py   # 5-state AI classifier (DEEP_WORK/REASONING/GENERATING/WAITING/STUCK)
├── guardian_judge.py        # Shared arbiter (human guardian always outranks AI)
├── ai_interrupt_evaluator.py # New instruction interception (urgent/hurry/redirect/parallel/general)
├── instruction_queue.py     # Priority queue with TTL expiry
├── decision_trace.py        # JSONL audit log + ring buffer
├── actions.py               # Intervention executor (protect/notify/prompt/interrupt/alert)
├── tests/                   # Unit tests (53/53 all green)
└── integration/             # worker_loop adapter
```

## Quick Start

```python
from tical_code.guardian import build_guardian
guardian = build_guardian()

# In worker loop, every 5 min:
await guardian.patrol()

# On each new user instruction while AI is busy:
from tical_code.guardian import NewInstruction
verdict = guardian.evaluate_instruction(NewInstruction(content=user_text))
```

## Core Philosophy

"Say NO to meaningless hurry and noise. Defend human flow and AI reasoning depth in both directions."

Phase 1: Pure software branch (no wearables required)
Phase 2: Wearable hardware integration (PhysioAdapter plugin interface ready)
