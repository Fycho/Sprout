import asyncio
import json
import os
import random

import aiohttp

turing_api_key = os.environ.get('TURING_KEY')
turing_api_url = 'http://openapi.tuling123.com/openapi/api/v2'


async def fetch_turing_results(user_id: int, input: str) -> dict:
    request_params = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": input
            },
            "selfInfo": {
            }
        },
        "userInfo": {
            "apiKey": turing_api_key,
            "userId": user_id
        },
    }
    json_params = json.dumps(request_params)
    async with aiohttp.ClientSession() as session:
        headers = {'content-type': 'application/json', 'charset': 'utf8'}
        async with session.post(url=turing_api_url, data=json_params, headers=headers) as resp:
            resp_text = await resp.text(encoding='utf8')
            return json.loads(resp_text)


async def handle_turing_api(bot, ctx) -> bool:
    rnd = random.random()
    if rnd > 0.01:
        return False

    message = ctx['message']
    user_id = ctx['user_id']

    resp = await fetch_turing_results(user_id, message)

    if resp['intent']['code'] != 10004:
        return False

    message = ''
    if 'results' in resp:
        for i, group in enumerate(resp['results']):
            if i == 0:
                message += group['values'][group['resultType']]
            else:
                message += '\n' + group['values'][group['resultType']]

        await asyncio.sleep(5)
        await bot.send(ctx, message)
        return True

    return False
