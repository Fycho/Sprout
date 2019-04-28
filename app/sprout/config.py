import os
from typing import Any, Dict

DEBUG = False
SUPER_USERS = {os.environ.get('SUPER_ACCOUNT')}
ADMIN_COMMANDS = {'ping', 'task'}
NORMAL_COMMANDS = {'info', 'weather', 'vtb', 'roll', 'moegirl', 'remind', 'help', 'rps', 'omok', 'tzfe'}

APSCHEDULER_CONFIG: Dict[str, Any] = {
    'apscheduler.timezone': 'Asia/Shanghai'
}
