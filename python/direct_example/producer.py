import pika

rabbit_credentials = pika.PlainCredentials('guest', 'guest')
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0', 32777, "/", credentials=rabbit_credentials))

channel = rabbit_connection.channel()

exchange_name = "direct_demo"
queue_name = "direct_queue"

channel.exchange_declare(exchange=exchange_name,
                         exchange_type='direct')

channel.queue_declare('even', durable=True)
channel.queue_bind('even', exchange_name, routing_key='number.even')

channel.queue_declare('odd', durable=True)
channel.queue_bind('odd', exchange_name, routing_key='number.odd')

channel.confirm_delivery()

for i in range(1000):
    message = 'Hello World, this is message number ' + str(i)

    if i % 2 == 0:
        route = "number.even"
    else:
        route = "number.odd"

    if channel.basic_publish(exchange=exchange_name, body=message, routing_key=route, mandatory=True):
        print(" [x] sent message %r" % i)
    else:
        print(" [x] ERROR ON MESSAGE %r" % i)
