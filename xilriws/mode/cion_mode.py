from __future__ import annotations

from litestar import Litestar, get
from litestar.di import Provide
from litestar.exceptions import HTTPException
from loguru import logger

from xilriws.browser import Browser, CionResponse
from xilriws.ptc_join import PtcJoin
from .basic_mode import BasicMode

logger = logger.bind(name="Xilriws")


@get("/api/v1/cion")
async def cion_endpoint(ptc_join: PtcJoin) -> list[CionResponse]:
    try:
        tokens = await ptc_join.get_join_tokens()
        logger.success(f"200: Returned {len(tokens)} Cion tokens")
        return tokens

    except Exception as e:
        logger.exception(e)
    logger.error("500: Internal Xilriws error, look above")
    raise HTTPException("internal error")


class CionMode(BasicMode):
    def __init__(self, browser: Browser):
        self.ptc_join = PtcJoin(browser)

    async def prepare(self) -> None:
        await self.ptc_join.prepare()

    async def _get_ptc_join(self):
        return self.ptc_join

    def get_litestar(self) -> Litestar:
        return Litestar(
            route_handlers=[cion_endpoint],
            dependencies={"ptc_join": Provide(self._get_ptc_join)}
        )
