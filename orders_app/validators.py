from orders_app.enums import OrderStatus
from orders_app.models import Order


def is_order_executed(order: Order):
    return order.status == OrderStatus.EXECUTED.value
