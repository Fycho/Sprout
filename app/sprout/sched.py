try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except ImportError:
    AsyncIOScheduler = None

if AsyncIOScheduler:
    class Scheduler(AsyncIOScheduler):
        pass
else:
    Scheduler = None