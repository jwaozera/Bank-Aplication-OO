"""
Menu Manager - TRATAMENTO ROBUSTO DE EXCEÇÕES

EXCEÇÕES TRATADAS:
1. ValueError - conversões de tipo inválidas
2. IndexError - acesso a índices inválidos
3. TypeError - tipos de dados incorretos
4. AttributeError - atributos inexistentes
5. ZeroDivisionError - divisões por zero
6. KeyError - chaves de dicionário inexistentes
7. Exceções personalizadas para regras de negócio

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
from core.loan_strategy import *


# ==================== EXCEÇÕES PERSONALIZADAS ====================

class BankingException(Exception):
    """Exceção base para erros bancários"""
    pass

class InsufficientBalanceException(BankingException):
    """Lançada quando saldo é insuficiente"""
    pass

class InvalidAmountException(BankingException):
    """Lançada quando o valor da transação é inválido"""
    pass

class AccountNotFoundException(BankingException):
    """Lançada quando conta não é encontrada"""
    pass

class InvalidCredentialsException(BankingException):
    """Lançada quando credenciais estão incorretas"""
    pass

class InvestorOnlyFeatureException(BankingException):
    """Lançada quando recurso é exclusivo para investidores"""
    pass


# ==================== UTILS VALIDAÇÃO ====================

class InputValidator:

    """Classe utilitária para validação de entradas"""
    
    @staticmethod
    def get_float_input(prompt: str, min_value: float = 0, max_value: float = float('inf')) -> float:
        """
        Obtém entrada float com validação robusta
        
        Previne ValueError e garante valores dentro do range esperado
        """
        while True:
            try:
                value = float(input(prompt))
                
                if value < min_value:
                    print(f"❌ Value must be at least {min_value}")
                    continue
                    
                if value > max_value:
                    print(f"❌ Value cannot exceed {max_value}")
                    continue
                    
                return value
                
            except ValueError:
                # TRATAMENTO: ValueError quando conversão para float falha
                print("❌ Invalid input. Please enter a valid number.")
            except KeyboardInterrupt:
                # TRATAMENTO: Permite ao usuário cancelar com Ctrl+C
                print("\n❌ Input cancelled by user.")
                raise
    
    @staticmethod
    def get_int_input(prompt: str, min_value: int = 0, max_value: int = 999999) -> int:
        """
        Obtém entrada int com validação
        
        Previne ValueError e IndexError em seleções de menu
        """
        while True:
            try:
                value = int(input(prompt))
                
                if value < min_value or value > max_value:
                    print(f"❌ Please enter a number between {min_value} and {max_value}")
                    continue
                    
                return value
                
            except ValueError:
                # TRATAMENTO: ValueError em conversão para int
                print("❌ Invalid input. Please enter a whole number.")
            except KeyboardInterrupt:
                print("\n❌ Input cancelled.")
                raise
    
    @staticmethod
    def get_choice(prompt: str, valid_options: list) -> str:
        """
        Obtém escolha validada de uma lista
        
        Previne KeyError e garante opções válidas
        """
        while True:
            try:
                choice = input(prompt).strip().lower()
                
                if choice in valid_options:
                    return choice
                    
                print(f"❌ Invalid option. Choose from: {', '.join(valid_options)}")
                
            except KeyboardInterrupt:
                print("\n❌ Selection cancelled.")
                raise


class MenuManager:
    """Gerencia operações do menu"""
    
    def __init__(self):
        self.bank_system = BankSystem()
        self.logged_account: Optional[User] = None
        self.validator = InputValidator()
    
    def initialize_system(self):
        """
        Inicializa sistema com tratamento de exceções
        
        Garante que falhas na inicialização não quebrem o programa
        """
        try:
            self.bank_system.initialize_demo_data()
            
            # Anexa observadores com proteção
            bill_observer = BillNotificationObserver()
            for bill in self.bank_system.get_bills():
                try:
                    bill.attach(bill_observer)
                except AttributeError as e:
                    # TRATAMENTO: Se bill não tem método attach
                    print(f"⚠️ Warning: Could not attach observer to bill: {e}")
                    
        except Exception as e:
            # TRATAMENTO: Qualquer erro na inicialização
            print(f"❌ Error initializing system: {e}")
            print("System will start with default configuration.")
    
    def login(self) -> bool:
        """
        Login com tratamento completo de exceções
        
        Evita crashes por credenciais inválidas ou erros de criação de conta
        """
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            try:
                print("\n" + "="*60)
                print("🏦 North Frontier Bank - Welcome!")
                print("="*60)
                
                nome = input("Enter your name: ").strip()
                
                # Valida nome não vazio
                if not nome:
                    raise InvalidCredentialsException("Name cannot be empty")
                
                senha = input("Enter your password: ").strip()
                
                if not senha:
                    raise InvalidCredentialsException("Password cannot be empty")
                
                # Busca conta existente
                account = self.bank_system.find_account(nome, senha)
                
                if account:
                    self.logged_account = account
                    print(f"✅ Welcome back, {self.logged_account.get_name()}!")
                    
                    # Anexa observadores com tratamento
                    try:
                        if not any(isinstance(obs, BalanceObserver) for obs in getattr(self.logged_account, "_observers", [])):
                            self.logged_account.attach(BalanceObserver())
                    except (AttributeError, TypeError) as e:
                        # TRATAMENTO: Falha ao anexar observador
                        print(f"⚠️ Warning: Observer attachment failed: {e}")
                    
                    return True
                else:
                    # Cria nova conta
                    print("\n📝 Account not found. Creating new account...")
                    
                    try:
                        regular_factory = UserFactoryProvider.get_factory("regular")
                        new_account = regular_factory.create_user(nome, senha, 0)
                        self.bank_system.add_account(new_account)
                        self.logged_account = new_account
                        
                        print(f"✅ Account created successfully for {nome}!")
                        return True
                        
                    except ValueError as e:
                        # TRATAMENTO: Erro na criação da conta
                        raise BankingException(f"Account creation failed: {e}")
                        
            except InvalidCredentialsException as e:
                # TRATAMENTO: Credenciais inválidas
                attempts += 1
                remaining = max_attempts - attempts
                print(f"❌ {e}")
                if remaining > 0:
                    print(f"Attempts remaining: {remaining}")
                    
            except BankingException as e:
                # TRATAMENTO: Erros bancários específicos
                print(f"❌ Banking error: {e}")
                attempts += 1
                
            except KeyboardInterrupt:
                # TRATAMENTO: Usuário cancelou (Ctrl+C)
                print("\n\n❌ Login cancelled by user.")
                return False
                
            except Exception as e:
                # TRATAMENTO: Qualquer outro erro inesperado
                print(f"❌ Unexpected error during login: {e}")
                attempts += 1
        
        print(f"\n❌ Maximum login attempts ({max_attempts}) exceeded.")
        return False
    
    def show_balance(self):
        """
        Mostra saldo com proteção contra erros
        
        Previne AttributeError se conta não estiver logada
        """
        try:
            if not self.logged_account:
                raise AccountNotFoundException("No account logged in")
            
            balance = self.logged_account.get_balance()
            dolar_balance = self.logged_account.get_dolar_balance()
            
            print("\n" + "="*50)
            print("💰 ACCOUNT BALANCE")
            print("="*50)
            print(f"Real (R$): {balance:.2f}")
            print(f"Dollar ($): {dolar_balance:.2f}")
            print("="*50)
            
        except AccountNotFoundException as e:
            print(f"❌ {e}")
        except AttributeError as e:
            # TRATAMENTO: Métodos get_balance não existem
            print(f"❌ Error accessing account data: {e}")
        except Exception as e:
            print(f"❌ Unexpected error showing balance: {e}")
        finally:
            input("\nPress Enter to continue...")
    
    def process_withdrawal(self):
        """
        Saque com tratamento completo de exceções
        
        Operação financeira crítica - requer validação rigorosa
        """
        try:
            print("\n" + "="*50)
            print("🏧 WITHDRAWAL")
            print("="*50)
            
            if not self.logged_account:
                raise AccountNotFoundException("No account logged in")
            
            current_balance = self.logged_account.get_balance()
            print(f"Current balance: R$ {current_balance:.2f}")
            
            # validação robusta de entrada
            amount = self.validator.get_float_input(
                "Enter withdrawal amount (R$): ",
                min_value=0.01,
                max_value=current_balance
            )
            
            # validação de saldo
            if amount > current_balance:
                raise InsufficientBalanceException(
                    f"Insufficient balance. Available: R$ {current_balance:.2f}"
                )
            
            # Executa saque
            self.logged_account.withdraw(amount)
            
            # Cria histórico
            factory = TransactionFactoryProvider.get_factory(self.logged_account)
            history = factory.create_transaction_history(
                "Withdrawal",
                f"Withdrew R$ {amount:.2f} from account",
                amount,
                self.logged_account.get_balance()
            )
            self.logged_account.add_history(history)
            
            print(f"✅ Withdrawal successful!")
            print(f"💰 New balance: R$ {self.logged_account.get_balance():.2f}")
            
        except AccountNotFoundException as e:
            print(f"❌ {e}")
        except InsufficientBalanceException as e:
            print(f"❌ {e}")
        except InvalidAmountException as e:
            print(f"❌ {e}")
        except ValueError as e:
            # TRATAMENTO: Erro no método withdraw
            print(f"❌ Withdrawal error: {e}")
        except AttributeError as e:
            print(f"❌ Account data error: {e}")
        except KeyboardInterrupt:
            print("\n❌ Withdrawal cancelled.")
        except Exception as e:
            # TRATAMENTO: Erros inesperados
            print(f"❌ Unexpected error during withdrawal: {e}")
        finally:
            input("\nPress Enter to continue...")
    
    def process_deposit(self):
        """
        Depósito com validação robusta
        
        Previne depósitos negativos ou inválidos
        """
        try:
            print("\n" + "="*50)
            print("💵 DEPOSIT")
            print("="*50)
            
            if not self.logged_account:
                raise AccountNotFoundException("No account logged in")
            
            amount = self.validator.get_float_input(
                "Enter deposit amount (R$): ",
                min_value=0.01,
                max_value=1000000  # Limite máximo de depósito
            )
            
            # depósito
            self.logged_account.deposit(amount)
            
            # histórico
            factory = TransactionFactoryProvider.get_factory(self.logged_account)
            history = factory.create_transaction_history(
                "Deposit",
                f"Deposited R$ {amount:.2f} into account",
                amount,
                self.logged_account.get_balance()
            )
            self.logged_account.add_history(history)
            
            print(f"✅ Deposit successful!")
            print(f"💰 New balance: R$ {self.logged_account.get_balance():.2f}")
            
        except AccountNotFoundException as e:
            print(f"❌ {e}")
        except ValueError as e:
            print(f"❌ Deposit error: {e}")
        except KeyboardInterrupt:
            print("\n❌ Deposit cancelled.")
        except Exception as e:
            print(f"❌ Unexpected error during deposit: {e}")
        finally:
            input("\nPress Enter to continue...")
    
    def process_transfer(self):
        """
        Transferência com tratamento extensivo de exceções
        
        Operação envolvendo duas contas - requer validação dupla
        """
        try:
            print("\n" + "="*50)
            print("🔄 TRANSFER")
            print("="*50)
            
            if not self.logged_account:
                raise AccountNotFoundException("No account logged in")
            
            other_accounts = self.bank_system.get_other_accounts(self.logged_account)
            
            if not other_accounts:
                print("❌ No other accounts available for transfer.")
                return
            
            # contas disponíveis
            print("\n📋 Available accounts:")
            for i, account in enumerate(other_accounts, 1):
                try:
                    name = account.get_name()
                    balance = account.get_balance()
                    print(f"{i}. {name} (Balance: R$ {balance:.2f})")
                except AttributeError:
                    print(f"{i}. [Account data unavailable]")
            
            # seleção de conta com validação
            choice = self.validator.get_int_input(
                "\nSelect account (number, 0 to cancel): ",
                min_value=0,
                max_value=len(other_accounts)
            )
            
            if choice == 0:
                print("❌ Transfer cancelled.")
                return
            
            try:
                target_account = other_accounts[choice - 1]
            except IndexError:
                # TRATAMENTO: Índice fora do range
                raise IndexError("Invalid account selection")
            
            # validação de valor
            current_balance = self.logged_account.get_balance()
            print(f"\n💰 Your balance: R$ {current_balance:.2f}")
            
            amount = self.validator.get_float_input(
                "Enter transfer amount (R$): ",
                min_value=0.01,
                max_value=current_balance
            )
            
            # confirmação
            target_name = target_account.get_name()
            confirm = self.validator.get_choice(
                f"\nConfirm transfer of R$ {amount:.2f} to {target_name}? (y/n): ",
                ['y', 'yes', 'n', 'no', 's', 'sim', 'não']
            )
            
            if confirm not in ['y', 'yes', 's', 'sim']:
                print("❌ Transfer cancelled.")
                return

            # execução da transferência
            from models.users import transaction
            transaction(self.logged_account, target_account, amount)
            
            print(f"\n✅ Transfer completed successfully!")
            print(f"💰 New balance: R$ {self.logged_account.get_balance():.2f}")
            
        except AccountNotFoundException as e:
            print(f"❌ {e}")
        except IndexError as e:
            print(f"❌ {e}")
        except InsufficientBalanceException as e:
            print(f"❌ {e}")
        except ValueError as e:
            print(f"❌ Transfer error: {e}")
        except KeyboardInterrupt:
            print("\n❌ Transfer cancelled.")
        except Exception as e:
            print(f"❌ Unexpected error during transfer: {e}")
        finally:
            input("\nPress Enter to continue...")
    
    def pay_bills(self):
        """
        Pagamento de boletos com tratamento de exceções
        
        Operação crítica que envolve listagem e seleção
        """
        try:
            print("\n" + "="*50)
            print("💳 PAY BILLS")
            print("="*50)
            
            if not self.logged_account:
                raise AccountNotFoundException("No account logged in")
            
            # Busca boletos com tratamento
            try:
                unpaid_bills = self.bank_system.get_unpaid_bills(user=self.logged_account)
            except AttributeError:
                # TRATAMENTO: Método não existe
                unpaid_bills = []
            
            if not unpaid_bills:
                print("✅ You have no unpaid bills!")
                return
            
            print(f"Found {len(unpaid_bills)} unpaid bill(s):")
            print("-" * 50)
            
            # Mostra boletos com proteção
            for i, bill in enumerate(unpaid_bills, 1):
                try:
                    status = "⚠️ OVERDUE" if bill.is_overdue() else "Pending"
                    owner = bill.get_owner()
                    owner_info = f" (Owner: {owner.get_name()})" if owner else " (Public)"
                    
                    print(f"{i}. {bill.get_description()}{owner_info}")
                    print(f"   💰 Value: R$ {bill.get_value():.2f}")
                    print(f"   📅 Due Date: {bill.get_due_date().strftime('%Y-%m-%d')}")
                    print(f"   🚨 Status: {status}")
                    print("-" * 30)
                    
                except AttributeError as e:
                    # TRATAMENTO: Dados do boleto incompletos
                    print(f"{i}. [Bill data unavailable: {e}]")
                    print("-" * 30)
            
            print(f"\n💳 Your balance: R$ {self.logged_account.get_balance():.2f}")
            
            # seleção com validação
            choice = self.validator.get_int_input(
                "\nSelect bill to pay (0 to cancel): ",
                min_value=0,
                max_value=len(unpaid_bills)
            )
            
            if choice == 0:
                print("❌ Payment cancelled.")
                return
            
            try:
                selected_bill = unpaid_bills[choice - 1]
            except IndexError:
                raise IndexError("Invalid bill selection")
            
            # Mostra detalhes
            print(f"\n📋 Bill Details:")
            print(f"Description: {selected_bill.get_description()}")
            print(f"Value: R$ {selected_bill.get_value():.2f}")
            
            if selected_bill.is_overdue():
                print("⚠️ WARNING: This bill is overdue!")
            
            # confirmação
            confirm = self.validator.get_choice(
                "\nConfirm payment? (y/n): ",
                ['y', 'yes', 'n', 'no', 's', 'sim']
            )
            
            if confirm not in ['y', 'yes', 's', 'sim']:
                print("❌ Payment cancelled.")
                return
            
            # pagamento
            try:
                selected_bill.pay(self.logged_account)
                print(f"✅ Bill paid successfully!")
                print(f"💰 New balance: R$ {self.logged_account.get_balance():.2f}")
                
            except ValueError as e:
                # TRATAMENTO: Saldo insuficiente ou boleto já pago
                print(f"❌ Payment failed: {e}")
                
        except AccountNotFoundException as e:
            print(f"❌ {e}")
        except IndexError as e:
            print(f"❌ {e}")
        except KeyboardInterrupt:
            print("\n❌ Payment cancelled.")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        finally:
            input("\nPress Enter to continue...")
    
    def create_investment_goal(self):
        """
        Criação de meta com validação para investidores
        
        Recurso exclusivo - requer verificação de tipo de conta
        """
        try:
            print("\n" + "="*50)
            print("🎯 CREATE INVESTMENT GOAL")
            print("="*50)
            
            if not self.logged_account:
                raise AccountNotFoundException("No account logged in")
            
            # Verifica tipo de conta
            if not isinstance(self.logged_account, Investor):
                raise InvestorOnlyFeatureException(
                    "Only Investor accounts can create investment goals. "
                    "Please upgrade your account."
                )
            
            print(f"💰 Current balance: R$ {self.logged_account.get_balance():.2f}")
            
            # validação de descrição
            description = input("\nEnter goal description: ").strip()
            
            if not description:
                raise InvalidAmountException("Description cannot be empty")
            
            if len(description) > 100:
                raise InvalidAmountException("Description too long (max 100 characters)")
            
            # validação de valor
            value_needed = self.validator.get_float_input(
                "Enter target amount (R$): ",
                min_value=1.00,
                max_value=10000000
            )
            
            # summary
            print(f"\n📋 Goal Summary:")
            print(f"Description: {description}")
            print(f"Target: R$ {value_needed:.2f}")
            
            # confirmação
            confirm = self.validator.get_choice(
                "\nConfirm goal creation? (y/n): ",
                ['y', 'yes', 'n', 'no', 's', 'sim']
            )
            
            if confirm not in ['y', 'yes', 's', 'sim']:
                print("❌ Goal creation cancelled.")
                return
            
            # criar meta
            Goal(value_needed, description, self.logged_account)
            
            goals_count = len(self.logged_account.get_investment_goals())
            print(f"\n✅ Investment goal created!")
            print(f"🎯 You now have {goals_count} active goal(s)")
            
        except AccountNotFoundException as e:
            print(f"❌ {e}")
        except InvestorOnlyFeatureException as e:
            print(f"❌ {e}")
        except InvalidAmountException as e:
            print(f"❌ {e}")
        except ValueError as e:
            print(f"❌ Error creating goal: {e}")
        except KeyboardInterrupt:
            print("\n❌ Goal creation cancelled.")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        finally:
            input("\nPress Enter to continue...")
