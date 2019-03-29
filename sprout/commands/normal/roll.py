import aiohttp
import random
import re


async def run(bot, ctx, cmd, arg) -> None:
    if ctx['message'].endswith('概率'):
        point = await get_random_int(0, 100)
        message = f'你摇到了概率：{point}%'

    else:
        point = str(random.randint(0, 100))
        message = f'你摇到了点数：{point}'

    await bot.send(ctx, message=message, at_sender=True)

# true random number
async def get_random_int(min, max) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://www.random.org/integers/?num=1&min={min}&max={max}&col=1&base=10&format=plain&rnd=new') as resp:
            resp_text = await resp.text()
            return re.findall(r'(\d+)', resp_text)[0]
