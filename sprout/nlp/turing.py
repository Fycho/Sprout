import json
import os
import re

import aiohttp

API_KEY = os.environ.get('TURING_KEY')
API_URL = 'http://openapi.tuling123.com/openapi/api/v2'


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
            "apiKey": API_KEY,
            "userId": user_id
        },
    }
    json_params = json.dumps(request_params)
    async with aiohttp.ClientSession() as session:
        headers = {'content-type': 'application/json', 'charset': 'utf8'}
        async with session.post(url=API_URL, data=json_params, headers=headers) as resp:
            resp_text = await resp.text(encoding='utf8')
            return json.loads(resp_text)


async def handle_turing_api(bot, ctx) -> bool:
    pattern = '|'.join(bot.config.NLP_DICT)
    matched = re.findall(pattern, ctx['message'])

    if len(matched) > 0:
        resp = await fetch_turing_results(ctx['user_id'], ctx['message'])
        message = ''
        if 'results' in resp:
            for i, group in enumerate(resp['results']):
                if i == 0:
                    message += group['values'][group['resultType']]
                else:
                    message += '\n' + group['values'][group['resultType']]

            await bot.send(ctx, message)
            return True

    return False
