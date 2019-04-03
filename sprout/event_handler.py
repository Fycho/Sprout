import importlib
import re
from typing import Tuple

from sprout.nlp.turing import handle_turing_api
from .log import logger


async def handle_message(bot, ctx) -> None:
    handled = await handle_command(bot, ctx)
    if handled:
        logger.info(f'Message {ctx["message_id"]} is handled as a command')
        return

    handled = await handle_natural_language(bot, ctx)
    if handled:
        logger.info(f'Message {ctx["message_id"]} is handled as natural language')
        return


async def handle_notice(bot, ctx) -> None:
    pass


async def handle_request(bot, ctx) -> None:
    pass


async def handle_meta_event(bot, ctx) -> None:
    pass


async def handle_command(bot, ctx) -> bool:
    user_id = ctx['user_id']
    message = ctx['message']
    indicator, cmd, arg = parse_command(message)

    if indicator == '!' and str(user_id) in bot.config.SUPER_USERS:
        return await _handle_admin_command(bot, ctx, cmd, arg)
    elif indicator == '/':
        return await _handle_normal_command(bot, ctx, cmd, arg)


async def _handle_admin_command(bot, ctx, cmd, arg) -> bool:
    if cmd not in bot.config.ADMIN_COMMANDS:
        return False

    cmd = importlib.import_module(f'.commands.admin.{cmd}', __package__)
    await cmd.run(bot, ctx, cmd, arg)
    return True


async def _handle_normal_command(bot, ctx, cmd, arg) -> bool:
    if cmd not in bot.config.NORMAL_COMMANDS:
        return False

    cmd = importlib.import_module(f'.commands.normal.{cmd}', __package__)
    await cmd.run(bot, ctx, cmd, arg)
    return True


async def handle_natural_language(bot, ctx) -> bool:
    handled = await handle_turing_api(bot, ctx)
    return handled


def parse_command(message) -> Tuple:
    res = {
        'indicator': message[0:1],
        'cmd': '',
        'arg': ''
    }
    matched = re.match(r'^(\w+)\s*(.*?)$', message[1:])
    if matched:
        res['cmd'] = matched.group(1)
        res['arg'] = matched.group(2)
    return (res['indicator'], res['cmd'], res['arg'])


__all__ = [
    'handle_message',
    'handle_notice',
    'handle_request',
    'handle_meta_event'
]
