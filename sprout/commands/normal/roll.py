import random


async def run(bot, ctx, cmd, arg) -> None:
    point = str(random.randint(0, 100))

    if ctx['message'].endswith('概率'):
        message = f'你摇到了概率：{point}%'

    else:
        message = f'你摇到了点数：{point}'

    await bot.send(ctx, message=message, at_sender=True)
