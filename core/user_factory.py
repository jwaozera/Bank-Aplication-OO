"""
Factory Method Pattern - User Factory
padrão responsável por criar diferentes tipos de user

"""

from abc import ABC, abstractmethod
from models.users import User, Investor

class UserFactory(ABC):
    """Abstract Factory para criar users"""
    
    @abstractmethod
    def create_user(self, name: str, password: str, balance: float):
        pass

class RegularUserFactory(UserFactory):
    """Factory para criar users regulares"""
    
    def create_user(self, name: str, password: str, balance: float) -> User:
        return User(name, password, balance)

class InvestorUserFactory(UserFactory):
    """Factory para criar users investidores"""
    
    def create_user(self, name: str, password: str, balance: float) -> Investor:
        return Investor(name, password, balance)

class UserFactoryProvider:
    """Provedor de factories para diferentes tipos de users"""
    
    @staticmethod
    def get_factory(user_type: str) -> UserFactory:
        if user_type.lower() == "regular":
            return RegularUserFactory()
        elif user_type.lower() == "investor":
            return InvestorUserFactory()
        else:
            raise ValueError(f"Unknown user type: {user_type}")
