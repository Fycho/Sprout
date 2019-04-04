import sqlite3


async def run(bot, ctx, cmd, arg) -> None:
    with sqlite3.connect(bot.config.db) as connect:
        c = connect.cursor()
        c.execute('DELETE FROM vtb WHERE vid=' + arg)
        c.execute('DELETE FROM user_subscribe WHERE vid=' + arg)

    await bot.send(ctx, '已删除该VTB，RIP')
