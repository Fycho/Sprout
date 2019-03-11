import requests, json, re, time


async def run(bot, ctx, cmd, arg) -> None:
    if not arg:
        await bot.send(ctx, '缺少参数：城市')
    else:
        args = re.split('\s+', arg)
        if len(args) < 2:
            args.append(0)
        weather_report = get_weather_of_city(args[0], args[1])
        await bot.send(ctx, weather_report)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def get_weather_of_city(city: str, day) -> str:
    if is_number(day) == False or day > 6:
        day = 0

    day_label = ('今天', '明天', '后天', '大后天', '大大后天', '大大大后天')
    day = int(day)

    ret = requests.get(f'http://wthrcdn.etouch.cn/weather_mini?city={city}')
    res_dict = json.loads(ret.text)
    if 'data' in res_dict:
        if len(res_dict['data']['forecast']) <= day:
            return '没有查询到该天的天气'
        today = res_dict['data']['forecast'][day]
        return f'{city}{day_label[day]}{today["type"]}，{today["fengxiang"]}{today["fengli"]}，{today["low"]}，{today["high"]}'
    else:
        return '没有查询到该城市的天气'
