from __future__ import annotations

import asyncio
import json
import logging
import os.path
import signal
import sys
from dataclasses import dataclass
from enum import Enum

import uvicorn
from litestar import Litestar, post, Response
from litestar.di import Provide
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from loguru import logger

from xilriws.browser import Browser
from xilriws.ptc import PtcAuth, LoginException, InvalidCredentials
from xilriws.reese_cookie import CookieMonster

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.CRITICAL)
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.CRITICAL)
nodriver_logger = logging.getLogger("nodriver")
nodriver_logger.setLevel(logging.CRITICAL)

logger = logger.bind(name="Xilriws")


@dataclass
class RequestData:
    username: str
    password: str
    proxy: str
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
async def auth_endpoint(ptc_auth: PtcAuth, data: RequestData) -> Response[ResponseData]:
    try:
        login_code = await ptc_auth.auth(data.username, data.password, data.url, data.proxy)

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


async def main():
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
    cookie_monster = CookieMonster(browser)
    ptc_auth = PtcAuth(cookie_monster)

    async def get_ptc_auth():
        return ptc_auth

    await cookie_monster.prepare()

    port = config.get("port", 5090)
    host = config.get("host", "0.0.0.0")

    app = Litestar(
        route_handlers=[auth_endpoint],
        dependencies={"ptc_auth": Provide(get_ptc_auth)}
    )
    server_config = uvicorn.Config(app, port=port, host=host, log_config=None)
    server = uvicorn.Server(server_config)

    if sys.platform != "win32":
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    logger.info(f"Starting Xilriws on http://{host}:{port}")

    await server.serve()


asyncio.run(main())
