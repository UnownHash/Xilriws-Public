from __future__ import annotations
import nodriver
from .ptc import ACCESS_URL, LoginException
from loguru import logger
import asyncio

logger = logger.bind(name="Browser")
HEADLESS = True


class Browser:
    browser: nodriver.Browser | None = None
    tab: nodriver.Tab | None = None

    def __init__(self, extension_paths: list[str]):
        self.extension_paths: list[str] = extension_paths

    async def get_reese_cookie(self) -> str | None:
        logger.info("Browser starting")
        try:
            if not self.browser:
                config = nodriver.Config(headless=HEADLESS)
                for path in self.extension_paths:
                    config.add_extension(path)
                self.browser = await nodriver.start(config)
                logger.info(
                    f"Starting browser: `{self.browser.config.browser_executable_path} "
                    f"{' '.join(self.browser.config())}"
                    "`"
                )
        except Exception as e:
            logger.error(str(e))
            logger.error(
                f"Error while starting the browser. Please confirm you can start it manually by running "
                f"`{self.browser.config.browser_executable_path}`"
            )
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

            logger.info("Opening tab")
            if not self.tab:
                self.tab = await self.browser.get()
            self.tab.add_handler(nodriver.cdp.network.ResponseReceived, js_check_handler)
            logger.info("Opening PTC")
            await self.tab.get(url=ACCESS_URL + "login")

            html = await self.tab.get_content()
            if "log in" not in html:
                logger.info("Got Error 15 page (this is NOT an error! it's intended)")
                if not js_future.done():
                    try:
                        await asyncio.wait_for(js_future, timeout=10)
                        self.tab.handlers.clear()
                        logger.info("JS check done. reloading")
                    except asyncio.TimeoutError:
                        raise LoginException("Timeout on JS challenge")
                await self.tab.reload()
                if "log in" not in await self.tab.get_content():
                    logger.error("Didn't pass JS check")
                    raise LoginException("Didn't pass JS check")

            logger.info("Getting cookies from browser")
            value: str | None = None
            cookies = await self.browser.cookies.get_all()
            for cookie in cookies:
                if cookie.name != "reese84":
                    continue
                logger.info("Got a cookie")
                value = cookie.value

            new_tab = await self.tab.get(new_tab=True)
            await self.tab.close()
            self.tab = new_tab

            if not value:
                raise LoginException("Didn't find reese cookie in browser")
            return value
        except LoginException as e:
            logger.error(f"{str(e)} while getting cookie")
        except Exception as e:
            logger.exception("Exception during browser", e)

        logger.error("Error while getting cookie from browser, it will be restarted next time")
        self.browser.stop()
        self.tab = None
        self.browser = None
        return None
