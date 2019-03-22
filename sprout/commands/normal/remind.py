import asyncio
import re


async def run(bot, ctx, cmd, arg) -> None:
    if not arg:
        return await bot.send(ctx, message='缺少参数')

    args = re.split('\s+', arg)

    if (len(args) < 2):
        return await bot.send(ctx, message='缺少参数')

    second = args[0]
    msg = args[1]

    delayed_task = asyncio.create_task(delay(bot, ctx, second, msg))
    reply_task = bot.send(ctx, message=f'收到，会在{second}秒后提醒你：{msg}', at_sender=True)
    asyncio.gather(delayed_task, reply_task)


async def delay(bot, ctx, second, msg):
    await asyncio.sleep(second)
    await bot.send(ctx, message=msg, at_sender=True)
