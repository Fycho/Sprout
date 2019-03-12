from random import choice
import requests, json


class MoeApi:
    pool = ('https://konachan.net', 'https://yande.re')
    sub_path = '/post/popular_recent.json'

    safe_rating = 's'
    questionable_rating = 'q'
    explicit_rating = 'e'

    def __init__(self, mode):
        self.mode = mode

    def exec(self):
        url = choice(self.pool) + self.sub_path
        print(f'get moe girl from: {url}')
        ret = requests.get(url)
        filtered_list = list(filter(lambda x: x['rating'] == self.mode, json.loads(ret.text)))
        print(filtered_list)
        return filtered_list


async def run(bot, ctx, cmd, arg) -> None:
    api = MoeApi(MoeApi.safe_rating)
    api_result = api.exec()
    jpeg_url = choice(api_result)['jpeg_url']
    await bot.send(ctx, message=f'[CQ:image,file={jpeg_url}]')
