import logging
from typing import Optional, Any

from aiocqhttp import CQHttp

from sprout.sched import Scheduler
from .event_handler import *
from .log import logger

scheduler = Scheduler()


class Sprout(CQHttp):
    def __init__(self, config) -> None:
        super().__init__()
        self.config = config

        if self.config.DEBUG:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

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


_bot: Optional[Sprout] = None


def get_bot() -> Sprout:
    if _bot is None:
        raise ValueError('Sprout instance has not been initialized')
    return _bot


def run(host: Optional[str] = None, port: Optional[int] = None, *args, **kwargs):
    get_bot().run(host=host, port=port, *args, **kwargs)


def init(config_object: Optional[Any] = None) -> None:
    global _bot
    _bot = Sprout(config_object)

    _bot.server_app.before_serving(_start_scheduler)


def _start_scheduler():
    if scheduler and not scheduler.running:
        scheduler.configure(_bot.config.APSCHEDULER_CONFIG)
        scheduler.start()


__all__ = [
    'Sprout', 'scheduler', 'init', 'get_bot', 'run'
]
