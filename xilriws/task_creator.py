from __future__ import annotations
import asyncio
from typing import Coroutine, Any, TypeVar, Generic


T = TypeVar("T")


class AwaitableSet(Generic[T]):
    def __init__(self):
        self.set: set[T] = set()
        self.cond = asyncio.Condition()

    def __len__(self):
        return len(self.set)

    def __bool__(self):
        return bool(len(self))

    async def add(self, element: T) -> None:
        async with self.cond:
            self.set.add(element)
            self.cond.notify_all()

    async def remove(self, element: T) -> None:
        if element not in self.set:
            return

        async with self.cond:
            self.set.remove(element)
            self.cond.notify_all()

    async def wait_until_shorter_than(self, threshold: int) -> None:
        async with self.cond:
            while len(self) >= threshold:
                await self.cond.wait()


class TaskCreator:
    def __init__(self, limit: int | None = None):
        self.coro_set = AwaitableSet()
        self.tasks: set[asyncio.Task] = set()
        self.limit = limit

    async def run_coro(self, coro: Coroutine[Any, Any, Any]) -> None:
        if self.limit:
            await self.coro_set.wait_until_shorter_than(self.limit)

        await self.coro_set.add(coro)
        await coro
        await self.coro_set.remove(coro)

    def create_task(self, coro: Coroutine[Any, Any, Any], loop: asyncio.AbstractEventLoop | None = None):
        internal_coro = self.run_coro(coro)

        if loop is None:
            task = asyncio.create_task(internal_coro)
        else:
            task = loop.create_task(internal_coro)

        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)


task_creator = TaskCreator()
