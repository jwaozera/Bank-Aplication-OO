"""
Here we are with the loan module


"""
from models.users import *
from models.history import *
from models.bill import *

class Loan:
    def __init__(self, amount: float, duration: int, user: User):
        self.__amount = amount
        self.__duration = duration
        self.__user = user

        #cria histórico e adiciona ao usuário
        history_entry = History_loan(
            action="Loan",
            description=f"{user.get_name()} took a loan of {self.__amount} for {self.__duration} months.",
            loan_amount=self.__amount
        )
        user.add_history(history_entry)

        user.add_loan(self)

    # ---------- Getters ----------
    def get_amount(self) -> float:
        return self.__amount

    def get_duration(self) -> int:
        return self.__duration


    # ---------- Setters ----------
    def set_amount(self, new_amount: float):
        self.__amount = new_amount

    def set_duration(self, new_duration: int):
        self.__duration = new_duration
