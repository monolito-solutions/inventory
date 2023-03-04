from pulsar.schema import *
from utils import time_millis
import uuid


class DispatchOrderPayload(Record):
    order_id = String()
    customer_id = String()
    order_date = String()
    order_status = String()
    order_items = String()
    order_total = Float()
    order_version = Long()


class CommandDispatchOrder(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v2")
    type = String(default="CommandDispatchOrder")
    datacontenttype = String()
    service_name = String(default="orders.entregasalpes")
    data_payload = DispatchOrderPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
