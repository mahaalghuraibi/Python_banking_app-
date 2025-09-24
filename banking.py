# ==========================
# مكتبة CSV
# ==========================
import csv

# ==========================
# ملف البيانات
# ==========================
DATA_FILE = "bank.csv"


# ==========================
# كلاس Customer (يمثل العميل)
# ==========================
class Customer:
    def __init__(self, first_name, last_name, password, checking=0, savings=0):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking = float(checking)
        self.savings = float(savings)

    # ---- الإيداع ----
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

    # ---- السحب ----
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

    # ---- التحويل ----
    def transfer(self, amount, from_account="checking", to_account="savings"):
        if amount <= 0:
            print("Amount must be positive")
            return
        if from_account == "checking" and to_account == "savings":
            if self.checking >= amount:
                self.checking -= amount
                self.savings += amount
                print("Transfer successful!")
            else:
                print("Insufficient funds in checking account")
        elif from_account == "savings" and to_account == "checking":
            if self.savings >= amount:
                self.savings -= amount
                self.checking += amount
                print("Transfer successful!")
            else:
                print("Insufficient funds in savings account")
        else:
            print("Invalid transfer accounts")

    # ---- تمثيل نصي للعميل ----
    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}, Checking: {self.checking}, Savings: {self.savings}"


# ==========================
# كلاس Account (يمثل الحساب)
# ==========================
class Account:
    def __init__(self, account_id, first_name, last_name, password):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def __str__(self):
        return f"Account {self.account_id}: {self.first_name} {self.last_name}"


# ==========================
# كلاس Bank (يمثل البنك)
# ==========================
class Bank:
    def __init__(self):
        self.data_path = "bank.csv"
        self.customers = {}

    max_id = 20

    # ---- إضافة عميل جديد ----
    def add_customer(
        self,
        first_name,
        last_name,
        password,
        has_checking=True,
        has_savings=False,
        initial_checking=0,
        initial_savings=0
    ):
        # check if max_id is less than or equal to 20
        if self.max_id <= 20:
            print("You can create an account")

            # if it is then you can creatre the account
            # create a new instance of the class, Account and pass it the parameters
            new_account_id = self.max_id + 1
            new_account = Account(new_account_id, first_name, last_name, password)

            self.customers[new_account_id] = new_account
            print(" New account created:", new_account)

            # ---- حفظ عميل جديد في CSV ----
            #  القيم اللي تنحفظ في الملف
            checking_field = initial_checking if has_checking else "False"
            savings_field  = initial_savings  if has_savings  else "False"

            # صف البيانات
            fieldnames = ["id", "first_name", "last_name", "password",
                          "checking", "savings", "active", "overdraft_count"]
            row_out = {
                "id": new_account_id,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "checking": checking_field,
                "savings": savings_field,
                "active": "True",
                "overdraft_count": 0
            }

            #صف جديد في csv
            with open(self.data_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(row_out)

            print(" Customer saved to CSV")

            # add 1 to max_id
            self.max_id += 1
        else:
            # else
            # print a message to say there too many account
            print(" A new account cannot be created (too many accounts)")
            # return
            return

    # Anorgwe function to ask user. to input informations
    def add_customer_interactive(self):
        # create a variable to store the input that asks for user informations
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        password = input("Enter password: ")

        has_checking = input("Do you want checking account? (y/n): ").lower() == "y"
        has_savings = input("Do you want savings account? (y/n): ").lower() == "y"

        # مبلغ الايداع في البداية
        initial_checking = 0
        if has_checking:
            initial_checking = int(input("Enter initial checking deposit: "))

        initial_savings = 0
        if has_savings:
            initial_savings = int(input("Enter initial savings deposit: "))

        # use add customer method and pass it the variables as arguments
        self.add_customer(first_name, last_name, password,
                          has_checking, has_savings,
                          initial_checking, initial_savings)
        print("Account created successfully!")

    
def main_menu(bank):
    while True :
        print("________________________________")
        print("Welcome to maha Bank ")
        print("________________________________")
        print("1) Create a new account")
        print("2) Login")
        print("3) Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            print(" Create a new account selected")
            bank.add_customer_interactive()          
            print(bank.customers)                   
        elif choice == "2":
            print(" Login selected")
        elif choice == "3":
            print("Thank you ")
            break
        else:
            print(" Invalid option, please try again.")



if __name__ == "__main__":

    bank = Bank()
    main_menu(bank)
