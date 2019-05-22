import datetime
import os
import re
from typing import Tuple, List
import jieba.analyse
import pymysql

HOST = os.environ.get('MYSQL_HOST')
USER = os.environ.get('MYSQL_USER')
PWD = os.environ.get('MYSQL_PWD')
DB = 'sprout'

stopwords_path = '/data/app/sprout/modules/analyzers/stopwords.txt'
user_dict_path = '/data/app/sprout/modules/analyzers/user_dict.txt'


async def run(bot, ctx, cmd, arg) -> None:
    if 'group_id' not in ctx:
        return await bot.send(ctx, '非群')

    message = '最近30天热词统计：'
    items = handle_group(ctx['group_id'])
    for item in items:
        message += f'\n{item[0]}({item[1]})'

    await bot.send(ctx, message)


def handle_group(gid) -> List[Tuple]:
    with pymysql.connect(host=HOST, user=USER, passwd=PWD, db=DB, charset='utf8') as c:
        now = datetime.datetime.now()
        oneweek = datetime.timedelta(days=30)
        time = (now - oneweek).strftime('%Y-%m-%d %H:%M:%S')
        c.execute(f'SELECT msg FROM msg WHERE msg NOT LIKE "%[CQ%" AND gid={gid} AND created>"{time}"')
        return handle_seg(c.fetchall())


def handle_seg(results) -> List[Tuple]:
    articles = []
    for result in results:
        articles.append(result[0])

    str_result = ''.join(articles)
    str_result = re.sub('[0-9!"#$%&\'()*+,-./:;<=>?@，。★、…【】《》？“”‘’！[\\]^_`{|}~\n\r]+', '', str_result)
    jieba.load_userdict(user_dict_path)
    jieba.analyse.set_stop_words(stopwords_path)
    seg_list = jieba.analyse.extract_tags(str_result, topK=10)
    return list(map(lambda seg: (seg, str_result.count(seg)), seg_list))
