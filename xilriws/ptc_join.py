from __future__ import annotations
from .browser import Browser, CionResponse
from .task_creator import task_creator
from loguru import logger
import asyncio
from .proxy_dispenser import ProxyDispenser
from .proxy import ProxyDistributor

logger = logger.bind(name="Tokens")


class PtcJoin:
    def __init__(self, browser: Browser, proxies: ProxyDistributor, proxy_dispenser: ProxyDispenser):
        self.browser = browser
        self.responses: list[CionResponse] = []
        self.proxies = proxies
        self.proxy_dispenser = proxy_dispenser

    async def get_join_tokens(self) -> list[CionResponse]:
        responses = self.responses.copy()
        self.responses.clear()
        return responses

    async def prepare(self):
        task_creator.create_task(self.fill_task())

    async def fill_task(self):
        # TODO: invalidate old tokens
        while True:
            logger.info("Getting tokens")
            try:
                proxy = await self.proxy_dispenser.get_auth_proxy()
                proxy.rate_limited()
                self.proxies.set_next_proxy(proxy)
                resp = await self.browser.get_join_tokens()
                if resp:
                    self.responses.append(resp)
            except Exception as e:
                logger.exception("unhandled exception while getting tokens", e)

            await asyncio.sleep(1.1)
