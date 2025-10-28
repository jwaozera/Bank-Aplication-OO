"""
Decorator Pattern - Adicionando funcionalidades extras as contas dinamicamente
Empilhando recursos sem modificar as classes base

Decorators:
- PremiumAccountDecorator: Cashback em transações
- InsuranceDecorator: Proteção contra fraudes
- NotificationDecorator: Notificações SMS/Email
- StudentAccountDecorator: Isenção de taxas
"""

from abc import ABC, abstractmethod
from models.users import User
from models.history import History


class UserDecorator(User):
    """Decorator base para adicionar funcionalidades aos usuários"""
    
    def __init__(self, user: User):
        # nao chama super().__init__ para evitar duplicação de atributos
        self._wrapped_user = user
    
    # delega todos os métodos para o usuário encapsulado
    def get_name(self) -> str:
        return self._wrapped_user.get_name()
    
    def get_password(self) -> str:
        return self._wrapped_user.get_password()
    
    def get_balance(self) -> float:
        return self._wrapped_user.get_balance()
    
    def get_dolar_balance(self) -> float:
        return self._wrapped_user.get_dolar_balance()
    
    def get_loans(self) -> list:
        return self._wrapped_user.get_loans()
    
    def get_history(self) -> list:
        return self._wrapped_user.get_history()
    
    def set_name(self, new_name: str):
        self._wrapped_user.set_name(new_name)
    
    def set_password(self, new_password: str):
        self._wrapped_user.set_password(new_password)
    
    def set_balance(self, new_balance: float):
        self._wrapped_user.set_balance(new_balance)
    
    def set_dolar_balance(self, new_dolar_balance: float):
        self._wrapped_user.set_dolar_balance(new_dolar_balance)
    
    def deposit(self, amount: float):
        self._wrapped_user.deposit(amount)
    
    def withdraw(self, amount: float):
        self._wrapped_user.withdraw(amount)
    
    def add_history(self, new_history: History):
        self._wrapped_user.add_history(new_history)
    
    def add_loan(self, loan):
        self._wrapped_user.add_loan(loan)
    
    def new_checkbook(self):
        self._wrapped_user.new_checkbook()
    
    # funções do Subject (Observer)
    def attach(self, observer):
        self._wrapped_user.attach(observer)
    
    def detach(self, observer):
        self._wrapped_user.detach(observer)
    
    def notify(self, event_type: str, data: dict):
        self._wrapped_user.notify(event_type, data)


class PremiumAccountDecorator(UserDecorator):
    """
    Conta Premium - add benefícios especiais:
    - Cashback de 1% em saques
    - Cashback de 0.5% em transferências
    - Taxa de câmbio preferencial (5% melhor)
    """
    
    def __init__(self, user: User):
        super().__init__(user)
        self.cashback_rate = 0.01  # 1%
        self.transfer_cashback_rate = 0.005  # 0.5%
        print("✨ Premium Account activated!")
    
    def withdraw(self, amount: float):
        """Saque com cashback de 1%"""
        super().withdraw(amount)
        cashback = amount * self.cashback_rate
        
        # Adiciona cashback
        current_balance = self._wrapped_user.get_balance()
        self._wrapped_user.set_balance(current_balance + cashback)
        
        print(f"💰 Premium Cashback: R$ {cashback:.2f} (1% of withdrawal)")
        
        # Registra no histórico
        from core.transaction_factory import TransactionFactoryProvider
        factory = TransactionFactoryProvider.get_factory(self._wrapped_user)
        history = factory.create_transaction_history(
            "Premium Cashback",
            f"Cashback from withdrawal of R$ {amount:.2f}",
            cashback,
            self._wrapped_user.get_balance()
        )
        self._wrapped_user.add_history(history)
    
    def get_exchange_bonus(self) -> float:
        """Retorna bônus na taxa de câmbio (5% melhor)"""
        return 0.05
 

class InsuranceDecorator(UserDecorator):
    """
    Seguro de Conta - Proteção contra transações suspeitas:
    - Proteção em transações acima de R$ 5.000
    - Reembolso automático em caso de fraude (simulado)
    - Notificação de transações grandes
    """
    
    def __init__(self, user: User):
        super().__init__(user)
        self.insurance_threshold = 5000.00
        self.monthly_fee = 29.90
        print("🛡️ Account Insurance activated!")
        print(f"   Protection for transactions above R$ {self.insurance_threshold:.2f}")
    
    def withdraw(self, amount: float):
        """Saque com proteção de seguro"""
        if amount > self.insurance_threshold:
            print(f"🛡️ INSURANCE ALERT: Large transaction detected!")
            print(f"   Amount: R$ {amount:.2f}")
            print(f"   This transaction is protected by insurance")
            
            confirm = input("   Confirm this transaction? (y/n): ").lower().strip()
            if confirm not in ['y', 'yes', 's', 'sim']:
                print("❌ Transaction cancelled by user")
                return
        
        super().withdraw(amount)
        
        if amount > self.insurance_threshold:
            print(f"✅ Protected transaction completed successfully")
    
    def charge_monthly_fee(self):
        """Cobra taxa mensal do seguro"""
        try:
            current_balance = self._wrapped_user.get_balance()
            self._wrapped_user.set_balance(current_balance - self.monthly_fee)
            print(f"📋 Insurance monthly fee charged: R$ {self.monthly_fee:.2f}")
        except Exception as e:
            print(f"⚠️ Could not charge insurance fee: {e}")


