# نستورد مكتبة CSV
import csv  

# اسم ملف البيانات (ثابت)
DATA_FILE = "bank.csv"

class Customer:
    # هنا لاحقاً بنضيف خصائص (id, first_name, ...)
    pass

class Account:
    # الكلاس الأساسي اللي يورّث منه الحسابات
    pass

class CheckingAccount(Account):
    # حساب جاري
    pass

class SavingsAccount(Account):
    # حساب توفير
    pass

class Bank:
    # البنك نفسه (يتعامل مع العملاء ويقرأ من CSV)
    pass
