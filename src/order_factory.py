"""file defines OrderFactory"""

from order import LimitOrder, MarketOrder, IOCOrder, FOKOrder, GTCOrder


class OrderFactory:
    """Defines a factory for creating Orders

    A factory design pattern is used to create objects without exposing
    the logic to client and referring to the newly created object using a
    common interface.
    This factory creates different types of Orders depending on the type.

    Attributes:
        submit_orders: a class attribute dictionary that maintains the
        different types of orders.
    """

    submit_orders = {
        "LO": LimitOrder
    }

    @classmethod
    def create_order(cls, type, order_dict):
        """Creates the order object according to the type

        Args:
            cls: OrderFactory class method
            type: type of the order as string
            order_dict: parsed order dictionary from input

        Returns:
            order: Order object
        """
        return cls.submit_orders[type](
            order_dict["action"],
            order_dict["id"],
            order_dict["type"],
            order_dict["side"],
            order_dict["quantity"],
            order_dict["price"],
        )
