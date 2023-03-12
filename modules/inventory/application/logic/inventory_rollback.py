from config.db import get_db
from fastapi import Depends
from modules.inventory.application.events.events import InventoryCheckedPayload, ProductPayload, EventInventoryChecked
from modules.inventory.infrastructure.repositories import InventoryRepositorySQLAlchemy
from modules.inventory.application.commands.commands import CommandDispatchOrder, DispatchOrderPayload
from sqlalchemy.exc import IntegrityError
from api.errors.exceptions import BaseAPIException
from infrastructure.dispatchers import Dispatcher
import utils
import json
from modules.inventory.domain.entities import Inventory, Order
from modules.products.domain.entities import Product

def revert_inventory(order):
    db = get_db()
    try:
        params = Order(
            order_id = order.order_id,
            customer_id = order.customer_id,
            order_date = order.order_date,
            order_status = order.order_status,
            order_items = json.loads(order.order_items),
            order_total = order.order_total,
            order_version = order.order_version
        )
        repository = InventoryRepositorySQLAlchemy(db)
        print(f'\params.order_items: {params.order_items}')

        print("Iniciando rollback de productos")
        for item in json.loads(params.order_items):
            inventory_tmp = repository.get_by_id(item["product_id"])
            print(f'\inventory: {inventory_tmp}')
            print(f'\Producto: {item["product_id"]}')
            inventory_tmp.quantity += item["quantity"]
            repository.update(inventory_tmp)
        
    except IntegrityError:
        raise BaseAPIException(f"Error rollback order products", 400)
    except Exception as e:
        raise BaseAPIException(f"Error rollback order : {e}", 500)
    finally:
        db.close()
