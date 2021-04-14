class Record:

    def __init__(self):
        self.__teacher__ = ''
        self.__student__ = ''
        self.__data__ = []

    def addUsers(self, teacher: str, student: str) -> None:
        self.__teacher__ = teacher
        self.__student__ = student

    def addData(self, acad_data: str) -> None:
        self.__data__.append(acad_data)

    def getTeacher(self) -> str:
        return self.__teacher__

    def getStudent(self) -> str:
        return self.__student__

    def printData(self) -> None:
        for data in self.__data__:
            print(data)
