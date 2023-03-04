import logging
import traceback
import pulsar
import _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from utils import broker_host


async def subscribe_to_topic(topic: str, subscription: str, schema: Record, consumer_type: _pulsar.ConsumerType = _pulsar.ConsumerType.Shared):
    try:
        async with aiopulsar.connect(f'pulsar://{broker_host()}:6650') as client:
            async with client.subscribe(
                topic,
                consumer_type=consumer_type,
                subscription_name=subscription,
                schema=AvroSchema(schema)
            ) as consumer:
                while True:
                    mensaje = await consumer.receive()
                    datos = mensaje.value()
                    print(f'\nEvent recibido: {datos}')
                    print(f"\nEvent data: {datos.data_payload}")
                    await consumer.acknowledge(mensaje)

    except:
        logging.error(
            f'ERROR: While subscribing to topic! {topic}, {subscription}, {schema}')
        traceback.print_exc()
