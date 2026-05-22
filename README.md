# Vigil

Quiet watcher. Invisible when not needed. Stands in front when called.

A runtime layer for `tical-code` that protects human focus and AI depth.  
No preaching. No noise. Just a wall between you and meaningless hurry.

## Core Belief

Say NO to noise that carries nothing.  
Defend flow — both human and machine — in both directions.

## Architecture

```
tical_code/vigil/
├── __init__.py              # build_vigil() + patrol/evaluate entry points
├── vigil_config.py/.yaml    # Configuration with sane defaults
├── signal_collector.py      # Human interaction signals + PhysioAdapter plugin
├── ai_signal_collector.py   # AI execution tracking + stuck detection
├── state_classifier.py      # 5-state human classifier
├── ai_state_classifier.py   # 5-state AI classifier
├── vigil_judge.py           # Shared arbiter (human always outranks AI)
├── interrupt_evaluator.py   # Instruction interception
├── instruction_queue.py     # Priority queue with TTL
├── trace_log.py             # JSONL audit log
├── actions.py               # Intervention executor
└── tests/                   # 30 tests, all green
```

## Integration — Two Lines

```python
from tical_code.vigil import build_vigil, NewInstruction

v = build_vigil()

# Every 5 min
await v.patrol()

# On each user input
verdict = v.evaluate_instruction(NewInstruction(content=user_text))
```

## Philosophy

> "安静地守望，不需要的时候隐形，需要的时候挡在你前面。"

*— Named by its creator*
