async def run(bot, ctx, cmd, arg) -> None:
    message = '欢迎提交PR、issues、features为豆芽菜作出贡献：https://github.com/Fycho/Sprout'
    await bot.send(ctx, message=message)