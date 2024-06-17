from user import User
from warehouse import Warehouse


class Basket:

    def __init__(self, user: User, warehouse: Warehouse):
        if user is None:
            raise ValueError("User cannot be none")
        if warehouse is None:
            raise ValueError("Warehouse cannot be none")
        self.__user = user
        self.__warehouse = warehouse
        self.__items_in_basket = {}

    def scan(self, item_id: str, quantity: int = 1):
        item = self.__warehouse.take_item(item_id, quantity=quantity)
        if item_id in self.__items_in_basket:
            self.__items_in_basket[item_id]['quantity'] += quantity
        else:
            self.__items_in_basket[item_id] = {'item': item, 'quantity': quantity}
        self.__warehouse.remove_item(item=item, quantity=quantity)
        print(f"Item {item_id} added to the basket.")

    def total(self) -> float:
        total_price = 0.0
        for item_id, item_info in self.__items_in_basket.items():
            if self.__warehouse.discount_available(item_id=item_id):
                discount_rule = self.__warehouse.get_discount_rule(item_id=item_id)
                total_price += discount_rule.apply(quantity=item_info['quantity'])
            else:
                total_price += item_info["item"].price * item_info['quantity']
        return total_price

    def get_basket_contents(self):
        for item_id, item_info in self.__items_in_basket.items():
            item = item_info['item']
            quantity = item_info['quantity']
            print(f"Item ID: {item_id}, Price: {item.price}, Quantity: {quantity}")

    def empty(self):
        for item_id, item_info in self.__items_in_basket.items():
            item = item_info['item']
            quantity = item_info['quantity']
            self.__warehouse.add_item(item=item, quantity=quantity)
        self.__items_in_basket.clear()
        print("Basket has been emptied.")

    def is_empty(self) -> bool:
        return len(self.__items_in_basket) == 0
