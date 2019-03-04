import nonebot, config
from os import path

nonebot.init(config)
nonebot.load_builtin_plugins()
nonebot.load_plugins(
    path.join(path.dirname(__file__), 'plugins'),
    'plugins'
)

bot = nonebot.get_bot()
app = bot.asgi

@bot.on_message()
async def handle_msg(context):
    # await bot.send(context, '你好呀，下面一条是你刚刚发的：')
    return {'reply': context['message']}

if __name__ == '__main__':
    nonebot.run(host='0.0.0.0', port=8888)
