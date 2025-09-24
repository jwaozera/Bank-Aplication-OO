"""

Singleton 
Garante que existe apenas uma instância do sistema bancário

"""

from typing import List, Optional
from models.users import User
from models.bill import Bill

class BankSystem:

    """Singleton que gerencia todo o sistema bancário"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BankSystem, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._accounts: List[User] = []
            self._bills: List[Bill] = []
            self._exchange_rate = 5.25  # Real para Dólar
            self._initialized = True
    
    def add_account(self, account: User) -> None:
        """Adiciona uma conta ao sistema"""
        self._accounts.append(account)
    
    def add_bill(self, bill: Bill) -> None:
        """Adiciona um boleto ao sistema"""
        self._bills.append(bill)
    
    def get_accounts(self) -> List[User]:
        """Retorna todas as contas do sistema"""
        return self._accounts.copy()
    
    def get_bills(self) -> List[Bill]:
        """Retorna todos os boletos do sistema"""
        return self._bills.copy()
    
    def get_exchange_rate(self) -> float:
        """Retorna a taxa de câmbio atual"""
        return self._exchange_rate
    
    def set_exchange_rate(self, rate: float) -> None:
        """Define uma nova taxa de câmbio"""
        if rate > 0:
            self._exchange_rate = rate
    
    def find_account(self, name: str, password: str) -> Optional[User]:
        """Busca uma conta por nome e senha"""
        for account in self._accounts:
            if account.get_name() == name and account.get_password() == password:
                return account
        return None
    
    def get_other_accounts(self, current_account: User) -> List[User]:
        """Retorna todas as contas exceto a atual"""
        return [acc for acc in self._accounts if acc != current_account]
    
    def get_unpaid_bills(self) -> List[Bill]:
        """Retorna apenas os boletos não pagos"""
        return [bill for bill in self._bills if not bill.is_paid()]
    
    def initialize_demo_data(self) -> None:
        """Inicializa dados de demonstração"""
        from core.user_factory import UserFactoryProvider
        
        # Criar usuários de exemplo usando Factory
        regular_factory = UserFactoryProvider.get_factory("regular")
        investor_factory = UserFactoryProvider.get_factory("investor")
        
        # Usuários regulares
        self.add_account(regular_factory.create_user("Kris", "1234", 1000))
        self.add_account(regular_factory.create_user("Susie", "9876", 1500))
        
        # Usuários investidores
        self.add_account(investor_factory.create_user("Aubrey", "4567", 2500))
        self.add_account(investor_factory.create_user("Kel", "999", 99999))
        self.add_account(investor_factory.create_user("Mari", "4444", 0))
        
        # Boletos de exemplo
        self.add_bill(Bill(100, "Font installation", "2023-10-31"))
        self.add_bill(Bill(200, "Stair railing", "2023-11-15"))
