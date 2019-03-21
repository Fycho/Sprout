# -*- coding: utf-8 -*-

import config
from sprout import *

sprout = init(config)
app = get_bot().server_app


@app.route('/admin')
async def admin():
    return '''
这里是豆芽菜的后台。
powered by Fycho.
    '''


if __name__ == '__main__':
    run(host='0.0.0.0', port=8888)
