from aiocqhttp import CQHttp
from .event_handler import *
from typing import Optional
import importlib, threading


class Sprout(CQHttp):
    def __init__(self, config) -> None:
        super().__init__()

        self.config = config

        @self.on_message
        async def _(ctx):
            await handle_message(self, ctx)

        @self.on_notice
        async def _(ctx):
            await handle_notice(self, ctx)

        @self.on_request
        async def _(ctx):
            await handle_request(self, ctx)

        @self.on_meta_event
        async def _(ctx):
            await handle_meta_event(self, ctx)

    def run(self, host: Optional[str] = None, port: Optional[int] = None, *args, **kwargs):
        run_schedule_tasks(self)
        super().run(host=host, port=port, *args, **kwargs)


def run_schedule_tasks(bot):
    schedules = ['vtb_subscribe']
    for schedule in schedules:
        task = importlib.import_module(f'.schedules.{schedule}', __package__)
        t = threading.Thread(target=task.initialize, args=(bot,), name=schedule)
        t.setDaemon(True)
        t.start()
