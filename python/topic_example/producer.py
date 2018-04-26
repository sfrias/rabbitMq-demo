import pika

rabbit_credentials = pika.PlainCredentials('guest', 'guest')
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0', 32777, "/", credentials=rabbit_credentials))

channel = rabbit_connection.channel()

exchange_name = "topic_demo"
queue_name = "topic_queue"

channel.exchange_declare(exchange=exchange_name,
                         exchange_type='topic')

channel.queue_declare('all_cars', durable=True)
channel.queue_bind('all_cars', exchange_name, routing_key='cars.#')

channel.queue_declare('all_audi', durable=True)
channel.queue_bind('all_audi', exchange_name, routing_key='cars.audi.*')

channel.queue_declare('all_nissan', durable=True)
channel.queue_bind('all_nissan', exchange_name, routing_key='cars.nissan.*')

channel.queue_declare('all_citroen', durable=True)
channel.queue_bind('all_citroen', exchange_name, routing_key='cars.citroen.*')

channel.confirm_delivery()

cars = [
    {'type': 'car', 'brand': 'audi', 'model': 'quattro', 'price': 40000},
    {'type': 'car', 'brand': 'audi', 'model': 'A1', 'price': 28000},
    {'type': 'car', 'brand': 'nissan', 'model': 'micra', 'price': 13000},
    {'type': 'car', 'brand': 'nissan', 'model': 'note', 'price': 17000},
    {'type': 'car', 'brand': 'nissan', 'model': 'qashqai', 'price': 28000},
    {'type': 'car', 'brand': 'citroen', 'model': 'saxo', 'price': 8500},
    {'type': 'car', 'brand': 'citroen', 'model': 'xsara', 'price': 16000},
]

for car in cars:
    car_name_queue = car['brand'] + "_" + car['model']
    car_route_key = 'cars.'+car['brand']+'.'+car['model']
    message = 'Car price is ' + str(car['price'])
    channel.queue_declare(car_name_queue, durable=False)
    channel.queue_bind(car_name_queue, exchange_name, routing_key=car_route_key)
    if channel.basic_publish(exchange=exchange_name, body=message, routing_key=car_route_key, mandatory=True):
        print(" [x] sent message %r" % car['model'])
    else:
        print(" [x] ERROR ON MESSAGE %r" % car['model'])
