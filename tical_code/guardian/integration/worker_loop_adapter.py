"""Worker loop adapter for tical-code integration."""
async def worker_loop_integration(guardian, user_text=None):
    """Call this on every iteration of the worker loop."""
    from tical_code.guardian import NewInstruction
    if user_text:
        verdict = guardian.evaluate_instruction(NewInstruction(content=user_text))
        if verdict.action == "reject":
            return None
        if verdict.action == "queue":
            guardian.instruction_queue.enqueue(NewInstruction(content=user_text), verdict.queue_priority, verdict)
            return None
    return user_text
