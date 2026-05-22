# Guardian Layer

AI safety runtime that protects **human focus** and **AI execution depth**.

> "敢于对无实质内容的催促与噪音说不，双向捍卫人类心流与AI推理深度"

## Two Guards, One Kernel

| Guard | What it protects | How |
|-------|-----------------|-----|
| **Human Guardian** | Your focus, rest, health | Signal → Classify (5 states) → Judge → Act |
| **AI Guardian** | AI's deep-work flow | Categorize new instruction → Queue / Reject / Interrupt |

## 5 Human States

FOCUS → deep work, protect
INSPIRATION → creative flow, protect
REST → recovery, let it be
FATIGUE → notify → prompt → interrupt (escalating)
DISTRESS → alert emergency

## 5 AI States

DEEP_WORK / REASONING / GENERATING → protect unless urgent
WAITING → always execute immediately
STUCK → force interrupt, switch task

## Quick Start

```python
from tical_code.guardian import build_guardian, NewInstruction

guardian = build_guardian()

# Patrol every 5 min (fatigue + stuck detection)
await guardian.patrol()

# Before passing user input to LLM
verdict = guardian.evaluate_instruction(NewInstruction(content=user_text))
if verdict.action == "reject":
    return  # "快点" → silently dropped
if verdict.action == "queue":
    guardian.instruction_queue.enqueue(...)
if verdict.action == "execute_now":
    process_normally(user_text)
```

## What gets rejected

"快点" "催" "搞快些" "faster" "hurry up" → reject (pure hurry, no content)

## What gets queued

"顺便查个天气" "顺便帮我翻译" "by the way..." → queue until current task done

## Dependencies

Zero. Pure Python 3.10+ standard library. Optional: PyYAML for config files.

## Test

```bash
pytest tical_code/guardian/tests/ -v
```
