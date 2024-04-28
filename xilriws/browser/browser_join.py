from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass

import nodriver
from loguru import logger

from xilriws.constants import JOIN_URL
from xilriws.debug import IS_DEBUG
from xilriws.extension_comm import FINISH_PROXY
from xilriws.js import load, recaptcha
from xilriws.ptc_auth import LoginException
from .browser import Browser, ProxyException
from xilriws.ptc import ptc_utils


logger = logger.bind(name="Browser")


@dataclass
class CionResponse:
    reese_cookie: dict
    create_tokens: list[str]
    activate_tokens: list[str]
    timestamp: int
    proxy: str


class BrowserJoin(Browser):
    async def get_join_tokens(self) -> CionResponse | None:
        try:
            await self.start_browser()
        except Exception:
            return None

        try:
            timestamp = int(time.time())
            js_future, js_check_handler = await self.get_js_check_handler(JOIN_URL)

            await self.new_tab()
            await self.change_proxy()

            proxy = self.proxies.current_proxy
            self.tab.add_handler(nodriver.cdp.network.ResponseReceived, js_check_handler)
            logger.info("Opening Join page")

            html = await self.tab.get_content()
            if "neterror" in html.lower():
                proxy.invalidate()  # TODO this doesn't actually do anything
                raise ProxyException(f"Page couldn't be reached (Proxy: {proxy.url})")

            try:
                await asyncio.wait_for(js_future, timeout=60)
                self.tab.handlers.clear()
                logger.info("JS check done. reloading")
            except asyncio.TimeoutError:
                raise LoginException("Timeout on JS challenge")

            await self.tab.reload()
            html = await self.tab.get_content()

            if "signup" not in html.lower():
                imp_code, imp_reason = ptc_utils.get_imperva_error_code(html)
                raise LoginException(f"Error code {imp_code} ({imp_reason}) with Proxy ({proxy.url})")

            # TODO check for error 16, mark proxies as dead

            try:
                await self.tab.wait_for("iframe[title='reCAPTCHA']", timeout=25)
            except asyncio.TimeoutError:
                raise LoginException("Timeout while waiting for captcha")

            obj, error = await self.tab.send(nodriver.cdp.runtime.evaluate(recaptcha.SRC))

            logger.info("Preparing token retreiving")

            obj, errors = await self.tab.send(nodriver.cdp.runtime.evaluate(load.SRC))
            obj: nodriver.cdp.runtime.RemoteObject

            logger.info("Getting tokens")
            r, errors = await self.tab.send(nodriver.cdp.runtime.await_promise(obj.object_id, return_by_value=True))

            logger.info("Getting cookies from browser")
            all_cookies = await self.get_cookies()
            recaptcha_tokens = r.value

            self.consecutive_failures = 0

            return CionResponse(
                reese_cookie=all_cookies,
                create_tokens=recaptcha_tokens["create"],
                activate_tokens=recaptcha_tokens["activate"],
                timestamp=timestamp,
                proxy=proxy.full_url.geturl(),
            )
        except LoginException as e:
            logger.error(f"{str(e)} while getting tokens")
            self.consecutive_failures += 1
            await asyncio.sleep(1)
            return None
        except ProxyException as e:
            logger.error(f"{str(e)} while getting tokens")
            return None
        except Exception as e:
            logger.exception("Exception during browser", e)

        logger.error("Error while getting cookie from browser, it will be restarted next time")
        self.stop_browser()
        return None
