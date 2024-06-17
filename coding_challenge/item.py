from exceptions.item_id_already_exists_exception import ItemIdAlreadyExistsException


class Item:
    __item_ids = []

    def __init__(self, item_id: str, price: float):
        if item_id in Item.__item_ids:
            raise ItemIdAlreadyExistsException(message="Item id {0} already used by another Item".format(item_id))
        else:
            Item.__item_ids.append(item_id)
        self.__item_id = item_id
        self.__price = price

    @property
    def item_id(self) -> str:
        return self.__item_id

    @item_id.setter
    def item_id(self, item_id: str):
        raise NotImplementedError("The item_id of an article cannot be changed")

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, price: float):
        self.__price = price
