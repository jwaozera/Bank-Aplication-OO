"""
Singleton
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
    
    def get_unpaid_bills(self, user: User = None) -> List[Bill]:
        """
        Retorna boletos não pagos
        CORRIGIDO: Se user fornecido, retorna apenas bills daquele usuário
        """
        unpaid = [bill for bill in self._bills if not bill.is_paid()]
        
        # NOVO: Filtra por usuário se fornecido
        if user:
            unpaid = [bill for bill in unpaid if bill.get_owner() == user or bill.get_owner() is None]
        
        return unpaid
    
    def get_user_bills(self, user: User, paid: bool = None) -> List[Bill]:
        """
        NOVO: Retorna bills de um usuário específico
        paid: None (todas), True (pagas), False (não pagas)
        """
        user_bills = [bill for bill in self._bills if bill.get_owner() == user]
        
        if paid is not None:
            user_bills = [bill for bill in user_bills if bill.is_paid() == paid]
        
        return user_bills
    
    def initialize_demo_data(self) -> None:
        """Inicializa dados de demonstração"""
        from core.user_factory import UserFactoryProvider
        
        # Criar usuários de exemplo usando Factory
        regular_factory = UserFactoryProvider.get_factory("regular")
        investor_factory = UserFactoryProvider.get_factory("investor")
        
        # Usuários regulares
        kris = regular_factory.create_user("Kris", "1234", 1000)
        susie = regular_factory.create_user("Susie", "9876", 1500)
        jwao = regular_factory.create_user("jwao", "admin", 100000)
        
        # Usuários investidores
        aubrey = investor_factory.create_user("Aubrey", "4567", 2500)
        kel = investor_factory.create_user("Kel", "999", 99999)
        mari = investor_factory.create_user("Mari", "4444", 100)
        
        # Adiciona ao sistema
        self.add_account(kris)
        self.add_account(susie)
        self.add_account(jwao)
        self.add_account(aubrey)
        self.add_account(kel)
        self.add_account(mari)
        
        # CORRIGIDO: Boletos específicos por usuário
        bill1 = Bill(100, "Internet Bill", "2023-10-31", owner=kris)
        bill2 = Bill(200, "Electricity Bill", "2023-11-15", owner=kris)
        bill3 = Bill(150, "Water Bill", "2023-12-01", owner=susie)
        bill4 = Bill(500, "Phone Bill", "2023-11-20", owner=aubrey)
        
        self.add_bill(bill1)
        self.add_bill(bill2)
        self.add_bill(bill3)
        self.add_bill(bill4)
        
        # Bills globais (sem owner - qualquer um pode pagar)
        global_bill = Bill(50, "Community Fee", "2023-12-15", owner=None)
        self.add_bill(global_bill)
