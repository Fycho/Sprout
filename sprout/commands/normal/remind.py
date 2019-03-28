import asyncio
import datetime
import re


async def run(bot, ctx, cmd, arg) -> None:
    if not arg:
        return await bot.send(ctx, message='缺少参数', at_sender=True)

    matched = re.match(r'^(\w+)\s+(.*?)$', arg)
    if matched:
        time = matched.group(1)
        msg = matched.group(2)
    else:
        return await bot.send(ctx, message='缺少参数或者参数不合法', at_sender=True)

    seconds = parse_duration(time)
    if seconds == False:
        seconds = parse_time(time)

    if seconds == False:
        return await bot.send(ctx, message='缺少参数或者参数不合法', at_sender=True)

    notice_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    formatted = notice_time.strftime('%Y年%m月%d日 %H:%M:%S')
    delayed_task = asyncio.create_task(delay(bot, ctx, seconds, msg))
    reply_task = bot.send(ctx, message=f'收到，会在{formatted}s提醒你：{msg}', at_sender=True)
    asyncio.gather(delayed_task, reply_task)


async def delay(bot, ctx, seconds, msg):
    await asyncio.sleep(seconds)
    await bot.send(ctx, message=msg, at_sender=True)


# 将形如2h40m30s|4h60s|5h40m|10m20这样的时间字符串解析成秒数
def parse_duration(str) -> int:
    matched = re.match(r'^(\d+h)?(\d+m)?(\d+s?)?$', str, re.I)
    if not matched:
        return False

    results = []
    for i in range(1, 4):
        results.append(matched.group(i))
    factor = [3600, 60, 1]
    total_second = 0
    for i, val in enumerate(factor):
        if not results[i]:
            continue
        sub_match = re.match(r'(\d+)', results[i], re.I)
        num = sub_match.group(1)
        total_second += int(num) * val

    return total_second


# 将形如15:30:00|15:30这样的时刻字符串解析成秒数（只支持下一个时间点）
def parse_time(str) -> int:
    matched = re.match(r'^(\d+):(\d+):?(\d+)?$', str, re.I)
    if not matched:
        return False

    h = matched.group(1)
    m = matched.group(2)
    s = matched.group(3)

    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')

    if s:
        d2 = datetime.datetime.strptime(f'{date} {h}:{m}:{s}', '%Y-%m-%d %H:%M:%S')
    else:
        d2 = datetime.datetime.strptime(f'{date} {h}:{m}:00', '%Y-%m-%d %H:%M:%S')

    delta = d2 - now
    return delta.seconds

