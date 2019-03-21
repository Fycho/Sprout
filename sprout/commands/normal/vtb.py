import json
import re
import sqlite3

import aiohttp

import config
from sprout.helpers import is_number

vtb_list = (
    {'vid': 1, 'name_zh': 'AIchannel', 'room_b': '1485080'},
    {'vid': 2, 'name_zh': '白上吹雪', 'room_b': '11588230'},
    {'vid': 3, 'name_zh': '夏色祭', 'room_b': '13946381'},
    {'vid': 4, 'name_zh': '湊-阿库娅', 'room_b': '14917277'},
    {'vid': 5, 'name_zh': '赤井心', 'room_b': '14275133'},
    {'vid': 6, 'name_zh': '大神澪', 'room_b': '21133979'},
    {'vid': 7, 'name_zh': '紫咲诗音', 'room_b': '21132965'},
    {'vid': 8, 'name_zh': '神楽めあ', 'room_b': '12235923'},
    {'vid': 9, 'name_zh': '犬山玉姬', 'room_b': '4634167'},
    {'vid': 10, 'name_zh': '本间向日葵', 'room_b': '21302477'},
    {'vid': 11, 'name_zh': '神楽七奈', 'room_b': '21304638'},
    {'vid': 12, 'name_zh': '猫宫日向', 'room_b': '9286381'},
    {'vid': 13, 'name_zh': '輝夜月', 'room_b': '7602132'},
    {'vid': 14, 'name_zh': 'Overidea', 'room_b': '704808'},
    {'vid': 15, 'name_zh': 'Mirai Akari', 'room_b': '850447'},
    {'vid': 16, 'name_zh': '田中姬铃木雏', 'room_b': '10209381'},
    {'vid': 17, 'name_zh': '虚拟女友Yomemi', 'room_b': '10363055'},
    {'vid': 18, 'name_zh': '有栖マナ', 'room_b': '3822389'},
    {'vid': 19, 'name_zh': '静凛', 'room_b': '21302352'},
    {'vid': 20, 'name_zh': '椎名唯华', 'room_b': '21302469'},
    {'vid': 21, 'name_zh': '【游戏部企划】梦咲枫', 'room_b': '6586670'},
    {'vid': 22, 'name_zh': '白音小雪', 'room_b': '6241497'},
    {'vid': 23, 'name_zh': '绿仙', 'room_b': '2077989'},
)


async def handle_list_message(bot, ctx):
    with sqlite3.connect(bot.config.db) as connect:
        connect.row_factory = sqlite3.Row
        c = connect.cursor()

        c.execute('SELECT * FROM vtb')
        rows = c.fetchall()
        items = list(map(lambda row: dict(zip([d[0] for d in c.description], row)), rows))

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
    message = '指令帮助：\n/vtb list - 查看支持的虚拟主播列表\n/vtb now - 查看现在有哪些虚拟主播在bilibili直播\n/vtb mylist - 查看已订阅主播\n/vtb subscribe <编号> - 订阅该主播 \n/vtb unsubscribe <编号> - 取消订阅该主播 \n/vtb subscribe all - 一键订阅全部 \n/vtb unsubscribe all - 一键取消所有订阅\n/vtb help - 本帮助'
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
        if sub_arg[0] == 'all':
            data = list(map(lambda x: (user_id, x['vid']), vtb_list))
            c.executemany('INSERT OR IGNORE INTO user_subscribe VALUES (?,?)', data)
        else:
            if is_number(sub_arg[0]) == False:
                return await bot.send(ctx, message='参数只能是编号或者all', at_sender=True)
            c.execute('INSERT OR IGNORE INTO user_subscribe VALUES (?,?)', [user_id, sub_arg[0]])

    return await bot.send(ctx, message='成功订阅', at_sender=True)


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

    return await bot.send(ctx, message='成功取消订阅', at_sender=True)


async def handle_query_status(bot, ctx):
    streaming_list = []
    roundplaying_list = []
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

    if sub_cmd == 'mylist':
        return await query_my_subscription(bot, ctx)
    elif sub_cmd == 'list':
        return await handle_list_message(bot, ctx)
    elif sub_cmd == 'subscribe':
        return await handle_subscribe(bot, ctx, sub_arg)
    elif sub_cmd == 'unsubscribe':
        return await handle_unsubscribe(bot, ctx, sub_arg)
    elif sub_cmd == 'now':
        return await handle_query_status(bot, ctx)
    elif sub_cmd == 'help':
        return await handle_help(bot, ctx)
    else:
        return


def db_init():
    with sqlite3.connect(config.db) as connect:
        connect.row_factory = sqlite3.Row
        c = connect.cursor()

        connect.execute('''
            CREATE TABLE IF NOT EXISTS vtb(
                vid PRIMARY KEY,
                name_zh TEXT,
                room_b TEXT,
                live_status INT
            );
        ''')

        connect.execute('''
            CREATE TABLE IF NOT EXISTS user_subscribe(
                user_id TEXT,
                vid INT,
                primary key(user_id, vid)
            );
        ''')

        # init vtb list
        data = list(map(lambda vtb: (vtb['vid'], vtb['name_zh'], vtb['room_b'], 0), vtb_list))
        c.execute('DELETE FROM vtb')
        c.executemany('INSERT INTO vtb VALUES (?,?,?,?)', data)


if __name__ == '__main__':
    db_init()
