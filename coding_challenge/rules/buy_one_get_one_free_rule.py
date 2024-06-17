from coding_challenge.item import Item
from coding_challenge.rules.discount_rule import DiscountRule
from math import floor


class BuyOneGetOneFreeRule(DiscountRule):
    def __init__(self, item: Item):
        super().__init__(item)

    def apply(self, quantity: int) -> float:
        free = floor(quantity / 2)
        items_to_pay = quantity - free
        return self._item.price * items_to_pay
