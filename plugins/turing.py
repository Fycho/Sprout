from nonebot import on_command, CommandSession
import os

turing_key = os.environ.get('TURING_API_KEY')

@on_command('turing', aliases=('图灵', '聊天'))
async def turing(session: CommandSession):
    print(os.environ.get('TURING_API_KEY'))
    await session.send('功能开发中')