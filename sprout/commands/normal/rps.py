import random


async def run(bot, ctx, cmd, arg) -> None:
    options = ('剪刀', '石头', '布')
    if not arg or arg not in options:
        return await bot.send(ctx, message='请出剪刀、石头或布中的一个', at_sender=True)

    user_index = options.index(arg)
    bot_index = random.randint(0, 2)

    message = f'你是{options[user_index]}，我是{options[bot_index]}，'

    result = check_win(bot_index, user_index)
    if result == 1:
        message += '我赢了！'

    elif result == 0:
        message += '是平局'

    elif result == 2:
        message += '你赢了！'

    await bot.send(ctx, message=message, at_sender=True)


# bot赢返回1，平局返回0，bot输返回2
def check_win(bot_index: int, user_index: int) -> int:
    return (bot_index - user_index) % 3
