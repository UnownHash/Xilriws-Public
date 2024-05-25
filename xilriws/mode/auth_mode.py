from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from litestar import Litestar, post, Response, Request
from litestar.di import Provide
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_403_FORBIDDEN
from loguru import logger

from xilriws.browser import Browser
from xilriws.ptc_auth import PtcAuth, LoginException, InvalidCredentials
from xilriws.reese_cookie import CookieMonster
from .basic_mode import BasicMode
from xilriws.proxy import ProxyDistributor, Proxy
from xilriws.proxy_dispenser import ProxyDispenser

logger = logger.bind(name="Xilriws")


@dataclass
class RequestData:
    username: str
    password: str
    url: str


class ResponseStatus(Enum):
    SUCCESS = 1
    ERROR = 2
    INVALID = 3


@dataclass
class ResponseData:
    status: str
    login_code: str = ""


@post("/api/v1/login-code")
async def auth_endpoint(request: Request, ptc_auth: PtcAuth, data: RequestData) -> Response[ResponseData]:
    user_agent = request.headers.get("User-Agent", "")
    if user_agent not in ("Go-http-client/1.1", "axios/1.6.8") or not user_agent.startswith("Dragonite/"):
        logger.critical("Please use Dragonite or TMS to connect to Xilriws")
        return Response(ResponseData(status=ResponseStatus.ERROR.name), status_code=HTTP_403_FORBIDDEN)

    try:
        login_code = await ptc_auth.auth(data.username, data.password, data.url)

        logger.success("200 OK: successful auth")
        return Response(
            ResponseData(login_code=login_code, status=ResponseStatus.SUCCESS.name), status_code=HTTP_200_OK
        )
    except InvalidCredentials:
        logger.warning("400 Bad Request: Invalid credentials")
        return Response(ResponseData(status=ResponseStatus.INVALID.name), status_code=HTTP_400_BAD_REQUEST)
    except LoginException as e:
        logger.error(f"Error: {str(e)}")
    except Exception as e:
        logger.exception(e)

    logger.warning("500 Internal Server Error: Additional output above")
    return Response(ResponseData(status=ResponseStatus.ERROR.name), status_code=HTTP_500_INTERNAL_SERVER_ERROR)


class AuthMode(BasicMode):
    def __init__(self, browser: Browser, proxies: ProxyDistributor, proxy_dispenser: ProxyDispenser):
        self.cookie_monster = CookieMonster(browser, proxies, proxy_dispenser)
        self.ptc_auth = PtcAuth(self.cookie_monster)

    async def prepare(self) -> None:
        await self.cookie_monster.prepare()

    async def _get_ptc_auth(self):
        return self.ptc_auth

    def get_litestar(self) -> Litestar:
        return Litestar(
            route_handlers=[auth_endpoint],
            dependencies={"ptc_auth": Provide(self._get_ptc_auth)}
        )
