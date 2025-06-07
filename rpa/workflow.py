from enum import Enum
from dataclasses import dataclass
import logging
import shutil

logger = logging.getLogger(__name__)

class StepType(Enum):
    CLICK = "click"
    INPUT = "input"
    CONDITION = "condition"
    FILE_COPY = "file_copy"
    LOOP = "loop"

@dataclass
class Step:
    step_type: StepType
    payload: dict | None = None


def execute_step(step: Step):
    """Execute a single automation step."""
    if step.step_type == StepType.CLICK:
        logger.info("Executing click step")
    elif step.step_type == StepType.INPUT:
        logger.info("Executing input step")
    elif step.step_type == StepType.FILE_COPY:
        payload = step.payload or {}
        src = payload.get("src")
        dst = payload.get("dst")
        if not src or not dst:
            raise ValueError("FILE_COPY step requires 'src' and 'dst'")
        shutil.copy(src, dst)
        logger.info("Copied %s -> %s", src, dst)
    elif step.step_type == StepType.CONDITION:
        payload = step.payload or {}
        conditions = payload.get("conditions", [])
        operator = payload.get("operator", "and")
        if not isinstance(conditions, list):
            raise ValueError("conditions must be a list")
        if operator == "and":
            result = all(conditions)
        elif operator == "or":
            result = any(conditions)
        else:
            raise ValueError(f"Invalid operator: {operator}")
        logger.info("Condition evaluated to %s", result)
        return result
    elif step.step_type == StepType.LOOP:
        payload = step.payload or {}
        count = int(payload.get("count", 1))
        sub_steps = payload.get("steps", [])
        if not isinstance(sub_steps, list):
            raise ValueError("steps must be a list")
        for i in range(count):
            logger.info("Loop iteration %s/%s", i + 1, count)
            for sub in sub_steps:
                execute_step(sub)
    else:
        logger.error("Unknown StepType: %s", step.step_type)
        raise ValueError(f"Unknown StepType: {step.step_type}")
