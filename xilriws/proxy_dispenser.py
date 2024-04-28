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

                proxy_url = proxy_url.strip()

                if proxy_url.lower() == "local":
                    proxy_url = None

                try:
                    self.proxies.append(Proxy(proxy_url))
                except Exception as e:
                    logger.error(f"There was a problem parsing proxy {proxy_url}: {str(e)}")

        if not self.proxies:
            logger.warning("No configured proxies! Using local IP only")
            self.proxies.append(Proxy(None))

        self.current_auth_index = 0

    async def get_auth_proxy(self) -> Proxy:
        proxy = self.proxies[self.current_auth_index]
        self.current_auth_index = (self.current_auth_index + 1) % len(self.proxies)
        return proxy

        # while True:
        #     for proxy in self.proxies:
        #         if not proxy.invalidated and proxy.last_limited + AUTH_TIMEOUT < time.time():
        #             return proxy
        #     logger.warning("No free proxies! Consider adding more")
        #     await asyncio.sleep(5)
