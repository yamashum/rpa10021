from enum import Enum
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

class StepType(Enum):
    CLICK = "click"
    INPUT = "input"

@dataclass
class Step:
    step_type: Enum
    payload: dict | None = None


def execute_step(step: Step):
    """Execute a single automation step."""
    if step.step_type == StepType.CLICK:
        logger.info("Executing click step")
    elif step.step_type == StepType.INPUT:
        logger.info("Executing input step")
    else:
        logger.error("Unknown StepType: %s", step.step_type)
        raise ValueError(f"Unknown StepType: {step.step_type}")
