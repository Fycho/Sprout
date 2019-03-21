import asyncio
import json
import sqlite3

import aiohttp

import config


# 获取需要查询的房间
def get_subscribed_rooms() -> list:
    with sqlite3.connect(config.db) as connect:
        c = connect.cursor()
        c.execute(
            'SELECT user_subscribe.vid,vtb.room_b,vtb.name_zh FROM user_subscribe LEFT JOIN vtb ON vtb.vid = user_subscribe.vid GROUP BY room_b')
        items = c.fetchall()

    return list(map(lambda i: {'vid': i[0], 'room_b': i[1], 'name_zh': i[2]}, items))


# 获取该房间的订阅者
def get_users_by_room(vid) -> list:
    with sqlite3.connect(config.db) as connect:
        c = connect.cursor()
        c.execute(
            'SELECT user_id FROM user_subscribe where vid=' + str(vid))
        items = c.fetchall()

    return list(map(lambda i: i[0], items))


async def initialize(bot):
    vtb_models = get_subscribed_rooms()
    live_status_dict = dict()
    tasks = list()
    for current_vtb in vtb_models:
        tasks.append(asyncio.create_task(handler(bot, current_vtb, live_status_dict)))

    asyncio.gather(*tasks)


async def handler(bot, current_vtb, live_status_dict):
    async with aiohttp.ClientSession() as session:
        url = config.api_url + current_vtb['room_b']
        async with session.get(url) as resp:
            resp_text = await resp.text()
            result = json.loads(resp_text)
            live_status = result['data']['live_status']
            print(current_vtb['room_b'] + ':' + str(live_status))
            if current_vtb['room_b'] in live_status_dict and live_status == 1 and current_vtb['room_b'] != 1:
                await push_message(current_vtb['vid'], bot)

            live_status_dict[current_vtb['room_b']] = result['data']['live_status']


# 向该房间的订阅者发送消息
async def push_message(vid, bot):
    with sqlite3.connect(bot.config.db) as connect:
        connect.row_factory = sqlite3.Row
        c = connect.cursor()
        c.execute(
            'SELECT * FROM vtb where vid=' + str(vid))
        row = c.fetchone()
        item = dict(zip([d[0] for d in c.description], row))

    user_ids = get_users_by_room(vid)
    for user_id in user_ids:
        await bot.send_private_msg(user_id=user_id,
                                   message='你订阅的' + item['name_zh'] + '开始直播：' + bot.config.room_url + item['room_b'])
