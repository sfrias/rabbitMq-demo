import pika
import time
import json

rabbit_credentials = pika.PlainCredentials('guest', 'guest')
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0', 32777, "/", credentials=rabbit_credentials))

channel = rabbit_connection.channel()

channel.queue_declare('basic', durable=True)

print('[x] Waiting for messages, press ctrl+C to stop')


def callback(channel, method, properties, body):
    message_dict = json.loads(str(body.decode("utf-8")))
    if message_dict.get('id') % 2 == 0:
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print('CONFIRMED -> message: ' + str(body.decode("utf-8")))
    else:
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        print('DENIED -> message: ' + str(body.decode("utf-8")))
    # time.sleep(1)


channel.basic_consume(callback,
                      queue='basic')

channel.start_consuming()