"Here is the main of the project"

from bill import *
from history import *
from goal import *
from loan import *
from users import *


def ask(prompt):
    print(prompt)
    choice = input("Select the number: ")
    return choice


def customer_service():
    """Customer Service menu with usage instructions"""
    while True:
        print("\n" + "="*50)
        print("🏧 NORTH FRONTIER BANK - CUSTOMER SERVICE 🏧")
        print("="*50)
        print("\n📞 How can we help you today?")
        print("\n1. 💰 Banking Operations Guide")
        print("2. 💳 Payment and Bills Guide")
        print("3. 🏦 Account Management Guide")
        print("4. 📈 Investment Guide (Investor Accounts)")
        print("5. 🆘 Emergency Contact")
        print("6. ↩️  Return to Main Menu")
        
        choice = input("\n🔢 Select an option (1-6): ")
        
        if choice == '1':
            print("\n" + "="*50)
            print("💰 BANKING OPERATIONS GUIDE")
            print("="*50)
            print("\n🔹 BALANCE: Check your current Real (R$) and Dollar ($) balance")
            print("🔹 WITHDRAW: Remove money from your account")
            print("   • Enter the amount you want to withdraw")
            print("   • Make sure you have sufficient balance")
            print("\n🔹 DEPOSIT: Add money to your account")
            print("   • Enter the amount you want to deposit")
            print("   • Money is immediately available")
            print("\n🔹 TRANSFER: Send money to other accounts")
            print("   • Select the recipient from the list")
            print("   • Enter the transfer amount")
            print("   • Confirm the transaction")
            print("\n🔹 CURRENCY EXCHANGE:")
            print("   • Real → Dollar: Current rate = R$ 5.25 per $1")
            print("   • Dollar → Real: Convert your dollars back to reais")
            input("\n📝 Press Enter to continue...")
            
        elif choice == '2':
            print("\n" + "="*50)
            print("💳 PAYMENT AND BILLS GUIDE")
            print("="*50)
            print("\n🔹 PAY BILLS: Manage your outstanding bills")
            print("   • View all unpaid bills with due dates")
            print("   • Select which bill to pay")
            print("   • Confirm payment (money deducted from balance)")
            print("   • ⚠️  Overdue bills are marked with warnings")
            print("\n🔹 LOANS: Get financial assistance")
            print("   • Maximum loan: 2x your current balance")
            print("   • Duration: 6-60 months")
            print("   • A payment bill is automatically created")
            print("   • Monthly payment = Loan amount ÷ Duration")
            print("\n🔹 CHECKBOOK: Order physical checks")
            print("   • First checkbook per month is FREE")
            print("   • Additional checkbooks cost R$ 25.00")
            input("\n📝 Press Enter to continue...")
            
        elif choice == '3':
            print("\n" + "="*50)
            print("🏦 ACCOUNT MANAGEMENT GUIDE")
            print("="*50)
            print("\n🔹 VIEW HISTORY: See all your transactions")
            print("   • Complete transaction log with timestamps")
            print("   • Includes deposits, withdrawals, transfers, bills, loans")
            print("   • Shows balance after each transaction")
            print("\n🔹 CHANGE ACCOUNT: Switch between your accounts")
            print("   • Select from available accounts")
            print("   • Enter the account password")
            print("   • Continue using the new account")
            print("\n🔹 ACCOUNT TYPES:")
            print("   • 👤 Regular User: Standard banking operations")
            print("   • 📈 Investor: All regular features + investment goals")
            input("\n📝 Press Enter to continue...")
            
        elif choice == '4':
            print("\n" + "="*50)
            print("📈 INVESTMENT GUIDE (INVESTOR ACCOUNTS ONLY)")
            print("="*50)
            print("\n🎯 CREATE INVESTMENT GOAL:")
            print("   • Set a financial target (e.g., vacation, car, house)")
            print("   • Define the target amount needed")
            print("   • Track your progress over time")
            print("\n💰 DEPOSIT IN GOAL:")
            print("   • Add money to your investment goals")
            print("   • Money is deducted from your balance")
            print("   • Goal automatically closes when target is reached")
            print("\n⚠️  NOTE: Only Investor accounts can create and manage")
            print("    investment goals. Regular users need to upgrade.")
            print("\n🎉 ACHIEVEMENT: When you reach your goal, it's")
            print("    automatically removed from your active goals list.")
            input("\n📝 Press Enter to continue...")
            
        elif choice == '5':
            print("\n" + "="*50)
            print("🆘 EMERGENCY CONTACT INFORMATION")
            print("="*50)
            print("\n📞 24/7 Customer Service: 0800-FRONTIER (0800-376-68437)")
            print("📧 Email Support: support@northfrontier.bank")
            print("💬 Online Chat: www.northfrontier.bank/chat")
            print("\n🚨 EMERGENCY SERVICES:")
            print("• Lost/Stolen Cards: 0800-911-CARD")
            print("• Fraud Report: 0800-FRAUD-HELP")
            print("• Account Lock: 0800-LOCK-NOW")
            print("\n🏢 HEADQUARTERS:")
            print("North Frontier Bank")
            print("123 Banking Street, Financial District")
            print("São Paulo, SP - Brazil")
            print("CEP: 01000-000")
            print("\n⏰ BUSINESS HOURS:")
            print("Monday to Friday: 9:00 AM - 6:00 PM")
            print("Saturday: 9:00 AM - 2:00 PM")
            print("Sunday: Closed (Online services available 24/7)")
            input("\n📝 Press Enter to continue...")
            
        elif choice == '6':
            print("\n↩️  Returning to Main Menu...")
            break
            
        else:
            print("\n❌ Invalid option. Please select a number from 1 to 6.")
            input("Press Enter to try again...")





