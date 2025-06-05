import logging
import pytest

import json
from rpa import run_workflow
from rpa.workflow import Step, StepType, execute_step


def test_execute_step_unknown_type_logs_error(caplog):
    class FakeType:
        pass

    step = Step(step_type=FakeType())

    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            execute_step(step)
    assert "Unknown StepType" in caplog.text


def test_condition_step_and_operator():
    step = Step(step_type=StepType.CONDITION,
                payload={"conditions": [True, True], "operator": "and"})
    result = execute_step(step)
    assert result is True


def test_condition_step_or_operator():
    step = Step(step_type=StepType.CONDITION,
                payload={"conditions": [False, True], "operator": "or"})
    result = execute_step(step)
    assert result is True


def test_file_copy_step(tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("data")
    step = Step(step_type=StepType.FILE_COPY,
                payload={"src": str(src), "dst": str(dst)})
    execute_step(step)
    assert dst.read_text() == "data"


def test_run_workflow_executes_steps(tmp_path, caplog):
    steps = [
        {"step_type": "click"},
        {"step_type": "condition", "payload": {"conditions": [True], "operator": "and"}},
    ]
    wf_file = tmp_path / "wf.json"
    wf_file.write_text(json.dumps(steps))

    with caplog.at_level(logging.INFO):
        run_workflow(str(wf_file))

    text = caplog.text
    assert "Executing click step" in text
    assert "Condition evaluated" in text
