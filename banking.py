# Write your code here
import random
import sqlite3

conn = None

conn = sqlite3.connect('card.s3db')

cur = conn.cursor()

def drop_table():
    cur.execute("DROP TABLE card;")
    conn.commit()

def create_table():
    cur.execute('CREATE TABLE card ('
                'id INTEGER,'
                'number TEXT,'
                'pin TEXT,'
                'balance INTEGER DEFAULT 0);')
    conn.commit()
# drop_table()
# create_table()
def add_account(acc_num, acc_pin):
    cur.execute("INSERT INTO card (number, pin) VALUES (?, ?)", (acc_num, acc_pin, ))
    conn.commit()

def search_account(acc_num):
    cur.execute("SELECT * FROM card WHERE (number = ?)", (acc_num, ))
    output = cur.fetchall()
    if len(output) == 0:
        return True
    return False

def add_income(amount, acc_num):
    cur.execute("SELECT * FROM card WHERE (number = ?)", (acc_num, ))
    balance = cur.fetchall()[0][3]
    balance += amount
    cur.execute("UPDATE card SET balance = ? WHERE (number = ?)", (balance, acc_num, ))
    conn.commit()

def remove_income(amount, acc_num):
    cur.execute("SELECT * FROM card WHERE (number = ?)", (acc_num, ))
    balance = cur.fetchall()[0][3]
    balance -= amount
    cur.execute("UPDATE card SET balance = ? WHERE (number = ?)", (balance, acc_num, ))
    conn.commit()

def delete_account(acc_num):
    cur.execute("DELETE FROM card WHERE number = ?", (acc_num, ))
    conn.commit()
def avail_balance(acc_num):
    cur.execute("SELECT * FROM card WHERE (number = ?)", (acc_num, ))
    balance = cur.fetchall()[0][3]
    return balance
# --------------------------------------------------

def luhn_algorithm(account_num):
    account_num = [int(x) for x in account_num]
    sum = 0
    for i in range(len(account_num)):
        if i % 2 == 0:
            account_num[i] *= 2
        if account_num[i] > 9:
            account_num[i] -= 9
        sum += account_num[i]
    if sum % 10 is 0:
        return 0
    return 10 - sum % 10

def new_account():
    while True:
        account_number = random.sample(range(10), 9)
        account_number = '400000' + ''.join([str(x) for x in account_number])
        check_sum = luhn_algorithm(account_number)
        account_number += str(check_sum)
        if (search_account(account_number)):
            return account_number
def new_pin():
    pin = random.sample(range(10), 4)
    pin = ''.join([str(x) for x in pin])
    return pin
def create_account():
    card_number = new_account()
    pin = new_pin()
    # account_details[card_number] = pin
    add_account(card_number, pin)
    print('Your card number:', card_number, sep='\n')
    print('Your card PIN:', pin, sep='\n')

def log_in(acc_num, acc_pin):
    cur.execute("SELECT * FROM card WHERE number = ? AND pin = ?", (acc_num, acc_pin, ))
    account = cur.fetchall()
    conn.commit()
    if len(account) == 0:
        print('Wrong card number or PIN')
        return
    print('You have successfully logged in!')
    while True:
        option = int(input('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit\n'''))
        if option is 1:
            balance = avail_balance(acc_num)
            print('Balance: {}'.format(balance))

        if option is 2:
            income = int(input('Enter income:\n'))
            add_income(income, acc_num)
            print('Income was added!')

        if option is 3:
            print('Transfer')
            card_number = input('Enter card number:\n')
            luhn_algo_last_digit = luhn_algorithm(card_number[0:15])

            if (str(luhn_algo_last_digit) != card_number[15]):
                print('Probably you made a mistake in the card number. Please try again!')
                continue

            if (search_account(card_number)):
                print('Such a card does not exist.')
                continue

            if (acc_num == card_number):
                print("You can't transfer money to the same account!")
                continue

            amount = int(input('Enter how much money you want to transfer:\n'))
            avail_bal = avail_balance(acc_num)

            if amount > avail_bal :
                print('Not enough money!')
            else:
                add_income(amount, card_number)
                remove_income(amount, acc_num)
                print('Success!')

        if option is 4:
            delete_account(acc_num)
            print('Your account has been closed!')
            break

        if option is 5:
            print('You have successfully logged out!')
            break

        if option is 0:
            print('Bye!')
            exit()
    return





# landing menu

while True:
    option = int(input('''1. Create an account
2. Log into account
0. Exit\n'''))

    if option is 1:
        create_account()

    if option is 2:
        account_num = input('Enter your card number:\n')
        pin = input('Enter your PIN:\n')
        log_in(account_num, pin)

    if option is 0:
        print('Bye!')
        exit()
