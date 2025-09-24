"""
Main refatorada aplicando os design patterns (Factory method Singleton e Abstract Factory)

"""
from core.menu_manager import MenuManager
from core.customer_service import CustomerService
from core.bank_singleton import BankSystem

def ask(prompt):
    print(prompt)
    choice = input("Select the number: ")
    return choice

def main():

    # gerenciador de menu (usando Singleton)
    menu_manager = MenuManager()
    
    # sistema com dados de exemplo
    menu_manager.initialize_system()
    
    # login
    if not menu_manager.login():
        print("Login failed. Exiting...")
        return
    
    # loop principal 
    while True:
        # notificações de boletos vencidos
        bank_system = BankSystem()  # sempre retorna a mesma instance (Singleton)
        bills = bank_system.get_unpaid_bills()
        
        for bill in bills:
            if bill.is_overdue():
                print(f"⚠️ Overdue Bill: {bill.get_description()} - Valor: R$ {bill.get_value():.2f}")
        
        print("=" * 50)
        
        # mostra menu de opções
        choice = ask("\n1. Balance\n2. Withdraw\n3. Deposit\n4. View History\n5. Transfer\n6. Change Account\n7. Pay Bill\n8. Exchange Real -> Dollar \n9. Exchange Dollar -> Real\n10. Loan\n11. Checkbook\n12. Create Investment Goal\n13. Deposit in Goal\n14. Customer Service\n15. Exit\n")
        
        # escolha do usuário
        if choice == '1':
            menu_manager.show_balance()
            
        elif choice == '2':
            menu_manager.process_withdrawal()
            
        elif choice == '3':
            menu_manager.process_deposit()
            
        elif choice == '4':
            menu_manager.show_history()
            
        elif choice == '5':
            menu_manager.process_transfer()
            
        elif choice == '6':
            # se a troca de conta deu bom continua com a nova conta
            menu_manager.change_account()
            
        elif choice == '7':
            menu_manager.pay_bills()
            
        elif choice == '8':
            menu_manager.exchange_real_to_dollar()
            
        elif choice == '9':
            menu_manager.exchange_dollar_to_real()
            
        elif choice == '10':
            menu_manager.process_loan()
            
        elif choice == '11':
            menu_manager.order_checkbook()
            
        elif choice == '12':
            menu_manager.create_investment_goal()
            
        elif choice == '13':
            menu_manager.deposit_in_goal()
            
        elif choice == '14':
            CustomerService.show_menu()
            
        elif choice == '15':
            print("Exiting...")
            break
            
        else:
            print("Invalid option. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
