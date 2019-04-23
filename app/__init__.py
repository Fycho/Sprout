import importlib
import logging
from typing import Any, Optional

from aiocqhttp import CQHttp

from app.games.omok_game import OmokGame
from app.sched import Scheduler
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

        self.omok_instance = OmokGame()

    def start_all_tasks(self):
        _run_vtb_notification(self)

    def stop_all_tasks(self):
        jobs = scheduler.get_jobs()
        for job in jobs:
            job.remove()


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
    _bot.server_app.after_serving(_bot.start_all_tasks)


def _start_scheduler():
    if scheduler and not scheduler.running:
        scheduler.configure(_bot.config.APSCHEDULER_CONFIG)
        scheduler.start()


def _run_vtb_notification(self):
    live_status_dict = dict()
    schedule_module = importlib.import_module('sprout.schedules.vtb_subscribe')
    scheduler.add_job(
        schedule_module.initialize,
        id='vtb_subscribe',
        kwargs={'bot': self, 'live_status_dict': live_status_dict},
        trigger='interval',
        replace_existing=True,
        minutes=1,
    )


__all__ = [
    'Sprout', 'scheduler', 'init', 'get_bot', 'run'
]
