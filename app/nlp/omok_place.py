import asyncio
import re


async def handle_omok(bot, ctx):
    game = bot.omok_instance
    user_id = ctx['user_id']
    if user_id not in game.players or len(game.players) != game.max_player:
        return False

    message = ctx['message']

    if user_id != game.players[game.current_turn]:
        await bot.send(ctx, message='当前不在你的回合。', at_sender=True)
        return True

    matched = re.match(r'^([a-z])(\d+)$', message, re.I)
    if not matched:
        await bot.send(ctx, message='落子参数不合法，请重新落子。', at_sender=True)
        return True

    i = matched.group(1)
    j = matched.group(2)
    if i not in game.position_i or j not in game.position_j:
        await bot.send(ctx, message='你落到了棋盘外面，请重新落子。', at_sender=True)
        return True

    ii = game.position_i.index(i)
    ij = game.position_j.index(j)
    if game.board[ii][ij] != 0:
        await bot.send(ctx, message='该棋盘点有子，请重新落子。', at_sender=True)
        return True

    game.place(ii, ij)

    await bot.send(ctx, message=game.format_output())

    if game.win_status == True:
        await bot.send(ctx, message=f'用户{game.players[game.current_turn]}胜利！游戏结束。')
        game.countdown_task.cancel()
        game.init()
        return True

    game.countdown_task.cancel()
    game.change_turn()
    game.countdown_task = asyncio.create_task(countdown(bot, ctx))
    task_main = bot.send(ctx, message='现在是用户' + str(game.players[game.current_turn]) + '的回合，倒计时30秒')
    await asyncio.gather(task_main, game.countdown_task)
    return True


async def countdown(bot, ctx):
    game = bot.omok_instance
    await asyncio.sleep(30)
    await bot.send(ctx, message='用户' + str(game.players[game.current_turn]) + '在30秒内没有操作，游戏结束。')
    game.init()
