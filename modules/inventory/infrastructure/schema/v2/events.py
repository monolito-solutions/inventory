
from pulsar.schema import String, Record, Float, Long, Field, Array
import uuid
import time

def time_millis():
    return int(time.time() * 1000)

class ProductPayload(Record):
    product_id = String()
    supplier_id = String()
    name = String()
    description = String()
    price = Float()
    quantity = Long()

    def dict(self):
        return str({k: str(v) for k, v in asdict(self).items()})

class OrderCreatedPayload(Record):
    order_id = String()
    customer_id = String()
    order_date = String()
    order_status = String()
    order_items = String()
    order_total = Float()
    order_version = Long()

class OrderCreatedEvent(Record):
    id = String(default=str(uuid.uuid4()))
    ingestion = Long(default=time_millis())
    specversion = Long(default=2)
    data = OrderCreatedPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
