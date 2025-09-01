"""
This module is basically for creating the objects in the history table
I need to decide whether make the history table a list of objects or make it a object that has a list of objects inside
Whe can use encapsulation here to show to the teacher
and use abstract class too, for every type os object in historys

"""
from abc import ABC, abstractmethod
from datetime import datetime, time

class History(ABC):
    """This is the abstract class for the history table"""

    def __init__(self, action: str, description: str):
        self.__action = action
        self.__time = datetime.now()
        self.__description = description

    @abstractmethod
    def show(self):
        print("Action: ", self.__action)
        print("Time: ", self.__time)
        print("Description: ", self.__description)
        pass

class History_transaction(History):
    """This class is for the transactions in the history table"""

    def __init__(self, action: str, description: str, amount: float, balance: float):
        super().__init__(action, description)
        self.__amount = amount
        self.__balance = balance

    def show(self):
        super().show()
        print("Amount: ", self.__amount)
        print("Balance: ", self.__balance)

class History_loan(History):
    """This class is for the loans in the history table"""

    def __init__(self, action: str, description: str, loan_amount: float,):
        super().__init__(action, description)
        self.__loan_amount = loan_amount

    def show(self):
        super().show()
        print("Loan Amount: ", self.__loan_amount)

class History_bill(History):
    """This class is for the bills in the history table"""

    def __init__(self, action: str, description: str, bill_amount: float, due_date: datetime):
        super().__init__(action, description)
        self.__bill_amount = bill_amount
        self.__due_date = due_date

    def show(self):
        super().show()
        print("Bill Amount: ", self.__bill_amount)
        print("Due Date: ", self.__due_date)

class History_investment(History):
    """This class is for the investments in the history table"""

    def __init__(self, action: str, description: str, investment_amount: float):
        super().__init__(action, description)
        self.__investment_amount = investment_amount

    def show(self):
        super().show()
        print("Investment Amount: ", self.__investment_amount)


class History_cheque_book(History):
    """This class is for the cheque book transactions in the history table"""

    def __init__(self, action: str, description: str, cheque_number: str):
        super().__init__(action, description)
        self.__cheque_number = cheque_number

    def show(self):
        super().show()
        print("Cheque Number: ", self.__cheque_number)
