from dataclasses import dataclass
from typing import List
import json
import uuid

@dataclass()
class Inventory:
    product_id: uuid.uuid4()
    product_name: str
    storage_location: str
    quantity: int

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "storage_location": self.storage_location,
            "quantity": self.quantity,
        }

@dataclass(frozen=True)
class Order:
    order_id: uuid.uuid4()
    customer_id: uuid.uuid4()
    order_date: str
    order_status: str
    order_items: List[dict]
    order_total: float
    order_version: int = 2

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "order_date": self.order_date,
            "order_status": self.order_status,
            "order_items": json.dumps(self.order_items),
            "order_total": self.order_total,
            "order_version": self.order_version
        }