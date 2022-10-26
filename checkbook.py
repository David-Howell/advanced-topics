import os
import csv
import datetime
import pickle


class account:
    '''
    The account class holds the first and last name of the account holder as well as the balance
    
    These can be called with:
    
    .first
    .last
    and
    .balance

    .show_balance() will print the balance

    .withdraw(amount: float) will lower the balance by amount

    .deposit(amount: float) will raise the balance by amount

    .write() will write that account to the account file

    NOTE: Currently there can only be one account because there's only one account_file
            This will be addressed in a later version
    '''
    def __init__(self, first_name_, last_name_, balance_):
        self.first = first_name_
        self.last = last_name_
        self.balance = float(balance_)
        self.balance = round(self.balance, 2)


    def show_balance(self):
        print(f'''
    #~~~~~~~~~~<  BALANCE  >~~~~~~~~~~#

  {f"{money(self.balance)}":>23}
''')

    def withdraw(self, value):
        self.balance -= value
        self.balance = round(self.balance, 2)

    def deposit(self, value):
        self.balance += value
        self.balance = round(self.balance, 2)

    def write(self):
        file = open('account_file', 'wb')
        pickle.dump(acct, file)
        file.close()

    # def read(self):

# The money class will display floats as money
class money(float):
    def __str__(self):
        return f'${round(self, 2):.2f}'

if os.path.exists('ledger.txt') == False:
    print('''\n\n\n\n
#~~~~~~~~<  Welcome to Terminal Checkbook  >~~~~~~~#
#                                                  #
#  Follow the options below to begin your journey  #
#           to financial FREEDOM!!                 #
#                                                  #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
\n\n''')
    first_name = input('\nWhat is your first name?       : ')
    last_name = input('\nWhat is your last name?        : ')
    works = False
    while works == False:
        balance = input('\nWhat is your begining balance? : $')

        try:
            float(balance)
        except:
            print(f'\n  You input: {balance} \n  This can not be resolved as a dollar amount...\n')
            print('Please try again...\n\n')
            continue
        works = True

    acct = account(first_name, last_name, balance)

    acct.write()

    print(f'''\n\n
    Hello, {acct.first} {acct.last}!

    Congratulations on having {money(acct.balance)} in your account
''')



    with open('ledger.txt', 'w') as begin:
# write the init transaction to the ledger
        begin.write(f'''
        | Transaction type: |  Balance:  |
        |-------------------|------------|
        |   Init Deposit    |   {money(acct.balance)}  |''')
        begin.close()

    with open('account_file', 'rb') as acct_info:
        acct = pickle.load(acct_info)
        acct_info.close()

else:
    f = open('ledger.txt', 'r')
    opening = f.readlines()
    f.close()

    acct_info = open('account_file', 'rb')
    acct = pickle.load(acct_info)
    acct_info.close()       

    print(f'''
\n\n\n\n
#~~~~~~~~<  Welcome to Terminal Checkbook  >~~~~~~~#

           Thank you for returning {acct.first}!

    ''')


my_input = ''

print(f'''
Your Current Balance is: {money(acct.balance)}
-----------------------------------------''')

while my_input not in ['quit', 'q', 'close', 'exit', '4', 'four', 'stop']:
    print(f'''

Please select an option from the menu below:

1) View current balance
2) Make a Withdawl from your account
3) Make a Deposit into your account
4) exit

''')

    my_input = input('Enter your choice now!  : ')

    if my_input.lower() in ['1', 'one', 'show', 'balance']:
        acct.show_balance()
        continue

    if my_input.lower() in ['2', 'two', 'to', 'too']:
        amount = input('How Much Money do you want?  : $')

        try:
            float(amount)
        except:
            print(f'\n  You input: {amount} \n  This can not be resolved as a dollar amount...\n')
            print('Returning to main menu...\n\n')
            continue

        amount = float(amount)
        if amount > acct.balance:
            print('\nThat\'s more money than you have... $orry... XD\n\n')
            continue
            
        else:
            print(f'\nSure thing, I can give you {money(amount)}, no reciepts though!\n\n')

            acct.withdraw(amount)
            acct.write()

            print(f'{money(amount)} was withdrawn')
            acct.show_balance()
            continue
    
        continue

    if my_input in [3, '3', 'three', 'tree']:
        amount = input('How Much Money do you have for me?  : $')
        
        try:
            float(amount)
        except:
            print(f'\n  You input: {amount} \n  This can not be resolved as a dollar amount...\n')
            print('Returning to main menu...\n\n')
            continue
        
        amount = float(amount)

        acct.deposit(amount)
        acct.write()

        print(f'{money(amount)} was deposited')
        acct.show_balance()
        continue
    
    if my_input in ['quit', 'q', 'close', 'exit', '4', 'four', 'stop']:
        exit()

    print(f'\n--> Please Select a Proper Option:\n\n    {my_input} is not on the menu')
    my_input = ''
# else:
#     exit()
