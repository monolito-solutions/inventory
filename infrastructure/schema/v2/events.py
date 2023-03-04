from pulsar.schema import String, Record, List, Float, Long
from utils.infrastructure.schema.v2.messages import Message

class OrderCreatedEvent(Record):
    order_id = String()
    customer_id = String()
    order_date = String()
    order_status = String()
    order_items = List()
    order_total = Float()
    order_version = Long()

class OrderCreatedPayload(Message):
    data = OrderCreatedEvent()
