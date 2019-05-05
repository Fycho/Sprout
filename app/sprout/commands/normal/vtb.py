import json
import re

import aiohttp
from sqlalchemy import and_

from database import session
from sprout.helpers import is_number
from sprout.models import UserSubscribe, Vtb

room_url = 'https://live.bilibili.com/'
api_url = 'https://api.live.bilibili.com/room/v1/Room/get_info?id='


async def handle_list_message(bot, ctx):
    items = get_vtb_list()
    message = '【Virtual Youtuber bilibili 开播提醒】可供订阅的Virtual Youtuber 列表：'
    for row in items:
        message += f'\n【{row.vid}】{row.name_zh}'

    return await bot.send(ctx, message=message)


async def query_my_subscription(bot, ctx):
    user_id = ctx['user_id']
    query = session.query(UserSubscribe, Vtb.vid, Vtb.name_zh) \
        .filter(UserSubscribe.user_id == user_id) \
        .join(Vtb, UserSubscribe.vid == Vtb.vid) \
        .order_by(UserSubscribe.vid)
    items = query.all()

    if len(items) == 0:
        message = '你没有订阅Virtual Youtuber'
    else:
        message = '你订阅的Virtual Youtuber：'
        for row in items:
            message += f'\n【{row.vid}】{row.name_zh}'

    return await bot.send(ctx, message=message, at_sender=True)


async def handle_subscribe(bot, ctx, sub_arg):
    session.flush()
    if len(sub_arg) == 0:
        return await bot.send(ctx, '缺少参数')

    if is_number(sub_arg[0]) == False and sub_arg[0] != 'all':
        return await bot.send(ctx, message='参数只能是编号或者all', at_sender=True)

    vid_list = list(map(lambda x: x[0], session.query(Vtb.vid).all()))
    user_id = ctx['user_id']
    try:
        if sub_arg[0] == 'all':
            session.bulk_save_objects([
                UserSubscribe(user_id=user_id, vid=vid) for vid in vid_list
            ])

        else:
            if int(sub_arg[0]) not in vid_list:
                return await bot.send(ctx, message='你订阅了不存在的vtb', at_sender=True)

            model = UserSubscribe(user_id=user_id, vid=sub_arg[0])
            session.merge(model)

    except Exception:
        session.rollback()

    return await bot.send(ctx, message='成功订阅（如已订阅请忽略）', at_sender=True)


async def handle_unsubscribe(bot, ctx, sub_arg):
    if len(sub_arg) == 0:
        return await bot.send(ctx, '缺少参数')

    if is_number(sub_arg[0]) == False and sub_arg[0] != 'all':
        return await bot.send(ctx, message='参数只能是编号或者all', at_sender=True)

    user_id = ctx['user_id']

    try:
        if sub_arg[0] == 'all':
            session.query(UserSubscribe).filter(UserSubscribe.user_id == user_id).delete()

        else:
            if is_number(sub_arg[0]) == False:
                return await bot.send(ctx, message='参数只能是编号或者all', at_sender=True)

            session.query(UserSubscribe).filter(
                and_(UserSubscribe.user_id == user_id, UserSubscribe.vid == sub_arg[0])).delete()

    except Exception:
        session.rollback()

    return await bot.send(ctx, message='成功取消订阅（如未订阅请忽略）', at_sender=True)


async def handle_query_status(bot, ctx):
    streaming_list = []
    vtb_list = get_vtb_list()
    for vtb in vtb_list:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url + vtb.room_b) as resp:
                resp_text = await resp.text()
                result = json.loads(resp_text)
                if result['data']['live_status'] == 1:
                    # 直播中
                    streaming_list.append(vtb)

    if len(streaming_list) < 1:
        message = '现在没有Virtual Youtuber在bilibili直播'
    else:
        message = '正在bilibili直播的Virtual Youtuber：'
        for vtb in streaming_list:
            message += f'\n - {vtb.name_zh} <{room_url}{vtb.room_b}>'

    await bot.send(ctx, message=message)


async def run(bot, ctx, cmd, arg) -> None:
    if not arg:
        return await handle_index(bot, ctx)

    args = re.split('\s+', arg)
    sub_cmd = args[0]
    sub_arg = args[1:]

    if sub_cmd == 'mylist' or sub_cmd == 'mine':
        return await query_my_subscription(bot, ctx)
    elif sub_cmd == 'list':
        return await handle_list_message(bot, ctx)
    elif sub_cmd == 'subscribe' or sub_cmd == 'sub':
        return await handle_subscribe(bot, ctx, sub_arg)
    elif sub_cmd == 'unsubscribe' or sub_cmd == 'unsub':
        return await handle_unsubscribe(bot, ctx, sub_arg)
    elif sub_cmd == 'now':
        return await handle_query_status(bot, ctx)
    elif sub_cmd == 'help':
        return await handle_help(bot, ctx)
    else:
        return


async def handle_index(bot, ctx):
    # 后期整合进/help, 嗯，先这样吧
    message = '欢迎使用Virtual Youtuber Helper，该指令提供了查看当前正在bilibili直播的虚拟主播以及订阅喜欢的虚拟主播的功能，被订阅的主播在直播时会给你发通知\n详情请/vtb help'
    return await bot.send(ctx, message)


async def handle_help(bot, ctx):
    # 后期整合进/help, 嗯，先这样吧
    message = '''/vtb 指令帮助：
/vtb list - 查看支持的虚拟主播列表
/vtb now - 查看现在有哪些虚拟主播在bilibili直播
/vtb mine - 查看已订阅主播
/vtb sub [编号] - 订阅该主播
/vtb unsub [编号] - 取消订阅该主播
/vtb sub all - 一键订阅全部
/vtb unsub all - 一键取消所有订阅
/vtb help - 本帮助'''
    return await bot.send(ctx, message)


def get_vtb_list(page=1, size=50):
    query = session.query(Vtb).order_by(Vtb.vid).limit(size).offset((page - 1) * size)
    return query.all()
