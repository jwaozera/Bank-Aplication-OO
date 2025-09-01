"""
Here we are with the loan module


"""
from users import *
from history import *

class Loan:
    def __init__(self, amount: float, duration: int, user: User):
        self.__amount = amount
        self.__duration = duration
        self.__user = user

        # Cria histórico e adiciona ao usuário
        history_entry = History_loan(
            action="Loan",
            description=f"{user.get_name()} took a loan of {self.__amount} for {self.__duration} months.",
            loan_amount=self.__amount
        )
        user.add_history(history_entry)

    # ---------- Getters ----------
    def get_amount(self) -> float:
        return self.__amount

    def get_duration(self) -> int:
        return self.__duration

    def get_interest_rate(self) -> float:
        return self.__interest_rate

    # ---------- Setters ----------
    def set_amount(self, new_amount: float):
        self.__amount = new_amount

    def set_duration(self, new_duration: int):
        self.__duration = new_duration

    def set_interest_rate(self, new_interest_rate: float):
        self.__interest_rate = new_interest_rate