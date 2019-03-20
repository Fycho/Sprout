import sqlite3, json, requests, time, asyncio
import config

sleep_time = 60


# 获取需要查询的房间
def get_available_rooms() -> list:
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


def initialize(bot):
    observable = dict()
    while True:
        models = get_available_rooms()
        for model in models:
            # run task (todo test async way
            url = config.api_url + model['room_b']
            resp = requests.get(url)
            result = json.loads(resp.text)
            live_status = result['data']['live_status']
            print(model['room_b'] + ':' + str(live_status))
            if model['room_b'] in observable and live_status == 1 and model['room_b'] != 1:
                asyncio.run(push_message(model['vid'], bot))

            observable[model['room_b']] = result['data']['live_status']

        time.sleep(sleep_time)


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
