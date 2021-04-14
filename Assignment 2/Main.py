import pickle
from os.path import exists

from Block import Block
from Record import Record
from User import User
from Util import zkpdiscretelog

difficulty = 4
previousHash = '0'
blockchain = []
records = []
users = []
teachers = []
p = 11
g = 2

if exists('state'):
    while True:
        opt = input('Previous data found... Import? (yes/no): ')
        if opt == 'yes':
            with open('state', 'rb') as f:
                previousHash, blockchain, records, users, teachers = pickle.load(f)
            print('Import Successful')
            break
        elif opt == 'no':
            break
        else:
            print('Unrecognized option\n')


def verifyTransaction(record: list, previousHash: str, data: Record) -> str:
    print('Trying to mineBlock...')
    block = Block(record, previousHash, data)
    block.mineBlock(difficulty)
    if verifyChain(block):
        blockchain.append(block)
    return block.getBlockHash()


def verifyChain(block: Block) -> bool:
    for i in range(1, len(blockchain)):
        if not blockchain[i].getPreviousHash() == blockchain[i-1].getBlockHash():
            return False
    if len(blockchain) > 0 and not blockchain[-1].getBlockHash() == block.getPreviousHash():
        return False
    return True


def viewUser() -> None:
    value = input('Are you a teacher or student? (t/s): ')
    if value == 't':
        teac = input('Enter your name: ')
        passwd = input('Enter your pass: ')
        flag = False
        for teacher in teachers:
            if teacher.getName() == teac and teacher.getPass() == passwd:
                for block in blockchain:
                    if block.teacher_name() == teac:
                        print(
                            'TimeStamp at which data was recorded: ' + str(block.getTimeStamp()))
                        print('Teacher:' + teac)
                        print('Student:' + block.student_name())
                        print('His Academic Data:')
                        block.printData()
                        print()
                        flag = True
                if flag:
                    break
        if not flag:
            print('Teacher Not Found')
    elif value == 's':
        stud = input('Enter your name: ')
        y = 0
        for user in users:
            if user.getName() == stud:
                x = int(user.getPass())
                y = pow(g, x, p)
        if not zkpdiscretelog(y):
            return
        flag = False
        for user in users:
            if user.getName() == stud:
                for block in blockchain:
                    if block.student_name() == stud:
                        print('Time: ' + str(block.getTimeStamp()))
                        print('Teacher:' + block.teacher_name())
                        print('Student:' + stud)
                        print("Student's Academic Data:")
                        block.printData()
                        print()
                        flag = True
                if flag:
                    break
        if not flag:
            print('Student Not Found')
    else:
        print('Option not recognized')


if __name__ == '__main__':
    teacher1 = User()
    teacher1.setName('Abhik')
    teacher1.setPass('1')
    teachers.append(teacher1)
    users.append(teacher1)

    teacher2 = User()
    teacher2.setName('Pranjal')
    teacher2.setPass('2')
    teachers.append(teacher2)
    users.append(teacher2)

    teacher3 = User()
    teacher3.setName('Yash')
    teacher3.setPass('3')
    teachers.append(teacher3)
    users.append(teacher3)

    choice = 'yes'
    while choice == 'yes':
        option = input('What do you want to do? (view/add/register): ')

        if option == 'register':
            name = input('Enter name: ')
            passwd = input('Enter password (integer only): ')
            passwd_v = input('Verify password: ')
            if passwd == passwd_v:
                new_student = User()
                new_student.setName(name)
                new_student.setPass(passwd)
                users.append(new_student)
            else:
                print('Password verification failed')

        elif option == 'add':
            tname = input('Enter teacher name: ')
            tpass = input('Enter teacher password: ')
            sname = input('Enter student name: ')
            y = 0
            for user in users:
                if user.getName() == sname:
                    x = int(user.getPass())
                    y = pow(g, x, p)
            if not zkpdiscretelog(y):
                continue

            new_rec = Record()
            new_rec.addUsers(tname, sname)

            flag = False

            for teacher in teachers:
                if teacher.getName() == tname and teacher.getPass() == tpass:
                    for user in users:
                        if user.getName() == sname:
                            while True:
                                ip = input('Enter data (y/n): ')
                                if ip == 'y':
                                    newdata = input('Enter Data: ')
                                    new_rec.addData(newdata)
                                elif ip == 'n':
                                    records.append(new_rec)
                                    previousHash = verifyTransaction(
                                        records, previousHash, new_rec)
                                    flag = True
                                    break
                                else:
                                    print('Option not recognized')
                        if flag:
                            break
                if flag:
                    break
            if not flag:
                print('Something Wrong!!!')

        elif option == 'view':
            viewUser()

        choice = input('Do you want to continue? (yes/no): ')

    with open('state', 'wb') as f:
        dump = (previousHash, blockchain, records, users, teachers)
        pickle.dump(dump, f)
