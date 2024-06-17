from abc import ABC, abstractmethod
from coding_challenge.item import Item


class DiscountRule(ABC):
    def __init__(self, item: Item):
        self._item = item

    @abstractmethod
    def apply(self, quantity: int) -> float:
        NotImplementedError("Discount rule not implemented")
