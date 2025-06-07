import argparse
import json
import logging

from .workflow import Step, StepType, execute_step

logger = logging.getLogger(__name__)


def _parse_step(entry: dict) -> Step:
    """Convert a raw dict into a ``Step`` instance."""
    try:
        stype = StepType(entry["step_type"])
    except Exception:
        logger.error("Unknown step type %s", entry.get("step_type"))
        raise

    payload = entry.get("payload") or {}
    if stype == StepType.LOOP:
        sub_entries = payload.get("steps", [])
        payload["steps"] = [_parse_step(e) for e in sub_entries]
    return Step(step_type=stype, payload=payload)


def load_steps(file_path: str) -> list[Step]:
    """Load workflow steps from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [_parse_step(entry) for entry in data]


def run_workflow(file_path: str) -> None:
    """Execute all steps defined in the given workflow file."""
    steps = load_steps(file_path)
    for step in steps:
        execute_step(step)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run RPA workflow")
    parser.add_argument("workflow", nargs="?", default="workflow.json",
                        help="Path to workflow JSON file")
    args = parser.parse_args(argv)
    run_workflow(args.workflow)


if __name__ == "__main__":
    main()
