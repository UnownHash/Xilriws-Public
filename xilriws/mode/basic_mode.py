from __future__ import annotations
from typing import Protocol
from litestar import Litestar
from nodriver import Browser


class BasicMode(Protocol):
    def __init__(self, browser: Browser):
        pass

    async def prepare(self) -> None:
        pass

    def get_litestar(self) -> Litestar:
        pass




