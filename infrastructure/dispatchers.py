import pulsar
from pulsar.schema import *
import utils


class Dispatcher:
    def __init__(self):
        ...

    def publish_message(self, mensaje, topic):
        client = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publisher = client.create_producer(
            topic, schema=AvroSchema(mensaje.__class__))
        publisher.send(mensaje)
        client.close()
