from time import time

import DES
import Util
from Record import Record


class Block:

    def __init__(self, record: list, previousHash: str, curr_med_data: Record, non=0):
        self.__non__ = non
        self.__curr_med_data__ = curr_med_data
        self.__previousHash__ = previousHash
        self.__timeStamp__ = int(time())
        self.__recordObj__ = record
        self.__blockHash__ = self.calculateHash()
        self.__desHash__ = ''

    def calculateHash(self) -> str:
        calculatedHash = Util.applySha256(
            self.__previousHash__ + str(self.__non__))
        return calculatedHash

    def mineBlock(self, difficulty: int) -> None:
        target = Util.getDifficultyString(difficulty)
        while not self.__blockHash__[0:difficulty] == target:
            self.__non__ += 1
            self.__blockHash__ = self.calculateHash()
        calculatedHash = self.__blockHash__.upper()
        first = DES.encrypt(calculatedHash[0:16])
        second = DES.encrypt(calculatedHash[16:32])
        third = DES.encrypt(calculatedHash[32:48])
        fourth = DES.encrypt(calculatedHash[48:64])
        self.__desHash__ = first + second + third + fourth
        print("Block Mined!!!  DES : " + self.__desHash__)

    def getPreviousHash(self) -> str:
        return self.__previousHash__

    def getBlockHash(self) -> str:
        return self.__blockHash__

    def getTimeStamp(self) -> int:
        return self.__timeStamp__

    def doc_name(self) -> str:
        return self.__curr_med_data__.getDoctor()

    def patient_name(self) -> str:
        return self.__curr_med_data__.getPatient()

    def printData(self) -> None:
        self.__curr_med_data__.printData()
