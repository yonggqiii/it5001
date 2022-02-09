"""file defines various types of orders"""

from abc import ABC, abstractmethod


class Order(ABC):
    """Defines an abstract type for an order

    An order is any transaction that is carried out by the matching engine.
    There are different types of orders and each has a different behavior of getting executed.
    However, all the orders are expected to get executed depending on the attributes defined below.

    Attributes:
        uid: A unique identifier string for the order
        type: A string indicating type of the order, possible values:
            -LO: Limit Order
        side: A string indicating the side of the order, possible values:
            -B: Buy Order
            -S: Sell Order
        quantity: An int indicating no of units requested for trade
        price: A float indicating the price of each unit
    """

    # pylint: disable=C0103
    def __init__(self, action, uid, type, side, quantity, price):
        """Inits Order class and its attributes"""
        self.action = action
        self.uid = uid
        self.type = type
        self.side = side
        self.quantity = quantity
        self.price = price

        super().__init__()

    def __lt__(self, other):
        """defines less than operator for order comparision"""
        return self.price < other.price

    @abstractmethod
    def __str__(self):
        """Abstract method enables string rep of the order"""

    @abstractmethod
    def _execute_sell_order(self, order_book):
        """Private abstract method enables sell order execution"""
        return

    @abstractmethod
    def _execute_buy_order(self, order_book):
        """Private abstract method enables buy order execution"""
        return

    @abstractmethod
    def execute(self, order_book):
        """Abstract method enables order execution"""
        return


class LimitOrder(Order):
    """Defines a Limit Order which is an Order type.

    A Limit order either gets fully executed or is not executed at all.
    If a buy limit order is requested, it is matched with the sell queue in the order book.
    If the sell price <= buy price, the order gets executed.
    Otherwise, it is added to the buy queue in the order book.
    If a sell limit order is requested, it is matched with the buy queue in the order book.
    If the buy price >= sell price, the order gets executed.
    Otherwise, it is added to the sell queue in the order book.

    Attributes:
        Same as the parent class.
    """

    def __str__(self):
        return f"({self.uid} {self.type} {self.side} {self.quantity} {self.price})"

    def execute(self, order_book):
        """Executes a Limit Order

        Args:
            order_book: OrderBook object to manage the buy/sell queue.
        Returns:
            The total sale as float
        """
        if self.side == "B":
            self._execute_buy_order(order_book)
        elif self.side == "S":
            self._execute_sell_order(order_book)

    def _execute_buy_order(self, order_book):
        """Executes a buy limit order.

        Args:
            order_book: OrderBook object to manage the buy/sell queue.
        Returns:
            The total sale as float
        """
        # maintain a history of orders executed
        sell_orders = []
        # track the quantity remaining to buy
        buy_quantity = self.quantity

        while order_book.sell and buy_quantity > 0:
            curr_sell_order = order_book.pop_sell()
            if curr_sell_order.price > self.price:
                break
            if curr_sell_order.quantity > buy_quantity:
                # this will happen only when order gets complete, handle the residue
                curr_sell_order.quantity -= buy_quantity
                order_book.push_to_sell_queue(curr_sell_order)

            # update buy quantity
            buy_quantity -= min(buy_quantity, curr_sell_order.quantity)
            sell_orders.append(curr_sell_order)

        if buy_quantity > 0:
            # restore the orders
            for order in reversed(sell_orders):
                order_book.push_to_sell_queue(order)
            # add the current order to queue
            order_book.push_to_buy_queue(self)

    def _execute_sell_order(self, order_book):
        """Executes a sell limit order.

        Args:
            order_book: OrderBook object to manage the buy/sell queue.
        Returns:
            The total sale as float
        """
        # maintain a history of orders executed
        buy_orders = []
        # track the quantity remaining to sell
        sell_quantity = self.quantity

        while order_book.buy and sell_quantity > 0:
            curr_buy_order = order_book.pop_buy()
            if curr_buy_order.price < self.price:
                break
            if curr_buy_order.quantity > sell_quantity:
                # this will happen only when order gets complete, handle the residue
                curr_buy_order.quantity -= sell_quantity
                order_book.push_to_buy_queue(curr_buy_order)

            # update sell quantity
            sell_quantity -= min(sell_quantity, curr_buy_order.quantity)
            print(sell_quantity)
            buy_orders.append(curr_buy_order)

        if sell_quantity > 0:
            # restore the orders
            for order in reversed(buy_orders):
                order_book.push_to_buy_queue(order)
            # add the current order to queue
            order_book.push_to_sell_queue(self)
