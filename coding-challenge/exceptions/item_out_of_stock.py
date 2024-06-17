class ItemOutOfStock(Exception):
    """
    Exception raised when an item is out of stock.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
