class Record:

    def __init__(self):
        self.__doctor__ = ''
        self.__patient__ = ''
        self.__data__ = []

    def addUsers(self, doctor: str, patient: str) -> None:
        self.__doctor__ = doctor
        self.__patient__ = patient

    def addData(self, medData: str) -> None:
        self.__data__.append(medData)

    def getDoctor(self) -> str:
        return self.__doctor__

    def getPatient(self) -> str:
        return self.__patient__

    def printData(self) -> None:
        for data in self.__data__:
            print(data)
