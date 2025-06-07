import logging
import json
import pytest

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


def test_loop_step_executes_sub_steps(caplog):
    sub_steps = [Step(step_type=StepType.CLICK), Step(step_type=StepType.INPUT)]
    step = Step(step_type=StepType.LOOP, payload={"count": 2, "steps": sub_steps})
    with caplog.at_level(logging.INFO):
        execute_step(step)
    text = caplog.text
    assert text.count("Executing click step") == 2
    assert text.count("Executing input step") == 2


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


def test_run_workflow_with_loop(tmp_path, caplog):
    steps = [
        {
            "step_type": "loop",
            "payload": {
                "count": 2,
                "steps": [
                    {"step_type": "click"},
                    {"step_type": "input"}
                ]
            }
        }
    ]
    wf_file = tmp_path / "loop.json"
    wf_file.write_text(json.dumps(steps))

    with caplog.at_level(logging.INFO):
        run_workflow(str(wf_file))

    text = caplog.text
    assert text.count("Executing click step") == 2
    assert text.count("Executing input step") == 2


def test_load_steps_with_invalid_type_logs_error(tmp_path, caplog):
    steps = [
        {"step_type": "nonexistent"}
    ]
    wf_file = tmp_path / "bad.json"
    wf_file.write_text(json.dumps(steps))

    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            run_workflow(str(wf_file))
    assert "Unknown step type" in caplog.text


def test_condition_step_logs(caplog):
    step = Step(step_type=StepType.CONDITION, payload={"condition": True})
    with caplog.at_level(logging.INFO):
        execute_step(step)
    assert "Condition evaluated" in caplog.text


def test_wait_step_logs_and_sleeps(monkeypatch, caplog):
    recorded = {}

    def fake_sleep(seconds):
        recorded["seconds"] = seconds

    monkeypatch.setattr("rpa.workflow.time.sleep", fake_sleep)

    step = Step(step_type=StepType.WAIT, payload={"seconds": 2})
    with caplog.at_level(logging.INFO):
        execute_step(step)

    assert recorded.get("seconds") == 2
    assert "wait step for 2 seconds" in caplog.text
