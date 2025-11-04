"""
Main refatorada aplicando os design patterns:
- Singleton, Factory Method, Abstract Factory 
- Template Method, Observer, Strategy 
- Decorator, Facade, Adapter (Padrões Estruturais)
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
        
        print("\n" + "="*60)
        print("🏦 NORTH FRONTIER BANK - MAIN MENU")
        print("="*60)
        
        # Menu principal expandido com novos padrões
        menu_text = """
╔══════════════════════════════════════════════════════════╗
║                    BASIC OPERATIONS                      ║
╠══════════════════════════════════════════════════════════╣
        1. 💰 Show Balance       2.  🏧 Withdraw
        3. 💵 Deposit            4.  📜 View History
        5. 🔄 Transfer           6.  🔐 Change Account
╠══════════════════════════════════════════════════════════╣
║                   PAYMENTS & LOANS                       ║
╠══════════════════════════════════════════════════════════╣
        7.  💳 Pay Bill           8.  💱 Real → Dollar          
        9.  💱 Dollar → Real      10. 💰 Loan                   
        11. 📔 Checkbook          12. 🎯 Create Goal            
        13. 📊 Deposit in Goal    14. 🛎️ Customer Service       
╠══════════════════════════════════════════════════════════╣
                      OTHER FEATURES               
╠══════════════════════════════════════════════════════════╣
        15. ✨ Upgrade Account               
        16. ⚡ Quick Operations                  
        17. 💳 Payment Methods                 
                                 
╠══════════════════════════════════════════════════════════╣
        0. ❌ Exit                                             
╚══════════════════════════════════════════════════════════╝
"""
        
        choice = ask(menu_text)
        
        # escolha do usuário
        if choice == '1':
            menu_manager.show_balance()
            c
        elif choice == '2':
            menu_manager.process_withdrawal()
            
        elif choice == '3':
            menu_manager.process_deposit()
            
        elif choice == '4':
            menu_manager.show_history()
            
        elif choice == '5':
            menu_manager.process_transfer()
            
        elif choice == '6':
            menu_manager.change_account()
            
        elif choice == '7':
            menu_manager.pay_bills()
            
        elif choice == '8':
            menu_manager.exchange_real_to_dollar()
            
        elif choice == '9':
            menu_manager.exchange_dollar_to_real()
            
        elif choice == '10':
            menu_manager.process_loan_with_strategy()
            
        elif choice == '11':
            menu_manager.order_checkbook()
            
        elif choice == '12':
            menu_manager.create_investment_goal()
            
        elif choice == '13':
            menu_manager.deposit_in_goal()
            
        elif choice == '14':
            CustomerService.show_menu()
        
        # ========== PADRÕES ESTRUTURAIS ==========
        
        elif choice == '15':
            # DECORATOR PATTERN
            menu_manager.upgrade_account()
            
        elif choice == '16':
            # FACADE PATTERN
            menu_manager.quick_operations_menu()
            
        elif choice == '17':
            # ADAPTER PATTERN
            menu_manager.payment_methods_menu()
            
        
        # ===============================================
            
        elif choice == '0':
            print("\n" + "="*60)
            print("👋 Thank you for using North Frontier Bank!")
            print("Exiting...")
            break
            
        else:
            print("❌ Invalid option. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
