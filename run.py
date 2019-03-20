# -*- coding: utf-8 -*-

from sprout import Sprout
import config

sprout = Sprout(config)
app = sprout.server_app


@app.route('/admin')
async def admin():
    return '''
这里是豆芽菜的后台。
powered by Fycho.
    '''

if __name__ == '__main__':
    sprout.run(host='0.0.0.0', port=8888)
