# ==========================
# مكتبات
# ==========================
import csv
import os

# ==========================
# ملف البيانات
# ==========================
DATA_FILE = "bank.csv"

# ==========================
# كلاس Account (يمثل حساب مفرد)
# ==========================
class Account:
    def __init__(self, kind, balance=None, active=True):
        self.kind = kind
        self.has_account = (balance is not None)
        self.balance = float(balance) if self.has_account else None
        self.active = bool(active)

    def exists(self):
        return self.has_account

    def fmt(self):
        if not self.has_account or self.balance is None:
            return "No account"
        try:
            return f"{float(self.balance):.2f}"
        except (TypeError, ValueError):
            return "No account"


# ==========================
# كلاس Customer ( العميل)
# ==========================
class Customer:
    def __init__(self, first_name, last_name, password,
                 checking=None, savings=None,
                 active=True, overdraft_count=0):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

        self.has_checking = (checking is not None)
        self.checking = float(checking) if self.has_checking else None

        self.has_savings = (savings is not None)
        self.savings = float(savings) if self.has_savings else None

        self.active = bool(active)
        self.overdraft_count = int(overdraft_count)

    # ---- الإيداع ----
    def deposit(self, amount, account_type="checking"):
        if amount <= 0:
            print("the amount deposit must be positive")
            return

        if account_type == "checking":
            if not self.has_checking:
                print("No checking account.")
                return
            self.checking += amount

        elif account_type == "savings":
            if not self.has_savings:
                print("No savings account.")
                return
            self.savings += amount

        else:
            print("Invalid account type")
            return

        print("Deposit successful!")

        if (not self.active and
            (self.checking is None or self.checking >= 0) and
            (self.savings  is None or self.savings  >= 0)):
            self.active = True
            print("Account reactivated.")

    def withdraw(self, amount, account_type="checking"):
        if not self.active:
            print("Account is deactivated due to overdrafts. Deposit to reactivate.")
            return

        if amount <= 0:
            print(" the account is empty Can not withdraw from it")
            return

        if account_type == "checking":
            if not self.has_checking:
                print("No checking account.")
                return
            if self.checking < 0:
                print("Checking is negative. Please deposit to bring it positive first.")
                return

        elif account_type == "savings":
            if not self.has_savings:
                print("No savings account.")
                return
            if self.savings < 0:
                print("Savings is negative. Please deposit to bring it positive first.")
                return
        else:
            print("Invalid account type")
            return

        if amount > 100:
            print("Cannot withdraw more than $100 in a single transaction")
            return

        if account_type == "checking":
            if self.checking >= amount:
                self.checking -= amount
                print("Withdrawal successful!")
            else:
                self.checking -= 35
                self.overdraft_count += 1
                print("Insufficient funds. Overdraft fee of $35 applied.")

        elif account_type == "savings":
            if self.savings >= amount:
                self.savings -= amount
                print("Withdrawal successful!")
            else:
                self.savings -= 35
                self.overdraft_count += 1
                print("Insufficient funds. Overdraft fee of $35 applied.")

        if self.overdraft_count >= 2:
            self.active = False
            print("Account deactivated after multiple overdrafts.")

    def transfer(self, amount, from_account="checking", to_account="savings"):
        if not self.active:
            print("Account is deactivated. Deposit first to reactivate.")
            return
        if amount <= 0:
            print("Amount must be positive")
            return

        if from_account == "checking" and to_account == "savings":
            if not self.has_checking:
                print("No checking account."); return
            if not self.has_savings:
                print("No savings account."); return
            if self.checking >= amount:
                self.checking -= amount
                self.savings += amount
                print("Transfer successful!")
            else:
                print("Insufficient funds in checking account")

        elif from_account == "savings" and to_account == "checking":
            if not self.has_savings:
                print("No savings account."); return
            if not self.has_checking:
                print("No checking account."); return
            if self.savings >= amount:
                self.savings -= amount
                self.checking += amount
                print("Transfer successful!")
            else:
                print("Insufficient funds in savings account")

        else:
            print("Invalid transfer accounts")

    def open_account(self, account_type):
        if account_type == "checking":
            if self.has_checking:
                print("You already have a checking account.")
                return False
            self.has_checking = True
            self.checking = 0.0
            print("Checking account opened with $0.00.")
            return True

        elif account_type == "savings":
            if self.has_savings:
                print("You already have a savings account.")
                return False
            self.has_savings = True
            self.savings = 0.0
            print("Savings account opened with $0.00.")
            return True

        else:
            print("Invalid account type")
            return False


