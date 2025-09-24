"""
Abstract Factory Pattern - Transaction Factory
famílias de objetos relacionados para transações

"""

from abc import ABC, abstractmethod
from models.history import *
from models.users import User

class TransactionAbstractFactory(ABC):
    """Factory abstrata para criar objetos relacionados a transações"""
    
    @abstractmethod
    def create_transaction_history(self, action: str, description: str, amount: float, balance: float) -> History_transaction:
        pass
    
    @abstractmethod
    def create_bill_history(self, action: str, description: str, bill_amount: float, due_date) -> History_bill:
        pass
    
    @abstractmethod
    def create_loan_history(self, action: str, description: str, loan_amount: float) -> History_loan:
        pass

class BankingTransactionFactory(TransactionAbstractFactory):
    """Factory concreta para transações bancárias básicas"""
    
    def create_transaction_history(self, action: str, description: str, amount: float, balance: float) -> History_transaction:
        return History_transaction(action, description, amount, balance)
    
    def create_bill_history(self, action: str, description: str, bill_amount: float, due_date) -> History_bill:
        return History_bill(action, description, bill_amount, due_date)
    
    def create_loan_history(self, action: str, description: str, loan_amount: float) -> History_loan:
        return History_loan(action, description, loan_amount)

class InvestmentTransactionFactory(TransactionAbstractFactory):
    """Factory concreta para transações de investimento"""
    
    def create_transaction_history(self, action: str, description: str, amount: float, balance: float) -> History_transaction:
        # Para investidores, adiciona informações extras na descrição
        enhanced_description = f"[INVESTOR] {description}"
        return History_transaction(action, enhanced_description, amount, balance)
    
    def create_bill_history(self, action: str, description: str, bill_amount: float, due_date) -> History_bill:
        enhanced_description = f"[INVESTOR] {description}"
        return History_bill(action, enhanced_description, bill_amount, due_date)
    
    def create_loan_history(self, action: str, description: str, loan_amount: float) -> History_loan:
        enhanced_description = f"[INVESTOR] {description}"
        return History_loan(action, enhanced_description, loan_amount)
    
    def create_investment_history(self, action: str, description: str, investment_amount: float) -> History_investment:
        """Método específico para investidores"""
        return History_investment(action, description, investment_amount)

class TransactionFactoryProvider:
    """Provedor de factories para diferentes tipos de transação"""
    
    @staticmethod
    def get_factory(user: User) -> TransactionAbstractFactory:
        from models.users import Investor
        if isinstance(user, Investor):
            return InvestmentTransactionFactory()
        else:
            return BankingTransactionFactory()