class NotificationDecorator(UserDecorator):
    """
    Notificações Avançadas - Envia alertas por múltiplos canais:
    - SMS para transações acima de R$ 1.000
    - Email para todas as transações
    - Push notification para login
    """
    
    def __init__(self, user: User, phone: str = None, email: str = None):
        super().__init__(user)
        self.phone = phone or "not_provided"
        self.email = email or "not_provided"
        print("📱 Advanced Notifications activated!")
    
    def withdraw(self, amount: float):
        """Saque com notificações"""
        super().withdraw(amount)
        self._send_notifications("Withdrawal", amount)
    
    def deposit(self, amount: float):
        """Depósito com notificações"""
        super().deposit(amount)
        self._send_notifications("Deposit", amount)
    
    def _send_notifications(self, transaction_type: str, amount: float):
        """Envia notificações por diferentes canais"""
        print(f"\n📧 Email notification sent to: {self.email}")
        print(f"   {transaction_type} of R$ {amount:.2f} completed")
        
        if amount > 1000:
            print(f"📱 SMS notification sent to: {self.phone}")
            print(f"   Large {transaction_type.lower()}: R$ {amount:.2f}")
        
        print()  # Linha em branco para melhor visualização


class StudentAccountDecorator(UserDecorator):
    """
    Conta Estudante - Benefícios para estudantes:
    - Isenção de taxa de talão (sempre grátis)
    - Desconto de 50% em IOF em câmbio
    - Limite de saque diário de R$ 500
    """
    
    def __init__(self, user: User, student_id: str):
        super().__init__(user)
        self.student_id = student_id
        self.daily_withdrawal_limit = 500.00
        self.daily_withdrawn = 0.0
        print("🎓 Student Account activated!")
        print(f"   Student ID: {student_id}")
        print(f"   Daily withdrawal limit: R$ {self.daily_withdrawal_limit:.2f}")
    
    def withdraw(self, amount: float):
        """Saque com limite diário para estudantes"""
        if self.daily_withdrawn + amount > self.daily_withdrawal_limit:
            remaining = self.daily_withdrawal_limit - self.daily_withdrawn
            raise ValueError(
                f"Student Account: Daily withdrawal limit exceeded. "
                f"Remaining today: R$ {remaining:.2f}"
            )
        
        super().withdraw(amount)
        self.daily_withdrawn += amount
        remaining = self.daily_withdrawal_limit - self.daily_withdrawn
        print(f"🎓 Student account - Remaining today: R$ {remaining:.2f}")
    
    def new_checkbook(self):
        """Talão sempre gratuito para estudantes"""
        print("🎓 Student benefit: FREE checkbook!")
        
        from models.history import History_cheque_book
        history_entry = History_cheque_book(
            "New Checkbook",
            "Ordered a new checkbook (FREE - Student benefit)"
        )
        self._wrapped_user.add_history(history_entry)
    
    def reset_daily_limit(self):
        """Reseta o limite diário (chamado a cada novo dia)"""
        self.daily_withdrawn = 0.0
        print("🎓 Daily withdrawal limit reset")


class VIPDecorator(UserDecorator):
    """
    Conta VIP - Máximo de benefícios:
    - Gerente pessoal dedicado
    - Prioridade em atendimento
    - Taxas de juros reduzidas em empréstimos
    - Sala VIP em agências
    """
    
    def __init__(self, user: User, manager_name: str):
        super().__init__(user)
        self.manager_name = manager_name
        self.interest_rate_discount = 0.30  # 30% de desconto em juros
        print("👑 VIP Account activated!")
        print(f"   Personal Manager: {manager_name}")
        print(f"   Interest rate discount: {self.interest_rate_discount * 100:.0f}%")
    
    def get_interest_rate_discount(self) -> float:
        """Retorna desconto em taxa de juros"""
        return self.interest_rate_discount
    
    def contact_manager(self):
        """Contata o gerente pessoal"""
        print(f"\n📞 Connecting you to your personal manager...")
        print(f"   Manager: {self.manager_name}")
        print(f"   Phone: 0800-VIP-MANAGER")
        print(f"   Available 24/7 for VIP clients")


# Função helper para aplicar múltiplos decorators facilmente
def decorate_user(user: User, decorators: list) -> User:
    """
    Aplica múltiplos decorators a um usuário
    
    Exemplo:
        decorated_user = decorate_user(user, [
            ('premium', {}),
            ('insurance', {}),
            ('notification', {'email': 'user@email.com', 'phone': '123456789'})
        ])
    """
    decorated = user
    
    decorator_map = {
        'premium': PremiumAccountDecorator,
        'insurance': InsuranceDecorator,
        'notification': NotificationDecorator,
        'student': StudentAccountDecorator,
        'vip': VIPDecorator
    }
    
    for decorator_type, kwargs in decorators:
        if decorator_type in decorator_map:
            decorator_class = decorator_map[decorator_type]
            decorated = decorator_class(decorated, **kwargs)
        else:
            print(f"⚠️ Unknown decorator type: {decorator_type}")
    
    return decorated
