from __future__ import annotations

import asyncio
import json
import logging
import os.path
import signal
import sys

import uvicorn
from loguru import logger

from xilriws.browser import Browser
from xilriws.mode import CionMode, AuthMode

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.CRITICAL)
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.CRITICAL)
nodriver_logger = logging.getLogger("nodriver")
nodriver_logger.setLevel(logging.CRITICAL)

logger = logger.bind(name="Xilriws")

if sys.platform != "win32":
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)


async def main(cion_mode: bool):
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config: dict[str, str | int] = json.load(f)
    else:
        config = {}

    browser = Browser(
        [
            config.get("fingerprint_random_path", "/xilriws/xilriws-fingerprint-random/"),
            config.get("cookie_delete_path", "/xilriws/xilriws-cookie-delete/"),
        ]
    )

    if cion_mode:
        logger.info("Starting in Cion Mode")
        mode = CionMode(browser)
    else:
        mode = AuthMode(browser)

    await mode.prepare()

    port = config.get("port", 5090)
    host = config.get("host", "0.0.0.0")

    app = mode.get_litestar()
    server_config = uvicorn.Config(app, port=port, host=host, log_config=None)
    server = uvicorn.Server(server_config)

    logger.info(f"Starting Xilriws on http://{host}:{port}")

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main(cion_mode=False))
