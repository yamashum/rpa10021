import json
import logging

logger = logging.getLogger(__name__)

try:
    import websockets
    import asyncio
except Exception:  # pragma: no cover - optional dependency
    websockets = None
    asyncio = None

try:
    import uiautomation as auto
except Exception:  # pragma: no cover - optional dependency
    auto = None

try:
    import pyautogui
except Exception:  # pragma: no cover - optional dependency
    pyautogui = None

try:
    import cv2
    import numpy as np
except Exception:  # pragma: no cover - optional dependency
    cv2 = None
    np = None


def fetch_web_element(selector: str, ws_url: str = "ws://localhost:8765") -> dict:
    """Fetch web element information via WebSocket.

    Parameters
    ----------
    selector: str
        CSS selector or XPath to query.
    ws_url: str
        WebSocket URL of the running browser extension.

    Returns
    -------
    dict
        Element information provided by the extension.
    """
    if not websockets or not asyncio:
        raise RuntimeError("websockets library is required for fetch_web_element")

    async def _fetch() -> dict:
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({"selector": selector}))
            data = await ws.recv()
            return json.loads(data)

    return asyncio.get_event_loop().run_until_complete(_fetch())


def get_desktop_element(**kwargs) -> dict:
    """Retrieve a Windows desktop element using uiautomation.

    Parameters can be any keyword arguments accepted by ``uiautomation.Control``.
    """
    if not auto:
        raise RuntimeError("uiautomation library is required for get_desktop_element")
    ctrl = auto.Control(**kwargs)
    rect = ctrl.BoundingRectangle
    return {
        "left": rect.left,
        "top": rect.top,
        "right": rect.right,
        "bottom": rect.bottom,
    }


def record_click_position() -> tuple:
    """Return the current mouse cursor position."""
    if not pyautogui:
        raise RuntimeError("pyautogui is required for record_click_position")
    return pyautogui.position()


def match_image(template_path: str, image_path: str) -> dict:
    """Find ``template_path`` inside ``image_path`` using OpenCV."""
    if not cv2 or not np:
        raise RuntimeError("opencv-python is required for match_image")
    template = cv2.imread(template_path, 0)
    image = cv2.imread(image_path, 0)
    if template is None or image is None:
        raise ValueError("Unable to read image files")
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _min_val, max_val, _min_loc, max_loc = cv2.minMaxLoc(res)
    return {"x": int(max_loc[0]), "y": int(max_loc[1]), "score": float(max_val)}
