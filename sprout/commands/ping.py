async def run(bot, ctx, cmd, arg) -> None:
    if not arg:
        await bot.send(ctx, 'pong')
    else:
        await bot.send(ctx, f'pong {arg}')