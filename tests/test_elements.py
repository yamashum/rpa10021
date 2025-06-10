import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rpa import elements


def test_fetch_web_element_requires_websockets(monkeypatch):
    monkeypatch.setattr(elements, "websockets", None)
    with pytest.raises(RuntimeError):
        elements.fetch_web_element("div")


def test_get_desktop_element_requires_uiautomation(monkeypatch):
    monkeypatch.setattr(elements, "auto", None)
    with pytest.raises(RuntimeError):
        elements.get_desktop_element(AutomationId="test")


def test_record_click_position_requires_pyautogui(monkeypatch):
    monkeypatch.setattr(elements, "pyautogui", None)
    with pytest.raises(RuntimeError):
        elements.record_click_position()


def test_match_image_requires_opencv(monkeypatch):
    monkeypatch.setattr(elements, "cv2", None)
    monkeypatch.setattr(elements, "np", None)
    with pytest.raises(RuntimeError):
        elements.match_image("a.png", "b.png")
