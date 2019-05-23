import json
import re
import random

from sprout.helpers import is_number
from typing import List


def get_employee_data():
    with open('/data/app/sprout/modules/ark/employee.json', 'r') as f:
        results = json.loads(f.read())

    return results


up_0 = ['能天使', '安洁莉娜', '天火', '可颂', '凛冬']
up_1 = ['夜莺', '推进之王', '芙兰卡', '白金', '德克萨斯']
up_2 = ['角峰', '初雪', '崖心', '银灰']


def get_ups(arg) -> List:
    if not arg or is_number(arg):
        ups = []
    else:
        try:
            ups = eval(f'up_{arg}')
        except Exception:
            ups = []

    return ups


async def handle_index(bot, ctx):
    message = '''/ark 明日方舟指令帮助：
/ark info [名字] - 查看干员信息
/ark draw - 模拟一次干员寻访
/ark crazy - 模拟十连干员寻访'''
    # / ark calc[标签1 | 标签2..] - 公开招募计算器「未开放」
    # /ark recruit [标签1|标签2..] - 模拟公开招募「未开放」
    return await bot.send(ctx, message=message, at_sender=True)


async def handle_info(bot, ctx, sub_arg):
    employees = get_employee_data()
    result = list(filter(lambda x: x['name'] == sub_arg[0], employees))
    if len(result) > 0:
        item = result[0]
        message = f'名字：{item["name"]}({item["name-en"]})\n阵营：{item["camp"]}\n类型：{item["type"]}\n稀有度：{item["level"]}星'
        tags = '、'.join(item.get("tags"))
        message += f'\n标签：{tags}'
        message += f'\n描述：{item["characteristic"]}'
        return await bot.send(ctx, message=message)
    else:
        return await bot.send(ctx, message='没有找到该干员')


async def handle_single_draw(bot, ctx, sub_arg):
    ups = get_ups(sub_arg[0])
    result = draw_once(ups)

    up_message = '、'.join(ups)
    message = f'本次卡池up：{up_message}，仅为概率模拟，实际以官方抽卡为准！\n你获得了{result["level"]}星{result["type"]}干员：{result["name"]}'
    return await bot.send(ctx, message=message, at_sender=True)


async def handle_ten_draw(bot, ctx, sub_arg):
    ups = get_ups(sub_arg[0])
    results = []
    for i in range(0, 10):
        results.append(draw_once(ups))

    up_message = '、'.join(ups)
    message = f'本次卡池up：{up_message}，仅为概率模拟，实际以官方抽卡为准！'

    for result in results:
        message += f'\n你获得了{result["level"]}星{result["type"]}干员：{result["name"]}'

    return await bot.send(ctx, message=message, at_sender=True)


async def run(bot, ctx, cmd, arg) -> None:
    if not arg:
        return await handle_index(bot, ctx)

    args = re.split('\s+', arg)
    sub_cmd = args[0]
    sub_arg = args[1:]

    if sub_cmd == 'info':
        return await handle_info(bot, ctx, sub_arg)
    elif sub_cmd == 'draw':
        return await handle_single_draw(bot, ctx, sub_arg)
    elif sub_cmd == 'crazy':
        return await handle_ten_draw(bot, ctx, sub_arg)
    else:
        return


def draw_once(ups):
    # 三、四、五、六星概率
    ps = [0.4, 0.5, 0.08, 0.02]
    rand = random.random()
    t = 0
    r = 0
    for rk, p in enumerate(ps):
        t += p
        if (rand <= t):
            r = rk
            break
        else:
            continue

    employees = get_employee_data()
    if r == 3:
        choices = list(filter(lambda x: x['level'] == 6 and x['private'], employees))
        result = pick_up(choices, ups)
    elif r == 2:
        choices = list(filter(lambda x: x['level'] == 5 and x['private'], employees))
        result = pick_up(choices, ups)
    elif r == 1:
        choices = list(filter(lambda x: x['level'] == 4 and x['private'], employees))
        result = pick_up(choices, ups)
    else:
        choices = list(filter(lambda x: x['level'] == 3 and x['private'], employees))
        result = pick_up(choices, ups)

    return result


def pick_up(choices, ups):
    rand = random.random()
    up_choices = list(filter(lambda x: x['name'] in ups, choices))
    else_choices = list(filter(lambda x: x['name'] not in ups, choices))
    if rand > 0.5 and len(up_choices) > 0:
        res = random.choice(up_choices)
    else:
        res = random.choice(else_choices)

    return res
