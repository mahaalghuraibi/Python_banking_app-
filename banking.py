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
        if amount <= 0:
            print("Amount must be positive")
            return
        if account_type == "checking":
            self.checking += amount
        elif account_type == "savings":
            self.savings += amount
        else:
            print("Invalid account type")

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



if __name__ == "__main__":
    c = Customer("Maha", "alghuribi", "1234", 100, 50)
    print(c)  # قبل الإيداع
    c.deposit(200, "checking")
    print(c)  # بعد الإيداع


c = Customer("Maha", "alghuribi", "1234", 100, 50)
print(c)  

# إيداع 200 في حساب التوفير
c.deposit(200, "savings")
print(c) 
