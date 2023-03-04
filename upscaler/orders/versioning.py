from modules.orders.domain.entities import OrderV1, OrderV2
from api.errors.exceptions import BaseAPIException


def detect_order_version(order):
    """Detects the version of the order and returns the corresponding object."""
    try:
        return OrderV2(**order)
    except TypeError:
        try:
            return OrderV1(**order).upscale()
        except TypeError:
            raise BaseAPIException("Order version not supported")