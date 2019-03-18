# -*- coding: utf-8 -*-

from sprout import Sprout
import config

sprout = Sprout(config)
app = sprout.server_app


@app.route('/admin')
async def admin():
    return '待填坑'

if __name__ == '__main__':
    sprout.run(host='0.0.0.0', port=8888)
