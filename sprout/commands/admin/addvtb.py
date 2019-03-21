import sqlite3


async def run(bot, ctx, cmd, arg) -> None:
    arg_arr = arg.split(',')
    with sqlite3.connect(bot.config.db) as connect:
        c = connect.cursor()
        c.execute('INSERT INTO vtb values(?,?,?,?)', arg_arr)

    await bot.send(ctx, '添加成功，你离DD又近了一步')
