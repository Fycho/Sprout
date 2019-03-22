import os
from typing import Dict, Any

su = os.environ.get('SUPER_ACCOUNT')

DEBUG = True
SUPER_USERS = {su}
ADMIN_COMMANDS = {'ping', 'task', 'addvtb'}
NORMAL_COMMANDS = {'info', 'weather', 'vtb', 'roll', 'moegirl', 'remind'}

APSCHEDULER_CONFIG: Dict[str, Any] = {
    'apscheduler.timezone': 'Asia/Shanghai'
}

room_url = 'https://live.bilibili.com/'
api_url = 'https://api.live.bilibili.com/room/v1/Room/get_info?id='
db = '/data/sprout/sprout/db/sprout.db'

