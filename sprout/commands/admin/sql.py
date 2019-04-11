import json
import sqlite3


async def run(bot, ctx, cmd, arg) -> None:
    try:
        with sqlite3.connect(bot.config.db) as connect:
            c = connect.cursor()
            c.execute(arg)
            r = c.fetchall()
            message = json.dumps(r, ensure_ascii=False)
    except sqlite3.Error as err:
        message = json.dumps(err, ensure_ascii=False)

    await bot.send(ctx, message)
