import os
from typing import Any, Dict

su = os.environ.get('SUPER_ACCOUNT')

DEBUG = False
SUPER_USERS = {su}
ADMIN_COMMANDS = {'ping', 'task', 'addvtb'}
NORMAL_COMMANDS = {'weather', 'vtb', 'roll', 'moegirl', 'remind', 'help', 'rps'}

APSCHEDULER_CONFIG: Dict[str, Any] = {
    'apscheduler.timezone': 'Asia/Shanghai'
}

room_url = 'https://live.bilibili.com/'
api_url = 'https://api.live.bilibili.com/room/v1/Room/get_info?id='
db = '/data/sprout/sprout/db/sprout.db'

