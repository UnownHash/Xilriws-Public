from __future__ import annotations

from typing import Protocol

from litestar import Litestar


class BasicMode(Protocol):
    async def prepare(self) -> None:
        pass

    def get_litestar(self) -> Litestar:
        pass




