import random


async def run(bot, ctx, cmd, arg) -> None:
    point = random.randint(0, 100)
    await bot.send(ctx, message=f'你摇到了点数：{point}', at_sender=True)
