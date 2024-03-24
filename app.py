from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass

import uvicorn
from litestar import Litestar, post, Request
from litestar.exceptions import HTTPException

from ptc_auth import PtcAuth

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.CRITICAL)
auth = PtcAuth()


@dataclass
class Data:
    username: str
    password: str
    proxy: str
    url: str


@post("/api/v1/login-code")
async def auth_endpoint(request: Request, data: Data) -> dict[str, str]:
    try:
        login_code = await auth.auth(data.username, data.password, data.url, data.proxy)

        return {"login_code": login_code, "random_code_verifier": None}
    except Exception as e:
        request.logger.exception(e)
        HTTPException(detail=str(e), status_code=500)


async def main():
    with open("config.json", "r") as f:
        config = json.load(f)

    app = Litestar(route_handlers=[auth_endpoint])
    server_config = uvicorn.Config(
        app,
        port=int(config["port"]),
        host=config["host"],
        # log_config=None,
    )
    server = uvicorn.Server(server_config)
    await server.serve()


asyncio.run(main())
