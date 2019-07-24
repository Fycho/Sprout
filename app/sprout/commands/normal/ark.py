import json
import re
import random

from sprout.helpers import is_number
from typing import List


def get_operators():
    with open('/data/app/sprout/modules/ark/operators.json', 'r') as f:
        results = json.loads(f.read())

    return results


up_01 = ['能天使', '安洁莉娜', '天火', '可颂', '凛冬']
up_02 = ['夜莺', '推进之王', '芙兰卡', '白金', '德克萨斯']
up_03 = ['艾雅法拉', '伊芙利特', '赫默', '梅尔', '拉普兰德']
up_04 = ['闪灵', '塞雷娅', '真理', '幽灵鲨', '红']
up_05 = ['银灰', '夜莺', '蓝毒', '白面鸮', '空']
up_06 = ['安洁莉娜', '推进之王', '狮蝎', '华法琳', '守林人']
up_07 = ['艾雅法拉', '塞雷娅', '普罗旺斯', '红', '芙兰卡']

up_e01 = ['角峰', '初雪', '崖心', '银灰']
up_e02 = ['斯卡蒂', '夜魔', '临光', '猎蜂', '暗锁']
up_e03 = ['陈', '诗怀雅', '食铁兽', '格雷伊']
up_e04 = ['星熊', '雷蛇', '陨星']

def get_ups(arg) -> List:
    tested = re.match(r'^e\d+$', arg, re.I)
    if not arg or not tested:
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
/ark draw <参数> - 模拟一次干员寻访（参数从01开始递增，表示了游戏内各期干员概率常规up池，活动池子从e01开始递增，无数字则各干员均等概率，例如/ark draw 01, /ark draw e01）
/ark genius <参数> - 模拟十连干员寻访（参数同上）
/ark idiot <参数> - 模拟五十连干员寻访（***刷屏警告***）'''
    return await bot.send(ctx, message=message, at_sender=True)


async def handle_info(bot, ctx, sub_arg):
    operators = get_operators()
    result = list(filter(lambda x: x['name'] == sub_arg[0], operators))
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
    if not sub_arg or len(sub_arg) < 1:
        ups = []
    else:
        ups = get_ups(sub_arg[0])
    result = draw_once(ups)

    if len(ups) > 0:
        up_message = '、'.join(ups)
        message = f'本次卡池up：{up_message}，仅为概率模拟，实际以官方抽卡为准！'
    else:
        message = f'本次卡池无up，仅为概率模拟，实际以官方抽卡为准！'

    message += f'\n你获得了{result["level"]}星{result["type"]}干员：{result["name"]}'
    return await bot.send(ctx, message=message, at_sender=True)


async def handle_multi_draws(bot, ctx, sub_arg, times = 10):
    if not sub_arg or len(sub_arg) < 1:
        ups = []
    else:
        ups = get_ups(sub_arg[0])
    results = []
    for i in range(0, times):
        results.append(draw_once(ups))

    if len(ups) > 0:
        up_message = '、'.join(ups)
        message = f'本次卡池up：{up_message}，仅为概率模拟，实际以官方抽卡为准！'
    else:
        message = f'本次卡池无up，仅为概率模拟，实际以官方抽卡为准！'

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
    elif sub_cmd == 'genius':
        return await handle_multi_draws(bot, ctx, sub_arg, 10)
    elif sub_cmd == 'idiot':
        return await handle_multi_draws(bot, ctx, sub_arg, 50)
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

    operators = get_operators()
    if r == 3:
        choices = list(filter(lambda x: x['level'] == 6 and x['private'], operators))
        result = pick_up(choices, ups, 0.5)
    elif r == 2:
        choices = list(filter(lambda x: x['level'] == 5 and x['private'], operators))
        result = pick_up(choices, ups, 0.5)
    elif r == 1:
        choices = list(filter(lambda x: x['level'] == 4 and x['private'], operators))
        result = pick_up(choices, ups, 0.2)
    else:
        choices = list(filter(lambda x: x['level'] == 3 and x['private'], operators))
        result = pick_up(choices, ups, 0.5)

    return result

# prob: x星内up的出货率
def pick_up(choices, ups, prob):
    rand = random.random()
    up_choices = list(filter(lambda x: x['name'] in ups, choices))
    else_choices = list(filter(lambda x: x['name'] not in ups, choices))
    if rand < prob and len(up_choices) > 0:
        res = random.choice(up_choices)
    else:
        res = random.choice(else_choices)

    return res
