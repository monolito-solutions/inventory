from sqlalchemy import String, Column, Float, Integer, Text
from config.db import Base

class InventoryDTO(Base):
    __tablename__ = "inventory"

    order_id = Column(String(36), primary_key=True, index=True)
    customer_id = Column(String(36), index=True)
    order_date = Column(String(100), index=True)
    order_status = Column(String(100), index=True)
    order_items = Column(Text(1000000), index=True)
    order_total = Column(Float, index=True)
    order_version = Column(Integer, index=True)