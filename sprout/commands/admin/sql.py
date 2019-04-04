import json
import sqlite3


async def run(bot, ctx, cmd, arg) -> None:
    with sqlite3.connect(bot.config.db) as connect:
        c = connect.cursor()
        c.execute(arg)
        r = c.fetchall()

    await bot.send(ctx, json.dumps(r, ensure_ascii=False, encoding='utf-8'))
