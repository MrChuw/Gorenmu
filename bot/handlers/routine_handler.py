from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import janus
from twitchio.ext import routines

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class RoutineHandler:
    def __init__(self, bot: Gorenmu):
        self.bot = bot
        self.routine_queue = janus.Queue()
        self.running_tasks: dict[str, asyncio.Task] = {}
        if not self.bot.mock:
            self._loop_task = asyncio.create_task(self._routine_manager_loop())

    async def _routine_manager_loop(self):
        while True:
            name, coro = await self.routine_queue.async_q.get()
            coro: routines.Routine
            if name in self.running_tasks:
                await self.stop_routine(name)
            task = coro.start()
            self.running_tasks[name] = task
            self.routine_queue.async_q.task_done()

    async def add_routine(self, name: str, coro):
        await self.routine_queue.async_q.put((name, coro))

    async def stop_routine(self, name: str):
        task = self.running_tasks.get(name)
        if task and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                self.bot.log.info(f"Routine: {name}, cancelled.")
            finally:
                self.running_tasks.pop(name, None)  # NOQA

    async def stop_routines_all(self):
        names = list(self.running_tasks.keys())
        for name in names:
            await self.stop_routine(name)

        if hasattr(self, "_loop_task"):
            self._loop_task.cancel()
