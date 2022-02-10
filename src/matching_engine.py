"""file defines MatchingEngine"""

from order_book import OrderBook
from order_factory import OrderFactory
from excepts import SingletonConstructorCallError


class MatchingEngine:
    """Defines a Singleton class for Matching Engine.

    A Matching Engine is responsible to coordinate the orders that are
    received on the platform. Every order is processed according to the
    action defined by the user.
    It maintains an order book to track the received orders.
    An order can be submitted to the orderbook or be cancelled using
    the order id.

    Attributes:
        __instance: class member, the singleton instance.
    """

    __instance = None

    @staticmethod
    def get_instance():
        """creates a singleton instance of MatchingEngine

        Args: None
        Returns:
            MatchingEngine instance
        """
        if MatchingEngine.__instance is None:
            MatchingEngine()
        return MatchingEngine.__instance

    def __init__(self):
        """inits MatchingEngine

        Args: None
        Returns: None
        Raises:
            Exception -> This is a singleton.
        """
        if MatchingEngine.__instance is not None:
            raise SingletonConstructorCallError

        self.order_book = OrderBook()
        MatchingEngine.__instance = self

    def process_order(self, order_dict):
        """Processes an order

        Args: order_dict, the defaultdict order from the parsed user input.
        Returns:
            -Total Sale: Float if SUB
            -0/1 if CXL
        """
        order = OrderFactory.create_order(order_dict["type"], order_dict)

        if order.action == "SUB":
            return order.execute(self.order_book)

        if order.action == "CXL":
            return self.order_book.cancel_order(order.id)
