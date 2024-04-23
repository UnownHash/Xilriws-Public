from __future__ import annotations

import websockets
import asyncio
import json
from loguru import logger
from copy import copy
from urllib.parse import ParseResult, urlparse
import time


class Proxy:
    def __init__(self, url: str):
        if isinstance(url, str):
            if "://" not in url:
                url = "http://" + url
            url = urlparse(url)

        self.full_url: ParseResult = url

        self.host = url.hostname
        self.port = url.port
        self.username = url.username
        self.password = url.password

        self.last_limited: float = 0
        self.invalidated: bool = False

    @property
    def url(self):
        return f"{self.host}:{self.port}"

    def rate_limited(self):
        self.last_limited = time.time()

    def invalidate(self):
        self.invalidated = True


logger = logger.bind(name="Proxy")


class ProxyDistributor:
    def __init__(self):
        self.clients: set[websockets.WebSocketServerProtocol] = set()
        self.next_proxy: Proxy | None = None
        self.current_proxy: Proxy | None = None

    async def echo(self, websocket: websockets.WebSocketServerProtocol):
        self.clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)

    def set_next_proxy(self, proxy: Proxy):
        self.next_proxy = proxy

    async def change_proxy(self, proxy: Proxy | None = None):
        if proxy is not None:
            self.set_next_proxy(proxy)

        if self.next_proxy is not None:
            self.current_proxy = copy(self.next_proxy)
        logger.info(f"Switching to Proxy {self.current_proxy.url}")

        message = json.dumps(
            {
                "host": self.current_proxy.host,
                "port": self.current_proxy.port,
                "password": self.current_proxy.password,
                "username": self.current_proxy.username,
            }
        )
        for client in self.clients:
            await client.send(message)

    async def start(self):
        async with websockets.serve(self.echo, "127.0.0.1", 9091):
            await asyncio.Future()