# ==========================
# كلاس Bank 
# ==========================
class Bank:
    FIELD_NAMES = ["id", "first_name", "last_name", "password",
                   "checking", "savings", "active", "overdraft_count"]

    def __init__(self, data_path=DATA_FILE):
        self.data_path = data_path
        if not os.path.exists(self.data_path):
            with open(self.data_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=Bank.FIELD_NAMES)
                writer.writeheader()

    def read(self):
        rows = []
        with open(self.data_path, "r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows.append(row)
        return rows

    def write(self, rows):
        with open(self.data_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=Bank.FIELD_NAMES)
            writer.writeheader()
            writer.writerows(rows)

    def next_id(self):
        rows = self.read()
        max_id = 0
        for r in rows:
            try:
                max_id = max(max_id, int(r.get("id", 0)))
            except:
                pass
        return max_id + 1

    def add_customer_interactive(self):
        first_name = input("Enter first name: ").strip()
        last_name  = input("Enter last name: ").strip()
        password   = input("Enter password: ").strip()

        print("\nChoose account type:")
        print("  [1] Checking")
        print("  [2] Savings")
        print("  [3] Both (Checking & Savings)")
        while True:
            choice = input("Your choice (1/2/3): ").strip()
            if choice in ("1", "2", "3"):
                break
            print("Invalid choice. Please enter 1, 2, or 3.")

        has_checking = (choice in ("1", "3"))
        has_savings  = (choice in ("2", "3"))

        cust = Customer(
            first_name, last_name, password,
            checking=0.0 if has_checking else None,
            savings=0.0 if has_savings else None,
            active=True, overdraft_count=0
        )

        rows = self.read()
        new_id = self.next_id()
        rows.append({
            "id": str(new_id),
            "first_name": cust.first_name,
            "last_name": cust.last_name,
            "password": cust.password,
            "checking": (str(cust.checking) if cust.has_checking else ""),
            "savings":  (str(cust.savings)  if cust.has_savings  else ""),
            "active": "True",
            "overdraft_count": "0"
        })
        self.write(rows)

        print("\nNew account created successfully.")
        print(f"Your new account id is: {new_id}")
        print("Please remember this id; you'll need it to login.")

    def add_customer(self, first_name, last_name, password,
                     checking=0.0, savings=0.0, active=True):
        rows = self.read()
        new_id = self.next_id()
        checking_val = "" if checking is None else str(float(checking))
        savings_val  = "" if savings  is None else str(float(savings))
        rows.append({
            "id": str(new_id),
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "checking": checking_val,
            "savings":  savings_val,
            "active": "True" if active else "False",
            "overdraft_count": "0"
        })
        self.write(rows)
        return new_id

    def authenticate(self, username, password):
        for row in self.read():
            if row.get("id") == str(username) and row.get("password") == password:
                chk_raw = row.get("checking", "")
                sav_raw = row.get("savings", "")

                has_checking = chk_raw not in ("", "False", None)
                has_savings  = sav_raw not in ("", "False", None)

                try:
                    checking = float(chk_raw) if has_checking else None
                except:
                    checking = None
                try:
                    savings = float(sav_raw) if has_savings else None
                except:
                    savings = None

                active = str(row.get("active", "True")).strip().lower() == "true"
                try:
                    overdrafts = int(row.get("overdraft_count", "0"))
                except:
                    overdrafts = 0

                return Customer(row.get("first_name", ""),
                                row.get("last_name", ""),
                                row.get("password", ""),
                                checking, savings, active, overdrafts)
        return None

    def login(self):
        username = input("Please enter your username (id): ").strip()
        password = input("Please enter your password: ").strip()

        cust = self.authenticate(username, password)
        if cust:
            print("Login successful")
            return username, cust

        print("Invalid username or password")
        return None, None

    def update_customer_in_csv(self, username, customer):
        rows = self.read()
        for r in rows:
            if r.get("id") == str(username):
                r["first_name"] = customer.first_name
                r["last_name"]  = customer.last_name
                r["password"]   = customer.password
                r["checking"]   = (str(customer.checking) if customer.has_checking else "")
                r["savings"]    = (str(customer.savings)  if customer.has_savings  else "")
                r["active"]     = "True" if customer.active else "False"
                r["overdraft_count"] = str(customer.overdraft_count)
                break
        self.write(rows)

    def transfer_to_other_user(self, from_user_id, from_account,
                               to_user_id, to_account, amount):
        if amount <= 0:
            print("Amount must be positive")
            return False
        if from_account not in ("checking", "savings") or to_account not in ("checking", "savings"):
            print("Invalid account type.")
            return False

        rows = self.read()
        from_row = None
        to_row = None
        for r in rows:
            if r.get("id") == str(from_user_id):
                from_row = r
            if r.get("id") == str(to_user_id):
                to_row = r

        if not from_row or not to_row:
            print("User not found (source or target).")
            return False

        if from_row.get(from_account, "") in ("", "False", None):
            print("Source user does not have the selected account.")
            return False
        if to_row.get(to_account, "") in ("", "False", None):
            print("Target user does not have the selected account.")
            return False

        try:
            from_balance = float(from_row[from_account] or 0)
            to_balance   = float(to_row[to_account] or 0)
        except ValueError:
            print("Corrupt balance in CSV.")
            return False

        if from_balance < 0:
            print("Source account is negative. Deposit first.")
            return False
        if from_balance < amount:
            print("Insufficient funds in source account.")
            return False

        # التحويل
        from_balance -= amount
        to_balance   += amount
        from_row[from_account] = str(from_balance)
        to_row[to_account]     = str(to_balance)
        self.write(rows)
        print("External transfer successful!")
        return True


# ==========================
# كلاس القائمة الرئيسية MainMenu
# ==========================
class MainMenu:
    def __init__(self, bank):
        self.bank = bank

    def run(self):
        while True:
            print("________________________________")
            print("Welcome to Maha Bank")
            print("________________________________")
            print("1) Create a new account")
            print("2) Login")
            print("3) Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.login()
            elif choice == "3":
                print("Thank you for using Maha Bank. Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")

    def create_account(self):
        first = input("Enter first name: ").strip()
        last = input("Enter last name: ").strip()
        pw = input("Enter password: ").strip()

        print("\nChoose account type:")
        print("  [1] Checking")
        print("  [2] Savings")
        print("  [3] Both (Checking & Savings)")
        while True:
            choice = input("Your choice (1/2/3): ").strip()
            if choice in ("1", "2", "3"):
                break
            print("Invalid choice. Please enter 1, 2, or 3.")

        checking = 0.0 if choice in ("1", "3") else None
        savings  = 0.0 if choice in ("2", "3") else None

        new_id = self.bank.add_customer(first, last, pw, checking, savings, active=True)

        print(f"\nAccount created successfully! Your ID is {new_id}")
        chk_status = "0.00" if checking is not None else "No account"
        sav_status = "0.00" if savings  is not None else "No account"
        print(f"Checking: {chk_status}, Savings: {sav_status}")

    # ---- تسجيل دخول ----
    def login(self):
        username = input("Please enter your username (id): ").strip()
        password = input("Please enter your password: ").strip()

        customer = self.bank.authenticate(username, password)
        if customer:
            print("Login successful!")
            user_menu(self.bank, username, customer)
        else:
            print("Invalid username or password.")


# ==========================
def ask_amount(prompt):
    while True:
        val = input(prompt).strip()
        try:
            return float(val)
        except ValueError:
            print("Amount must be a number, try again.")


def ask_account_type(prompt):
    while True:
        val = input(prompt).strip().lower()
        if val in ("checking", "savings"):
            return val
        print("Please type exactly: checking or savings.")


def fmt_balance(v):
    if v is None or str(v).strip().upper() in ("", "FALSE", "NO ACCOUNT"):
        return "No account"
    try:
        return f"{float(v):.2f}"
    except (TypeError, ValueError):
        return "No account"


def view_balances(customer):
    chk = fmt_balance(customer.checking)
    sav = fmt_balance(customer.savings)
    print(f"Checking: {chk}, Savings: {sav}")


# ==========================
# قائمة المستخدم بعد تسجيل الدخول
# ==========================
def user_menu(bank, username, customer):
    while True:
        print("________________________________")
        print(f"Welcome, {customer.first_name}!")
        print("________________________________")
        print("1) View balances")
        print("2) Deposit")
        print("3) Withdraw")
        print("4) Transfer (checking ⟷ savings)")
        print("5) Change password")
        print("6) Logout")
        print("7) Transfer to another user's account")
        print("8) Open another account (create missing type)")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_balances(customer)

        elif choice == "2":
            amount = ask_amount("Enter deposit amount: ")
            account = ask_account_type("Deposit to (checking/savings): ")
            customer.deposit(amount, account)
            bank.update_customer_in_csv(username, customer)

        elif choice == "3":
            amount = ask_amount("Enter withdraw amount: ")
            account = ask_account_type("Withdraw from (checking/savings): ")
            customer.withdraw(amount, account)
            bank.update_customer_in_csv(username, customer)

        elif choice == "4":
            amount = ask_amount("Enter transfer amount: ")
            direction = ask_account_type("From which account? (checking/savings): ")
            if direction == "checking":
                customer.transfer(amount, "checking", "savings")
            else:
                customer.transfer(amount, "savings", "checking")
            bank.update_customer_in_csv(username, customer)

        elif choice == "5":
            new_pw = input("Enter new password: ").strip()
            if new_pw:
                customer.password = new_pw
                bank.update_customer_in_csv(username, customer)
                print("Password updated.")
            else:
                print("Password not changed.")

        elif choice == "6":
            print("Logging out...")
            break

        elif choice == "7":
            amount = ask_amount("Enter transfer amount: ")
            from_acc = ask_account_type("From which of YOUR accounts? (checking/savings): ")
            to_user_id = input("Enter TARGET user id: ").strip()
            to_acc = ask_account_type("To which TARGET account? (checking/savings): ")
            ok = bank.transfer_to_other_user(username, from_acc, to_user_id, to_acc, amount)
            if ok:
                if from_acc == "checking" and customer.has_checking:
                    customer.checking -= amount
                elif from_acc == "savings" and customer.has_savings:
                    customer.savings -= amount

        elif choice == "8":
            acc_to_open = ask_account_type("Which account to open? (checking/savings): ")
            opened = customer.open_account(acc_to_open)
            if opened:
                bank.update_customer_in_csv(username, customer)

        else:
            print("Invalid option, please try again.")


# ==========================
# تشغيل
# ==========================
if __name__ == "__main__":
    bank = Bank()
    MainMenu(bank).run()
