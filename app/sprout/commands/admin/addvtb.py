import sqlite3


async def run(bot, ctx, cmd, arg) -> None:
    arg_arr = arg.split(',')
    with sqlite3.connect(bot.config.db) as connect:
        c = connect.cursor()
        sql = 'INSERT INTO vtb (name_zh, room_b) VALUES (:name, :room)'
        c.execute(sql, {
            'name': arg_arr[0],
            'room': arg_arr[1]
        })

    await bot.send(ctx, '添加成功，你离DD又近了一步')
