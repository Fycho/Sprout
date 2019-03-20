import os

su = os.environ.get('SUPER_ACCOUNT')

SUPER_USERS = {su}
ADMIN_COMMANDS = {'ping'}
NORMAL_COMMANDS = {'weather', 'vtb', 'roll', 'moegirl'}

room_url = 'https://live.bilibili.com/'
api_url = 'https://api.live.bilibili.com/room/v1/Room/get_info?id='
db = '/data/sprout/sprout/db/sprout.db'
