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



    with caplog.at_level(logging.INFO):
        run_workflow(str(wf_file))

    text = caplog.text
    assert "Executing click step" in text
    assert "Condition evaluated" in text

