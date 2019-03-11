import random


async def run(bot, ctx, cmd, arg) -> None:
    point = str(random.randint(0, 100))

    if ctx['message'].endswith('概率'):
        point += '%'

    point = random.randint(0, 100)
    await bot.send(ctx, message=f'你摇到了点数：{point}', at_sender=True)
