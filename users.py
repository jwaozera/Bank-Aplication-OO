"""
This module is for managing user accounts and their associated data.

We are going to have two classes, the normal user and the investor user.

The normal one can do all the things, but cant invest.
The investor do all the things the normal user can do, plus invest in the stock market and other investment opportunities.

The normal is the superclass of investor (to make polymorphism easier).
"""

from history import *


class User:
    def __init__(self, name: str, password: str, balance: float):
        self.__name = name
        self.__password = password
        self.__balance = balance
        self.__dolar_balance = 0.0
        self.__loans = []
        self.__history = []
        self.__checkbook = 0


    # ---------- Getters ----------
    def get_name(self) -> str:
        return self.__name

    def get_password(self) -> str:
        return self.__password

    def get_balance(self) -> float:
        return self.__balance

    def get_dolar_balance(self) -> float:
        return self.__dolar_balance

    def get_loans(self) -> list:
        return self.__loans

    def get_history(self) -> list:
        return self.__history

    # ---------- Setters ----------
    def set_name(self, new_name: str):
        self.__name = new_name

    def set_password(self, new_password: str):
        self.__password = new_password

    def set_balance(self, new_balance: float):
        """Apenas atualiza o saldo (sem registrar histórico)."""
        self.__balance = new_balance


    def deposit(self, amount: float):
        """Faz um depósito e registra no histórico."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.__balance += amount
        


    def withdraw(self, amount: float):
        """Faz um saque e registra no histórico."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if self.__balance < amount:
            raise ValueError("Insufficient funds for withdrawal.")

        self.__balance -= amount

    def set_dolar_balance(self, new_dolar_balance: float):
        self.__dolar_balance = new_dolar_balance

    # ---------- Outros métodos ----------
    def add_history(self, new_history: History):
        if not isinstance(new_history, History):
            raise TypeError("new_history must be an instance of History or its subclasses.")
        self.__history.append(new_history)

    def add_loan(self, loan):
        self.__loans.append(loan)



    def new_checkbook(self):
        if self.__checkbook == 0:
            self.__checkbook = 1
            print("✅ New checkbook.")
        else:
            print("❌ You already had a checkbook this month.")
            print("Do you wish to pay R$ 25 for a new one?")
            choice = input("Y/N")

            if choice == "y" or choice == "yes" or choice == "sim":
                self.set_balance(self.get_balance() - 25.00)
                print("New checkbook ordered")
            else:
                print("Canceled transaction")

        self.add_history(History_cheque_book("New Checkbook", "Ordered a new checkbook."))

class Investor(User):
    def __init__(self, name: str, password: str, balance: float):
        super().__init__(name, password, balance)
        self.__investments_goals = []

    # ---------- Getters ----------
    def get_investment_goals(self) -> list:
        return self.__investments_goals

    # ---------- Setters ----------
    def set_investment_goals(self, new_goals: list):
        self.__investments_goals = new_goals

    def add_investment(self, investment):
        self.__investments_goals.append(investment)


def transaction(user1, user2, amount: float):
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    if user1.get_balance() < amount:
        raise ValueError("Insufficient funds for transfer.")

    #saída do remetente
    user1.withdraw(amount)

    #entrada no destinatário
    user2.deposit(amount)

    # Histórico extra descritivo
    user1.add_history(History_transaction(
        action="Transfer Sent",
        description=f"Transferred {amount} to {user2.get_name()}",
        amount=-amount,
        balance=user1.get_balance()
    ))

    user2.add_history(History_transaction(
        action="Transfer Received",
        description=f"Received {amount} from {user1.get_name()}",
        amount=amount,
        balance=user2.get_balance()
    ))
