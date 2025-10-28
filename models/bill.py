"""
Bill module - CORRIGIDO
Agora cada bill pertence a um usuário específico
"""

from datetime import datetime
from models.users import *
from models.history import *
from core.observers import Subject


class Bill(Subject):
    def __init__(self, value: float, description: str, due_date: str, owner: User = None):
        """
        due_date needs to be in the format 'YYYY-MM-DD'
        owner: User que possui este boleto (NOVO)
        """
        super().__init__()  
        self.__value = value
        self.__description = description
        self.__due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.__paid = False
        self.__owner = owner  # NOVO: dono do boleto

    # ---------- Getters ----------
    def get_value(self) -> float:
        return self.__value

    def get_due_date(self) -> datetime:
        return self.__due_date

    def is_paid(self) -> bool:
        return self.__paid
    
    def get_description(self) -> str:
        return self.__description
    
    def get_owner(self) -> User:
        """ retorna o dono do boleto"""
        return self.__owner

    # ---------- Setters ----------
    def set_value(self, new_value: float):
        self.__value = new_value

    def set_due_date(self, new_due_date: str):
        self.__due_date = datetime.strptime(new_due_date, "%Y-%m-%d")

    def set_paid(self, paid: bool):
        self.__paid = paid
    
    def set_owner(self, owner: User):
        """ define o dono do boleto"""
        self.__owner = owner

    # ---------- Métodos extras ----------
    def is_overdue(self) -> bool:
        """
        Return True if the bill is overdue (and not paid yet).
        """
        return (datetime.now() > self.__due_date) and (not self.__paid)

    def pay(self, user: User):
        """
        Pays the bill and updates the user's balance and history.
        verifica se o usuário é o dono do boleto
        """
        if self.__paid:
            raise ValueError("This bill has already been paid.")
        
        # verifica se é o dono do boleto
        if self.__owner and user != self.__owner:
            raise ValueError(f"This bill belongs to {self.__owner.get_name()}. You cannot pay it.")

        if user.get_balance() < self.__value:
            raise ValueError("Insufficient balance to pay the bill.")

        self.notify("BILL_PAID", {
            "description": self.__description,
            "amount": self.__value
        })    

        # Deduct from balance
        user.set_balance(user.get_balance() - self.__value)

        # Mark bill as paid
        self.__paid = True

        # Add history entry
        description = f"Paid bill of {self.__value} due on {self.__due_date.date()}"
        history_entry = History_bill(
            action="Bill Payment",
            description=description,
            bill_amount=self.__value,
            due_date=self.__due_date
        )
        user.add_history(history_entry)

        print("Bill paid successfully.")

    def check_overdue(self):
        """
        Check if the bill is overdue and notify if it is
        """
        if self.is_overdue():
            self.notify("BILL_OVERDUE", {
                "description": self.__description,
                "amount": self.__value
            })
