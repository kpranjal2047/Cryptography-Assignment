class User:

    def __init__(self):
        self.__uname__: str
        self.__passwd__: str

    def getName(self) -> str:
        return self.__uname__

    def setName(self, name: str) -> None:
        self.__uname__ = name

    def getPass(self) -> str:
        return self.__passwd__

    def setPass(self, passwd: str) -> None:
        self.__passwd__ = passwd
