class ItemIdAlreadyExistsException(Exception):
    """
    Exception raised when a new item is created with an id that is already used by another item.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
