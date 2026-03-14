
class BankAccount:
    def __init__(self , account_holder , balance = 0 ):
        self.account_holder = account_holder 
        self.balance= balance 

    def __str__(self):
        return f"Account belonging to {self.account_holder}. Current balance: ${self.balance}"

    def deposit(self , amount):
        if amount >= 0 :
            if amount >0:
                self.balance += amount
                return f'The amount {amount} is deposited . The total balance is {self.balance}'
            elif amount == 0 :
                raise ValueError("Deposit amount cannot be 0 . Please Try Again")
        elif amount < 0 :
            raise ValueError("The ammount to be deposit should be positive . Please try again ")

    def withdraw(self , amount):
        if amount > 0 :
            if  amount <= self.balance :
                self.balance -= amount 
                return f'The amount {amount} is withdrawn . The total balance is {self.balance}'
            else :
                print("The given amount  of money is not in your account . ")
        elif amount < 0 :
            raise ValueError("Cannot witdraw when you dont have any money . ")
        elif amount == 0 :
            raise ValueError("Plese try again. The amount given cannot be withdrawn ")

name  = input("Enter the name of the account holder : ")
balance= int(input("Enter the amount  of money to deposit while creating the account : "))

a = BankAccount(name , balance)

dep_amount = int(input("Enter the mount of money to deposit in the account : "))

print(a.deposit(dep_amount))

withdrawn_amount = int(input("Enter the amount to be withdrawn from the account : "))

print(a.withdraw(withdrawn_amount))



        

# print(BankAccount("Anupam"))