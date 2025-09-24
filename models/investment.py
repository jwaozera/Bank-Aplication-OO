"""
in this module, we are going to do everything inherent to investments

We need:
 - The value of the investment
 - The duration of it
 - The tax it contains

"""

from models.users import *
from models.history import *

class Investment():
    def __init__(self, value: float, duration: int, user: User):
        """
        value: valor investido
        duration: duração do investimento em meses
        user: usuário que fez o investimento
        """
        self.__value = value
        self.__duration = duration
        self.__user = user

        #define a taxa conforme a duração
        self.__tax = 15 if duration <= 3 else 5

        #cria histórico e adiciona ao usuário
        history_entry = History_investment(
            action="Investment",
            description=f"{user.get_name()} invested with {self.__tax}% tax for {self.__duration} months",
            investment_amount=self.__value
            )
        user.add_history(history_entry)

    # ---------- Getters ----------
    def get_value(self) -> float:
        return self.__value

    def get_duration(self) -> int:
        return self.__duration

    def get_tax(self) -> float:
        return self.__tax

    # ---------- Setters ----------
    def set_value(self, new_value: float):
        self.__value = new_value

    def set_duration(self, new_duration: int):
        self.__duration = new_duration

    def set_tax(self, new_tax: float):
        self.__tax = new_tax
