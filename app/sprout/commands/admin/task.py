from sprout import Sprout


async def run(bot: Sprout, ctx, cmd, arg) -> None:
    if arg == 'start':
        bot.start_all_tasks()
        await bot.send(ctx, '已启动所有计划任务')
    elif arg == 'stop':
        bot.stop_all_tasks()
        await bot.send(ctx, '已停止所有计划任务')
