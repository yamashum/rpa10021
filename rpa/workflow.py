from enum import Enum
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

class StepType(Enum):
    CLICK = "click"
    INPUT = "input"
    CONDITION = "condition"

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
    else:
        logger.error("Unknown StepType: %s", step.step_type)
        raise ValueError(f"Unknown StepType: {step.step_type}")
