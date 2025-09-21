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
        if amount <= 0:
            print("Amount must be positive")
            return
        if account_type == "checking":
            if self.checking >= amount:
                self.checking -= amount
                print("Withdrawal successful!")
            else:
                print("Insufficient funds in checking account")
        elif account_type == "savings":
            if self.savings >= amount:
                self.savings -= amount
                print("Withdrawal successful!")
            else:
                print("Insufficient funds in savings account")
        else:
            print("Invalid account type")

    def transfer(self, amount, from_account="checking", to_account="savings"):
        pass  # لاحقًا

    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}, Checking: {self.checking}, Savings: {self.savings}"


class Bank:
    pass


class Account:
    pass


class CheckingAccount(Account):
    pass


class SavingsAccount(Account):
    pass

if __name__ == "__main__":
    # إنشاء حساب جديد
    new_customer = Customer("Sara", "Ahmed", "sa123", 500, 200)
    print(new_customer)

if __name__ == "__main__":
    c = Customer("Maha", "alghuribi", "1234", 100, 50)
    print(c)

    # تجربة الإيداع
    c.deposit(200, "checking")
    print(c)

    # تجربة السحب من الجاري 
    c.withdraw(50, "checking")
    print(c)

    # تجربة السحب من التوفير 
    c.withdraw(30, "savings")
    print(c)

    # تجربة سحب أكثر من الرصيد 
    c.withdraw(500, "savings")
    print(c)
