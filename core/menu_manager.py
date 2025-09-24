"""
Menu Manager - Gerencia todas as operações do menu
Utilizando os padrões implementados para executar operações

"""

from typing import Optional
from models.users import User, Investor
from core.bank_singleton import BankSystem
from core.transaction_factory import TransactionFactoryProvider
from core.user_factory import UserFactoryProvider
from models.bill import Bill
from models.loan import Loan
from models.goal import Goal
from datetime import datetime, timedelta

class MenuManager:

    """Gerencia todas as operações do menu do sistema bancário"""
    
    def __init__(self):
        self.bank_system = BankSystem()
        self.logged_account: Optional[User] = None
    
    def initialize_system(self):
        """Inicializa o sistema com dados de exemplo"""
        self.bank_system.initialize_demo_data()
    
    def login(self) -> bool:
        """Processa o login do usuário"""
        print("North Frontier Bank - Welcome!")
        print("Log in to an existing account or create a new one.")
        nome = input("Enter your name: ")
        senha = input("Enter your password: ")
        
        # busca conta existente
        account = self.bank_system.find_account(nome, senha)
        
        if account:
            self.logged_account = account
            print(f"Welcome, {self.logged_account.get_name()}!")
            return True
        else:
            # cria nova conta
            print("Conta não encontrada. Criando uma nova conta...")
            regular_factory = UserFactoryProvider.get_factory("regular")
            new_account = regular_factory.create_user(nome, senha, 0)
            self.bank_system.add_account(new_account)
            self.logged_account = new_account
            return True
    
    def show_balance(self):
        """Mostra o saldo atual"""
        print(f"Your balance is: R$ {self.logged_account.get_balance():.2f}")
        print(f"Your dollar balance is: $ {self.logged_account.get_dolar_balance():.2f}")
    
    def process_withdrawal(self):
        """Processa saque"""
        try:
            amount = float(input("Enter the amount to withdraw: "))
            self.logged_account.withdraw(amount)
            
            # factory para criar histórico
            factory = TransactionFactoryProvider.get_factory(self.logged_account)
            history = factory.create_transaction_history(
                "Withdrawal",
                f"Withdrew {amount} from account",
                amount,
                self.logged_account.get_balance()
            )
            self.logged_account.add_history(history)
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def process_deposit(self):
        """Processa depósito"""
        try:
            amount = float(input("Enter the amount to deposit: "))
            self.logged_account.deposit(amount)
            
            # factory para criar histórico
            factory = TransactionFactoryProvider.get_factory(self.logged_account)
            history = factory.create_transaction_history(
                "Deposit",
                f"Deposited {amount} into account",
                amount,
                self.logged_account.get_balance()
            )
            self.logged_account.add_history(history)
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def show_history(self):
        """Mostra histórico de transações"""
        print("\n========== History ==========\n")
        historico = self.logged_account.get_history()
        
        if not historico:
            print("📝 No transactions found.")
        else:
            print(f"📊 Total transactions: {len(historico)}")
            print("-" * 50)
            
            for i, history in enumerate(historico, 1):
                print(f"\n🔹 Transaction {i}:")
                history.show()
                print("-" * 30)
        
        print("\n" + "=" * 45)
        input("Press Enter to continue...")
    
    def process_transfer(self):
        """Processa transferência"""
        print("\n========== Transfer ==========\n")
        
        other_accounts = self.bank_system.get_other_accounts(self.logged_account)
        
        if not other_accounts:
            print("No other accounts available for transfer.")
            return
        
        # contas disponíveis
        for i, account in enumerate(other_accounts, 1):
            print(f"{i}. {account.get_name()}")
        
        try:
            choice = int(input("Select the account to transfer to (number): "))
            if 1 <= choice <= len(other_accounts):
                target_account = other_accounts[choice - 1]
                amount = float(input("Enter the amount to transfer: "))
                
                # Usa a função transaction existente
                from models.users import transaction
                transaction(self.logged_account, target_account, amount)
                print(f"✅ Transfer completed successfully!")
                
            else:
                print("Invalid account selection.")
                
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
    
    def change_account(self) -> bool:
        """Troca de conta - retorna True se mudou de conta"""
        print("\n========== Change Account ==========\n")
        print(f"Currently logged in as: {self.logged_account.get_name()}")
        
        other_accounts = self.bank_system.get_other_accounts(self.logged_account)
        
        if not other_accounts:
            print("No other accounts available to switch to.")
            input("Press Enter to continue...")
            return False
        
        print("\nAvailable accounts:")
        for i, account in enumerate(other_accounts, 1):
            account_type = "Investor" if isinstance(account, Investor) else "Regular User"
            print(f"{i}. {account.get_name()} ({account_type})")
        
        try:
            choice = int(input("\nSelect the account to switch to (number, 0 to cancel): "))
            
            if choice == 0:
                print("Account switch cancelled.")
                return False
            elif 1 <= choice <= len(other_accounts):
                selected_account = other_accounts[choice - 1]
                password = input(f"Enter password for {selected_account.get_name()}: ")
                
                if password == selected_account.get_password():
                    self.logged_account = selected_account
                    print(f"✅ Successfully switched to account: {self.logged_account.get_name()}")
                    print(f"Account type: {'Investor' if isinstance(self.logged_account, Investor) else 'Regular User'}")
                    print(f"Balance: R$ {self.logged_account.get_balance():.2f}")
                    return True
                else:
                    print("❌ Incorrect password. Account switch failed.")
            else:
                print("❌ Invalid account selection.")
                
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
        
        input("Press Enter to continue...")
        return False
    


    def pay_bills(self):
        """
        Processa pagamento de boletos
        
        TODO -> Boletos devem ser individuais de cada user
        """

        print("\n========== Pay Bills ==========\n")
        
        unpaid_bills = self.bank_system.get_unpaid_bills()
        
        if not unpaid_bills:
            print("✅ All bills have been paid!")
            input("Press Enter to continue...")
            return
        
        print(f"Found {len(unpaid_bills)} unpaid bill(s):")
        print("-" * 50)
        
        # Mostra boletos não pagos
        for i, bill in enumerate(unpaid_bills, 1):
            status = "⚠️ OVERDUE" if bill.is_overdue() else "Pending"
            print(f"{i}. {bill.get_description()}")
            print(f"   💰 Value: R$ {bill.get_value():.2f}")
            print(f"   📅 Due Date: {bill.get_due_date().strftime('%Y-%m-%d')}")
            print(f"   🚨 Status: {status}")
            print("-" * 30)
        
        print(f"\n💳 Your current balance: R$ {self.logged_account.get_balance():.2f}")
        
        try:
            choice = int(input("\nSelect the bill to pay (number, 0 to cancel): "))
            
            if choice == 0:
                print("❌ Payment cancelled.")
            elif 1 <= choice <= len(unpaid_bills):
                selected_bill = unpaid_bills[choice - 1]
                
                print(f"\n📋 Bill Details:")
                print(f"Description: {selected_bill.get_description()}")
                print(f"Value: R$ {selected_bill.get_value():.2f}")
                print(f"Due Date: {selected_bill.get_due_date().strftime('%Y-%m-%d')}")
                
                if selected_bill.is_overdue():
                    print("⚠️  WARNING: This bill is overdue!")
                
                confirm = input("\nConfirm payment? (y/n): ").lower().strip()
                
                if confirm in ['y', 'yes', 's', 'sim']:
                    try:
                        selected_bill.pay(self.logged_account)
                        print(f"✅ Bill paid successfully!")
                        print(f"💰 New balance: R$ {self.logged_account.get_balance():.2f}")
                    except ValueError as e:
                        print(f"❌ Error: {e}")
                else:
                    print("❌ Payment cancelled.")
            else:
                print("❌ Invalid bill selection.")
                
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
        
        input("\nPress Enter to continue...")
    
    def exchange_real_to_dollar(self):
        """Troca Real para Dólar"""
        print("\n💱 Exchange Real to Dollar")
        try:
            amount = float(input("Enter amount in R$: "))
            exchange_rate = self.bank_system.get_exchange_rate()
            dollars = amount / exchange_rate
            
            if amount > self.logged_account.get_balance():
                print("❌ Insufficient funds for this exchange.")
            else:
                self.logged_account.set_balance(self.logged_account.get_balance() - amount)
                self.logged_account.set_dolar_balance(self.logged_account.get_dolar_balance() + dollars)
                print(f"✅ Successfully exchanged R$ {amount:.2f} to $ {dollars:.2f}")
                print(f"💰 New balance: R$ {self.logged_account.get_balance():.2f}, $ {self.logged_account.get_dolar_balance():.2f}")
        except ValueError:
            print("❌ Invalid amount entered.")
    
    def exchange_dollar_to_real(self):
        """Troca Dólar para Real"""
        print("\n💱 Exchange Dollar to Real")
        try:
            amount = float(input("Enter amount in $: "))
            exchange_rate = self.bank_system.get_exchange_rate()
            reais = amount * exchange_rate
            
            if amount > self.logged_account.get_dolar_balance():
                print("❌ Insufficient funds for this exchange.")
            else:
                self.logged_account.set_dolar_balance(self.logged_account.get_dolar_balance() - amount)
                self.logged_account.set_balance(self.logged_account.get_balance() + reais)
                print(f"✅ Successfully exchanged $ {amount:.2f} to R$ {reais:.2f}")
                print(f"💰 New balance: R$ {self.logged_account.get_balance():.2f}, $ {self.logged_account.get_dolar_balance():.2f}")
        except ValueError:
            print("❌ Invalid amount entered.")
    
    def process_loan(self):
        """Processa empréstimo"""
        print("\n💰 Make a Loan")
        print(f"Current balance: R$ {self.logged_account.get_balance():.2f}")
        print(f"Maximum loan amount: R$ {self.logged_account.get_balance() * 2:.2f}")
        
        try:
            amount = float(input("Enter loan amount: R$ "))
            
            if amount <= 0:
                print("❌ Loan amount must be positive.")
                return
            elif amount > self.logged_account.get_balance() * 2:
                print("❌ Loan amount exceeds limit (max 2x your current balance).")
                return
            
            duration = int(input("Enter loan duration in months (6-60): "))
            
            if duration < 6 or duration > 60:
                print("❌ Loan duration must be between 6 and 60 months.")
                return
            
            print(f"\n📋 Loan Summary:")
            print(f"Loan amount: R$ {amount:.2f}")
            print(f"Duration: {duration} months")
            
            confirm = input("\nConfirm loan? (y/n): ").lower().strip()
            
            if confirm in ['y', 'yes', 's', 'sim']:
                # cria o empréstimo
                Loan(amount, duration, self.logged_account)
                
                # cria boleto para pagamento
                due_date = datetime.now() + timedelta(days=duration * 30)
                due_date_str = due_date.strftime("%Y-%m-%d")
                
                payment_bill = Bill(amount, f"Loan Payment - {duration} months", due_date_str)
                self.bank_system.add_bill(payment_bill)
                
                # Adiciona saldo
                self.logged_account.set_balance(self.logged_account.get_balance() + amount)
                
                print(f"✅ Loan approved: R$ {amount:.2f}")
                print(f"💰 New balance: R$ {self.logged_account.get_balance():.2f}")
                print(f"📅 Payment due: {due_date_str}")
                print(f"💳 A bill has been created for the amount: R$ {amount:.2f}")
            else:
                print("❌ Loan cancelled.")
                
        except ValueError:
            print("❌ Invalid input. Please enter valid numbers.")
        
        input("Press Enter to continue...")
    
    def order_checkbook(self):
        """Processa pedido de talão"""
        self.logged_account.new_checkbook()
    
    def create_investment_goal(self):
        """Cria meta de investimento"""
        if not isinstance(self.logged_account, Investor):
            print("❌ Only Investor accounts can create investment goals.")
            input("Press Enter to continue...")
            return
        
        print("\n🎯 Create Investment Goal")
        print(f"💰 Current balance: R$ {self.logged_account.get_balance():.2f}")
        
        try:
            description = input("Enter your investment goal description: ")
            
            if not description.strip():
                print("❌ Description cannot be empty.")
                input("Press Enter to continue...")
                return
            
            value_needed = float(input("Enter the target amount for your goal (R$): "))
            
            if value_needed <= 0:
                print("❌ Target amount must be positive.")
                input("Press Enter to continue...")
                return
            
            print(f"\n📋 Investment Goal Summary:")
            print(f"Description: {description}")
            print(f"Target Amount: R$ {value_needed:.2f}")
            
            confirm = input("\nConfirm investment goal creation? (y/n): ").lower().strip()
            
            if confirm in ['y', 'yes', 's', 'sim']:
                Goal(value_needed, description, self.logged_account)
                print(f"✅ Investment goal created successfully!")
                print(f"🎯 Goal: {description}")
                print(f"💰 Target: R$ {value_needed:.2f}")
                print(f"📊 You now have {len(self.logged_account.get_investment_goals())} active investment goal(s)")
            else:
                print("❌ Investment goal creation cancelled.")
                
        except ValueError:
            print("❌ Invalid input. Please enter valid numbers.")
        
        input("Press Enter to continue...")
    
    def deposit_in_goal(self):
        """Deposita em meta de investimento"""
        print("\n💰 Deposit in Investment Goal")
        
        if not isinstance(self.logged_account, Investor):
            print("❌ Only Investor accounts can deposit into investment goals.")
            input("Press Enter to continue...")
            return


        goals = self.logged_account.get_investment_goals()
        
        if not goals:
            print("❌ No investment goals found. Create a goal first (option 12).")
            input("Press Enter to continue...")
            return
        
        print(f"💳 Current balance: R$ {self.logged_account.get_balance():.2f}")
        print("\n📋 Your Investment Goals:")
        print("-" * 50)
        
        # metas disponiveis
        for i, goal in enumerate(goals, 1):
            print(f"{i}. {goal.get_description()}")
            print(f"   🎯 Target: R$ {goal.get_value_needed():.2f}")
            print("-" * 30)
        
        try:
            choice = int(input("\nSelect goal to deposit into (number, 0 to cancel): "))
            
            if choice == 0:
                print("❌ Operation cancelled.")
            elif 1 <= choice <= len(goals):
                selected_goal = goals[choice - 1]
                
                print(f"\n📋 Selected Goal: {selected_goal.get_description()}")
                print(f"🎯 Target Amount: R$ {selected_goal.get_value_needed():.2f}")
                print(f"💰 Your balance: R$ {self.logged_account.get_balance():.2f}")
                
                deposit_amount = float(input("\nEnter amount to deposit in goal (R$): "))
                
                if deposit_amount <= 0:
                    print("❌ Deposit amount must be positive.")
                elif deposit_amount > self.logged_account.get_balance():
                    print("❌ Insufficient balance for this deposit.")
                else:
                    confirm = input(f"\nConfirm deposit of R$ {deposit_amount:.2f} into '{selected_goal.get_description()}'? (y/n): ").lower().strip()
                    
                    if confirm in ['y', 'yes', 's', 'sim']:
                        selected_goal.add_value(self.logged_account, deposit_amount)
                        print(f"✅ Successfully deposited R$ {deposit_amount:.2f} into your investment goal!")
                        print(f"💰 New balance: R$ {self.logged_account.get_balance():.2f}")
                        
                        if selected_goal.get_value_needed() <= 0:
                            print("🎉 Congratulations! You've reached your investment goal!")
                    else:
                        print("❌ Deposit cancelled.")
            else:
                print("❌ Invalid goal selection.")
                
        except ValueError:
            print("❌ Invalid input. Please enter valid numbers.")
        
        input("Press Enter to continue...")
