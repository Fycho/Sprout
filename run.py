import nonebot
import config
from nonebot import on_command, CommandSession

nonebot.init(config)
nonebot.load_builtin_plugins()

bot = nonebot.get_bot()
app = bot.asgi

@on_command('repeat')
async def echo(session: CommandSession):
    await session.send(session.state.get('message') or session.current_arg)

if __name__ == '__main__':
    nonebot.run(host='0.0.0.0', port=8888)
