import pika

rabbit_credentials = pika.PlainCredentials('guest', 'guest')
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0', 32777, "/", credentials=rabbit_credentials))

channel = rabbit_connection.channel()

exchange_name = queue_name = 'basic'

channel.exchange_declare(exchange=exchange_name,
                         exchange_type='direct')
channel.queue_declare(queue_name,durable=True)
channel.queue_bind(queue_name, exchange_name, routing_key='')

for i in range(1000):
    message = 'Hello World, this is message number ' + str(i)

    channel.basic_publish(exchange=exchange_name, body=message, routing_key='')
    print(" [x] sent message %r" % i)
