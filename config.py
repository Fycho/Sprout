import os
from typing import Any, Dict

su = os.environ.get('SUPER_ACCOUNT')

DEBUG = False
SUPER_USERS = {su}
ADMIN_COMMANDS = {'ping', 'task', 'addvtb'}
NORMAL_COMMANDS = {'weather', 'vtb', 'roll', 'moegirl', 'remind', 'help', 'rps'}

NLP_DICT: tuple = ('豆芽菜', '？', '吃饭', '什么', '谁', '问', '睡觉', '玩', '几', '在哪', '有吗')
APSCHEDULER_CONFIG: Dict[str, Any] = {
    'apscheduler.timezone': 'Asia/Shanghai'
}

room_url = 'https://live.bilibili.com/'
api_url = 'https://api.live.bilibili.com/room/v1/Room/get_info?id='
db = '/data/sprout/sprout/db/sprout.db'

