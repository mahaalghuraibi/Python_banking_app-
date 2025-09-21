# مكتبة CSV
import csv

# ملف البيانات
DATA_FILE = "bank.csv"

class Customer:
    def __init__(self, first_name, last_name, password, checking=0, savings=0):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking = checking
        self.savings = savings

    def deposit(self, amount, account_type="checking"):
        pass

    def withdraw(self, amount, account_type="checking"):
        pass

    def transfer(self, amount, from_account="checking", to_account="savings"):
        pass

    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}, Checking: {self.checking}, Savings: {self.savings}"


class Bank:
    pass


class Account:
    # كلاس أساسي للحسابات
    pass


class CheckingAccount(Account):
    # حساب جاري
    pass


class SavingsAccount(Account):
    # حساب توفير
    pass