def loop_menu(logged_account, accounts, bills_list):
    while True:
        print("\n=========== Menu de Operações ===========\n")
        # Exibe notificações de boletos vencidos
        for boleto in bills_list:
            if isinstance(boleto, Bill) and boleto.is_overdue():
                print(f"⚠️ Overdue Bill: {boleto.get_description()} - Valor: R$ {boleto.get_value():.2f}")

        print("=" * 50)

        choice = ask("\n1. Balance\n2. Withdraw\n3. Deposit\n4. View History\n5. Transfer\n6. Change Account\n7. Pay Bill\n8. Exchange Real -> Dollar \n9. Exchange Dollar -> Real\n10. Loan\n11. Checkbook\n12. Create Investment Goal\n13. Deposit in Goal\n14. Customer Service\n15. Exit\n")

        #first option is show balance
        if choice == '1':
            print(f"Your balance is: R$ {logged_account.get_balance():.2f}")
            print(f"Your dollar balance is: $ {logged_account.get_dolar_balance():.2f}")

        #second option is withdraw
        elif choice == '2':
            amount = float(input("Enter the amount to withdraw: "))
            logged_account.withdraw(amount)

            history = History_transaction(
            action="Withdrawal",
            description=f"Withdrew {amount} from account",
            amount=amount,
            balance=logged_account.get_balance()
            )
            logged_account.add_history(history)

        #third option is deposit
        elif choice == '3':
            amount = float(input("Enter the amount to deposit: "))
            logged_account.deposit(amount)

            history = History_transaction(
            action="Deposit",
            description=f"Deposited {amount} into account",
            amount=amount,
            balance=logged_account.get_balance()
            )
            logged_account.add_history(history)

        #fourth option is view history
        elif choice == '4':
            #fourth option is view history
            print("\n========== History ==========\n")
            historico = logged_account.get_history()
            
            if not historico:
                print("📝 No transactions found.")
            else:
                print(f"📊 Total transactions: {len(historico)}")
                print("-" * 50)
                
                for i, history in enumerate(historico, 1):
                    print(f"\n🔹 Transaction {i}:")
                    history.show()  #chama o método show() específico de cada tipo
                    print("-" * 30)
            
            print("\n" + "=" * 45)
            input("Press Enter to continue...")  #pausa para o usuário ler

        #fifth option is transfer
        elif choice == '5':
            print("\n========== Transfer ==========\n")

            #exibe a lista de contas para transferência
            for i, account in enumerate(accounts, 1):
                if account != logged_account:  #não exibe a conta logada
                    print(f"{i}. {account.get_name()}")

            choice = int(input("Select the account to transfer to (number): "))
            if 1 <= choice <= len(accounts):
                target_account = accounts[choice - 1]
                amount = float(input("Enter the amount to transfer: "))
                transaction(logged_account, target_account, amount)
            else:
                print("Invalid account selection.")

        #sixty option is change account
        elif choice == '6':
            print("\n========== Change Account ==========\n")
            print(f"Currently logged in as: {logged_account.get_name()}")
            print("\nAvailable accounts:")
            
            #cria uma lista das outras contas (excluindo a atual)
            other_accounts = [account for account in accounts if account != logged_account]
            
            if not other_accounts:
                print("No other accounts available to switch to.")
                input("Press Enter to continue...")
                continue
            
            #exibe a lista de contas para troca
            for i, account in enumerate(other_accounts, 1):
                account_type = "Investor" if isinstance(account, Investor) else "Regular User"
                print(f"{i}. {account.get_name()} ({account_type})")

            try:
                choice = int(input("\nSelect the account to switch to (number, 0 to cancel): "))
                
                if choice == 0:
                    print("Account switch cancelled.")
                    continue
                elif 1 <= choice <= len(other_accounts):
                    selected_account = other_accounts[choice - 1]
                    password = input(f"Enter password for {selected_account.get_name()}: ")
                    
                    if password == selected_account.get_password():
                        logged_account = selected_account
                        print(f"✅ Successfully switched to account: {logged_account.get_name()}")
                        print(f"Account type: {'Investor' if isinstance(logged_account, Investor) else 'Regular User'}")
                        print(f"Balance: R$ {logged_account.get_balance():.2f}")
                        print("You can now continue using the menu with your new account.")
                    else:
                        print("❌ Incorrect password. Account switch failed.")
                else:
                    print("❌ Invalid account selection.")
                    
            except ValueError:
                print("❌ Invalid input. Please enter a valid number.")
            
            input("Press Enter to continue...")

        #seventh option is pay bills
        elif choice == '7':
            print("\n========== Pay Bills ==========\n")
    
            #verifica se existem boletos na lista
            if not bills_list:
                print("No bills available to pay.")
                input("Press Enter to continue...")
            else:
                #filtra apenas boletos não pagos
                unpaid_bills = [bill for bill in bills_list if not bill.is_paid()]
                
                if not unpaid_bills:
                    print("✅ All bills have been paid!")
                    input("Press Enter to continue...")
                else:
                    print(f"Found {len(unpaid_bills)} unpaid bill(s):")
                    print("-" * 50)
                    
                    #exibe os boletos não pagos com informações detalhadas
                    for i, bill in enumerate(unpaid_bills, 1):
                        status = "⚠️ OVERDUE" if bill.is_overdue() else "Pending"
                        print(f"{i}. {bill.get_description()}")
                        print(f"   💰 Value: R$ {bill.get_value():.2f}")
                        print(f"   📅 Due Date: {bill.get_due_date().strftime('%Y-%m-%d')}")
                        print(f"   🚨 Status: {status}")
                        print("-" * 30)
                    
                    print(f"\n💳 Your current balance: R$ {logged_account.get_balance():.2f}")
                    
                    try:
                        choice = int(input("\nSelect the bill to pay (number, 0 to cancel): "))
                        
                        if choice == 0:
                            print("❌ Payment cancelled.")
                        elif 1 <= choice <= len(unpaid_bills):
                            selected_bill = unpaid_bills[choice - 1]
                            
                            #confirmação antes do pagamento
                            print(f"\n📋 Bill Details:")
                            print(f"Description: {selected_bill.get_description()}")
                            print(f"Value: R$ {selected_bill.get_value():.2f}")
                            print(f"Due Date: {selected_bill.get_due_date().strftime('%Y-%m-%d')}")
                            
                            if selected_bill.is_overdue():
                                print("⚠️  WARNING: This bill is overdue!")
                            
                            confirm = input("\nConfirm payment? (y/n): ").lower().strip()
                            
                            if confirm in ['y', 'yes', 's', 'sim']:
                                try:
                                    #tenta pagar o boleto usando o método da classe Bill
                                    selected_bill.pay(logged_account)
                                    print(f"✅ Bill paid successfully!")
                                    print(f"💰 New balance: R$ {logged_account.get_balance():.2f}")
                                    
                                except ValueError as e:
                                    print(f"❌ Error: {e}")
                            else:
                                print("❌ Payment cancelled.")
                                
                        else:
                            print("❌ Invalid bill selection.")
                            
                    except ValueError:
                        print("❌ Invalid input. Please enter a valid number.")
                    
                    input("\nPress Enter to continue...")

        #eigth option is to exchange real to dolar
        elif choice == '8':
            print("\n💱 Exchange Real to Dollar")
            amount = float(input("Enter amount in R$: "))
            exchange_rate = 5.25
            dollars = amount / exchange_rate
            if amount > logged_account.get_balance():
                print("❌ Insufficient funds for this exchange.")
            else:
                logged_account.set_balance(logged_account.get_balance() - amount)
                logged_account.set_dolar_balance(logged_account.get_dolar_balance() + dollars)
                print(f"✅ Successfully exchanged R$ {amount:.2f} to $ {dollars:.2f}")
                print(f"💰 New balance: R$ {logged_account.get_balance():.2f}, $ {logged_account.get_dolar_balance():.2f}")

        #ninth option is to exchange dollar to real
        elif choice == '9':
            print("\n💱 Exchange Dollar to Real")
            amount = float(input("Enter amount in $: "))
            exchange_rate = 5.25
            reais = amount * exchange_rate
            if amount > logged_account.get_dolar_balance():
                print("❌ Insufficient funds for this exchange.")
            else:
                logged_account.set_dolar_balance(logged_account.get_dolar_balance() - amount)
                logged_account.set_balance(logged_account.get_balance() + reais)
                print(f"✅ Successfully exchanged $ {amount:.2f} to R$ {reais:.2f}")
                print(f"💰 New balance: R$ {logged_account.get_balance():.2f}, $ {logged_account.get_dolar_balance():.2f}")

        # tenth option is to make a loan
        elif choice == '10':
            print("\n💰 Make a Loan")
            print(f"Current balance: R$ {logged_account.get_balance():.2f}")
            print(f"Maximum loan amount: R$ {logged_account.get_balance() * 2:.2f}")
            
            try:
                amount = float(input("Enter loan amount: R$ "))
                
                if amount <= 0:
                    print("❌ Loan amount must be positive.")
                elif amount > logged_account.get_balance() * 2:
                    print("❌ Loan amount exceeds limit (max 2x your current balance).")
                else:
                    #solicita duração do empréstimo
                    duration = int(input("Enter loan duration in months (6-60): "))
                    
                    if duration < 6 or duration > 60:
                        print("❌ Loan duration must be between 6 and 60 months.")
                    else:
                        print(f"\n📋 Loan Summary:")
                        print(f"Loan amount: R$ {amount:.2f}")
                        print(f"Duration: {duration} months")
                        
                        confirm = input("\nConfirm loan? (y/n): ").lower().strip()
                        
                        if confirm in ['y', 'yes', 's', 'sim']:
                            #cria o empréstimo
                            Loan(amount, duration, logged_account)
                            
                            #cria o boleto para pagamento (usando a data atual + duração)
                            from datetime import datetime, timedelta
                            due_date = datetime.now() + timedelta(days=duration * 30)
                            due_date_str = due_date.strftime("%Y-%m-%d")
                            
                            payment_bill = Bill(amount, f"Loan Payment - {duration} months", due_date_str)
                            bills_list.append(payment_bill)  #adiciona à lista de boletos

                            #adiciona o saldo ao usuário
                            logged_account.set_balance(logged_account.get_balance() + amount)
    
                            print(f"✅ Loan approved: R$ {amount:.2f}")
                            print(f"💰 New balance: R$ {logged_account.get_balance():.2f}")
                            print(f"📅 Payment due: {due_date_str}")
                            print(f"💳 A bill has been created for the amount: R$ {amount:.2f}")
                        else:
                            print("❌ Loan cancelled.")
                    
            except ValueError:
                print("❌ Invalid input. Please enter valid numbers.")
            
            input("Press Enter to continue...")

        #eleventh option is checkbook
        elif choice == '11':
            logged_account.new_checkbook()
        
        #twelfth option is create investment goal
        elif choice == '12':

            if isinstance(logged_account, User) and not isinstance(logged_account, Investor):
                print("❌ Only Investor accounts can create investment goals.")
                input("Press Enter to continue...")
                continue

            else:
                print("\n🎯 Create Investment Goal")
                print(f"💰 Current balance: R$ {logged_account.get_balance():.2f}")
                
                try:
                    #solicita informações da meta de investimento
                    description = input("Enter your investment goal description: ")
                    
                    if not description.strip():
                        print("❌ Description cannot be empty.")
                        input("Press Enter to continue...")
                        continue
                        
                    value_needed = float(input("Enter the target amount for your goal (R$): "))
                    
                    if value_needed <= 0:
                        print("❌ Target amount must be positive.")
                        input("Press Enter to continue...")
                        continue
                    
                    #confirmação dos dados
                    print(f"\n📋 Investment Goal Summary:")
                    print(f"Description: {description}")
                    print(f"Target Amount: R$ {value_needed:.2f}")
                    
                    confirm = input("\nConfirm investment goal creation? (y/n): ").lower().strip()
                    
                    if confirm in ['y', 'yes', 's', 'sim']:
                        #cria a meta de investimento usando a classe Goal
                        from goal import Goal
                        new_goal = Goal(value_needed, description, logged_account)
                        
                        print(f"✅ Investment goal created successfully!")
                        print(f"🎯 Goal: {description}")
                        print(f"💰 Target: R$ {value_needed:.2f}")
                        print(f"📊 You now have {len(logged_account.get_investment_goals())} active investment goal(s)")
                        
                    else:
                        print("❌ Investment goal creation cancelled.")
                        
                except ValueError:
                    print("❌ Invalid input. Please enter valid numbers.")
                
                input("Press Enter to continue...")

        #thirteenth option is deposit in goal (bonus - para complementar a funcionalidade)
        elif choice == '13':
            print("\n💰 Deposit in Investment Goal")
            
            goals = logged_account.get_investment_goals()
            
            if not goals:
                print("❌ No investment goals found. Create a goal first (option 12).")
                input("Press Enter to continue...")
            else:
                print(f"💳 Current balance: R$ {logged_account.get_balance():.2f}")
                print("\n📋 Your Investment Goals:")
                print("-" * 50)
                
                #exibe as metas disponíveis
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
                        print(f"💰 Your balance: R$ {logged_account.get_balance():.2f}")
                        
                        deposit_amount = float(input("\nEnter amount to deposit in goal (R$): "))
                        
                        if deposit_amount <= 0:
                            print("❌ Deposit amount must be positive.")
                        elif deposit_amount > logged_account.get_balance():
                            print("❌ Insufficient balance for this deposit.")
                        else:
                            confirm = input(f"\nConfirm deposit of R$ {deposit_amount:.2f} into '{selected_goal.get_description()}'? (y/n): ").lower().strip()
                            
                            if confirm in ['y', 'yes', 's', 'sim']:
                                #usa o método add_value da classe Goal
                                selected_goal.add_value(logged_account, deposit_amount)
                                print(f"✅ Successfully deposited R$ {deposit_amount:.2f} into your investment goal!")
                                print(f"💰 New balance: R$ {logged_account.get_balance():.2f}")
                                
                                #verifica se a meta foi atingida
                                if selected_goal.get_value_needed() <= 0:
                                    print("🎉 Congratulations! You've reached your investment goal!")
                            else:
                                print("❌ Deposit cancelled.")
                    else:
                        print("❌ Invalid goal selection.")
                        
                except ValueError:
                    print("❌ Invalid input. Please enter valid numbers.")
                
                input("Press Enter to continue...")

        #fourtenth option client suport
        elif choice == '14':
            customer_service()

        #exit
        else:
            print("Exiting...")
            break

