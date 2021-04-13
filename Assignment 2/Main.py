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
doctors = []
p = 11
g = 2

if exists('state'):
    while True:
        opt = input('Previous data found... Import? (yes/no): ')
        if opt == 'yes':
            with open('state', 'rb') as f:
                previousHash, blockchain, records, users, doctors = pickle.load(f)
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
    value = input('Are you a doctor or patient? (d/p): ')
    if value == 'd':
        doct = input('Enter your name: ')
        passwd = input('Enter your pass: ')
        flag = False
        for doctor in doctors:
            if doctor.getName() == doct and doctor.getPass() == passwd:
                for block in blockchain:
                    if block.doc_name == doct:
                        print(
                            'TimeStamp at which data was recorded: ' + str(block.getTimeStamp()))
                        print('Doctor:' + doct)
                        print('Patient:' + block.patient_name())
                        print('His Medical Data:')
                        block.printData()
                        print()
                        flag = True
                if flag:
                    break
        if not flag:
            print('Doctor Not Found')
    elif value == 'p':
        pat = input('Enter your name: ')
        y = 0
        for user in users:
            if user.getName() == pat:
                x = int(user.getPass())
                y = pow(g, x, p)
        if not zkpdiscretelog(y):
            return
        flag = False
        for user in users:
            if user.getName() == pat:
                for block in blockchain:
                    if block.patient_name() == pat:
                        print('Time: ' + str(block.getTimeStamp()))
                        print('Doctor:' + block.doc_name())
                        print('Patient:' + pat)
                        print("Patient's Medical Data:")
                        block.printData()
                        print()
                        flag = True
                if flag:
                    break
        if not flag:
            print('Patient Not Found')
    else:
        print('Option not recognized')


if __name__ == '__main__':
    doc1 = User()
    doc1.setName('Abhik')
    doc1.setPass('1')
    doctors.append(doc1)
    users.append(doc1)

    doc2 = User()
    doc2.setName('Pranjal')
    doc2.setPass('2')
    doctors.append(doc2)
    users.append(doc2)

    doc3 = User()
    doc3.setName('Yash')
    doc3.setPass('3')
    doctors.append(doc3)
    users.append(doc3)

    choice = 'yes'
    while choice == 'yes':
        option = input('What do you want to do? (view/add/register): ')

        if option == 'register':
            name = input('Enter name: ')
            passwd = input('Enter password (integer only): ')
            passwd_v = input('Verify password: ')
            if passwd == passwd_v:
                new_patient = User()
                new_patient.setName(name)
                new_patient.setPass(passwd)
                users.append(new_patient)
            else:
                print('Password verification failed')

        elif option == 'add':
            dname = input('Enter doctor name: ')
            dpass = input('Enter doctor password: ')
            pname = input('Enter patient name: ')
            y = 0
            for user in users:
                if user.getName() == pname:
                    x = int(user.getPass())
                    y = pow(g, x, p)
            if not zkpdiscretelog(y):
                continue

            new_rec = Record()
            new_rec.addUsers(dname, pname)

            flag = False

            for doctor in doctors:
                if doctor.getName() == dname and doctor.getPass() == dpass:
                    for user in users:
                        if user.getName() == pname:
                            while True:
                                ip = input('Enter data (y/n): ')
                                if ip == 'y':
                                    newdata = input()
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
        dump = (previousHash, blockchain, records, users, doctors)
        pickle.dump(dump, f)
