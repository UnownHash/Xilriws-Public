from __future__ import annotations

from .proxy import Proxy, ProxyDistributor
from loguru import logger
import time
import asyncio

logger = logger.bind(name="Proxy Dispenser")
AUTH_TIMEOUT = 60 * 60


class ProxyDispenser:
    def __init__(self, list_path: str):
        self.proxies: list[Proxy] = []
        with open(list_path, "r") as f:
            for proxy_url in f.readlines():
                if not proxy_url:
                    continue

                try:
                    self.proxies.append(Proxy(proxy_url))
                except Exception as e:
                    logger.error(f"There was a problem parsing proxy {proxy_url}: {str(e)}")

    async def get_auth_proxy(self) -> Proxy:
        while True:
            for proxy in self.proxies:
                if not proxy.invalidated and proxy.last_limited + AUTH_TIMEOUT < time.time():
                    return proxy
            logger.warning("No free proxies! Consider adding more")
            await asyncio.sleep(5)
