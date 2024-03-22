from __future__ import annotations

import json
import asyncio
import base64
import hashlib
import random
import re
from dataclasses import dataclass
from urllib.parse import urlencode

import nodriver
import uvicorn
from litestar import Litestar, post, Request
from litestar.exceptions import HTTPException

QueueType = "asyncio.Queue[tuple[str, str, Logger, asyncio.Future]]"


class LoginException(Exception):
    pass


class MalteLogin:
    ACCESS_URL = "https://access.pokemon.com/"
    browser: nodriver.Browser | None = None
    tab: nodriver.Tab | None = None
    queue: QueueType
    task: asyncio.Task | None = None

    def make_queue(self):
        self.queue = asyncio.Queue()

    async def solve(self):
        while True:
            username, password, logger, fut = await self.queue.get()

            try:
                random_code_verifier: str = self.__get_random_string(86)
                random_state: str = self.__get_random_string(24)

                code_challenge = self.__challenge_from_code_verifier(random_code_verifier)

                params = {
                    "state": random_state,
                    "scope": "openid offline email dob pokemon_go member_id username",
                    "redirect_uri": "https://www.pokemongolive.com/dl?app=pokemongo&dl_action=OPEN_LOGIN",
                    "client_id": "pokemon-go",
                    "response_type": "code",
                    "code_challenge": code_challenge,
                    "code_challenge_method": "S256",
                }
                full_url = self.ACCESS_URL + "oauth2/auth?" + urlencode(params)

                if not self.tab:
                    self.browser = await nodriver.start(headless=True)

                js_future = asyncio.get_running_loop().create_future()

                async def js_check_handler(event: nodriver.cdp.network.ResponseReceived):
                    url = event.response.url
                    if not url.startswith("https://access.pokemon.com/"):
                        return
                    if not url.endswith("?d=access.pokemon.com"):
                        return
                    js_future.set_result(True)

                self.tab = await self.browser.get(url=full_url)
                self.tab.add_handler(nodriver.cdp.network.ResponseReceived, js_check_handler)

                html = await self.tab.get_content()
                if "Log in" not in html:
                    try:
                        await asyncio.wait_for(js_future, timeout=10)
                    except asyncio.TimeoutError:
                        raise LoginException("Timeout on JS challenge")

                    await self.tab.reload()

                self.tab.handlers.clear()

                accept_input = await self.tab.wait_for("input#accept")

                js_email = f'document.querySelector("input#email").value="{username}"'
                js_pass = f'document.querySelector("input#password").value="{password}"'

                await self.tab.evaluate(js_email + ";" + js_pass)

                pokemongo_url_future = asyncio.get_running_loop().create_future()

                async def send_handler(event: nodriver.cdp.network.RequestWillBeSent):
                    url = event.request.url
                    if url.startswith("pokemongo://"):
                        pokemongo_url_future.set_result(url)

                self.tab.add_handler(nodriver.cdp.network.RequestWillBeSent, send_handler)

                await accept_input.click()

                await self.tab.wait_for("html")
                await self.tab.update_target()

                if self.tab.target.url.startswith("https://access.pokemon.com/consent"):
                    consent_accept = await self.tab.wait_for("input#accept")
                    if not consent_accept:
                        raise LoginException("no consent button")
                    await consent_accept.click()

                try:
                    pokemongo_url = await asyncio.wait_for(pokemongo_url_future, timeout=20)
                except asyncio.TimeoutError:
                    print("Timeout error!")
                    raise LoginException("Timeout while waiting for browser to finish")

                self.tab.handlers.clear()

                login_code = self.__extract_login_code(pokemongo_url)
                if not login_code:
                    raise LoginException("no login code found")
                fut.set_result({"login_code": login_code, "random_code_verifier": random_code_verifier})

            except Exception as e:
                logger.exception(e)
                fut.set_result(e)

    def get_self(self):
        return self

    def __extract_login_code(self, html) -> str | None:
        matches = re.search(r"pokemongo://state=(.*?),code=(.*)", html)

        if matches and len(matches.groups()) == 2:
            return matches.group(2)

    def __get_random_string(self, length: int) -> str:
        output = ""
        for _ in range(length):
            output += random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
        return output

    def __challenge_from_code_verifier(self, code_verifier) -> str:
        challenge_bin = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(challenge_bin).decode("utf-8").rstrip("=")


malte_login_ = MalteLogin()


@dataclass
class Data:
    username: str
    password: str
    proxy: str


@post("/v1/login-code", sync_to_thread=False)
async def auth(request: Request, data: Data) -> dict[str, str]:
    request.logger.info("requested auth for " + data.username)
    future = asyncio.get_running_loop().create_future()
    malte_login_.queue.put_nowait((data.username, data.password, request.logger, future))
    result = await future

    if isinstance(result, Exception):
        raise HTTPException(detail=str(result), status_code=500)
    return result


async def main():
    with open("config.json", "r") as f:
        config = json.load(f)

    app = Litestar(route_handlers=[auth])
    server_config = uvicorn.Config(
        app,
        port=int(config["port"]),
        host=config["host"],
        # log_config=None,
    )
    server = uvicorn.Server(server_config)
    malte_login_.make_queue()
    malte_login_.task = asyncio.create_task(malte_login_.solve())
    await server.serve()


asyncio.run(main())
