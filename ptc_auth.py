from __future__ import annotations

import asyncio
import logging
import re
import time

import httpx
import nodriver

logger = logging.getLogger("browser")
MAX_COOKIE_USES = 6


class LoginException(Exception):
    """generic login exception, don't log the traceback"""
    pass


class BadLoginException(LoginException):
    """don't retry logging in"""
    pass


class InvalidCredentials(BadLoginException):
    """Invalid account credentials"""
    pass


class PtcAuth:
    ACCESS_URL = "https://access.pokemon.com/"
    reese_cookie: str | None = None
    reese_expiration: int = 0
    reese_uses: int = 0
    browser_lock: asyncio.Lock
    browser_event: asyncio.Event
    extension_paths: list[str]

    browser: nodriver.Browser | None = None
    tab: nodriver.Tab | None = None

    async def prepare(self):
        self.browser_lock = asyncio.Lock()
        self.browser_event = asyncio.Event()

    async def auth(self, username: str, password: str, full_url: str, proxy: str | None = None) -> str:
        logger.info(f"Requested auth for {username}")

        if not self.cookie_is_ok():
            self.browser_event.clear()

        async with self.browser_lock:
            if not self.browser_event.is_set():
                logger.info("reese cookie expired, getting a new one")
                try:
                    resp = await self.browser_auth(username, password, full_url)
                except BadLoginException as e:
                    self.browser_event.set()
                    raise e
                except Exception as e:
                    logger.warning(f"Browser login failed ({str(e)}). trying again once")
                    resp = await self.browser_auth(username, password, full_url)

                self.browser_event.set()
                return resp
        return await self.serving_auth_the_old_fashioned_way(username, password, full_url=full_url, proxy=proxy)

    def cookie_is_ok(self) -> bool:
        return self.reese_cookie and time.time() < self.reese_expiration and self.reese_uses < MAX_COOKIE_USES

    async def browser_auth(self, username: str, password: str, full_url: str) -> str:
        logger.info("BROWSER: starting")
        try:
            if not self.browser:
                config = nodriver.Config(headless=True)
                for path in self.extension_paths:
                    config.add_extension(path)
                self.browser = await nodriver.start(config)
        except Exception as e:
            logger.error(f"got exception {str(e)} while starting browser")
            raise e

        try:
            js_future = asyncio.get_running_loop().create_future()

            async def js_check_handler(event: nodriver.cdp.network.ResponseReceived):
                url = event.response.url
                if not url.startswith("https://access.pokemon.com/"):
                    return
                if not url.endswith("?d=access.pokemon.com"):
                    return
                if not js_future.done():
                    js_future.set_result(True)

            logger.info("BROWSER: opening tab")
            if not self.tab:
                self.tab = await self.browser.get()
            self.tab.add_handler(nodriver.cdp.network.ResponseReceived, js_check_handler)
            logger.info("BROWSER: opening PTC")
            await self.tab.get(url=full_url)

            html = await self.tab.get_content()
            if "Log in" not in html:
                logger.info("BROWSER: Got Error 15 page (this NOT an error! it's intended)")
                if not js_future.done():
                    try:
                        await asyncio.wait_for(js_future, timeout=10)
                        self.tab.handlers.clear()
                        logger.info("BROWSER: JS check done. reloading")
                    except asyncio.TimeoutError:
                        raise LoginException("Timeout on JS challenge")
                await self.tab.reload()
                if "Log in" not in await self.tab.get_content():
                    logger.error("BROWSER: Did NOT pass JS check. This is not good")
                    raise LoginException("Didn't pass JS check")

            logger.info("BROWSER: getting cookies")
            cookies = await self.browser.cookies.get_all()
            for cookie in cookies:
                if cookie.name != "reese84":
                    continue
                logger.info("BROWSER: setting reese84 cookie")
                self.reese_cookie = cookie.value
                # self.reese_expiration = int(cookie.expires)
                self.reese_expiration = int(time.time()) + 15 * 60
                self.reese_uses = 0

            accept_input = await self.tab.wait_for("input#accept")
            logger.info("BROWSER: got login page")

            js_email = f'document.querySelector("input#email").value="{username}"'
            parsed_password = password.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$")
            js_pass = f'document.querySelector("input#password").value="{parsed_password}"'

            await self.tab.evaluate(js_email + ";" + js_pass)
            logger.info("BROWSER: filled out login form")

            pokemongo_url_future = asyncio.get_running_loop().create_future()

            async def send_handler(event: nodriver.cdp.network.RequestWillBeSent):
                url = event.request.url
                if url.startswith("pokemongo://"):
                    pokemongo_url_future.set_result(url)

            self.tab.add_handler(nodriver.cdp.network.RequestWillBeSent, send_handler)

            await accept_input.click()
            logger.info("BROWSER: submitted login form")

            await self.tab.wait_for("html")
            await self.tab.update_target()
            logger.info("BROWSER: finished login")

            if "/consent" in self.tab.target.url:
                logger.info("BROWSER: got consent screen")
                consent_accept = await self.tab.wait_for("input#accept")
                if not consent_accept:
                    raise LoginException("no consent button")
                await consent_accept.click()
                logger.info("BROWSER: gave consent")
            elif self.tab.target.url.endswith("/login"):
                content = await self.tab.get_content()
                self.check_error_on_login_page(content)

            # it might be possible to get the pokemongo:// uri at this point already,
            # there's some 30x requests that contain them in their body

            try:
                logger.info("BROWSER: waiting for pokemongo uri")
                pokemongo_url = await asyncio.wait_for(pokemongo_url_future, timeout=15)
                logger.info("BROWSER: got pokemongo uri")
            except asyncio.TimeoutError:
                await self.tab.update_target()
                logger.info(
                    f"Please send this to Malte on Discord: {self.tab.target.url}\n{await self.tab.get_content()}"
                )
                raise LoginException("Timeout while waiting for pokemongo:// uri")

            self.tab.handlers.clear()

            new_tab = await self.tab.get(new_tab=True)
            await self.tab.close()
            self.tab = new_tab

            login_code = self.__extract_login_code(pokemongo_url)
            if not login_code:
                raise LoginException("No login code found")
        except InvalidCredentials as e:
            raise e
        except Exception as e:
            logger.error(f"Got {str(e)} during browser login - killing chrome")
            self.browser.stop()
            self.tab = None
            self.browser = None
            raise e

        return login_code

    async def serving_auth_the_old_fashioned_way(
        self, username: str, password: str, full_url: str, proxy: str | None = None
    ) -> str:
        if not self.reese_cookie:
            raise LoginException("this error does not happen")

        self.reese_uses += 1

        proxies = None
        if proxy:
            proxies = {"http://": proxy, "https://": proxy}

        async with httpx.AsyncClient(
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-us",
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate, br",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 "
                "(KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1",
            },
            follow_redirects=True,
            verify=False,
            timeout=10,
            proxies=proxies,
            cookies={"reese84": self.reese_cookie},
        ) as client:
            logger.info("Calling PTC page 1/2")

            resp = await client.get(full_url)

            if resp.status_code == 403:
                self.reese_cookie = None
                logger.info("cookie expired. opening the browser")
                return await self.auth(username, password, full_url, proxy)  # bad

            if resp.status_code != 200:
                raise LoginException(f"OAUTH: {resp.status_code} but expected 200")

            csrf, challenge = self.__extract_csrf_and_challenge(resp.text)

            logger.info("Calling PTC page 2/2")

            login_resp = await client.post(
                self.ACCESS_URL + "login",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={"_csrf": csrf, "challenge": challenge, "email": username, "password": password},
            )

            if login_resp.status_code == 403:
                self.reese_cookie = None
                logger.info("cookie expired. opening the browser")
                return await self.auth(username, password, full_url, proxy)  # bad

            if login_resp.status_code != 200:
                raise LoginException(f"LOGIN: {login_resp.status_code} but expected 200")

            login_code = self.__extract_login_code(login_resp.text)

            if not login_code:
                if "error-message" in login_resp.text:
                    self.check_error_on_login_page(login_resp.text)
                    logger.error(f"Please send this to Malte on Discord (error page after login)\n{login_resp.text}")
                    raise LoginException("Login failed, probably invalid credentials")

                logger.info("Need to give consent (+1 extra PTC page)")

                csrf_consent, challenge_consent = self.__extract_csrf_and_challenge(login_resp.text)
                resp_consent = await client.post(
                    self.ACCESS_URL + "consent",
                    data={"challenge": challenge_consent, "_csrf": csrf_consent, "allow_submit": "Allow"},
                )
                if resp_consent.status_code != 200:
                    raise LoginException(f"Consent: {resp_consent.status_code} but expected 200")
                login_code = self.__extract_login_code(resp_consent.text)
                if not login_code:
                    raise LoginException("No Login Code after consent, please check account")

            logger.info("Got login code")
            return login_code

    def check_error_on_login_page(self, content: str):
        if "Your username or password is incorrect." in content:
            logger.warning("BROWSER: Incorrect credentials")
            raise InvalidCredentials("Incorrect account credentials")
        elif "your account has been disabled for" in content:
            logger.error("BROWSER: Account is temporarily disabled")
            raise InvalidCredentials("Account temporarily disabled")

    def __extract_login_code(self, html) -> str | None:
        matches = re.search(r"pokemongo://state=(.*?)(?:,code=(.*?))?(?='|$)", html)

        if matches and len(matches.groups()) == 2:
            return matches.group(2)

    def __extract_csrf_and_challenge(self, html: str) -> tuple[str, str]:
        csrf_regex = re.compile(r'name="_csrf" value="(.*?)">')
        challenge_regex = re.compile(r'name="challenge" value="(.*?)">')

        csrf_matches = csrf_regex.search(html)
        challenge_matches = challenge_regex.search(html)

        if csrf_matches and challenge_matches:
            return csrf_matches.group(1), challenge_matches.group(1)

        raise LoginException("Couldn't find CSRF or challenge in Auth response")
