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
    content = json.dumps({'uid': ctx['user_id'], 'gid': ctx['group_id'], 'msg': ctx['message'],
                          'created': now.strftime('%Y-%m-%d %H:%M:%S')}, ensure_ascii=False)
    message_body = base64.b64encode(bytes(content, encoding='utf8'))
    rmq_produce(exchange='exchange', routing_key='msg', queue='msg', body=message_body)


def rmq_produce(exchange, queue, routing_key, body, durable=True):
    credentials = pika.PlainCredentials(USER, PWD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(HOST, PORT, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=durable)
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)
    connection.close()
