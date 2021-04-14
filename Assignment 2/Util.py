import hashlib
import random


def applySha256(input: str) -> str:
    return hashlib.sha256(input.encode()).hexdigest()


def getDifficultyString(difficulty: int) -> str:
    return '0' * difficulty


def zkpdiscretelog(y1: int) -> bool:
    print('\nKindly verify yourself as a user')
    print('Zero Knowledge Proof')
    print('Choose a random number between 0 and 9 (r)')
    h = int(input('Please compute h = (2^r) mod 11 and Enter h: '))
    print('h is ' + str(h))
    b = random.randint(0, 1)
    print('Random bit(b) is: ' + str(b))
    s = int(input('''
Please compute s = (r + b*x) mod 10.
Here x is the number you are proving you know (i.e., the password): 
'''))
    val1 = pow(2, s, 11)
    val2 = (h * pow(y1, b, 11)) % 11
    if val1 == val2:
        print('Zero Knowledge Proof Successful.You are verified as registered user\n')
        return True
    else:
        print('Zero Knowledge Proof Failed.Please try again\n')
        return False
