class User:

    def __init__(self):
        self.__firstname = "Max"
        self.__lastname = "Mustermann"
        self.__username = ".".join((self.__firstname.lower(), self.__lastname.lower()))
        self.__email = "@".join((self.__username, "example.org"))

    def __str__(self):
        return f"User(firstname={self.__firstname}," \
               f" lastname={self.__lastname}," \
               f" username={self.__username}," \
               f" email={self.__email})"
