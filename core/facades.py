"""
Facade Pattern - Simplifica operações complexas do sistema bancário
Fornece interfaces unificadas para subsistemas complexos

Facades disponíveis:
- BankingFacade: Operações bancárias simplificadas
- InvestmentFacade: Gestão de investimentos facilitada
- ReportFacade: Geração de relatórios completos
"""

from typing import List, Dict, Optional
from models.users import User, Investor, transaction
from models.bill import Bill
from models.goal import Goal
from models.loan import Loan
from core.bank_singleton import BankSystem
from core.transaction_factory import TransactionFactoryProvider
from core.loan_strategy import LoanStrategyProvider, LoanProcessor
from datetime import datetime, timedelta


class BankingFacade:
    """
    Facade para operações bancárias complexas
    Simplifica operações que envolvem múltiplos subsistemas
    """
    
    def __init__(self, user: User):
        self.user = user
        self.bank = BankSystem()
        self.transaction_factory = TransactionFactoryProvider.get_factory(user)
    
    def quick_transfer_with_exchange(self, target_user: User, 
                                     amount: float, currency: str = "BRL") -> bool:
        """
        Transfere dinheiro com conversão automática se necessário
        
        Args:
            target_user: Usuário destinatário
            amount: Valor a transferir
            currency: Moeda ("BRL" ou "USD")
        
        Returns:
            True se sucesso, False se falhou
        """
        try:
            print(f"\n💸 Quick Transfer with Exchange")
            print(f"From: {self.user.get_name()}")
            print(f"To: {target_user.get_name()}")
            print(f"Amount: {amount} {currency}")
            
            if currency.upper() == "USD":
                rate = self.bank.get_exchange_rate()
                amount_brl = amount * rate
                
                if self.user.get_dolar_balance() < amount:
                    print(f"❌ Insufficient dollar balance")
                    return False
                
                # Converte dólares para reais
                self.user.set_dolar_balance(self.user.get_dolar_balance() - amount)
                print(f"💱 Exchange: ${amount:.2f} → R$ {amount_brl:.2f} (Rate: {rate})")
            else:
                amount_brl = amount
            
            # Executa a transferência
            transaction(self.user, target_user, amount_brl)
            print(f"✅ Transfer completed successfully!")
            print(f"   {self.user.get_name()}: R$ {self.user.get_balance():.2f}")
            print(f"   {target_user.get_name()}: R$ {target_user.get_balance():.2f}")
            return True
            
        except Exception as e:
            print(f"❌ Transfer failed: {e}")
            return False
    
    def pay_all_bills(self, filter_overdue: bool = False) -> Dict[str, any]:
        """
        Paga todos os boletos pendentes de uma vez
        
        Args:
            filter_overdue: Se True, paga apenas boletos vencidos
        
        Returns:
            Dicionário com estatísticas do pagamento
        """
        print(f"\n💳 Pay All Bills")
        
        bills = self.bank.get_unpaid_bills()
        
        if filter_overdue:
            bills = [b for b in bills if b.is_overdue()]
            print(f"📋 Paying only overdue bills")
        
        if not bills:
            print("✅ No bills to pay!")
            return {"success": True, "paid": 0, "total": 0}
        
        total = sum(bill.get_value() for bill in bills)
        print(f"📊 Found {len(bills)} bill(s)")
        print(f"💰 Total amount: R$ {total:.2f}")
        print(f"💳 Your balance: R$ {self.user.get_balance():.2f}")
        
        if self.user.get_balance() < total:
            shortfall = total - self.user.get_balance()
            print(f"❌ Insufficient balance!")
            print(f"   Missing: R$ {shortfall:.2f}")
            return {"success": False, "paid": 0, "total": total}
        
        confirm = input("\n⚠️  Pay all bills? (y/n): ").lower().strip()
        if confirm not in ['y', 'yes', 's', 'sim']:
            print("❌ Payment cancelled")
            return {"success": False, "paid": 0, "total": total}
        
        # Paga todos os boletos
        paid_count = 0
        for bill in bills:
            try:
                bill.pay(self.user)
                paid_count += 1
            except Exception as e:
                print(f"⚠️ Error paying {bill.get_description()}: {e}")
        
        print(f"\n✅ Successfully paid {paid_count} bill(s)")
        print(f"💰 New balance: R$ {self.user.get_balance():.2f}")
        
        return {
            "success": True,
            "paid": paid_count,
            "total": total,
            "remaining_balance": self.user.get_balance()
        }
    
    def create_savings_plan(self, monthly_amount: float, goal_description: str, 
                           months: int) -> bool:
        """
        Cria um plano de poupança completo
        
        Args:
            monthly_amount: Valor mensal a poupar
            goal_description: Descrição da meta
            months: Duração em meses
        
        Returns:
            True se criado com sucesso
        """
        print(f"\n💰 Create Savings Plan")
        
        if not isinstance(self.user, Investor):
            print("❌ Only Investor accounts can create savings plans")
            print("   Upgrade your account to access this feature")
            return False
        
        total_goal = monthly_amount * months
        
        print(f"📋 Plan Summary:")
        print(f"   Goal: {goal_description}")
        print(f"   Monthly deposit: R$ {monthly_amount:.2f}")
        print(f"   Duration: {months} months")
        print(f"   Total target: R$ {total_goal:.2f}")
        print(f"   Start date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"   End date: {(datetime.now() + timedelta(days=months*30)).strftime('%Y-%m-%d')}")
        
        if self.user.get_balance() < monthly_amount:
            print(f"\n⚠️ Warning: Insufficient balance for first deposit")
            print(f"   Current balance: R$ {self.user.get_balance():.2f}")
            print(f"   Required: R$ {monthly_amount:.2f}")
        
        confirm = input("\n❓ Create this savings plan? (y/n): ").lower().strip()
        if confirm not in ['y', 'yes', 's', 'sim']:
            print("❌ Savings plan cancelled")
            return False
        
        # Cria a meta de investimento
        Goal(total_goal, goal_description, self.user)
        
        print(f"\n✅ Savings plan created successfully!")
        print(f"📊 Tip: Use option 13 to make monthly deposits")
        
        return True
    
    def emergency_loan(self, reason: str) -> bool:
        """
        Solicita empréstimo emergencial com processo simplificado
        Usa a melhor estratégia disponível automaticamente
        
        Args:
            reason: Motivo do empréstimo emergencial
        
        Returns:
            True se aprovado
        """
        print(f"\n🚨 Emergency Loan Request")
        print(f"Reason: {reason}")
        print(f"Current balance: R$ {self.user.get_balance():.2f}")
        
        # Usa estratégia automática
        strategy = LoanStrategyProvider.get_strategy(self.user, "auto")
        max_loan = strategy.calculate_max_loan(self.user)
        
        # Sugere valor (50% do máximo)
        suggested_amount = max_loan * 0.5
        
        print(f"\n📊 Emergency Loan Details:")
        print(f"   Maximum available: R$ {max_loan:.2f}")
        print(f"   Suggested amount: R$ {suggested_amount:.2f}")
        
        try:
            amount = float(input(f"\nEnter loan amount (max R$ {max_loan:.2f}): R$ "))
            duration = 12  # Empréstimo emergencial padrão: 12 meses
            
            processor = LoanProcessor(self.user, strategy)
            
            if processor.process_loan_request(amount, duration):
                confirm = input("\n⚠️  Confirm emergency loan? (y/n): ").lower().strip()
                
                if confirm in ['y', 'yes', 's', 'sim']:
                    # Processa o empréstimo
                    interest_rate = strategy.calculate_interest_rate(amount, duration, self.user)
                    total_amount = amount * (1 + interest_rate / 100)
                    
                    Loan(amount, duration, self.user)
                    
                    # Cria boleto de pagamento
                    due_date = datetime.now() + timedelta(days=duration * 30)
                    payment_bill = Bill(
                        total_amount,
                        f"Emergency Loan Payment - {reason}",
                        due_date.strftime("%Y-%m-%d")
                    )
                    self.bank.add_bill(payment_bill)
                    
                    # Adiciona saldo
                    self.user.set_balance(self.user.get_balance() + amount)
                    
                    print(f"\n✅ Emergency loan approved!")
                    print(f"💰 New balance: R$ {self.user.get_balance():.2f}")
                    return True
            
            print("❌ Loan not approved")
            return False
            
        except Exception as e:
            print(f"❌ Error processing emergency loan: {e}")
            return False
    
    def get_account_summary(self) -> Dict[str, any]:
        """
        Retorna um resumo completo da conta
        
        Returns:
            Dicionário com todas as informações relevantes
        """
        unpaid_bills = [b for b in self.bank.get_unpaid_bills()]
        overdue_bills = [b for b in unpaid_bills if b.is_overdue()]
        
        summary = {
            "name": self.user.get_name(),
            "account_type": "Investor" if isinstance(self.user, Investor) else "Regular",
            "balance_brl": self.user.get_balance(),
            "balance_usd": self.user.get_dolar_balance(),
            "loans": len(self.user.get_loans()),
            "transactions": len(self.user.get_history()),
            "unpaid_bills": len(unpaid_bills),
            "overdue_bills": len(overdue_bills),
            "total_debt": sum(b.get_value() for b in unpaid_bills)
        }
        
        if isinstance(self.user, Investor):
            summary["investment_goals"] = len(self.user.get_investment_goals())
        
        return summary
    
    def print_account_summary(self):
        """Imprime um resumo visual da conta"""
        summary = self.get_account_summary()
        
        print("\n" + "="*50)
        print("📊 ACCOUNT SUMMARY")
        print("="*50)
        print(f"👤 Name: {summary['name']}")
        print(f"🏦 Account Type: {summary['account_type']}")
        print(f"\n💰 BALANCES:")
        print(f"   Real: R$ {summary['balance_brl']:.2f}")
        print(f"   Dollar: $ {summary['balance_usd']:.2f}")
        print(f"\n📈 ACTIVITY:")
        print(f"   Transactions: {summary['transactions']}")
        print(f"   Active Loans: {summary['loans']}")
        print(f"\n💳 BILLS:")
        print(f"   Unpaid: {summary['unpaid_bills']}")
        print(f"   Overdue: {summary['overdue_bills']}")
        print(f"   Total Debt: R$ {summary['total_debt']:.2f}")
        
        if 'investment_goals' in summary:
            print(f"\n🎯 INVESTMENTS:")
            print(f"   Active Goals: {summary['investment_goals']}")
        
        print("="*50)


class InvestmentFacade:
    """
    Facade para operações de investimento
    Simplifica a gestão de portfólio para investidores
    """
    
    def __init__(self, user: Investor):
        if not isinstance(user, Investor):
            raise TypeError("InvestmentFacade requires an Investor account")
        self.user = user
        self.bank = BankSystem()
    
    def create_diversified_portfolio(self, total_amount: float, 
                                    goals: List[Dict[str, any]]) -> bool:
        """
        Cria um portfólio diversificado com múltiplas metas
        
        Args:
            total_amount: Valor total a investir
            goals: Lista de dicionários com 'description' e 'percentage'
        
        Exemplo:
            goals = [
                {'description': 'Emergency Fund', 'percentage': 30},
                {'description': 'Vacation', 'percentage': 40},
                {'description': 'New Car', 'percentage': 30}
            ]
        """
        print(f"\n📊 Create Diversified Portfolio")
        print(f"Total investment: R$ {total_amount:.2f}")
        
        if self.user.get_balance() < total_amount:
            print(f"❌ Insufficient balance")
            print(f"   Required: R$ {total_amount:.2f}")
            print(f"   Available: R$ {self.user.get_balance():.2f}")
            return False
        
        # Valida percentuais
        total_percentage = sum(g['percentage'] for g in goals)
        if abs(total_percentage - 100) > 0.01:
            print(f"❌ Percentages must sum to 100% (current: {total_percentage}%)")
            return False
        
        print(f"\n📋 Portfolio Allocation:")
        for goal in goals:
            amount = total_amount * (goal['percentage'] / 100)
            print(f"   • {goal['description']}: {goal['percentage']}% (R$ {amount:.2f})")
        
        confirm = input("\n❓ Create this portfolio? (y/n): ").lower().strip()
        if confirm not in ['y', 'yes', 's', 'sim']:
            print("❌ Portfolio creation cancelled")
            return False
        
        # Cria as metas
        for goal in goals:
            amount = total_amount * (goal['percentage'] / 100)
            Goal(amount, goal['description'], self.user)
            print(f"✅ Created: {goal['description']}")
        
        print(f"\n✅ Portfolio created successfully!")
        print(f"📊 Total goals: {len(goals)}")
        return True
    
    def auto_invest_monthly(self, monthly_amount: float) -> bool:
        """
        Distribui investimento mensal automaticamente entre metas ativas
        
        Args:
            monthly_amount: Valor a investir mensalmente
        """
        print(f"\n💰 Auto-Invest Monthly: R$ {monthly_amount:.2f}")
        
        goals = self.user.get_investment_goals()
        if not goals:
            print("❌ No active investment goals")
            return False
        
        if self.user.get_balance() < monthly_amount:
            print(f"❌ Insufficient balance")
            return False
        
        # Distribui igualmente entre metas
        per_goal = monthly_amount / len(goals)
        
        print(f"📊 Distributing among {len(goals)} goal(s):")
        print(f"   Amount per goal: R$ {per_goal:.2f}")
        
        for goal in goals:
            print(f"   • {goal.get_description()}: R$ {per_goal:.2f}")
        
        confirm = input("\n❓ Execute auto-invest? (y/n): ").lower().strip()
        if confirm not in ['y', 'yes', 's', 'sim']:
            print("❌ Auto-invest cancelled")
            return False
        
        # Executa os investimentos
        for goal in goals:
            goal.add_value(self.user, per_goal)
        
        print(f"\n✅ Auto-invest completed!")
        print(f"💰 New balance: R$ {self.user.get_balance():.2f}")
        return True
    
    def get_portfolio_summary(self) -> Dict[str, any]:
        """Retorna resumo do portfólio de investimentos"""
        goals = self.user.get_investment_goals()
        
        total_target = sum(g.get_value_needed() for g in goals)
        
        return {
            "total_goals": len(goals),
            "total_target": total_target,
            "goals_detail": [
                {
                    "description": g.get_description(),
                    "target": g.get_value_needed(),
                    "remaining": g.get_value_needed()
                }
                for g in goals
            ]
        }
    
    def print_portfolio_summary(self):
        """Imprime resumo visual do portfólio"""
        summary = self.get_portfolio_summary()
        
        print("\n" + "="*50)
        print("📊 INVESTMENT PORTFOLIO SUMMARY")
        print("="*50)
        print(f"🎯 Active Goals: {summary['total_goals']}")
        print(f"💰 Total Target: R$ {summary['total_target']:.2f}")
        print(f"\n📋 Goals Detail:")
        
        for i, goal in enumerate(summary['goals_detail'], 1):
            print(f"\n{i}. {goal['description']}")
            print(f"   Target: R$ {goal['target']:.2f}")
            print(f"   Remaining: R$ {goal['remaining']:.2f}")
            progress = ((goal['target'] - goal['remaining']) / goal['target'] * 100) if goal['target'] > 0 else 0
            print(f"   Progress: {progress:.1f}%")
        
        print("="*50)


class ReportFacade:
    """
    Facade para geração de relatórios
    Gera relatórios completos e análises do usuário
    """
    
    def __init__(self, user: User):
        self.user = user
        self.bank = BankSystem()
    
    def generate_financial_report(self, period_days: int = 30) -> Dict[str, any]:
        """
        Gera relatório financeiro completo
        
        Args:
            period_days: Período em dias para análise
        
        Returns:
            Dicionário com análise financeira
        """
        from datetime import datetime, timedelta
        
        history = self.user.get_history()
        cutoff_date = datetime.now() - timedelta(days=period_days)
        
        # Filtra transações do período
        recent_transactions = [h for h in history]  # Simplificado
        
        # Análise de transações
        deposits = []
        withdrawals = []
        
        from models.history import History_transaction
        for h in recent_transactions:
            if isinstance(h, History_transaction):
                # Aqui seria necessário acessar o amount, mas está privado
                # Em produção, adicionaríamos getters
                pass
        
        report = {
            "period_days": period_days,
            "total_transactions": len(recent_transactions),
            "current_balance": self.user.get_balance(),
            "total_loans": len(self.user.get_loans()),
            "account_type": "Investor" if isinstance(self.user, Investor) else "Regular"
        }
        
        return report
    
    def print_financial_report(self, period_days: int = 30):
        """Imprime relatório financeiro formatado"""
        report = self.generate_financial_report(period_days)
        
        print("\n" + "="*60)
        print("📈 FINANCIAL REPORT")
        print("="*60)
        print(f"📅 Period: Last {report['period_days']} days")
        print(f"👤 Account: {self.user.get_name()} ({report['account_type']})")
        print(f"\n💰 CURRENT STATUS:")
        print(f"   Balance: R$ {report['current_balance']:.2f}")
        print(f"   Dollar Balance: $ {self.user.get_dolar_balance():.2f}")
        print(f"\n📊 ACTIVITY:")
        print(f"   Total Transactions: {report['total_transactions']}")
        print(f"   Active Loans: {report['total_loans']}")
        
        if isinstance(self.user, Investor):
            goals = self.user.get_investment_goals()
            print(f"\n🎯 INVESTMENTS:")
            print(f"   Active Goals: {len(goals)}")
        
        print("="*60)
    
    def generate_tax_report(self) -> Dict[str, any]:
        """
        Gera relatório para declaração de imposto de renda
        """
        print("\n📋 TAX REPORT GENERATOR")
        print("="*50)
        
        history = self.user.get_history()
        
        report = {
            "taxpayer": self.user.get_name(),
            "year": datetime.now().year,
            "total_transactions": len(history),
            "current_balance": self.user.get_balance(),
            "loans_taken": len(self.user.get_loans())
        }
        
        print(f"Taxpayer: {report['taxpayer']}")
        print(f"Year: {report['year']}")
        print(f"Total Transactions: {report['total_transactions']}")
        print(f"Current Balance: R$ {report['current_balance']:.2f}")
        print(f"Loans: {report['loans_taken']}")
        print("\n✅ Tax report generated")
        print("📧 Report ready for export")
        
        return report
    
    def compare_with_average(self) -> Dict[str, any]:
        """
        Compara a conta do usuário com médias do sistema
        """
        all_accounts = self.bank.get_accounts()
        
        if not all_accounts:
            return {}
        
        avg_balance = sum(acc.get_balance() for acc in all_accounts) / len(all_accounts)
        avg_transactions = sum(len(acc.get_history()) for acc in all_accounts) / len(all_accounts)
        
        user_balance = self.user.get_balance()
        user_transactions = len(self.user.get_history())
        
        comparison = {
            "user_balance": user_balance,
            "avg_balance": avg_balance,
            "balance_difference": user_balance - avg_balance,
            "user_transactions": user_transactions,
            "avg_transactions": avg_transactions,
            "transaction_difference": user_transactions - avg_transactions
        }
        
        return comparison
    
    def print_comparison_report(self):
        """Imprime relatório comparativo"""
        comp = self.compare_with_average()
        
        if not comp:
            print("❌ Unable to generate comparison")
            return
        
        print("\n" + "="*60)
        print("📊 COMPARATIVE ANALYSIS")
        print("="*60)
        
        print(f"\n💰 BALANCE COMPARISON:")
        print(f"   Your balance: R$ {comp['user_balance']:.2f}")
        print(f"   System average: R$ {comp['avg_balance']:.2f}")
        
        if comp['balance_difference'] > 0:
            print(f"   ✅ You're R$ {comp['balance_difference']:.2f} above average")
        else:
            print(f"   ⚠️  You're R$ {abs(comp['balance_difference']):.2f} below average")
        
        print(f"\n📈 ACTIVITY COMPARISON:")
        print(f"   Your transactions: {comp['user_transactions']}")
        print(f"   System average: {comp['avg_transactions']:.1f}")
        
        if comp['transaction_difference'] > 0:
            print(f"   📊 You're more active than average")
        else:
            print(f"   📊 You're less active than average")
        
        print("="*60)


# Função helper para criar facades facilmente
def get_facades(user: User) -> Dict[str, any]:
    """
    Retorna todas as facades disponíveis para um usuário
    
    Returns:
        Dicionário com facades disponíveis
    """
    facades = {
        'banking': BankingFacade(user),
        'report': ReportFacade(user)
    }
    
    if isinstance(user, Investor):
        facades['investment'] = InvestmentFacade(user)
    
    return facades
