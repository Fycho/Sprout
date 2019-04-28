import json

from database import engine
from sprout.log import logger


async def run(bot, ctx, cmd, arg) -> None:
    try:
        with engine.connect() as conn:
            logger.info(f'executing raw sql: "{arg}" by {ctx["user_id"]}')
            res = conn.execute(arg).fetchall()
            message = json.dumps([dict(r) for r in res], ensure_ascii=False)
            await bot.send(ctx, message=message)

    except Exception as error:
        logger.error(error)
