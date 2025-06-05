import logging
import pytest

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
