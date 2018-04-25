import pika

rabbit_credentials = pika.PlainCredentials('guest', 'guest')
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0', 32777, "/", credentials=rabbit_credentials))

channel = rabbit_connection.channel()

exchange_name = queue_name = 'basic_fanout'

channel.exchange_declare(exchange=exchange_name,
                         exchange_type='fanout')


# DECLARE 3 QUEUES
def queue_declarator(channel, num):
    channel.queue_declare(queue_name + "_" + str(num), durable=True)
    channel.queue_bind(queue_name + "_" + str(num), 'basic_fanout', routing_key='')


queue_declarator(channel, 1)
queue_declarator(channel, 2)
queue_declarator(channel, 3)

for i in range(100):
    message = 'Hello World, this is message number ' + str(i)

    channel.basic_publish(exchange=exchange_name, body=message, routing_key='')
    print(" [x] sent message %r" % i)
