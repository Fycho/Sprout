from random import choice
from urllib import parse
import json, aiohttp, re, asyncio


class MoeApi:
    danbooru_pool = ('https://konachan.net', 'https://yande.re')
    popular_path = '/post/popular_recent.json'
    search_path = '/post.json'

    safe_rating = 's'
    questionable_rating = 'q'
    explicit_rating = 'e'

    def __init__(self, mode):
        self.mode = mode

    async def popular(self):
        url = choice(self.danbooru_pool) + self.popular_path
        print(f'get moe girl from: {url}')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp_text = await resp.text()
                filtered_list = list(filter(lambda x: x['rating'] == self.mode, json.loads(resp_text)))
                return filtered_list

    async def search(self, params):
        built_params = parse.urlencode({
            'api_version': 2,
            'limit': 100,
            'include_tags': 1,
            'tags': params
        })
        url = choice(self.danbooru_pool) + self.search_path + '?' + built_params
        print(f'get moe girl from: {url}')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp_text = await resp.text()
                result = json.loads(resp_text)
                filtered_list = list(filter(lambda x: x['rating'] == self.mode, result['posts']))
                return filtered_list


async def run(bot, ctx, cmd, arg) -> None:
    api = MoeApi(MoeApi.safe_rating)
    if not arg:
        api_result = await api.popular()
    else:
        params = re.sub(r'\s+', '+', arg)
        api_result = await api.search(params)

    if len(api_result) == 0:
        return await bot.send(ctx, message='没有找到相关资源')
    jpeg_url = choice(api_result)['jpeg_url']
    await bot.send(ctx, message=jpeg_url)


async def mock_coroutine():
    api = MoeApi(MoeApi.safe_rating)
    api_result = await api.search('kafuu_chino')
    jpeg_url = choice(api_result)['jpeg_url']
    print(jpeg_url)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mock_coroutine())
    loop.close()