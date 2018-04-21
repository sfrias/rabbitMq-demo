import pika

rabbit_credentials = pika.PlainCredentials('guest', 'guest')
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0', 32777, "/", credentials=rabbit_credentials))

channel = rabbit_connection.channel()

channel.queue_declare('basic', durable=True)

print('[x] Waiting for messages, press ctrl+C to stop')


def callback(channel, method, properties, body):
    print(' -> message: ' + str(body.decode("utf-8")))
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(callback,
                      queue='basic')

channel.start_consuming()