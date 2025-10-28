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
from core.observers import BalanceObserver, BillNotificationObserver

class MenuManager:

    """Gerencia todas as operações do menu do sistema bancário"""
    
    def __init__(self):
        self.bank_system = BankSystem()
        self.logged_account: Optional[User] = None
    
    def initialize_system(self):
        """Inicializa o sistema com dados de exemplo e anexa observadores"""
        self.bank_system.initialize_demo_data()

        # anexa observadores aos boletos existentes no sistema
        bill_observer = BillNotificationObserver()
        for bill in self.bank_system.get_bills():
            bill.attach(bill_observer)

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
        else:
            # cria nova conta
            print("Conta não encontrada. Criando uma nova conta...")
            regular_factory = UserFactoryProvider.get_factory("regular")
            new_account = regular_factory.create_user(nome, senha, 0)
            self.bank_system.add_account(new_account)
            self.logged_account = new_account

        # anexa os observadores a conta logada
        # anexa BalanceObserver apenas se não estiver anexado
        if not any(isinstance(obs, BalanceObserver) for obs in getattr(self.logged_account, "observers", [])):
            self.logged_account.attach(BalanceObserver())
        # se o user for um investidor GoalProgressObserver aqui
        # if isinstance(self.logged_account, Investor):
        #     self.logged_account.attach(GoalProgressObserver())

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
            CORRIGIDO: Agora mostra apenas bills do usuário logado
        """
        print("\n========== Pay Bills ==========\n")
        
        # CORRIGIDO: Pega apenas bills do usuário logado
        unpaid_bills = self.bank_system.get_unpaid_bills(user=self.logged_account)
        
        if not unpaid_bills:
            print("✅ You have no unpaid bills!")
            input("Press Enter to continue...")
            return
        
        print(f"Found {len(unpaid_bills)} unpaid bill(s) for {self.logged_account.get_name()}:")
        print("-" * 50)
        
        # Mostra boletos não pagos
        for i, bill in enumerate(unpaid_bills, 1):
            status = "⚠️ OVERDUE" if bill.is_overdue() else "Pending"
            owner_info = f" (Owner: {bill.get_owner().get_name()})" if bill.get_owner() else " (Public bill)"
            print(f"{i}. {bill.get_description()}{owner_info}")
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

    def upgrade_account(self):
        """Aplica decorators à conta do usuário para adicionar funcionalidades"""
        print("\n" + "="*50)
        print("✨ ACCOUNT UPGRADE CENTER")
        print("="*50)
        print(f"Current account: {self.logged_account.get_name()}")
        print(f"Balance: R$ {self.logged_account.get_balance():.2f}")
        
        print("\n📋 Available Upgrades:")
        print("1. 💎 Premium Account (Cashback on transactions)")
        print("2. 🛡️  Insurance Protection (Large transaction protection)")
        print("3. 📱 Advanced Notifications (SMS + Email)")
        print("4. 🎓 Student Account (Fee exemptions)")
        print("5. 👑 VIP Account (Personal manager + discounts)")
        print("6. 🎁 Premium Bundle (Premium + Insurance + Notifications)")
        print("0. ↩️  Back to menu")
        
        choice = input("\nSelect upgrade (0-6): ").strip()
        
        from core.decorators import (
            PremiumAccountDecorator,
            InsuranceDecorator,
            NotificationDecorator,
            StudentAccountDecorator,
            VIPDecorator,
            decorate_user
        )
        
        if choice == '1':
            self.logged_account = PremiumAccountDecorator(self.logged_account)
            print("\n✅ Premium Account activated!")
            
        elif choice == '2':
            self.logged_account = InsuranceDecorator(self.logged_account)
            print("\n✅ Insurance Protection activated!")
            
        elif choice == '3':
            email = input("Enter your email: ")
            phone = input("Enter your phone: ")
            self.logged_account = NotificationDecorator(
                self.logged_account, 
                phone=phone, 
                email=email
            )
            print("\n✅ Advanced Notifications activated!")
            
        elif choice == '4':
            student_id = input("Enter your student ID: ")
            self.logged_account = StudentAccountDecorator(
                self.logged_account, 
                student_id=student_id
            )
            print("\n✅ Student Account activated!")
            
        elif choice == '5':
            print("\n👑 VIP Account Activation")
            managers = ["Alice Johnson", "Bob Smith", "Carol Williams"]
            print("Available personal managers:")
            for i, mgr in enumerate(managers, 1):
                print(f"{i}. {mgr}")
            mgr_choice = int(input("Select your manager (1-3): "))
            manager = managers[mgr_choice - 1] if 1 <= mgr_choice <= 3 else managers[0]
            
            self.logged_account = VIPDecorator(self.logged_account, manager_name=manager)
            print("\n✅ VIP Account activated!")
            
        elif choice == '6':
            print("\n🎁 Activating Premium Bundle...")
            email = input("Enter your email: ")
            phone = input("Enter your phone: ")
            
            self.logged_account = decorate_user(self.logged_account, [
                ('premium', {}),
                ('insurance', {}),
                ('notification', {'email': email, 'phone': phone})
            ])
            print("\n✅ Premium Bundle activated!")
            print("   ✨ Premium Cashback")
            print("   🛡️  Transaction Insurance")
            print("   📱 Advanced Notifications")
            
        elif choice == '0':
            return
        else:
            print("❌ Invalid option")
        
        input("\nPress Enter to continue...")



    def quick_operations_menu(self):
        """Menu de operações rápidas usando Facade Pattern"""
        from core.facades import BankingFacade, InvestmentFacade, ReportFacade
        
        banking_facade = BankingFacade(self.logged_account)
        report_facade = ReportFacade(self.logged_account)
        
        while True:
            print("\n" + "="*50)
            print("⚡ QUICK OPERATIONS (Facade Pattern)")
            print("="*50)
            print("1. 💸 Quick Transfer with Exchange")
            print("2. 💳 Pay All Bills at Once")
            print("3. 💰 Create Savings Plan")
            print("4. 🚨 Emergency Loan")
            print("5. 📊 Account Summary")
            print("6. 📈 Financial Report")
            print("7. 📊 Comparison Report")
            
            if isinstance(self.logged_account, Investor):
                print("8. 🎯 Create Diversified Portfolio")
                print("9. 💰 Auto-Invest Monthly")
                print("10. 📊 Portfolio Summary")
            
            print("0. ↩️  Back to main menu")
            
            choice = input("\nSelect operation: ").strip()
            
            if choice == '1':
                # Quick Transfer with Exchange
                other_accounts = self.bank_system.get_other_accounts(self.logged_account)
                if not other_accounts:
                    print("❌ No other accounts available")
                    continue
                
                print("\n📋 Available accounts:")
                for i, acc in enumerate(other_accounts, 1):
                    print(f"{i}. {acc.get_name()}")
                
                try:
                    acc_choice = int(input("Select account: "))
                    target = other_accounts[acc_choice - 1]
                    amount = float(input("Amount: "))
                    currency = input("Currency (BRL/USD): ").upper()
                    
                    banking_facade.quick_transfer_with_exchange(target, amount, currency)
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            elif choice == '2':
                # Pay All Bills
                banking_facade.pay_all_bills()
            
            elif choice == '3':
                # Create Savings Plan
                try:
                    monthly = float(input("Monthly amount: R$ "))
                    goal = input("Goal description: ")
                    months = int(input("Duration (months): "))
                    
                    banking_facade.create_savings_plan(monthly, goal, months)
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            elif choice == '4':
                # Emergency Loan
                reason = input("Reason for emergency loan: ")
                banking_facade.emergency_loan(reason)
            
            elif choice == '5':
                # Account Summary
                banking_facade.print_account_summary()
            
            elif choice == '6':
                # Financial Report
                days = int(input("Period in days (default 30): ") or "30")
                report_facade.print_financial_report(days)
            
            elif choice == '7':
                # Comparison Report
                report_facade.print_comparison_report()
            
            elif choice == '8' and isinstance(self.logged_account, Investor):
                # Diversified Portfolio
                investment_facade = InvestmentFacade(self.logged_account)
                try:
                    total = float(input("Total investment amount: R$ "))
                    num_goals = int(input("Number of goals: "))
                    
                    goals = []
                    for i in range(num_goals):
                        print(f"\nGoal {i+1}:")
                        desc = input("  Description: ")
                        pct = float(input("  Percentage: "))
                        goals.append({'description': desc, 'percentage': pct})
                    
                    investment_facade.create_diversified_portfolio(total, goals)
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            elif choice == '9' and isinstance(self.logged_account, Investor):
                # Auto-Invest
                investment_facade = InvestmentFacade(self.logged_account)
                try:
                    monthly = float(input("Monthly investment: R$ "))
                    investment_facade.auto_invest_monthly(monthly)
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            elif choice == '10' and isinstance(self.logged_account, Investor):
                # Portfolio Summary
                investment_facade = InvestmentFacade(self.logged_account)
                investment_facade.print_portfolio_summary()
            
            elif choice == '0':
                break
            else:
                print("❌ Invalid option")
            
            input("\nPress Enter to continue...")


    """
