import os
su = os.environ.get('SUPER_ACCOUNT')

SUPER_USERS = {su}
ADMIN_COMMANDS = {'ping'}
NORMAL_COMMANDS = {'weather', 'vtb'}