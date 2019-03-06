import os, requests, json

turing_key = os.environ.get('TURING_API_KEY')

async def run(bot, ctx, cmd, arg) -> None:
    if not arg:
        await bot.send(ctx, '缺少参数：城市')
    else:
        weather_report = get_weather_of_city(arg)
        await bot.send(ctx, weather_report)


def get_weather_of_city(city: str) -> str:
    ret = requests.get(f'http://wthrcdn.etouch.cn/weather_mini?city={city}')
    res_dict = json.loads(ret.text)
    if 'data' in res_dict:
        today = res_dict['data']['forecast'][0]
        return f'{city}今天的天气是{today["type"]}，{today["fengxiang"]}{today["fengli"]}，{today["low"]}，{today["high"]}'
    else:
        return '没有查询到该城市的天气'