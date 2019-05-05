import asyncio

from sprout import Sprout


async def run(bot: Sprout, ctx, cmd, arg) -> None:
    if not arg or arg == 'help':
        message = '双人对战五子棋【请在电脑上使用！！手机上显示会崩坏！！】\n确认加入/omok join，退出游戏/omok quit。一方加入后30秒内无另一方加入则自动退出。游戏开始后如一方30秒无输入则游戏自动结束。'
        await bot.send(ctx, message=message)

    if arg == 'join':
        await handle_join(bot, ctx)

    elif arg == 'quit':
        await handle_quit(bot, ctx)


async def handle_join(bot, ctx):
    game = bot.omok_instance
    if len(game.players) >= game.max_player:
        return await bot.send(ctx, message=f'当前玩家已满，请等待他们游戏结束。')

    if len(game.players) == 0:
        game.init()

    user_id = ctx['user_id']
    game.join(user_id)
    task_main = bot.send(ctx, message=f'用户{user_id}已加入游戏')

    if len(game.players) == game.max_player:
        game.wait_task.cancel()
        await task_main
        message = '游戏开始。用户' + str(game.players[0]) + '代表O, ' + str(game.players[1]) + '代表X。请直接输入对于的棋盘坐标来摆放棋子，例如A5。'
        await bot.send(ctx, message=message)
        await game_start(bot, ctx)
    else:
        game.wait_task = asyncio.create_task(waitfor(bot, ctx))
        await asyncio.gather(task_main, game.wait_task)


async def handle_quit(bot, ctx):
    game = bot.omok_instance
    user_id = ctx['user_id']
    if user_id not in game.players:
        return await bot.send(ctx, message=f'用户{user_id}不在游戏中', at_sender=True)

    game.quit(user_id)
    await bot.send(ctx, message=f'用户{user_id}已离开游戏')
    game.wait_task.cancel()


async def game_start(bot, ctx):
    game = bot.omok_instance
    await bot.send(ctx, message=game.format_output())
    game.countdown_task = asyncio.create_task(countdown(bot, ctx))
    task_main = bot.send(ctx, message='现在是' + str(game.players[game.current_turn]) + '的回合，倒计时30秒')
    await asyncio.gather(task_main, game.countdown_task)


async def countdown(bot, ctx):
    game = bot.omok_instance
    await asyncio.sleep(30)
    await bot.send(ctx, message='用户' + str(game.players[game.current_turn]) + '在30秒内没有操作，游戏结束。')
    game.init()


async def waitfor(bot, ctx):
    game = bot.omok_instance
    await asyncio.sleep(30)
    await bot.send(ctx, message='30秒没有其他人加入，你已经退出游戏，如需继续请重新加入。', at_sender=True)
    game.init()
