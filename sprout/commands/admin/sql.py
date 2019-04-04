import json
import sqlite3


async def run(bot, ctx, cmd, arg) -> None:
    with sqlite3.connect(bot.config.db) as connect:
        c = connect.cursor()
        r = c.execute(arg)

    await bot.send(ctx, json.dumps(r))
