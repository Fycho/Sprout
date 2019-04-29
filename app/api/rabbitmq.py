import base64
import datetime
import json
import os

import pika

HOST = os.environ.get('RMQ_HOST')
PORT = 5672
USER = os.environ.get('RMQ_USER')
PWD = os.environ.get('RMQ_PWD')

def handle_message_api(bot, ctx):
    if 'group_id' not in ctx:
        return

    now = datetime.datetime.now()
    timestr = now.strftime('%Y-%m-%d %H:%M:%S')
    content = json.dumps({'ctx': ctx, 'time': timestr}, ensure_ascii=False)

    message_body = base64.b64encode(bytes(content, encoding='utf8'))
    credentials = pika.PlainCredentials(USER, PWD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(HOST, PORT, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='msg', durable=True)
    channel.basic_publish(exchange='exchange', routing_key='msg', body=message_body)
    connection.close()
