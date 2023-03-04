from uuid import UUID
from modules.inventory.domain.entities import Inventory
from .dtos import InventoryDTO


class OrdersRepositorySQLAlchemy:

    def __init__(self, db) -> None:
        self.db = db

    def get_by_id(self, id: UUID) -> Inventory:
        order_dto = self.db.session.query(InventoryDTO).filter_by(id=str(id)).one()
        return Inventory(**order_dto.to_dict())

    def create(self, Inventory: Inventory):
        order_dto = InventoryDTO(**Inventory.to_dict())
        self.db.add(order_dto)
        self.db.commit()
        self.db.refresh(order_dto)
        return order_dto

    def delete(self, id: UUID):
        # TODO
        raise NotImplementedError
