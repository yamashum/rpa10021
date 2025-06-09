import asyncio
import json
import threading

try:
    import websockets  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    websockets = None


class WebElementServer:
    """Simple WebSocket server to receive captured web element info."""

    def __init__(self, host: str = "localhost", port: int = 8765) -> None:
        self.host = host
        self.port = port
        self.elements = []
        self.loop: asyncio.AbstractEventLoop | None = None
        self.server = None
        self.thread: threading.Thread | None = None

    async def _handler(self, websocket):  # type: ignore[no-untyped-def]
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                continue
            self.elements.append(data)

    def start(self) -> None:
        """Start the WebSocket server in a background thread."""
        if not websockets:
            raise RuntimeError("websockets library not installed")
        self.loop = asyncio.new_event_loop()
        self.server = self.loop.run_until_complete(
            websockets.serve(self._handler, self.host, self.port)
        )
        self.thread = threading.Thread(target=self.loop.run_forever, daemon=True)
        self.thread.start()

    def stop(self) -> None:
        """Stop the WebSocket server."""
        if self.server and self.loop:
            self.loop.call_soon_threadsafe(self.server.close)
            self.loop.call_soon_threadsafe(self.loop.stop)
            if self.thread:
                self.thread.join()
        self.server = None
        self.loop = None
        self.thread = None

    def get_elements(self):
        """Return list of captured elements."""
        return list(self.elements)
