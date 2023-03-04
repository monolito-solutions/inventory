from uuid import UUID
from modules.inventory.domain.entities import Inventory
from .dtos import InventoryDTO
from sqlalchemy.exc import NoResultFound

class InventoryRepositorySQLAlchemy:

    def __init__(self, db) -> Inventory:
        self.db = db

    def get_by_id(self, id: UUID) -> Inventory:
        try:
            inventory_dto = self.db.query(InventoryDTO).filter_by(product_id=str(id)).one()
            print(f'\get_by_id inventory_dto: {inventory_dto}')
            return Inventory(**inventory_dto.to_dict())
        except NoResultFound:
            return None


    def create(self, inventory: Inventory):
        inventory_dto = InventoryDTO(**inventory.to_dict())
        self.db.add(inventory_dto)
        self.db.commit()
        self.db.refresh(inventory_dto)
        return inventory_dto

    def update(self, inventory: Inventory):
        inventory_dto = self.db.query(InventoryDTO).filter_by(product_id=str(inventory.product_id)).one()
        inventory_dto.quantity = inventory.quantity
        self.db.commit()
        return inventory_dto

    def delete(self, id: UUID):
        # TODO
        raise NotImplementedError
