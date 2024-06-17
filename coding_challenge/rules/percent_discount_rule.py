from coding_challenge.item import Item
from coding_challenge.rules.discount_rule import DiscountRule


class PercentDiscountRule(DiscountRule):

    def __init__(self, item: Item, discount: float):
        super().__init__(item)
        if discount > 1.0 or discount <= 0.0:
            raise ValueError("Invalid percentage")
        self.__discount = discount

    def apply(self, quantity: int) -> float:
        return self._item.price * quantity * (1.0 - self.__discount)
