# 🏦 North Frontier Bank System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen.svg)
![Patterns](https://img.shields.io/badge/Design%20Patterns-9-orange.svg)
![Exception Handling](https://img.shields.io/badge/Exception%20Handling-Robusto-green.svg)

A comprehensive banking system simulation built with Python, featuring **9 Object-Oriented Design Patterns**, **Robust Exception Handling**, and complete financial management capabilities.

> 🔄 **Refactoring Project**: This is a complete architectural refactoring of Alison Bruno's Bank Application for the Software Design course, demonstrating professional design pattern implementation, modular architecture, and enterprise-grade error handling.

---

## 🎯 Overview

North Frontier Bank is a modular banking application that demonstrates professional software architecture through the implementation of industry-standard design patterns and robust exception handling. The system supports account management, transactions, loans, bills, investment goals, and multiple payment methods with comprehensive error recovery mechanisms.

---

## ✨ Key Features

### Banking Operations
- 💰 **Complete Banking Operations**: Deposits, withdrawals, transfers, and balance inquiries
- 💳 **Bill Management**: Pay bills with due date tracking and overdue notifications
- 🏦 **Loan System**: Apply for loans with automatic payment scheduling and multiple strategies
- 💱 **Currency Exchange**: Real ↔ Dollar conversion with premium rates for upgraded accounts
- 📊 **Investment Goals**: Track and achieve financial targets (Investor accounts)
- 📝 **Transaction History**: Complete audit trail of all operations with enhanced logging

### Advanced Features
- 🔔 **Smart Notifications**: Real-time alerts using Observer pattern
- ✨ **Account Upgrades**: Premium, Insurance, VIP, and Student accounts via Decorator pattern
- ⚡ **Quick Operations**: Simplified complex operations through Facade pattern
- 💳 **Multiple Payment Methods**: PIX, Credit Card, Cryptocurrency, International transfers via Adapter pattern
- 🛡️ **Robust Error Handling**: Comprehensive exception handling for all operations
- 📞 **Customer Service**: Interactive help system

---

## 🏗️ Design Patterns Implemented

### 1️⃣ **Singleton Pattern** (Creational)
**Location**: `core/bank_singleton.py`

Ensures only one instance of the banking system exists throughout the application.

**Benefits**:
- Centralized state management
- Prevents data inconsistencies
- Global access point for accounts and bills
- Thread-safe implementation

```python
# Single source of truth for the entire banking system
bank_system = BankSystem()  # Always returns the same instance
```

**Key Methods**:
- `add_account()` - Register new accounts
- `get_unpaid_bills()` - Query bills with user filtering
- `find_account()` - Secure account lookup
- `initialize_demo_data()` - Bootstrap system with test data

---

### 2️⃣ **Factory Method Pattern** (Creational)
**Location**: `core/user_factory.py`

Creates different types of users (Regular/Investor) without exposing instantiation logic.

**Benefits**:
- Simplified object creation
- Easy to extend with new user types
- Separation of concerns
- Consistent object initialization

```python
# Clean user creation through factories
factory = UserFactoryProvider.get_factory("investor")
user = factory.create_user(name, password, balance)
```

**Factory Types**:
- `RegularUserFactory` - Standard banking accounts
- `InvestorUserFactory` - Accounts with investment features
- `UserFactoryProvider` - Dynamic factory selection

---

### 3️⃣ **Abstract Factory Pattern** (Creational)
**Location**: `core/transaction_factory.py`

Creates families of related transaction history objects with context-aware enhancements.

**Benefits**:
- Consistent object creation across user types
- Enhanced history tracking for different user categories
- Easier maintenance and extension
- Type-safe object creation

```python
# Context-aware transaction history
factory = TransactionFactoryProvider.get_factory(user)
history = factory.create_transaction_history(action, description, amount, balance)
```

**Factory Families**:
- `BankingTransactionFactory` - Standard transaction history
- `InvestmentTransactionFactory` - Enhanced history with investor tags
- Support for: Transactions, Bills, Loans, Investments

---

### 4️⃣ **Template Method Pattern** (Behavioral)
**Location**: `models/history.py`

Defines the skeleton of the `show()` operation in the abstract `History` class, allowing subclasses to customize specific steps while maintaining a consistent structure.

**Benefits**:
- Code reuse through inheritance
- Consistent interface across history types
- Easy to add new history types
- Enforces structure while allowing customization

**Implementations**:
- `History_transaction`: Shows transaction details with amount and balance
- `History_loan`: Shows loan-specific information
- `History_bill`: Shows bill payment details with due date
- `History_investment`: Shows investment-specific data
- `History_cheque_book`: Shows checkbook order records

```python
# Abstract base class defines the template
class History(ABC):
    def show(self):
        print("Action: ", self.__action)
        print("Time: ", self.__time)
        print("Description: ", self.__description)
        # Subclasses extend with specific details
```

---

### 5️⃣ **Observer Pattern** (Behavioral)
**Location**: `core/observers.py`

Implements event-driven notifications for important banking events.

**Benefits**:
- Real-time notifications for critical events
- Loose coupling between components
- Easy to add new notification types
- Automatic event propagation

**Observers Implemented**:
- `BillNotificationObserver`: Alerts for overdue and paid bills
- `BalanceObserver`: Warnings for low/negative balance
- `GoalProgressObserver`: Investment goal progress tracking

```python
# Automatic notifications when events occur
user.attach(BalanceObserver())
bill.attach(BillNotificationObserver())

# Events trigger notifications
user.withdraw(amount)  # → LOW_BALANCE notification if < R$ 100
bill.pay(user)         # → BILL_PAID notification
```

**Event Types**:
- `LOW_BALANCE` - Balance below R$ 100
- `NEGATIVE_BALANCE` - Account overdrawn
- `BILL_OVERDUE` - Bill past due date
- `BILL_PAID` - Bill successfully paid
- `GOAL_PROGRESS` - Investment goal update
- `GOAL_ACHIEVED` - Goal target reached

---

### 6️⃣ **Strategy Pattern** (Behavioral)
**Location**: `core/loan_strategy.py`

Defines a family of loan approval algorithms and makes them interchangeable based on user type and requirements.

**Benefits**:
- Flexible loan policies without modifying existing code
- Easy to add new loan strategies
- Dynamic strategy selection at runtime
- Encapsulates different approval criteria

**Strategies Implemented**:
- `StandardLoanStrategy`: Default policy for regular users (2x balance, 5% interest)
- `InvestorLoanStrategy`: Premium conditions for investors (3x balance, 3% interest)
- `ConservativeLoanStrategy`: Stricter requirements (1.5x balance, 6% interest)

```python
# Automatic strategy selection based on user type
strategy = LoanStrategyProvider.get_strategy(user, "auto")
processor = LoanProcessor(user, strategy)
processor.process_loan_request(amount, duration)
```

**Strategy Features**:
- `calculate_max_loan()` - Determines loan limit
- `calculate_interest_rate()` - Computes interest based on duration
- `can_approve_loan()` - Validates loan eligibility

---

### 7️⃣ **Decorator Pattern** (Structural)
**Location**: `core/decorators.py`

Dynamically adds responsibilities to user accounts without modifying their structure.

**Benefits**:
- Add features dynamically at runtime
- Stack multiple decorators for combined functionality
- Follows Open/Closed Principle
- No need to modify base User class

**Decorators Implemented**:
- `PremiumAccountDecorator`: 1% cashback on withdrawals, better exchange rates
- `InsuranceDecorator`: Protection for large transactions (>R$ 5,000)
- `NotificationDecorator`: SMS/Email alerts for all transactions
- `StudentAccountDecorator`: Fee exemptions, daily withdrawal limits
- `VIPDecorator`: Personal manager, reduced interest rates

```python
# Stack decorators for combined features
user = PremiumAccountDecorator(user)
user = InsuranceDecorator(user)
user = NotificationDecorator(user, email="user@email.com", phone="123456789")

# Or use helper function for multiple decorators
user = decorate_user(user, [
    ('premium', {}),
    ('insurance', {}),
    ('notification', {'email': 'user@email.com', 'phone': '123456789'})
])
```

**Decorator Features**:
- **Premium**: 1% cashback on withdrawals, 0.5% on transfers, 5% better exchange rate
- **Insurance**: Protection for transactions >R$ 5,000, R$ 29.90/month
- **Notifications**: Email for all transactions, SMS for >R$ 1,000
- **Student**: Free checkbooks, R$ 500 daily limit, 50% off exchange fees
- **VIP**: Personal manager, 30% interest discount, priority service

---

### 8️⃣ **Facade Pattern** (Structural)
**Location**: `core/facades.py`

Provides simplified interfaces to complex subsystems for common banking operations.

**Benefits**:
- Simplifies complex multi-step operations
- Reduces learning curve for system usage
- Encapsulates business logic
- Makes the system easier to use and understand

**Facades Implemented**:
- `BankingFacade`: Simplified banking operations (quick transfers, pay all bills, emergency loans)
- `InvestmentFacade`: Portfolio management (diversified portfolios, auto-invest)
- `ReportFacade`: Financial reporting (account summaries, tax reports, comparisons)

```python
# Complex operation simplified into one call
facade = BankingFacade(user)
facade.pay_all_bills(filter_overdue=True)

# Multi-step portfolio creation made easy
investment_facade = InvestmentFacade(investor)
investment_facade.create_diversified_portfolio(total_amount, goals_list)
```

**Facade Operations**:

**BankingFacade**:
- `quick_transfer_with_exchange()` - Transfer with automatic currency conversion
- `pay_all_bills()` - Batch bill payment with filtering
- `create_savings_plan()` - Automated monthly savings
- `emergency_loan()` - Simplified loan process
- `get_account_summary()` - Comprehensive account overview

**InvestmentFacade**:
- `create_diversified_portfolio()` - Multi-goal portfolio setup
- `auto_invest_monthly()` - Automatic investment distribution
- `get_portfolio_summary()` - Portfolio analytics

**ReportFacade**:
- `generate_financial_report()` - Period-based analysis
- `generate_tax_report()` - Tax declaration data
- `compare_with_average()` - Benchmark against system average

---

### 9️⃣ **Adapter Pattern** (Structural)
**Location**: `core/adapters.py`

Integrates external payment systems (PIX, Credit Card, Crypto, International) with the bank's internal interface.

**Benefits**:
- Seamless integration with third-party APIs
- Uniform interface for different payment methods
- Easy to add new payment providers
- Isolates system from external API changes

**Adapters Implemented**:
- `PixAdapter`: Integrates PIX payment system with key validation
- `CreditCardAdapter`: Credit card gateway with CVV/expiry validation
- `CryptoAdapter`: Cryptocurrency exchange (BTC, ETH)
- `InternationalBankAdapter`: SWIFT international transfers

**External APIs Simulated**:
- `PixAPI`: Brazilian instant payment system with key registry
- `CreditCardGateway`: Card processing with validation
- `CryptoExchangeAPI`: Cryptocurrency trading with real-time rates
- `InternationalBankingAPI`: SWIFT transfers with fee calculation

```python
# Unified payment interface for different methods
payment_manager = PaymentManager(user)

# Add various payment methods
pix_adapter = PixAdapter(pix_api, user, "user@email.com")
card_adapter = CreditCardAdapter(gateway, user, card_number, cvv, expiry, name)
crypto_adapter = CryptoAdapter(crypto_api, user)
swift_adapter = InternationalBankAdapter(swift_api, user)

payment_manager.add_payment_method("PIX", pix_adapter)
payment_manager.add_payment_method("Credit Card", card_adapter)
payment_manager.add_payment_method("Crypto", crypto_adapter)
payment_manager.add_payment_method("International", swift_adapter)

# Pay using any method with same interface
payment_manager.pay_with("PIX", amount, description, destination="merchant@bank.com")
payment_manager.pay_bill_with_method(bill, "Credit Card")
```

**Adapter Features**:
- **PIX**: Instant transfers, key validation, transaction history
- **Credit Card**: Credit limit management, CVV/expiry validation, invoice payment
- **Crypto**: BTC/ETH trading, balance tracking, buy/sell operations
- **International**: SWIFT transfers, fee calculation (3%), 3-day processing

---

## 🛡️ Exception Handling Architecture

### Overview
The system implements **enterprise-grade exception handling** with custom exception hierarchies, input validation, and graceful error recovery.

**Location**: `core/menu_manager.py` (Updated with comprehensive exception handling)

### Custom Exception Hierarchy

```python
BankingException (Base)
├── InsufficientBalanceException    # Saldo insuficiente
├── InvalidAmountException          # Valor inválido
├── AccountNotFoundException        # Conta não encontrada
├── InvalidCredentialsException     # Credenciais inválidas
└── InvestorOnlyFeatureException    # Recurso exclusivo para investidores
```

### Exception Handling Features

#### 1. **Input Validation (`InputValidator` class)**
**Benefits**:
- Centralized validation logic
- Reusable across all operations
- Consistent error messages
- Type-safe input collection

**Methods**:
```python
# Float input with range validation
amount = validator.get_float_input(
    "Enter amount: ",
    min_value=0.01,
    max_value=1000000
)

# Integer input for menu selections
choice = validator.get_int_input(
    "Select option: ",
    min_value=1,
    max_value=10
)

# Choice validation from list
confirm = validator.get_choice(
    "Confirm? (y/n): ",
    ['y', 'yes', 'n', 'no']
)
```

#### 2. **Operation-Specific Exception Handling**

**Login (`login()`)**:
- Handles empty credentials
- Limits login attempts (3 max)
- Catches account creation failures
- Supports Ctrl+C cancellation

**Withdrawal (`process_withdrawal()`)**:
- Validates account existence
- Checks sufficient balance
- Prevents negative withdrawals
- Ensures transaction atomicity

**Transfer (`process_transfer()`)**:
- Validates both accounts
- Prevents invalid selections
- Checks balance before transfer
- Handles index errors gracefully

**Bill Payment (`pay_bills()`)**:
- Handles empty bill lists
- Validates bill ownership
- Prevents duplicate payments
- Manages overdue bills

**Investment Goals (`create_investment_goal()`)**:
- Enforces investor-only access
- Validates goal descriptions
- Checks amount ranges
- Prevents invalid goals

#### 3. **Exception Handling Patterns**

**Pattern 1: Try-Except-Finally**
```python
try:
    critical_operation()
except SpecificException as e:
    print(f"❌ Specific error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
finally:
    input("Press Enter to continue...")  # Always executes
```

**Pattern 2: Multiple Exception Types**
```python
try:
    operation()
except (ValueError, TypeError, IndexError) as e:
    print(f"❌ Input error: {e}")
```

**Pattern 3: Exception Chaining**
```python
try:
    low_level_operation()
except ValueError as e:
    raise InvalidAmountException(f"Invalid amount: {e}") from e
```

### Benefits of Exception Handling

1. **🛡️ Robustness**: System never crashes from user input
2. **🔒 Security**: No sensitive data leaked in stack traces
3. **👤 User Experience**: Clear, actionable error messages
4. **🔧 Maintainability**: Easy to add new error cases
5. **🐛 Debugging**: Specific exceptions pinpoint issues
6. **💾 Data Integrity**: Banking data remains consistent

### Exception Handling Coverage

| Operation | Exceptions Handled | Recovery Strategy |
|-----------|-------------------|-------------------|
| Login | `InvalidCredentialsException`, `ValueError` | Retry with attempt limit |
| Withdrawal | `InsufficientBalanceException`, `ValueError` | Show balance, allow retry |
| Deposit | `InvalidAmountException`, `ValueError` | Validate input, allow retry |
| Transfer | `AccountNotFoundException`, `IndexError` | Show accounts, allow retry |
| Bill Payment | `ValueError`, `AttributeError` | Skip corrupted bills |
| Investment Goals | `InvestorOnlyFeatureException` | Suggest account upgrade |
| All Operations | `KeyboardInterrupt` | Graceful cancellation |

---

## 📁 Project Structure

```
north_frontier_bank/
├── main.py                          # Application entry point with pattern demos
├── core/                            # Core business logic
│   ├── __init__.py                  # Package initialization with exports
│   ├── bank_singleton.py            # ✅ Singleton Pattern
│   ├── user_factory.py              # ✅ Factory Method Pattern
│   ├── transaction_factory.py       # ✅ Abstract Factory Pattern
│   ├── observers.py                 # ✅ Observer Pattern
│   ├── loan_strategy.py             # ✅ Strategy Pattern
│   ├── decorators.py                # ✅ Decorator Pattern
│   ├── facades.py                   # ✅ Facade Pattern
│   ├── adapters.py                  # ✅ Adapter Pattern
│   ├── menu_manager.py              # Menu operations + Exception Handling
│   └── customer_service.py          # Help and support system
└── models/                          # Domain models
    ├── __init__.py                  # Package initialization
    ├── users.py                     # User and Investor classes with Observer
    ├── bill.py                      # Bill management with Observer
    ├── history.py                   # ✅ Template Method Pattern
    ├── loan.py                      # Loan handling
    ├── goal.py                      # Investment goals
    └── investment.py                # Investment operations
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (only standard library modules required)
- No external dependencies needed!

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/jwaozera/Bank-Aplication-OO.git
cd north_frontier_bank
```

2. **Run the application**
```bash
python main.py
```

---

## 👥 Demo Accounts

### Regular Users
- **Kris**: Password `1234` | Balance: R$ 1,000.00
- **Susie**: Password `9876` | Balance: R$ 1,500.00
- **jwao**: Password `admin` | Balance: R$ 100,000.00

### Investor Users
- **Aubrey**: Password `4567` | Balance: R$ 2,500.00
- **Kel**: Password `999` | Balance: R$ 99,999.00
- **Mari**: Password `4444` | Balance: R$ 100.00

---

## 📱 Main Menu Options

```
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
```

---

## 🔄 Architectural Improvements

### Before Refactoring (Original Code)
- ❌ Monolithic `main.py` with 800+ lines
- ❌ Mixed responsibilities and concerns
- ❌ Hard to maintain and extend
- ❌ Direct object instantiation everywhere
- ❌ No design patterns implemented
- ❌ Limited modularity
- ❌ Basic error handling with print statements
- ❌ No input validation

### After Refactoring (Software Design Course Project)
- ✅ Modular architecture with clear separation of concerns
- ✅ **9 Design patterns** 
- ✅ **Robust exception handling** with custom exception hierarchy
- ✅ **Input validation** through dedicated validator class
- ✅ Easy to test and maintain
- ✅ Factory-based object creation
- ✅ Event-driven notifications (Observer pattern)
- ✅ Single source of truth (Singleton pattern)
- ✅ Consistent history display (Template Method pattern)
- ✅ Flexible transaction creation (Abstract Factory pattern)
- ✅ Multiple loan strategies (Strategy pattern)
- ✅ Dynamic account features (Decorator pattern)
- ✅ Simplified complex operations (Facade pattern)
- ✅ Integrated payment systems (Adapter pattern)
- ✅ Enterprise-grade error recovery
- ✅ Type-safe operations with validation

---

## 🛠️ Technologies Used

- **Language**: Python 3.8+
- **Paradigm**: Object-Oriented Programming
- **Patterns**: 9 Design Patterns
- **Architecture**: Modular with separation of concerns
- **Error Handling**: Custom exception hierarchy with graceful recovery
- **Validation**: Centralized input validation system

---

## 📊 Design Patterns Summary

| Pattern | Type | Location | Purpose |
|---------|------|----------|---------|
| **Singleton** | Creational | `core/bank_singleton.py` | Single banking system instance |
| **Factory Method** | Creational | `core/user_factory.py` | User object creation |
| **Abstract Factory** | Creational | `core/transaction_factory.py` | Transaction history families |
| **Template Method** | Behavioral | `models/history.py` | History display structure |
| **Observer** | Behavioral | `core/observers.py` | Event notifications |
| **Strategy** | Behavioral | `core/loan_strategy.py` | Loan approval algorithms |
| **Decorator** | Structural | `core/decorators.py` | Dynamic account features |
| **Facade** | Structural | `core/facades.py` | Simplified operations |
| **Adapter** | Structural | `core/adapters.py` | External payment integration |

---

## ⚠️ Limitations

### Current Limitations

1. **Data Persistence**
   - ❌ No database integration - data lost on restart
   - ❌ In-memory storage only
   - **Impact**: Demo/testing purposes only
   - **Workaround**: Use demo accounts for testing

2. **Security**
   - ⚠️ Passwords stored in plain text
   - ⚠️ No encryption for sensitive data
   - ⚠️ No authentication tokens
   - **Impact**: Not production-ready for real banking
   - **Note**: For educational purposes

3. **External APIs**
   - ⚠️ Payment APIs are simulated/mocked
   - ⚠️ No real PIX/Credit Card integration
   - ⚠️ Exchange rates are hardcoded
   - **Impact**: Cannot process real payments
   - **Purpose**: Demonstrates adapter pattern only



---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Credits

**Original Project**: Alison Bruno's Bank Application  
**Refactoring & Design Patterns**: João Euclides ([@jwaozera](https://github.com/jwaozera))  
**Course**: Software Design (Projeto de Software) - Professor Baldoino Fonseca  
**Focus**: Design Pattern Implementation & Architectural Refactoring

---

## 🎓 Educational Purpose

This refactoring project was developed as part of a Software Design course to demonstrate:
- Professional software engineering practices
- Design pattern implementation (9 patterns)
- Modular architecture and separation of concerns
- Object-oriented design best practices
- Code maintainability and scalability
- Exception handling

**Learning Outcomes**:
- ✅ Transformed monolithic code into modular architecture
- ✅ Implemented 9 industry-standard design patterns
- ✅ Improved code maintainability
- ✅ Enhanced scalability and testability
- ✅ Exception handling 

Learning advanced Python concepts, software design patterns, and refactoring techniques

---
