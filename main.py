"Here is the main of the project"

from bill import *
from history import *
from investment import *
from loan import *
from users import *


def ask_int(prompt):
    print(prompt)
    opcao = input("Digite o número da opção desejada: ")
    return opcao

def loop_menu(logged_account, accounts, bills_list):
    while True:
        print("\n=========== Menu de Operações ===========\n")
         # Exibe notificações de boletos vencidos
        opcao = ask_int("\n1. Balance\n2. Withdraw\n3. Deposit\n4. View History\n5. Transfer\n6. Change Account\n7. Pay Bill\n8. Exchange Real -> Dollar \n9. Exchange Dollar -> Real\n10. Loan\n11. Checkbook\n12. Create Investment Goal\n13. Deposit in Goal\n14. Customer Service\n15. Exit\n")

        #first option is show balance
        if opcao == '1':
            print(f"Your balance is: R$ {logged_account.get_balance():.2f}")
            print(f"Your dollar balance is: $ {logged_account.get_dolar_balance():.2f}")

        #second option is withdraw
        if opcao == '2':
            amount = float(input("Enter the amount to withdraw: "))
            logged_account.set_balance(logged_account.get_balance() - amount, withdraw=True)

        #third option is deposit
        if opcao == '3':
            amount = float(input("Enter the amount to deposit: "))
            logged_account.set_balance(logged_account.get_balance() + amount)

        #fourth option is view history
        if opcao == '4':
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
                    history.show()  # Chama o método show() específico de cada tipo
                    print("-" * 30)
            
            print("\n" + "=" * 45)
            input("Press Enter to continue...")  # Pausa para o usuário ler

        #fifth option is transfer
        if opcao == '5':
            print("\n========== Transfer ==========\n")

            # Exibe a lista de contas para transferência
            for i, account in enumerate(accounts, 1):
                if account != logged_account:  # Não exibe a conta logada
                    print(f"{i}. {account.get_name()}")

            choice = int(input("Select the account to transfer to (number): "))
            if 1 <= choice <= len(accounts):
                target_account = accounts[choice - 1]
                amount = float(input("Enter the amount to transfer: "))
                transaction(logged_account, target_account, amount)
            else:
                print("Invalid account selection.")

        #sixty option is change account
        if opcao == '6':
            print("\n========== Change Account ==========\n")
            # Exibe a lista de contas para troca
            for i, account in enumerate(accounts, 1):
                if account != logged_account:  # Não exibe a conta logada
                    print(f"{i}. {account.get_name()}")

            choice = int(input("Select the account to switch to (number): "))
            if 1 <= choice <= len(accounts):
                if input("Enter the password:") == accounts[choice - 1]:
                    logged_account = accounts[choice - 1]
                    print(f"Switched to account: {logged_account.get_name()}")
            else:
                print("Invalid account selection.")

        #seventh option is pay bills
        if opcao == '7':
            print("\n========== Pay Bills ==========\n")
    
        # Verifica se existem boletos na lista
        if not bills_list:
            print("📋 No bills available to pay.")
            input("Press Enter to continue...")
        else:
            # Filtra apenas boletos não pagos
            unpaid_bills = [bill for bill in bills_list if not bill.is_paid()]
            
            if not unpaid_bills:
                print("✅ All bills have been paid!")
                input("Press Enter to continue...")
            else:
                print(f"📊 Found {len(unpaid_bills)} unpaid bill(s):")
                print("-" * 50)
                
                # Exibe os boletos não pagos com informações detalhadas
                for i, bill in enumerate(unpaid_bills, 1):
                    status = "⚠️ OVERDUE" if bill.is_overdue() else "📅 Pending"
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
                        
                        # Confirmação antes do pagamento
                        print(f"\n📋 Bill Details:")
                        print(f"Description: {selected_bill.get_description()}")
                        print(f"Value: R$ {selected_bill.get_value():.2f}")
                        print(f"Due Date: {selected_bill.get_due_date().strftime('%Y-%m-%d')}")
                        
                        if selected_bill.is_overdue():
                            print("⚠️  WARNING: This bill is overdue!")
                        
                        confirm = input("\nConfirm payment? (y/n): ").lower().strip()
                        
                        if confirm in ['y', 'yes', 's', 'sim']:
                            try:
                                # Tenta pagar o boleto usando o método da classe Bill
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





        

def main():
    accounts = [] # lista para armazenar as contas criadas e fazer as validações necessárias

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
    bills_list.append(Bill(100, "Instalação da fonte", "2023-10-31"))
    bills_list.append(Bill(200, "Corrimão da escada", "2023-11-15"))


     #começo do menu no terminal, pede o usuário e a senha
    print("North Frontier Bank - Welcome!")
    print("Log in to an existing account or create a new one.")
    nome = input("Enter your name: ")
    senha = input("Enter your password: ")

    #loop para login (bem simples, possívelmente alterar depois)
    for account in accounts:
        if account.get_name() == nome and account.get_password() == senha:
            account_logged = account # armazena a conta atual(conta logada)
            print(f"Welcome, {account_logged.get_name()}!")
            break
    else:
        # se não encontrar a conta, cria uma nova
        print("Conta não encontrada. Criando uma nova conta...")
        account_nova = User(nome, senha, 0)
        accounts.append(account_nova)
        account_logged = account_nova

    loop_menu(account_logged, accounts, bills_list)


if __name__ == "__main__":
    main()