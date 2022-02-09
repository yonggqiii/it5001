""" Entry point for the matching engine """

from collections import defaultdict
from matching_engine import MatchingEngine
from excepts import InvalidInputError


def parse_order(order):
    """Parses the order from the input string
    Args:
        order: the order string to be parsed, one of the following formats
            - SUB, type, side, order_id, quantity, price
            - CXL order_id
    Returns:
        the order defaultdict
    Raises:
        InvalidInputError: if the input is not of the correct format
    """
    order_dict = defaultdict(lambda: None)
    order_list = order.split()

    order_dict["action"] = order_list[0]

    if order_dict["action"] == "CXL":
        order_dict["id"] = order_list[1]
    elif order_dict["action"] == "SUB":
        order_dict["type"] = order_list[1]
        order_dict["side"] = order_list[2]
        order_dict["id"] = order_list[3]
        order_dict["quantity"] = int(order_list[4])
        try:
            # some orders may not have a price
            order_dict["price"] = int(order_list[5])
        except IndexError:
            pass
    else:
        raise InvalidInputError()

    return order_dict


if __name__ == "__main__":
    matching_engine = MatchingEngine.get_instance()
    while True:
        line = input()
        if line == "END":
            print(matching_engine.order_book)
            break

        order_dict = parse_order(line)
        matching_engine.process_order(order_dict)
