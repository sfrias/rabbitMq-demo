import pika
import time

rabbit_credentials = pika.PlainCredentials('guest', 'guest')
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0', 32777, "/", credentials=rabbit_credentials))

channel = rabbit_connection.channel()

channel.queue_declare('direct_queue', durable=True)

print('[x] Waiting for messages, press ctrl+C to stop')


def callback(channel, method, properties, body):
    print(' -> message: ' + str(body.decode("utf-8")))
    channel.basic_ack(delivery_tag=method.delivery_tag)
    time.sleep(0.5)


channel.basic_consume(callback,
                      queue='direct_queue')

channel.start_consuming()