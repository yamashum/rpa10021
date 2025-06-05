import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Mock pyautogui before importing StepManager
class MockPyAutoGUI:
    def __init__(self):
        self.click = Mock()
        self.typewrite = Mock()

from unittest.mock import Mock
mock_pyautogui = MockPyAutoGUI()
sys.modules['pyautogui'] = mock_pyautogui

from rpa10021.manager import StepManager

def test_run_calls_pyautogui_methods():
    workflow = [
        {'action': 'click', 'pos': (10, 20)},
        {'action': 'typewrite', 'text': 'hello'},
    ]
    manager = StepManager(workflow)
    manager.run()
    mock_pyautogui.click.assert_called_with(10, 20)
    mock_pyautogui.typewrite.assert_called_with('hello')
