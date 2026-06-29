import os
import socket
import threading
import time

import uvicorn
import webview

from app.desktop.api import DesktopApi
from app.main import app

HOST = "127.0.0.1"
PORT = 8765


def _run_server() -> None:
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning")


def _wait_for_server(timeout: float = 10.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((HOST, PORT), timeout=0.5):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("Backend server did not start in time")


def main() -> None:
    threading.Thread(target=_run_server, daemon=True).start()
    _wait_for_server()

    dev_frontend_url = os.environ.get("DTDUBBING_DEV_URL")
    url = dev_frontend_url or f"http://{HOST}:{PORT}"

    api = DesktopApi()
    window = webview.create_window("DTDUBBING Tools", url=url, js_api=api, width=1200, height=800)
    api._window = window
    webview.start()


if __name__ == "__main__":
    main()
