import json
import re


def get_employee_data():
    with open('/data/app/sprout/modules/ark/employee.json', 'r') as f:
        results = json.loads(f.read())

    return results


async def handle_index(bot, ctx):
    message = '''/ark 明日方舟指令帮助：
/ark info [名字] - 查看干员信息
/ark calc [标签1|标签2..] - 公开招募计算器「未开放」
/ark draw - 模拟私有寻访（无up、保底计算）「未开放」
/ark crazy - 模拟十连（无up、保底计算）「未开放」
/ark recruit [标签1|标签2..] - 模拟公开招募「未开放」'''
    return await bot.send(ctx, message=message, at_sender=True)


async def handle_info(bot, ctx, sub_arg):
    employees = get_employee_data()
    result = list(filter(lambda x: x['name'] == sub_arg[0], employees))
    if len(result) > 0:
        item = result[0]
        message = f'姓名：{item["name"]}({item["name-en"]})\n阵营：{item["camp"]}\n类型：{item["type"]}\n稀有度{item["level"]}'
        tags = '|'.join(item["tags"])
        message += f'\n标签：{tags}'
        message += f'\n描述：{item["characteristic"]}'
        return await bot.send(ctx, message=message, at_sender=True)
    else:
        return await bot.send(ctx, message='没有找到该干员', at_sender=True)


async def run(bot, ctx, cmd, arg) -> None:
    if not arg:
        return await handle_index(bot, ctx)

    args = re.split('\s+', arg)
    sub_cmd = args[0]
    sub_arg = args[1:]

    if sub_cmd == 'info':
        return await handle_info(bot, ctx, sub_arg)
    else:
        return