SUBSTITUIR O MÉTODO payment_methods_menu() em menu_manager.py por este:
"""

    def payment_methods_menu(self):
        """Menu de métodos de pagamento usando Adapter Pattern - CORRIGIDO"""
        from core.adapters import (
            PaymentManager,
            PixAdapter, PixAPI,
            CreditCardAdapter, CreditCardGateway,
            CryptoAdapter, CryptoExchangeAPI,
            InternationalBankAdapter, InternationalBankingAPI
        )
        
        # Cria o gerenciador de pagamentos
        payment_manager = PaymentManager(self.logged_account)

        # Inicializa APIs externas (simuladas)
        pix_api = PixAPI()
        card_gateway = CreditCardGateway()
        crypto_api = CryptoExchangeAPI()
        swift_api = InternationalBankingAPI()

        while True:
                print("\n" + "="*50)
                print("💳 PAYMENT METHODS (Adapter Pattern)")
                print("="*50)
                print("1. ➕ Add PIX Payment Method")
                print("2. ➕ Add Credit Card")
                print("3. ➕ Add Cryptocurrency")
                print("4. ➕ Add International Transfer")
                print("5. 📋 List Payment Methods")
                print("6. 💳 Pay Bill with Specific Method")
                print("7. 💰 Make Payment")
                print("8. 📊 Payment Methods Summary")
                print("0. ↩️  Back to main menu")
                
                choice = input("\nSelect option: ").strip()
                
                if choice == '1':
                    # Add PIX - CORRIGIDO: passa o user
                    pix_key = input("Enter your PIX key (email/phone): ")
                    adapter = PixAdapter(pix_api, self.logged_account, pix_key)
                    payment_manager.add_payment_method("PIX", adapter)
                    print(f"✅ PIX added with key: {pix_key}")
                
                elif choice == '2':
                    # Add Credit Card - CORRIGIDO: passa o user
                    print("\n💳 Add Credit Card")
                    card_num = input("Card number (16 digits): ")
                    cvv = input("CVV: ")
                    expiry = input("Expiry (MM/YY): ")
                    name = input("Cardholder name: ")
                    
                    adapter = CreditCardAdapter(
                        card_gateway, 
                        self.logged_account,  # CORRIGIDO
                        card_num, 
                        cvv, 
                        expiry, 
                        name
                    )
                    payment_manager.add_payment_method("Credit Card", adapter)
                    print(f"✅ Credit Card added (ending in {card_num[-4:]})")
                
                elif choice == '3':
                    # Add Crypto - já estava correto
                    adapter = CryptoAdapter(crypto_api, self.logged_account)
                    payment_manager.add_payment_method("Cryptocurrency", adapter)
                    print("✅ Cryptocurrency payment method added")
                    print("   Supported: BTC, ETH")
                
                elif choice == '4':
                    # Add International Transfer - já estava correto
                    adapter = InternationalBankAdapter(swift_api, self.logged_account)
                    payment_manager.add_payment_method("International Transfer", adapter)
                    print("✅ International transfer method added (SWIFT)")
                
                elif choice == '5':
                    # List Methods
                    methods = payment_manager.list_payment_methods()
                    print(f"\n📋 Available payment methods: {len(methods)}")
                    for i, method in enumerate(methods, 1):
                        print(f"{i}. {method}")
                
                elif choice == '6':
                    # Pay Bill with Method - CORRIGIDO: pega bills do usuário
                    unpaid_bills = self.bank_system.get_unpaid_bills(user=self.logged_account)
                    
                    if not unpaid_bills:
                        print("✅ No bills to pay")
                        continue
                    
                    print("\n📋 Your unpaid bills:")
                    for i, bill in enumerate(unpaid_bills, 1):
                        owner_info = f" ({bill.get_owner().get_name()})" if bill.get_owner() else " (Public)"
                        print(f"{i}. {bill.get_description()}{owner_info} - R$ {bill.get_value():.2f}")
                    
                    methods = payment_manager.list_payment_methods()
                    if not methods:
                        print("❌ No payment methods configured")
                        print("   Add a payment method first (options 1-4)")
                        input("Press Enter to continue...")
                        continue
                    
                    print("\n💳 Available methods:")
                    for i, method in enumerate(methods, 1):
                        print(f"{i}. {method}")
                    
                    try:
                        bill_idx = int(input("\nSelect bill: ")) - 1
                        method_idx = int(input("Select payment method: ")) - 1
                        
                        if 0 <= bill_idx < len(unpaid_bills) and 0 <= method_idx < len(methods):
                            selected_bill = unpaid_bills[bill_idx]
                            selected_method = methods[method_idx]
                            
                            payment_manager.pay_bill_with_method(selected_bill, selected_method)
                        else:
                            print("❌ Invalid selection")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                
                elif choice == '7':
                    # Make Payment
                    methods = payment_manager.list_payment_methods()
                    if not methods:
                        print("❌ No payment methods configured")
                        continue
                    
                    print("\n💳 Available methods:")
                    for i, method in enumerate(methods, 1):
                        balance = payment_manager.payment_methods[method].check_balance()
                        balance_str = f"R$ {balance:.2f}" if balance != float('inf') else "Unlimited"
                        print(f"{i}. {method} (Balance: {balance_str})")
                    
                    try:
                        method_idx = int(input("\nSelect payment method: ")) - 1
                        
                        if 0 <= method_idx < len(methods):
                            selected_method = methods[method_idx]
                            
                            amount = float(input("Amount: R$ "))
                            description = input("Description: ")
                            
                            destination = None
                            if selected_method == "PIX":
                                destination = input("Destination PIX key (email/phone): ")
                                print(f"ℹ️  Tip: Try test@test.com or 123456789")
                            elif selected_method == "Cryptocurrency":
                                destination = input("Crypto (BTC/ETH): ").upper()
                            elif selected_method == "International Transfer":
                                print("\nAvailable SWIFT codes for testing:")
                                print("  BOFAUS3N - Bank of America")
                                print("  CITIUS33 - Citibank")
                                swift = input("SWIFT code: ").upper()
                                account = input("Account number: ")
                                name = input("Beneficiary name: ")
                                destination = f"{swift}:{account}:{name}"
                            
                            result = payment_manager.pay_with(
                                selected_method, amount, description, destination
                            )
                            
                            if result["success"]:
                                print(f"\n✅ Payment successful!")
                                print(f"   Method: {result.get('method')}")
                                print(f"   Transaction ID: {result.get('transaction_id')}")
                                if result.get('message'):
                                    print(f"   Details: {result['message']}")
                            else:
                                print(f"\n❌ Payment failed!")
                                print(f"   Reason: {result.get('message')}")
                        else:
                            print("❌ Invalid selection")
                        
                    except Exception as e:
                        print(f"❌ Error: {e}")
                
                elif choice == '8':
                    # Summary
                    payment_manager.print_payment_summary()
                
                elif choice == '0':
                    break
                else:
                    print("❌ Invalid option")
                
                input("\nPress Enter to continue...")
    # ==================== DEMO PADRÕES ====================

    def demonstrate_patterns(self):
        """Demonstra todos os padrões estruturais em ação"""
        print("\n" + "="*60)
        print("🎓 STRUCTURAL PATTERNS DEMONSTRATION")
        print("="*60)
        
        print("\n1️⃣  DECORATOR PATTERN")
        print("-" * 60)
        print("Adding features dynamically to accounts...")
        
        from core.decorators import PremiumAccountDecorator
        
        original_balance = self.logged_account.get_balance()
        print(f"Original balance: R$ {original_balance:.2f}")
        
        # Aplica Premium temporariamente
        temp_account = PremiumAccountDecorator(self.logged_account)
        print("✨ Applied Premium Decorator")
        print("Now withdrawals will generate cashback!")
        
        print("\n2️⃣  FACADE PATTERN")
        print("-" * 60)
        print("Simplifying complex operations...")
        
        from core.facades import BankingFacade
        facade = BankingFacade(self.logged_account)
        
        print("📊 Getting account summary using Facade:")
        summary = facade.get_account_summary()
        print(f"   Name: {summary['name']}")
        print(f"   Type: {summary['account_type']}")
        print(f"   Balance: R$ {summary['balance_brl']:.2f}")
        print(f"   Transactions: {summary['transactions']}")
        
        print("\n3️⃣  ADAPTER PATTERN")
        print("-" * 60)
        print("Integrating external payment systems...")
        
        from core.adapters import PaymentManager, PixAPI, PixAdapter
        
        payment_manager = PaymentManager(self.logged_account)
        pix_api = PixAPI()
        pix_adapter = PixAdapter(pix_api, self.logged_account, "demo@email.com")
        
        payment_manager.add_payment_method("PIX Demo", pix_adapter)
        print("✅ Integrated PIX payment system")
        print("   Now can pay bills using PIX!")
        
        print("\n" + "="*60)
        print("✅ All structural patterns demonstrated!")
        print("="*60)
        
        input("\nPress Enter to continue...")
