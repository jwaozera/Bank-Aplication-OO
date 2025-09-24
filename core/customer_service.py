"""
customer services - Modularização do atendimento ao cliente

"""

class CustomerService:
    """Gerencia o sistema de atendimento ao cliente"""
    
    @staticmethod
    def show_menu():
        """Exibe o menu principal do atendimento"""
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
                CustomerService._show_banking_guide()
            elif choice == '2':
                CustomerService._show_payments_guide()
            elif choice == '3':
                CustomerService._show_account_guide()
            elif choice == '4':
                CustomerService._show_investment_guide()
            elif choice == '5':
                CustomerService._show_emergency_contact()
            elif choice == '6':
                print("\n↩️  Returning to Main Menu...")
                break
            else:
                print("\n❌ Invalid option. Please select a number from 1 to 6.")
                input("Press Enter to try again...")
    
    @staticmethod
    def _show_banking_guide():
        """Exibe guia de operações bancárias"""
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
    
    @staticmethod
    def _show_payments_guide():
        """Exibe guia de pagamentos e boletos"""
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
    
    @staticmethod
    def _show_account_guide():
        """Exibe guia de gerenciamento de conta"""
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
    
    @staticmethod
    def _show_investment_guide():
        """Exibe guia de investimentos"""
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
    
    @staticmethod
    def _show_emergency_contact():
        """Exibe informações de contato de emergência"""
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
