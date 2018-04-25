import pika

rabbit_credentials = pika.PlainCredentials('guest', 'guest')
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0', 32777, "/", credentials=rabbit_credentials))

channel = rabbit_connection.channel()

exchange_name = queue_name = 'basic'

channel.exchange_declare(exchange=exchange_name,
                         exchange_type='direct')
channel.confirm_delivery()
channel.queue_declare(queue_name, durable=True)
channel.queue_bind(queue_name, exchange_name, routing_key='good')

for i in range(1000):
    message = '{"id": ' + str(i) + ', "string": "Hello World"}'

    if channel.basic_publish(exchange=exchange_name, body=message, routing_key='good', mandatory=True):
        print(" [x] sent message %r" % i)
    else:
        print('Message could not be confirmed')