def main():
    accounts = [] #lista para armazenar as contas criadas e fazer as validações necessárias

    #inicializando contas de exemplo para o banco
    #parâmetros (Nome do usuário, Senha, Saldo inicial, Talões de Cheque)
    accounts.append(User("Kris", "1234", 1000))
    accounts.append(User("Susie", "9876", 1500))
    accounts.append(Investor("Aubrey", "4567", 2500))
    accounts.append(Investor("Kel", "999", 99999))
    accounts.append(Investor("Mari", "4444", 0))

    #inicializando boletos de exemplo
    bills_list = [] # lista para armazenar os boletos criados
    #parâmetros (Titular, Valor, Nome do boleto, Vencimento)
    bills_list.append(Bill(100, "Font installation", "2023-10-31"))
    bills_list.append(Bill(200, "Stair railing", "2023-11-15"))


     #começo do menu no terminal, pede o usuário e a senha
    print("North Frontier Bank - Welcome!")
    print("Log in to an existing account or create a new one.")
    nome = input("Enter your name: ")
    senha = input("Enter your password: ")

    #loop para login (bem simples, possívelmente alterar depois)
    for account in accounts:
        if account.get_name() == nome and account.get_password() == senha:
            account_logged = account #armazena a conta atual(conta logada)
            print(f"Welcome, {account_logged.get_name()}!")
            break
    else:
        #se não encontrar a conta, cria uma nova
        print("Conta não encontrada. Criando uma nova conta...")
        account_nova = User(nome, senha, 0)
        accounts.append(account_nova)
        account_logged = account_nova

    loop_menu(account_logged, accounts, bills_list)


if __name__ == "__main__":
    main()