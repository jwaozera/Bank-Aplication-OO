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
        self.__investments_goals = []
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

    def get_investments_goals(self) -> list:
        return self.__investments_goals

    # ---------- Setters ----------
    def set_name(self, new_name: str):
        self.__name = new_name

    def set_password(self, new_password: str):
        self.__password = new_password

    def set_balance(self, new_balance: float, withdraw: bool = False):
        self.__balance = new_balance

        if withdraw:
            if self.__balance < 0:
                raise ValueError("Insufficient funds for withdrawal.")
            history =History_transaction(
                action="Withdrawal",
                description=f"Withdrew {self.__balance} from account",
                amount=self.__balance,
                balance=self.__balance
            )

        else:
            history = History_transaction(
                action="Deposit",
                description=f"Deposited {self.__balance} into account",
                amount=self.__balance,
                balance=self.__balance
            )
        self.add_history(history)

    def set_dolar_balance(self, new_dolar_balance: float):
        self.__dolar_balance = new_dolar_balance

    def set_investments_goals(self, new_goals: list):
        self.__investments_goals = new_goals

    # ---------- Outros métodos ----------
    def add_history(self, new_history: History):
        if not isinstance(new_history, History):
            raise TypeError("new_history must be an instance of History or its subclasses.")
        self.__history.append(new_history)

    def add_goal(self, goal: str):
        self.__investments_goals.append(goal)

    def add_loan(self, loan):
        self.__loans.append(loan)

    def add_investment_goal(self, investment_goal):
        self.__investments_goals.append(investment_goal)


    def new_checkbook(self):
        if self.__checkbook == 0:
            self.__checkbook = 1
            print("✅ New checkbook.")
        else:
            print("❌ You already had a checkbook this month.")
            print("Do you wish to pay R$ 25 for a new one?")
            choice = input("Y/N")

            if choice == "y" or choice == "yes" or choice == "sim":
                self.set_balance(self.get_balance() - 25.00, True)
                print("New checkbook ordered")
            else:
                print("Canceled transaction")

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


def transaction(user1: User, user2: User, amount: float): #user 1 paga e o user 2 recebe, só pode ser feita pelo pagante

    if amount <= 0:
        raise ValueError("Transaction amount must be positive.")

    if user1.get_balance() < amount:
        raise ValueError(f"{user1.get_name()} does not have enough balance to make the transaction.")

    #atualiza os saldos
    user1.set_balance(user1.get_balance() - amount)
    user2.set_balance(user2.get_balance() + amount)

    #cria os históricos da transação
    history1 = History_transaction(
        action="Debit",
        description=f"Transferred {amount} to {user2.get_name()}",
        amount=amount,
        balance=user1.get_balance()
    )

    history2 = History_transaction(
        action="Credit",
        description=f"Received {amount} from {user1.get_name()}",
        amount=amount,
        balance=user2.get_balance()
    )

    #adiciona os históricos
    user1.add_history(history1)
    user2.add_history(history2)
