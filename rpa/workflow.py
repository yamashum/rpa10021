from enum import Enum
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


    else:
        logger.error("Unknown StepType: %s", step.step_type)
        raise ValueError(f"Unknown StepType: {step.step_type}")
