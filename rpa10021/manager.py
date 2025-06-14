import pyautogui

class StepManager:
    def __init__(self, workflow=None):
        self.workflow = workflow or []

    def run(self):
        for step in self.workflow:
            action = step.get('action')
            if action == 'click':
                x, y = step.get('pos', (0, 0))
                pyautogui.click(x, y)
            elif action == 'typewrite':
                text = step.get('text', '')
                pyautogui.typewrite(text)
