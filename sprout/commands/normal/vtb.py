import json
import re
import sqlite3

import aiohttp

from sprout.helpers import is_number


def get_vtb_list(bot):
    with sqlite3.connect(bot.config.db) as connect:
        connect.row_factory = sqlite3.Row
        c = connect.cursor()

        c.execute('SELECT * FROM vtb ORDER BY vid ASC')
        rows = c.fetchall()
        return list(map(lambda row: dict(zip([d[0] for d in c.description], row)), rows))


async def handle_list_message(bot, ctx):
    items = get_vtb_list(bot)

    message = '【Virtual Youtuber bilibili 开播提醒】可供订阅的Virtual Youtuber 列表：'
    for i in items:
        message += '\n【' + str(i['vid']) + '】' + i['name_zh']

    return await bot.send(ctx, message)


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


async def query_my_subscription(bot, ctx):
    user_id = ctx['user_id']
    with sqlite3.connect(bot.config.db) as connect:
        c = connect.cursor()
        c.execute(
            'SELECT us.user_id,us.vid,v.name_zh FROM user_subscribe as us LEFT JOIN vtb as v ON v.vid=us.vid WHERE us.user_id=' + str(
                user_id)
        )
        rows = c.fetchall()
        items = list(map(lambda row: dict(zip([d[0] for d in c.description], row)), rows))

    if len(items) == 0:
        message = '你没有订阅Virtual Youtuber'
    else:
        message = '你订阅的Virtual Youtuber：'
        for i in items:
            message += '\n【' + str(i['vid']) + '】' + i['name_zh']

    return await bot.send(ctx, message=message, at_sender=True)


async def handle_subscribe(bot, ctx, sub_arg):
    if len(sub_arg) == 0:
        return await bot.send(ctx, '缺少参数')

    user_id = ctx['user_id']
    with sqlite3.connect(bot.config.db) as connect:
        connect.row_factory = sqlite3.Row
        c = connect.cursor()
        items = get_vtb_list(bot)
        vid_list = list(map(lambda x: x['vid'], items))
        if sub_arg[0] == 'all':
            data = list(map(lambda x: (user_id, x['vid']), items))
            c.executemany('INSERT OR IGNORE INTO user_subscribe VALUES (?,?)', data)
        else:
            if is_number(sub_arg[0]) == False:
                return await bot.send(ctx, message='参数只能是编号或者all', at_sender=True)
            if int(sub_arg[0]) not in vid_list:
                return await bot.send(ctx, message='你订阅了不存在的vtb', at_sender=True)
            c.execute('INSERT OR IGNORE INTO user_subscribe VALUES (?,?)', [user_id, sub_arg[0]])

    return await bot.send(ctx, message='成功订阅（如已订阅请忽略）', at_sender=True)


async def handle_unsubscribe(bot, ctx, sub_arg):
    if len(sub_arg) == 0:
        return await bot.send(ctx, '缺少参数')

    with sqlite3.connect(bot.config.db) as connect:
        c = connect.cursor()
        if sub_arg[0] == 'all':
            c.execute('DELETE FROM user_subscribe WHERE user_id=' + str(ctx['user_id']))
        else:
            if is_number(sub_arg[0]) == False:
                return await bot.send(ctx, message='参数只能是编号或者all', at_sender=True)
            c.execute('DELETE FROM user_subscribe WHERE user_id=' + str(ctx['user_id']) + ' AND vid=' + sub_arg[0])

    return await bot.send(ctx, message='成功取消订阅（如未订阅请忽略）', at_sender=True)


async def handle_query_status(bot, ctx):
    streaming_list = []
    roundplaying_list = []
    vtb_list = get_vtb_list(bot)
    for vtb in vtb_list:
        async with aiohttp.ClientSession() as session:
            async with session.get(bot.config.api_url + vtb['room_b']) as resp:
                resp_text = await resp.text()
                result = json.loads(resp_text)
                if result['data']['live_status'] == 1:
                    # 直播中
                    streaming_list.append((vtb['room_b'], vtb['name_zh']))
                elif result['data']['live_status'] == 2:
                    # 轮播中
                    roundplaying_list.append((vtb['room_b'], vtb['name_zh']))

    if len(streaming_list) < 1:
        message = '现在没有Virtural Youtuber在bilibili直播'
    else:
        message = '正在bilibili直播的Virtural Youtuber：'
        for v in streaming_list:
            message += '\n - ' + v[1] + ' <' + bot.config.room_url + v[0] + '>'

    # message += '\n正在bilibili轮播的Virtural Youtuber：'
    # for v in roundplaying_list:
    #     message += '\n - ' + v[1] + ' <' + bot.config.room_url + v[0] + '>'
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
