"""file defines OrderBook"""

import heapq


class OrderBook:
    """Class representing the Order book.

    An order book maintains two separate queues to track the submitted orders.
    The buy queue is a priority queue (max heap) sorted by order price.
    The sell queue is a priority queue (min heap) sorted by order price.
    The order queue exposes APIs to push-to or pop-from these queues.
    Given an order id, it should be possible to cancel the corresponding order.

    Attributes:
        None
    """

    def __init__(self):
        """Inits OrderBook class, initializes empty buy and sell queues"""
        # descending
        self.buy = []
        # ascending
        self.sell = []

    def __str__(self):
        """returns string representation of the object"""
        buy_str = f"BUY Queue: [{', '.join(list(map(str, [buyorder[1] for buyorder in self.buy])))}]"
        sell_str = f"SELL Queue: [{''.join(list(map(str, [sellorder[1] for sellorder in self.sell])))}]"
        return buy_str + "\n" + sell_str

    def push_to_buy_queue(self, order):
        """Pushes an order to buy queue

        Args:
            order: Order object
        """
        heapq.heappush(self.buy, (-order.price, order))

    def push_to_sell_queue(self, order):
        """Pushes an order to sell queue

        Args:
            order: Order object
        """
        heapq.heappush(self.sell, (order.price, order))

    def pop_buy(self):
        """Pops an order from buy queue"""
        return heapq.heappop(self.buy)[1]

    def pop_sell(self):
        """Pops an order from sell queue"""
        return heapq.heappop(self.sell)[1]

    def cancel_order(self, order_id):
        """Pops an order from sell queue

        Args:
            order_id: uid of order
        """
        for idx, order in enumerate(self.sell):
            if order.uid == order_id:
                self.sell[idx] = self.sell[-1]
                self.sell.pop()
                heapq.heappop(self.sell)
                # return at this point, no need to check buy queue
                return

        for idx, order in enumerate(self.buy):
            if order.uid == order_id:
                self.buy[idx] = self.buy[-1]
                self.buy.pop()
                heapq.heappop(self.buy)
