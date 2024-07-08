
from . models import Transaction, Category, SubCategory
from accounts.bank_account_helper import add_amount, deduct_amount


expense_category = "Expense"
income_category = "Income"

def create_transaction(description, date, amount, account, category, sub_cat):

    category = Category.objects.get(name=category)
    sub_category = SubCategory.objects.get(sub_category=sub_cat)
    bank_acc = account
    trans1 = Transaction.objects.create(date=date, amount=amount, transaction_from_account=bank_acc, sub_category=sub_category)
    if category == expense_category:
        deduct_amount(bank_acc, amount)
    else:
        add_amount(bank_acc, amount)
    return trans1

def delete_transaction(transaction):
    bank_acc = transaction.transaction_from_account
    if transaction.sub_category.category == expense_category:
        add_amount(bank_acc, transaction.amount)
    else:
        deduct_amount(bank_acc, transaction.amount)
    transaction.delete()
