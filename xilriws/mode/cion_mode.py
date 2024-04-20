from __future__ import annotations

import litestar.logging
from litestar import Litestar, get
from litestar.di import Provide
from litestar.exceptions import HTTPException
from loguru import logger

from xilriws.browser import Browser, CionResponse
from xilriws.ptc_join import PtcJoin
from .basic_mode import BasicMode
from xilriws.proxy import ProxyDistributor, Proxy

logger = logger.bind(name="Xilriws")

# PROXIES = """38.162.8.113:3128
# 154.6.97.155:3128
# 38.162.21.83:3128
# 38.162.0.33:3128
# 38.162.31.151:3128
# 38.162.29.43:3128
# 38.162.7.136:3128
# 38.162.13.227:3128
# 38.162.9.177:3128
# 38.162.12.167:3128
# 154.6.98.67:3128
# 89.213.231.225:3128
# 38.162.11.226:3128""".strip()
#
# current_i = [0]
all_proxies = []
# for raw_proxy in PROXIES.split("\n"):
#     host, port = raw_proxy.split(":")
#     all_proxies.append(Proxy(host, int(port), None, None))


@get("/api/v1/cion")
async def cion_endpoint(ptc_join: PtcJoin, proxy: None) -> list[CionResponse]:
    try:
        tokens = await ptc_join.get_join_tokens()
        logger.success(f"200: Returned {len(tokens)} Cion tokens")
        return tokens

    except Exception as e:
        logger.exception(e)
    logger.error("500: Internal Xilriws error, look above")
    raise HTTPException("internal error")


class CionMode(BasicMode):
    def __init__(self, browser: Browser, proxies: ProxyDistributor):
        self.ptc_join = PtcJoin(browser)
        self.proxies = proxies
        self.current_proxy_index = 0

    async def prepare(self) -> None:
        await self.ptc_join.prepare()
        await self._get_proxy()

    async def _get_ptc_join(self):
        return self.ptc_join

    async def _get_proxy(self):
        self.current_proxy_index = (self.current_proxy_index + 1) % len(all_proxies)
        proxy = all_proxies[self.current_proxy_index]
        self.proxies.set_next_proxy(proxy)

    def get_litestar(self) -> Litestar:
        return Litestar(
            route_handlers=[cion_endpoint],
            dependencies={"ptc_join": Provide(self._get_ptc_join), "proxy": Provide(self._get_proxy)},
        )
