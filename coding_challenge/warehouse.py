import random

from coding_challenge.exceptions.item_not_listed_in_store import ItemNotListedInStore
from coding_challenge.exceptions.item_out_of_stock import ItemOutOfStock
from item import Item
from rules.discount_rule import DiscountRule


def generate_random_inventory(amount_of_items_to_generate: int = 10) -> dict:
    """
    Generate a random set of inventory for the store
    :param amount_of_items_to_generate:
    :return: A random inventory that can be used by a store.
    """
    inventory = {}
    for i in range(1, amount_of_items_to_generate + 1):
        item_id = f"A{i:04}"
        price = round(random.uniform(5.0, 100.0), 2)
        item = Item(item_id, price)
        quantity = random.randint(1, 50)
        inventory[item_id] = (item, quantity)
    return inventory


class Warehouse:

    def __init__(self, currency: str = "€"):
        self.__inventory = generate_random_inventory()
        self.__discount_rules = {}
        self.__currency = currency

    @property
    def inventory(self) -> dict:
        return self.__inventory

    def add_item(self, item: Item, quantity: int = 1):
        """
        Adds an item to the inventory.

        If the item already exists in the inventory, its quantity is increased
        by the specified amount. If the item does not exist, it is added to the
        inventory with the specified quantity.

        :param item: The item to be added to the inventory.
        :param quantity: The number of items to be added. Must be a non-negative integer. Default is 1.

        :raises ValueError: If the quantity is negative.

        :return: None
        """
        if quantity < 0:
            raise ValueError("Cannot add negative amount to inventory")

        if item.item_id in self.__inventory:
            _, current_quantity = self.__inventory[item.item_id]
            self.__inventory[item.item_id] = (item, current_quantity + quantity)
        else:
            self.__inventory[item.item_id] = (item, quantity)

    def remove_item(self, item: Item, quantity: int = 1):
        """
        Removes an item from the inventory.

        :param item: The item object to be removed.
        :param quantity: The number of items to remove. Must be a positive integer. Defaults to 1.

        :raises ValueError: If the quantity is negative.
        :raises ItemOutOfStock: If the item does not exist in the inventory or the requested quantity is greater than the available stock.

        :return: None
        """
        if quantity < 0:
            raise ValueError("Cannot remove negative amount from inventory")

        if item.item_id in self.__inventory:
            _, current_quantity = self.__inventory[item.item_id]
            if current_quantity >= quantity:
                new_quantity = current_quantity - quantity
                if new_quantity == 0:
                    del self.__inventory[item.item_id]
                else:
                    self.__inventory[item.item_id] = (item, new_quantity)
            else:
                raise ItemOutOfStock("Not enough items in inventory.")
        else:
            raise ItemOutOfStock("Item does not exist in inventory.")

    def list_inventory(self):
        """
        Prints the details of all items in the inventory.

        This function iterates through the inventory and prints information for each item, including its ID, price, and quantity.

        :return: None
        """
        for item_id, (item, quantity) in self.__inventory.items():
            print(f"Item ID: {item.item_id}, Price: {item.price}, Quantity: {quantity}")

    def take_item(self, item_id: str, quantity: int = 1) -> Item:
        """
        Retrieves an item from the inventory.

        :param item_id: The ID of the item to retrieve (string).
        :param quantity: The number of items to retrieve (defaults to 1). Must be positive.

        :raises ItemNotListedInStore: If the item with the provided ID is not found in the inventory.
        :raises ItemOutOfStock: If the requested quantity is greater than the available stock for the item.

        :return: The item that was took from the inventory if successfully.
        """
        if item_id not in self.__inventory:
            raise ItemNotListedInStore(message="The item with the id {0} is not listed by the store".format(item_id))
        else:
            item, current_quantity = self.__inventory[item_id]
            if current_quantity < quantity:
                raise ItemOutOfStock("Not enough items in inventory.")
            return item

    def add_discount_rule(self, item_id: str, discount_rule: DiscountRule):
        """
        Associates a discount rule with a specific item in the inventory.

        :param item_id: The ID of the item to associate the discount with (string).
        :param discount_rule: The DiscountRule object defining the discount.

        :raise ItemNotListedInStore: If the item with the provided ID is not found in the inventory.

        :return: None
        """
        if item_id in self.__inventory:
            self.__discount_rules[item_id] = discount_rule
        else:
            raise ItemNotListedInStore(message="The item with the id {0} is not listed by the store".format(item_id))

    def get_discount_rule(self, item_id: str) -> DiscountRule:
        """
        Retrieves the discount rule associated with an item in the inventory.

        :param item_id: The ID of the item to get the discount rule for (string).

        :return: DiscountRule: The discount rule object associated with the item, or None if no rule exists.
        """
        return self.__discount_rules.get(item_id, None)

    def discount_available(self, item_id: str) -> bool:
        """
        Checks if a discount is available for a specific item in the inventory.

        :param item_id: The ID of the item to check for a discount (string).

        :returns: bool: True if a discount rule is associated with the item, False otherwise.
        """
        return item_id in self.__discount_rules

    def currency(self) -> str:
        """
        Returns the currency used by the inventory system.

        :return: str: The currency symbol or code.
        """
        return self.__currency
