import utils
from modules.inventory.application.events.events import EventInventoryChecked, InventoryCheckedPayload, ProductPayload
from modules.inventory.application.commands.commands import CommandDispatchOrder, DispatchOrderPayload
from infrastructure.dispatchers import Dispatcher
import json

print("Creating event...")

event_payload = InventoryCheckedPayload(
    order_id = "50030f67-d3b5-4943-b741-bf7b3f8314f2",
    customer_id = "0ba9db2f-45cd-462c-83da-d70061769a49",
    order_date = "2023-03-04T12:00:23Z",
    order_status = "Pendiente",
    order_items = json.dumps([{
    "product_id": "9cad4dc7-50c0-44d7-9ed9-3f887a9d565b",
    "supplier_id": "987eba3c-ae2b-4382-86f9-7ea238733e05",
    "name": "product1",
    "description": "Test Desc",
    "price": 33000.0,
    "quantity": 5
    }]),
    order_total = 124500.0,
    order_version = 1
)

event = EventInventoryChecked(
    time = utils.time_millis(),
    ingestion = utils.time_millis(),
    datacontenttype = InventoryCheckedPayload.__name__,
    data_payload = event_payload
)

command_payload = DispatchOrderPayload(**event_payload.to_dict())
command_payload.order_status = "Ready to check inventory"

command = CommandDispatchOrder(
    time = utils.time_millis(),
    ingestion = utils.time_millis(),
    datacontenttype = DispatchOrderPayload.__name__,
    data_payload = command_payload,
    type = "CommandCheckInventory"
)

dispatcher = Dispatcher()
dispatcher.publish_message(event, "order-events")
dispatcher.publish_message(command, "order-commands")

print("Event dispatched...")
