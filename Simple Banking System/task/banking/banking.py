# Write your code here
import random
import sqlite3

# create db and table

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()


def luhn_checksum(card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10

def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0

class Accounts:

    def __init__(self):
        self.accounts = {}
        self.balance = {}
        self.current_account = []
        self.loggedin = False


    def status(self, bool):
        if bool == False:
            self.loggedin = False
        else:
            self.loggedin = True



    def create(self):
        #temp_one = ''
        temp_two = ''
        done = False
        while done != True:
            temp_one = ''
            for i in range(10):
                temp_one += str(random.randint(0, 9))
            temp_one = '400000' + temp_one

            if self.accounts.get(temp_one) is None and is_luhn_valid(temp_one) is True:
                for i in range(4):
                    temp_two += str(random.randint(0, 9))
                self.accounts.update({temp_one: temp_two})
                cur.execute('INSERT INTO card (number, pin) VALUES ("' + temp_one + '", "' + temp_two + '")')
                conn.commit()
                self.balance.update({temp_one: 0})
                print('\nYour card has been created\nYour card number:\n'
                      + temp_one + '\nYour card PIN:\n' + temp_two + '\n')
                done = True

    def login(self):
        print('\nEnter your card number:')
        card = input()
        print('Enter your PIN:')
        passw = input()

#        if self.accounts.get(card) and self.accounts.get(card) == passw:
        if cur.execute('SELECT number, pin FROM card WHERE number = "' + card + '" AND pin = "' + passw + '";') and cur.fetchall():
            print('\nYou have successfully logged in!')
            self.loggedin = True
            self.current_account = [card, passw]
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')

        else:
            print('\nWrong card number or PIN!\n')
            self.status(False)
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')

print('1. Create an account')
print('2. Log into account')
print('0. Exit')
button = 5
accs = Accounts()
while button != 0:
    current = int(input())
    if current == 1:
        if accs.loggedin == False:
            accs.create()
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')
        else:
            # print('Balance: ', accs.balance.get(accs.current_account))
            compare = accs.current_account
            cur.execute('SELECT balance FROM card WHERE number = "' + compare[0] + '" AND pin = "' + compare[1] + '";')
            print('Balance:', cur.fetchall()[0][0])
            print('\n1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
    elif current == 2:
        if not accs.loggedin:
            accs.login()
        elif accs.loggedin:
            print('Enter income:')
            cur.execute('SELECT balance FROM card WHERE number = "' + str(accs.current_account[0]) + '";')
            mybalance = cur.fetchall()[0][0]
            fin_income = int(input()) + mybalance
            len = 'UPDATE card SET balance =' + str(fin_income) + ' WHERE number = "' + str(accs.current_account[0]) + '";'
            cur.execute(len)
            conn.commit()
            print('Income was added!')
            print('\n1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
    elif current == 3 and accs.loggedin == True:
        print ('Transfer\nEnter card number:')
        tocard = int(input())
        cur.execute('SELECT number FROM card WHERE number = "' + str(tocard) + '";')
        card_exist = cur.fetchall()
        if card_exist != []:
            card_exist = card_exist[0][0]
        else:
            card_exist = 0
        # 4000002665039093 4549
        # 4000006719295551 9081
        if not is_luhn_valid(tocard):
            print('Probably you made a mistake in the card number. Please try again!')
            print('\n1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
        elif accs.current_account[0] == card_exist:
            print("You can't transfer money to the same account!")
            print('\n1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
        elif card_exist == 0:
            print ('Such a card does not exist.')
            print('\n1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
        elif tocard == accs.current_account[0]:
            print("You can't transfer money to the same account!")
            print('\n1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
        else:
            print('Enter how much money you want to transfer:')
            transfer_amount = int(input())
            if cur.execute('SELECT balance FROM card WHERE number = "' + str(accs.current_account[0]) + '";'):
                balancefrom = cur.fetchall()[0][0]
            if balancefrom >= transfer_amount:
                cur.execute('SELECT balance FROM card WHERE number = "' + str(tocard) + '";')
                balanceto = cur.fetchall()[0][0]
                end_balance = balanceto + transfer_amount
                cur.execute('UPDATE card SET balance =' + str(end_balance) + ' WHERE number = "' + str(tocard) + '";')
                conn.commit()
                cur.execute('UPDATE card SET balance =' + str(balancefrom-transfer_amount) + ' WHERE number = "' + str(accs.current_account[0]) + '";')
                conn.commit()
                print('Success!')
                print('\n1. Balance')
                print('2. Add income')
                print('3. Do transfer')
                print('4. Close account')
                print('5. Log out')
                print('0. Exit')
            else:
                print('Not enough money!')
                print('\n1. Balance')
                print('2. Add income')
                print('3. Do transfer')
                print('4. Close account')
                print('5. Log out')
                print('0. Exit')

    elif current == 4 and accs.loggedin == True:
        cur.execute('DELETE FROM card WHERE number ="' + str(accs.current_account[0]) + '";')
        conn.commit()
        accs.loggedin = False
        accs.current_account = []
        print('Success!')
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')


    elif current == 5 and accs.loggedin == True:
        print('You have successfully logged out!\n')
        accs.loggedin = False
        accs.current_account = []
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')

    else:
        button = 0
        accs.loggedin = False
        cur.close()
        print('Bye!')
