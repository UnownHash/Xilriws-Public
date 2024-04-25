from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from dataclasses import dataclass

import nodriver
from loguru import logger

from .constants import ACCESS_URL
from .constants import JOIN_URL
from .debug import IS_DEBUG
from .extension_comm import ExtensionComm, FINISH_PROXY, FINISH_COOKIE_PURGE
from .js import load, recaptcha
from .proxy import ProxyDistributor, Proxy
from .ptc_auth import LoginException
from .reese_cookie import ReeseCookie

logger = logger.bind(name="Browser")
HEADLESS = not IS_DEBUG


class ProxyException(Exception):
    pass


@dataclass
class CionResponse:
    reese_cookie: dict
    create_tokens: list[str]
    activate_tokens: list[str]
    timestamp: int
    proxy: str


class Browser:
    browser: nodriver.Browser | None = None
    tab: nodriver.Tab | None = None
    consecutive_failures = 0
    last_cookies: list[nodriver.cdp.network.CookieParam] | None = None
    cookie_future: asyncio.Future | None = None
    session_count = 0

    def __init__(self, extension_paths: list[str], proxies: ProxyDistributor, ext_comm: ExtensionComm):
        self.extension_paths: list[str] = extension_paths
        self.proxies = proxies
        self.ext_comm = ext_comm

    async def start_browser(self):
        if self.consecutive_failures >= 30:
            logger.critical(f"{self.consecutive_failures} consecutive failures in the browser! this is really bad")
            await asyncio.sleep(60 * 30)
            self.consecutive_failures -= 1
            return None

        logger.info("Browser starting")

        if self.browser:
            self.session_count += 1

            if self.session_count % 100 == 0:
                logger.info("Time for a browser restart")
                self.browser.stop()
                self.browser = None

        if not self.browser:
            config = nodriver.Config(headless=HEADLESS, browser_executable_path=self.__find_chrome_executable())
            config.add_argument(
                '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3"'
            )
            full_command = f"{config.browser_executable_path} {' '.join(config())}"

            try:
                for path in self.extension_paths:
                    config.add_extension(path)

                self.browser = await nodriver.start(config)
                logger.info(f"Starting browser: `{full_command}`")

                if "brave" in self.browser.config.browser_executable_path.lower():
                    await self.set_setting(
                        shadow_roots=[
                            "settings-ui",
                            "settings-main",
                            "settings-basic-page",
                            "settings-default-brave-shields-page",
                        ],
                        element_id="fingerprintingSelectControlType",
                        new_value="block",
                        uri="brave://settings/shields"
                    )
                    await self.set_setting(
                        shadow_roots=[
                            "settings-ui",
                            "settings-main",
                            "settings-basic-page",
                            "settings-privacy-page",
                            "settings-personalization-options",
                            "settings-brave-personalization-options",
                            "settings-dropdown-menu",
                        ],
                        element_id="dropdownMenu",
                        new_value="disable_non_proxied_udp",
                        uri="brave://settings/privacy"
                    )

            except Exception as e:
                logger.error(str(e))
                logger.error(
                    f"Error while starting the browser. Please confirm you can start it manually by running "
                    f"`{full_command}`"
                )
                raise e

    async def get_reese_cookie(self, proxy: Proxy) -> ReeseCookie | None:
        try:
            await self.start_browser()
        except Exception:
            return None

        try:
            js_future = asyncio.get_running_loop().create_future()

            async def js_check_handler(event: nodriver.cdp.network.ResponseReceived):
                url = event.response.url
                if not url.startswith(ACCESS_URL):
                    return
                if not url.endswith("?d=access.pokemon.com"):
                    return
                if not js_future.done():
                    js_future.set_result(True)

            await self._open_tab()

            # await asyncio.sleep(10000)

            # await self.tab.set_window_size(0, 0, 720, 1080)

            proxy_future = await self.ext_comm.add_listener(FINISH_PROXY)
            await self.proxies.change_proxy()

            try:
                await asyncio.wait_for(proxy_future, 2)
            except asyncio.TimeoutError:
                logger.info("Didn't get confirmation that proxy changed, continuing anyway")

            if self.last_cookies:
                if self.cookie_future:
                    try:
                        await asyncio.wait_for(self.cookie_future, 2)
                    except asyncio.TimeoutError:
                        logger.info("Didn't get confirmation that cookies were cleared, continuing anyway")
                await self.browser.cookies.set_all(self.last_cookies)

            proxy = self.proxies.current_proxy

            if IS_DEBUG:
                await self._log_ip()

            self.tab.add_handler(nodriver.cdp.network.ResponseReceived, js_check_handler)
            logger.info("Opening PTC")
            await self.tab.get(url=ACCESS_URL + "login")

            html = await self.tab.get_content()
            if "ERR_EMPTY_RESPONSE" in html or "ERR_EMPTY_RESPONSE" in html:
                proxy.invalidate()  # TODO this doesn't actually do anything
                raise ProxyException(f"Proxy {proxy.url} couldn't be reached")
            if "log in" not in html.lower():
                logger.info("Got Error 15 page (this is NOT an error! it's intended)")
                if not js_future.done():
                    try:
                        await asyncio.wait_for(js_future, timeout=10)
                        self.tab.handlers.clear()
                        logger.info("JS check done. reloading")
                    except asyncio.TimeoutError:
                        await asyncio.sleep(10)
                        raise LoginException("Timeout on JS challenge")
                await self.tab.reload()
                new_html = await self.tab.get_content()
                if "log in" not in new_html.lower():
                    logger.debug(new_html)
                    proxy.rate_limited()
                    code_match = re.search(r";edet=(\d*)&", new_html)
                    if code_match and code_match.group(1):
                        code = code_match.group(1)
                    else:
                        code = "unknown"
                    raise LoginException(f"Didn't pass JS check. Code: {code}")

            logger.info("Getting cookies from browser")
            value: str | None = None
            all_cookies: dict[str, str] = {}
            attempts = 10
            while not value and attempts > 0:
                attempts -= 1
                cookies = await self.browser.cookies.get_all()
                for cookie in cookies:
                    if cookie.name == "reese84":
                        logger.info("Got a cookie")
                        value = cookie.value
                        continue

                if not value:
                    await self.tab.wait(0.3)
                else:
                    all_cookies = {c.name: c.value for c in cookies}
                    self.last_cookies = cookies

            if not value:
                raise LoginException("Didn't find reese cookie in browser")

            self.cookie_future = await self.ext_comm.add_listener(FINISH_COOKIE_PURGE)
            new_tab = await self.tab.get(new_tab=True)
            await self.tab.close()
            self.tab = new_tab

            self.consecutive_failures = 0
            return ReeseCookie(all_cookies, proxy.full_url.geturl())
        except LoginException as e:
            logger.error(f"{str(e)} while getting cookie")
            self.consecutive_failures += 1
            await asyncio.sleep(1)
            return None
        except ProxyException as e:
            logger.error(f"{str(e)} while getting cookie")
            return None
        except Exception as e:
            logger.exception("Exception in browser", e)

        logger.error("Error while getting cookie from browser, it will be restarted next time")
        self.consecutive_failures += 1
        self.browser.stop()
        self.tab = None
        self.browser = None
        return None

    async def get_join_tokens(self) -> CionResponse | None:
        try:
            await self.start_browser()
        except Exception:
            return None

        try:
            js_future = asyncio.get_running_loop().create_future()
            timestamp = int(time.time())

            async def js_check_handler(event: nodriver.cdp.network.ResponseReceived):
                url = event.response.url
                if not url.startswith(JOIN_URL):
                    return
                if not url.endswith("?d=join.pokemon.com"):
                    return
                if not js_future.done():
                    js_future.set_result(True)

            await self._open_tab()
            # await asyncio.sleep(300000000)

            proxy_future = await self.ext_comm.add_listener(FINISH_PROXY)
            await self.proxies.change_proxy()

            try:
                await asyncio.wait_for(proxy_future, 2)
            except asyncio.TimeoutError:
                logger.info("Didn't get confirmation that proxy changed, continuing anyway")

            if self.cookie_future:
                try:
                    await asyncio.wait_for(self.cookie_future, 2)
                except asyncio.TimeoutError:
                    logger.info("Didn't get confirmation that cookies were cleared, continuing anyway")

            if IS_DEBUG:
                await self._log_ip()

            proxy = self.proxies.current_proxy
            self.tab.add_handler(nodriver.cdp.network.ResponseReceived, js_check_handler)
            logger.info("Opening Join page")
            await self.tab.get(url=JOIN_URL + "login")

            html = await self.tab.get_content()
            try:
                await asyncio.wait_for(js_future, timeout=60)
                self.tab.handlers.clear()
                logger.info("JS check done. reloading")
            except asyncio.TimeoutError:
                raise LoginException("Timeout on JS challenge")

            await self.tab.reload()
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

            recaptcha_tokens = r.value

            # await asyncio.sleep(30000)

            logger.info("Getting cookies from browser")
            value: str | None = None
            all_cookies: dict[str, str] = {}
            attempts = 10
            while not value and attempts > 0:
                attempts -= 1
                cookies = await self.browser.cookies.get_all()
                for cookie in cookies:
                    if cookie.name == "reese84":
                        logger.info("Got a cookie")
                        value = cookie.value
                        continue

                if not value:
                    await self.tab.wait(0.3)
                else:
                    all_cookies = {c.name: c.value for c in cookies}
                    self.last_cookies = cookies

            if not value:
                raise LoginException("Didn't find reese cookie in browser")

            self.cookie_future = await self.ext_comm.add_listener(FINISH_COOKIE_PURGE)
            new_tab = await self.tab.get(new_tab=True)
            await self.tab.close()
            self.tab = new_tab
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
            # self.consecutive_failures += 1
            # await asyncio.sleep(1)
            # return None
        except Exception as e:
            logger.exception("Exception during browser", e)

        logger.error("Error while getting cookie from browser, it will be restarted next time")
        self.browser.stop()
        self.tab = None
        self.browser = None
        return None

    async def set_setting(self, shadow_roots: list[str], element_id: str, new_value: str, uri: str | None = None):
        if uri is not None:
            self.tab = await self.browser.get(uri)
            await self.tab.wait_for("html")

        inject_js = "const element=document."
        inject_js += ".".join(f"querySelector('{s}').shadowRoot" for s in shadow_roots)
        inject_js += f".getElementById('{element_id}');"
        inject_js += f"element.value='{new_value}';"
        inject_js += "element.dispatchEvent(new Event('change'));"

        print(inject_js)
        try:
            await self.tab.evaluate(inject_js)
        except Exception as e:
            logger.warning(f"{str(e)} while changing setting {element_id}, ignoring")

    async def _open_tab(self):
        logger.info("Opening tab")
        if not self.tab:
            self.tab = await self.browser.get("chrome://extensions" if IS_DEBUG else "about:blank")

    async def _log_ip(self):
        await self.tab.get(url="https://api.ipify.org/")
        ip_html = await self.tab.get_content()
        ip = re.search(r"\d*\.\d*\.\d*\.\d*", ip_html)
        if ip and ip.group(0):
            logger.info(f"Browser IP check: {ip.group(0)}")
        else:
            logger.info("Browser IP check failed")

    def __find_chrome_executable(self, return_all=False):
        candidates = []
        if sys.platform.startswith(("darwin", "cygwin", "linux", "linux2")):
            for item in os.environ.get("PATH").split(os.pathsep):
                for subitem in (
                    "brave",
                    "google-chrome",
                    "chromium",
                    "chromium-browser",
                    "chrome",
                    "google-chrome-stable",
                ):
                    candidates.append(os.sep.join((item, subitem)))
            if "darwin" in sys.platform:
                candidates += [
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "/Applications/Chromium.app/Contents/MacOS/Chromium",
                ]

        else:
            for item in map(
                os.environ.get,
                ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA", "PROGRAMW6432"),
            ):
                if item is not None:
                    for subitem in (
                        "BraveSoftware/Brave-Browser/Application",
                        "Google/Chrome/Application",
                        "Google/Chrome Beta/Application",
                        "Google/Chrome Canary/Application",
                        # "Chromium/Application"
                    ):
                        candidates.append(os.sep.join((item, subitem, "brave.exe")))
                        candidates.append(os.sep.join((item, subitem, "chrome.exe")))
        rv = []
        for candidate in candidates:
            if os.path.exists(candidate) and os.access(candidate, os.X_OK):
                logger.debug("%s is a valid candidate... " % candidate)
                rv.append(candidate)

        winner = None

        if return_all and rv:
            return rv

        winner = next((r for r in rv if "brave" in r.lower()), None)

        if not winner:
            if rv and len(rv) > 1:
                # assuming the shortest path wins
                winner = min(rv, key=lambda x: len(x))

            elif len(rv) == 1:
                winner = rv[0]

        if winner:
            return os.path.normpath(winner)

        raise FileNotFoundError(
            "could not find a valid chrome browser binary. please make sure chrome is installed."
            "or use the keyword argument 'browser_executable_path=/path/to/your/browser' "
        )
