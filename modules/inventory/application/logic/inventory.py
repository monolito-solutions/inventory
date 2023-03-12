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

def check_inventory(order):
    try:
        order_is_ok = True
        db = get_db()

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

        print("Iniciando validacion de productos")
        for item in json.loads(params.order_items):
            inventory_tmp = repository.get_by_id(item["product_id"])
            print(f'\inventory: {inventory_tmp}')
            if inventory_tmp is None:
                order_is_ok = False
                break
            if(item["quantity"] <= inventory_tmp.quantity) :
                print(f'\Si hay inventario para el producto: {item["product_id"]}')
                inventory_tmp.quantity -= item["quantity"]
                repository.update(inventory_tmp)
            else:
                print(f'\Si NO hay inventario para el producto: {item["product_id"]}')
                order_is_ok = False
                break
            
        if(order_is_ok == True):
            order_success(order)
        else:
            order_error(order)
        
        db.close()
    except IntegrityError:
        raise BaseAPIException(f"Error checking order products", 400)
    except Exception as e:
        raise BaseAPIException(f"Error checking order : {e}", 500)


def order_success(order):
    event_payload = InventoryCheckedPayload(
        order_id = str(order.order_id),
        customer_id = str(order.customer_id),
        order_date = str(order.order_date),
        order_status = str(order.order_status),
        order_items = order.order_items,
        order_total = float(order.order_total),
        order_version = int(order.order_version)
    )
    event_payload.order_status = "Ready to dispatch"

    event = EventInventoryChecked(
        time = utils.time_millis(),
        ingestion = utils.time_millis(),
        datacontenttype = InventoryCheckedPayload.__name__,
        data_payload = event_payload
    )

    command_payload = DispatchOrderPayload(**event_payload.to_dict())

    command = CommandDispatchOrder(
        time = utils.time_millis(),
        ingestion = utils.time_millis(),
        datacontenttype = DispatchOrderPayload.__name__,
        data_payload = command_payload
    )

    dispatcher = Dispatcher()
    dispatcher.publish_message(event, "order-events")
    dispatcher.publish_message(command, "order-commands")


def order_error(order):
    event_payload = ErrorCheckingInventoryPayload(
        order_id = str(order.order_id),
        customer_id = str(order.customer_id),
        order_date = str(order.order_date),
        order_status = str(order.order_status),
        order_items = order.order_items,
        order_total = float(order.order_total),
        order_version = int(order.order_version)
    )
    event_payload.order_status = "Error checking orders products"

    event = EventErrorCheckingInventory(
        time = utils.time_millis(),
        ingestion = utils.time_millis(),
        datacontenttype = ErrorCheckingInventoryPayload.__name__,
        data_payload = event_payload
    )

    dispatcher = Dispatcher()
    dispatcher.publish_message(event, "order-events")
