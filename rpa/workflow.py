from enum import Enum
from dataclasses import dataclass
from typing import Optional
import logging
import time

logger = logging.getLogger(__name__)


class StepType(Enum):
    CLICK = "click"
    INPUT = "input"
    SCREENSHOT = "screenshot"
    FILE_COPY = "file_copy"
    EXCEL_WRITE = "excel_write"
    CONDITION = "if"
    LOOP = "loop"
    WAIT = "wait"
    NOTIFY = "notify"


@dataclass
class Step:
    step_type: Enum
    payload: Optional[dict] = None


def execute_step(step: Step):
    """Execute a single automation step."""
    if step.step_type == StepType.CLICK:
        logger.info("Executing click step")
    elif step.step_type == StepType.INPUT:
        logger.info("Executing input step")
    elif step.step_type == StepType.SCREENSHOT:
        logger.info("Executing screenshot step")
    elif step.step_type == StepType.FILE_COPY:
        logger.info("Executing file copy step")
    elif step.step_type == StepType.EXCEL_WRITE:
        logger.info("Executing excel write step")
    elif step.step_type == StepType.CONDITION:
        logger.info("Executing conditional step")
    elif step.step_type == StepType.LOOP:
        logger.info("Executing loop step")
    elif step.step_type == StepType.WAIT:
        seconds = 0
        if step.payload is not None:
            seconds = step.payload.get("seconds", 0)
        logger.info("Executing wait step for %s seconds", seconds)
        if seconds > 0:
            time.sleep(seconds)
    elif step.step_type == StepType.NOTIFY:
        logger.info("Executing notify step")
    else:
        logger.error("Unknown StepType: %s", step.step_type)
        raise ValueError(f"Unknown StepType: {step.step_type}")
