import asyncio
import re

from sprout.helpers import is_number


async def run(bot, ctx, cmd, arg) -> None:
    if not arg:
        return await bot.send(ctx, message='缺少参数')

    matched = re.match(r'^(\w+)\s+(.*?)$', arg)
    if matched:
        time = matched.group(1)
        msg = matched.group(2)
    else:
        return await bot.send(ctx, message='缺少参数或者参数不合法')

    if is_number(time) == False:
        return await bot.send(ctx, message='参数#1只能为数字')

    time = int(time)

    delayed_task = asyncio.create_task(delay(bot, ctx, time, msg))
    reply_task = bot.send(ctx, message=f'收到，会在{time}秒后提醒你：{msg}', at_sender=True)
    asyncio.gather(delayed_task, reply_task)


async def delay(bot, ctx, time, msg):
    await asyncio.sleep(time)
    await bot.send(ctx, message=msg, at_sender=True)
