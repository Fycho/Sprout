import asyncio
import json

import aiohttp

from database import session
from sprout.log import logger
from sprout.models import Vtb

room_url = 'https://live.bilibili.com/'
api_url = 'https://api.live.bilibili.com/room/v1/Room/get_info?id='

async def initialize(bot, live_status_dict) -> None:
    vtb_models = session.query(Vtb).all()
    tasks = list()
    for vtb in vtb_models:
        tasks.append(asyncio.create_task(handler(bot, vtb, live_status_dict)))

    await asyncio.gather(*tasks)


async def handler(bot, current_vtb, live_status_dict) -> None:
    async with aiohttp.ClientSession() as session:
        url = api_url + current_vtb.room_b
        async with session.get(url) as resp:
            resp_text = await resp.text()
            result = json.loads(resp_text)
            live_status = result['data']['live_status']
            title = result['data']['title']
            if current_vtb.room_b in live_status_dict and live_status == 1 and live_status_dict[
                current_vtb.room_b] != 1:
                live_status_dict[current_vtb.room_b] = result['data']['live_status']
                logger.debug(current_vtb.name_zh + '<' + current_vtb.room_b + '> started streaming.')
                await push_message(current_vtb.vid, title, bot)


# 向该房间的订阅者发送消息
async def push_message(vid, title, bot) -> None:
    # 获取该vid的订阅者
    vtb = session.query(Vtb).get(vid)
    user_subs = session.query(Vtb).get(vid).user_subscribes.all()
    user_ids = list(map(lambda x: x.user_id, user_subs))
    tasks = list()

    for user_id in user_ids:
        logger.info('Notified user' + ': ' + str(user_id))
        message = f'你订阅的{vtb.name_zh}开始直播：{room_url}{vtb.room_b}。标题：{title}'
        tasks.append(asyncio.create_task(bot.send_private_msg(user_id=user_id, message=message)))

    await asyncio.gather(*tasks)