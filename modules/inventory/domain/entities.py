from dataclasses import dataclass
from typing import List
import uuid
from datetime import datetime


@dataclass(frozen=True)
class Inventory:
    order_id: uuid.uuid4()
    customer_id: uuid.uuid4()
    order_date: str
    order_status: str
    order_items: List[dict]
    order_total: float
    order_version: int = 2
    despacho_date: str
    pod_id: str


    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "order_date": self.order_date,
            "order_status": self.order_status,
            "order_items": self.order_items,
            "order_total": self.order_total,
            "order_version": self.order_version,
            "despacho_date": self.despacho_date,
            "pod_id": self.pod_id
        }