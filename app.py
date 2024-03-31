from __future__ import annotations

import asyncio
import json
import logging
import signal
import sys
from dataclasses import dataclass
from enum import Enum

import uvicorn
from litestar import Litestar, post, Request, Response
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK

from ptc_auth import PtcAuth, InvalidCredentials, LoginException

VERSION = "0.2.0"

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.CRITICAL)
auth = PtcAuth()


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
    random_code_verifier: None = None


@post("/api/v1/login-code")
async def auth_endpoint(request: Request, data: RequestData) -> Response[ResponseData]:
    try:
        login_code = await auth.auth(data.username, data.password, data.url, data.proxy)

        return Response(ResponseData(login_code=login_code, status=ResponseStatus.SUCCESS.name), status_code=HTTP_200_OK)
    except InvalidCredentials:
        return Response(ResponseData(status=ResponseStatus.INVALID.name), status_code=HTTP_400_BAD_REQUEST)
    except LoginException as e:
        request.logger.error(f"Error: {str(e)}")
    except Exception as e:
        request.logger.exception(e)

    return Response(ResponseData(status=ResponseStatus.ERROR.name), status_code=HTTP_500_INTERNAL_SERVER_ERROR)


async def main():
    with open("config.json", "r") as f:
        config = json.load(f)

    auth.extension_paths = [
        config.get("fingerprint_random_path", "/maltelogin/xilriws-fingerprint-random/"),
        config.get("cookie_delete_path", "/maltelogin/xilriws-cookie-delete/"),
    ]
    await auth.prepare()

    app = Litestar(route_handlers=[auth_endpoint])
    server_config = uvicorn.Config(
        app,
        port=int(config["port"]),
        host=config["host"],
        # log_config=None,
    )
    server = uvicorn.Server(server_config)

    if sys.platform != "win32":
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    version_logger = logging.getLogger("version")
    version_logger.info("Starting Xilriws")

    await server.serve()


asyncio.run(main())
