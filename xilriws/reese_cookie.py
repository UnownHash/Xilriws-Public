from __future__ import annotations
import time
from .browser import Browser
from loguru import logger
import asyncio

from .constants import EXPIRATION, MAX_USES, COOKIE_STORAGE
from .task_creator import task_creator, AwaitableSet

logger = logger.bind(name="Cookie")


class ReeseCookie:
    def __init__(self, value: str):
        self.value: str = value
        self.expiration: float = time.time() + EXPIRATION
        self.uses: int = 0

    def is_good(self) -> bool:
        return time.time() < self.expiration and self.uses < MAX_USES

    def use(self) -> None:
        self.uses += 1


class CookieMonster:
    fill_event: asyncio.Event

    def __init__(self, browser: Browser):
        self.browser: Browser = browser
        self.cookies: AwaitableSet[ReeseCookie] = AwaitableSet()

    async def prepare(self):
        self.fill_event = asyncio.Event()
        task_creator.create_task(self.fill_task())
        self.fill_event.set()

    async def get_reese_cookie(self) -> ReeseCookie:
        logger.info("Getting a reese cookie from storage")
        cookie: ReeseCookie | None = None

        while not cookie:
            possible_cookie = await self.get_next_cookie()
            if not possible_cookie.is_good():
                await self.cookies.remove(possible_cookie)
                self.fill_event.set()
            else:
                cookie = possible_cookie

        cookie.use()
        logger.info("Cookie selected")

        return cookie

    async def remove_cookie(self, cookie: ReeseCookie) -> None:
        await self.cookies.remove(cookie)
        self.fill_event.set()

    async def fill_task(self):
        while True:
            await self.fill_event.wait()
            logger.info("Filling cookie storage in the background")

            try:
                while len(self.cookies) < COOKIE_STORAGE:
                    fresh_cookie = await self.__get_one_cookie()
                    logger.info(f"Cookie storage at {len(self.cookies)}/{COOKIE_STORAGE}")

                    if len(self.cookies) < COOKIE_STORAGE and fresh_cookie:
                        await asyncio.sleep(1.1)
                        # the extension clears cookies 1s after closing the tab. TODO: update the extension
            except Exception as e:
                logger.exception("unahdnled excpetion while filling cookie storage, please report", e)

            self.fill_event.clear()

    async def get_next_cookie(self) -> ReeseCookie:
        async with self.cookies.cond:
            while not len(self.cookies):
                await self.cookies.cond.wait()

            next_cookie: ReeseCookie | None = None
            for potential_cookie in self.cookies.set:
                if next_cookie is None:
                    next_cookie = potential_cookie
                elif potential_cookie.expiration < next_cookie.expiration:
                    next_cookie = potential_cookie

            return next_cookie

    async def __get_one_cookie(self) -> ReeseCookie | None:
        logger.info("Opening browser to get a cookie")
        value = await self.browser.get_reese_cookie()

        if not value:
            return None

        cookie = ReeseCookie(value)
        await self.cookies.add(cookie)
        return cookie

