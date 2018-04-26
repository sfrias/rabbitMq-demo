import pika

rabbit_credentials = pika.PlainCredentials('guest', 'guest')
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0', 32777, "/", credentials=rabbit_credentials))

channel = rabbit_connection.channel()

exchange_name = "fanout_demo"
queue_name = "fanout_queue"

channel.confirm_delivery()

channel.exchange_declare(exchange=exchange_name,
                         exchange_type='fanout')


# DECLARE 3 QUEUES
def queue_declaration(channel, num):
    channel.queue_declare(queue_name + "_" + str(num), durable=True)
    channel.queue_bind(queue_name + "_" + str(num), exchange_name, routing_key='')


queue_declaration(channel, 1)
queue_declaration(channel, 2)
queue_declaration(channel, 3)

for i in range(1000):
    message = 'Hello World, this is message number ' + str(i)

    channel.basic_publish(exchange=exchange_name, body=message, routing_key='')
    print(" [x] sent message %r" % i)
