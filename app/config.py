import os
from typing import Any, Dict

su = os.environ.get('SUPER_ACCOUNT')

DEBUG = False
SUPER_USERS = {su}
ADMIN_COMMANDS = {'ping', 'task', 'addvtb', 'sql'}
NORMAL_COMMANDS = {'info', 'weather', 'vtb', 'roll', 'moegirl', 'remind', 'help', 'rps', 'omok', 'tzfe'}

APSCHEDULER_CONFIG: Dict[str, Any] = {
    'apscheduler.timezone': 'Asia/Shanghai'
}


