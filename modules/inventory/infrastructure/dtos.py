from sqlalchemy import String, Column, Float, Integer, Text
from config.db import Base

class InventoryDTO(Base):
    __tablename__ = "inventory"

    product_id = Column(String(36), primary_key=True, index=True)
    product_name = Column(String(36), index=True)
    storage_location = Column(String(36), index=True)
    quantity = Column(Integer(), index=True)


    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "storage_location": self.storage_location,
            "quantity": self.quantity,
        }