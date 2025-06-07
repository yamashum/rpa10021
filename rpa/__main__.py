import argparse
import json
import logging
from typing import Optional

from .workflow import Step, StepType, execute_step

logger = logging.getLogger(__name__)


def load_steps(file_path: str) -> list[Step]:
    """Load workflow steps from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    steps = []
    for entry in data:
        stype = StepType(entry["step_type"])
        payload = entry.get("payload")
        steps.append(Step(step_type=stype, payload=payload))
    return steps


def run_workflow(file_path: str) -> None:
    """Execute all steps defined in the given workflow file."""
    steps = load_steps(file_path)
    for step in steps:
        execute_step(step)


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Run RPA workflow")
    parser.add_argument("workflow", nargs="?", default="workflow.json",
                        help="Path to workflow JSON file")
    args = parser.parse_args(argv)
    run_workflow(args.workflow)


if __name__ == "__main__":
    main()
