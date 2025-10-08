"""
 **Strategy Pattern** (Behavioral)

Strategy Pattern - Estratégias de Empréstimo
Permite diferentes políticas de aprovação e cálculo de empréstimos

"""

from abc import ABC, abstractmethod
from models.users import User, Investor

class LoanStrategy(ABC):
    """Estratégia abstrata para políticas de empréstimo"""
    
    @abstractmethod
    def calculate_max_loan(self, user: User) -> float:
        """Calcula o valor máximo que pode ser emprestado"""
        pass
    
    @abstractmethod
    def calculate_interest_rate(self, amount: float, duration: int, user: User) -> float:
        """Calcula a taxa de juros do empréstimo"""
        pass
    
    @abstractmethod
    def can_approve_loan(self, user: User, amount: float, duration: int) -> tuple[bool, str]:
        """Verifica se o empréstimo pode ser aprovado
        Retorna: (aprovado: bool, mensagem: str)
        """
        pass

class StandardLoanStrategy(LoanStrategy):
    """Estratégia padrão para usuários regulares"""
    
    def calculate_max_loan(self, user: User) -> float:
        """Máximo de 2x o saldo atual"""
        return user.get_balance() * 2
    
    def calculate_interest_rate(self, amount: float, duration: int, user: User) -> float:
        """Taxa base de 5% + 0.5% por ano de duração"""
        years = duration / 12
        return 5.0 + (years * 0.5)
    
    def can_approve_loan(self, user: User, amount: float, duration: int) -> tuple[bool, str]:
        max_loan = self.calculate_max_loan(user)
        
        if amount <= 0:
            return False, "Loan amount must be positive."
        
        if amount > max_loan:
            return False, f"Loan exceeds limit. Maximum: R$ {max_loan:.2f}"
        
        if duration < 6 or duration > 60:
            return False, "Duration must be between 6 and 60 months."
        
        if user.get_balance() < 100:
            return False, "Minimum balance of R$ 100 required for loan approval."
        
        return True, "Loan approved under standard conditions."

class InvestorLoanStrategy(LoanStrategy):
    """Estratégia premium para investidores - condições melhores"""
    
    def calculate_max_loan(self, user: User) -> float:
        """Investidores podem pegar até 3x o saldo"""
        return user.get_balance() * 3
    
    def calculate_interest_rate(self, amount: float, duration: int, user: User) -> float:
        """Taxa reduzida: 3% + 0.3% por ano"""
        years = duration / 12
        return 3.0 + (years * 0.3)
    
    def can_approve_loan(self, user: User, amount: float, duration: int) -> tuple[bool, str]:
        max_loan = self.calculate_max_loan(user)
        
        if amount <= 0:
            return False, "Loan amount must be positive."
        
        if amount > max_loan:
            return False, f"Loan exceeds limit. Maximum: R$ {max_loan:.2f}"
        
        if duration < 3 or duration > 120:
            return False, "Investor duration: 3 to 120 months."
        
        # Investidores podem ter saldo negativo temporário
        if user.get_balance() < -500:
            return False, "Balance too low for loan approval."
        
        return True, "Loan approved under premium investor conditions! 🎉"

class ConservativeLoanStrategy(LoanStrategy):
    """Estratégia conservadora - requisitos mais rigorosos"""
    
    def calculate_max_loan(self, user: User) -> float:
        """Apenas 1.5x o saldo para segurança"""
        return user.get_balance() * 1.5
    
    def calculate_interest_rate(self, amount: float, duration: int, user: User) -> float:
        """Taxa um pouco maior: 6% + 0.7% por ano"""
        years = duration / 12
        return 6.0 + (years * 0.7)
    
    def can_approve_loan(self, user: User, amount: float, duration: int) -> tuple[bool, str]:
        max_loan = self.calculate_max_loan(user)
        
        if amount <= 0:
            return False, "Loan amount must be positive."
        
        if amount > max_loan:
            return False, f"Conservative limit exceeded. Maximum: R$ {max_loan:.2f}"
        
        if duration < 12 or duration > 36:
            return False, "Conservative policy: 12 to 36 months only."
        
        if user.get_balance() < 500:
            return False, "Minimum balance of R$ 500 required."
        
        # verifica histórico de empréstimos
        if len(user.get_loans()) >= 3:
            return False, "Maximum of 3 active loans allowed."
        
        return True, "Loan approved under conservative policy."

class LoanStrategyProvider:
    """Provedor de estratégias de empréstimo"""
    
    @staticmethod
    def get_strategy(user: User, strategy_type: str = "auto") -> LoanStrategy:

        """
        retorna a estratégia apropriada
        strategy_type: 'auto', 'standard', 'investor', 'conservative'
        auto decide baseado no tipo de usuário
        """
        if strategy_type == "auto":
            # decisão automática baseada no tipo de usuário
            if isinstance(user, Investor):
                return InvestorLoanStrategy()
            else:
                return StandardLoanStrategy()
        elif strategy_type == "standard":
            return StandardLoanStrategy()
        elif strategy_type == "investor":
            return InvestorLoanStrategy()
        elif strategy_type == "conservative":
            return ConservativeLoanStrategy()
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")

        return True

class LoanProcessor:

    """
    processa um pedido de empréstimo usando uma estratégia específica

    """
    
    def __init__(self, user: User, strategy: LoanStrategy):
        self.user = user
        self.strategy = strategy
        
    def process_loan_request(self, amount: float, duration: int) -> bool:
        """
        processa o pedido de empréstimo e retorna se foi aprovado
        """
        approved, message = self.strategy.can_approve_loan(self.user, amount, duration)
        
        print(f"\n🔍 Loan Analysis Result:")
        print(f"'{message}'")
        
        if approved:
            interest_rate = self.strategy.calculate_interest_rate(amount, duration, self.user)
            total_amount = amount * (1 + interest_rate / 100)
            monthly_payment = total_amount / duration
            
            print(f"\n📋 Loan Proposal:")
            print(f"Interest Rate: {interest_rate:.2f}% per year")
            print(f"Total Amount (with interest): R$ {total_amount:.2f}")
            print(f"Monthly Payment: R$ {monthly_payment:.2f}")
            
        return approved
