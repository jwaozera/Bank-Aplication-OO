"""
In this module, we define the Bill and everything around them

We need: 
 - The value of the bill
 - The due date of the bill
 - The status of the bill (paid/unpaid) (if paid we need to exclude it from the list of bills)

The list of bills will be declared in the main module. (or at least will be executed in a function later)
"""

from datetime import datetime
from models.users import *
from models.history import *

class Bill:
    def __init__(self, value: float, description: str, due_date: str):
        """
        due_date needs to be in the format 'YYYY-MM-DD'
        """
        self.__value = value
        self.__description = description
        self.__due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.__paid = False

    # ---------- Getters ----------
    def get_value(self) -> float:
        return self.__value

    def get_due_date(self) -> datetime:
        return self.__due_date

    def is_paid(self) -> bool:
        return self.__paid
    
    def get_description(self) -> str:
        return self.__description

    # ---------- Setters ----------
    def set_value(self, new_value: float):
        self.__value = new_value

    def set_due_date(self, new_due_date: str):
        self.__due_date = datetime.strptime(new_due_date, "%Y-%m-%d")

    def set_paid(self, paid: bool):
        self.__paid = paid

    # ---------- Métodos extras ----------
    def is_overdue(self) -> bool:
        """
        Return True if the bill is overdue (and not paid yet).
        """
        return (datetime.now() > self.__due_date) and (not self.__paid)

    def pay(self, user: User):
        """
        Pays the bill and updates the user's balance and history.
        """
        if self.__paid:
            raise ValueError("This bill has already been paid.")

        if user.get_balance() < self.__value:
            raise ValueError("Insufficient balance to pay the bill.")

        #deduct from balance
        user.set_balance(user.get_balance() - self.__value)

        #mark bill as paid
        self.__paid = True

        #add history entry
        description = f"Paid bill of {self.__value} due on {self.__due_date.date()}"
        history_entry = History_bill(
            action="Bill Payment",
            description=description,
            bill_amount=self.__value,
            due_date=self.__due_date
        )
        user.add_history(history_entry)

        print("Bill paid successfully.")
