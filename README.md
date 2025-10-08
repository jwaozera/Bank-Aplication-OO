# 🏦 North Frontier Bank System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow.svg)

A comprehensive banking system simulation built with Python, featuring **5 Object-Oriented Design Patterns** and complete financial management capabilities.

> 🔄 **Refactoring Project**: This is a complete architectural refactoring of Alison Bruno's Bank Application for the Software Design course, demonstrating professional design pattern implementation and modular architecture.

---

## 🎯 Overview

North Frontier Bank is a modular banking application that demonstrates professional software architecture through the implementation of industry-standard design patterns. The system supports account management, transactions, loans, bills, and investment goals.

---

## ✨ Key Features

- 💰 **Complete Banking Operations**: Deposits, withdrawals, transfers, and balance inquiries
- 💳 **Bill Management**: Pay bills with due date tracking and overdue notifications
- 🏦 **Loan System**: Apply for loans with automatic payment scheduling
- 💱 **Currency Exchange**: Real ↔ Dollar conversion
- 📊 **Investment Goals**: Track and achieve financial targets (Investor accounts)
- 📝 **Transaction History**: Complete audit trail of all operations
- 🔔 **Smart Notifications**: Real-time alerts using Observer pattern
- 🛟 **Customer Service**: Comprehensive help system

---

## 🏗️ Design Patterns Implemented

### 1️⃣ **Singleton Pattern** (Creational)
**Location**: `core/bank_singleton.py`

Ensures only one instance of the banking system exists throughout the application.

**Benefits**:
- Centralized state management
- Prevents data inconsistencies
- Global access point for accounts and bills

```python
# Single source of truth for the entire banking system
bank_system = BankSystem()  # Always returns the same instance
```

---

### 2️⃣ **Factory Method Pattern** (Creational)
**Location**: `core/user_factory.py`

Creates different types of users (Regular/Investor) without exposing instantiation logic.

**Benefits**:
- Simplified object creation
- Easy to extend with new user types
- Separation of concerns

```python
# Clean user creation through factories
factory = UserFactoryProvider.get_factory("investor")
user = factory.create_user(name, password, balance)
```

---

### 3️⃣ **Abstract Factory Pattern** (Creational)
**Location**: `core/transaction_factory.py`

Creates families of related transaction history objects with context-aware enhancements.

**Benefits**:
- Consistent object creation across user types
- Enhanced history tracking for different user categories
- Easier maintenance and extension

```python
# Context-aware transaction history
factory = TransactionFactoryProvider.get_factory(user)
history = factory.create_transaction_history(action, description, amount, balance)
```

---

### 4️⃣ **Template Method Pattern** (Behavioral)
**Location**: `models/history.py`

Defines the skeleton of the `show()` operation in the abstract `History` class, allowing subclasses to customize specific steps while maintaining a consistent structure.

**Benefits**:
- Code reuse through inheritance
- Consistent interface across history types
- Easy to add new history types

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

**Observers Implemented**:
- `BillNotificationObserver`: Alerts for overdue and paid bills
- `BalanceObserver`: Warnings for low/negative balance
- `GoalProgressObserver`: Investment goal progress tracking

```python
# Automatic notifications when events occur
user.attach(BalanceObserver())
bill.attach(BillNotificationObserver())
```

---

## 📁 Project Structure

```
north_frontier_bank/
├── main.py                          # Application entry point
├── core/                            # Core business logic
│   ├── __init__.py
│   ├── bank_singleton.py            # Singleton Pattern
│   ├── user_factory.py              # Factory Method Pattern
│   ├── transaction_factory.py       # Abstract Factory Pattern
│   ├── observers.py                 # Observer Pattern
│   ├── menu_manager.py              # Menu operations manager
│   └── customer_service.py          # Help and support system
└── models/                          # Domain models
    ├── __init__.py
    ├── users.py                     # User and Investor classes
    ├── bill.py                      # Bill management
    ├── history.py                   # Transaction history (Abstract class)
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
1.  💰 Balance              - View your Real and Dollar balances
2.  📤 Withdraw             - Remove funds from account
3.  📥 Deposit              - Add funds to account
4.  📜 View History         - Complete transaction log
5.  🔄 Transfer             - Send money to other accounts
6.  🔐 Change Account       - Switch between user accounts
7.  💳 Pay Bill             - Manage and pay bills
8.  💱 Real → Dollar        - Currency exchange
9.  💱 Dollar → Real        - Currency exchange
10. 💰 Loan                 - Apply for financial assistance
11. 📔 Checkbook            - Order checkbooks
12. 🎯 Create Goal          - Set investment targets (Investors)
13. 📊 Deposit in Goal      - Fund your goals (Investors)
14. 🛟 Customer Service     - Help and support
15. ❌ Exit                 - Close application
```

---

## 🔄 Architectural Improvements

### Before Refactoring (Original Code by Alison Bruno)
- ❌ Monolithic `main.py` with 800+ lines
- ❌ Mixed responsibilities and concerns
- ❌ Hard to maintain and extend
- ❌ Direct object instantiation everywhere
- ❌ No design patterns implemented
- ❌ Limited modularity

### After Refactoring (Software Design Course Project)
- ✅ Modular architecture with clear separation
- ✅ **5 Design patterns** professionally implemented
- ✅ Easy to test and maintain
- ✅ Factory-based object creation
- ✅ Event-driven notifications (Observer pattern)
- ✅ Single source of truth (Singleton pattern)
- ✅ Consistent history display (Template Method pattern)
- ✅ Flexible transaction creation (Abstract Factory pattern)

---

## 🛠️ Technologies Used

- **Language**: Python 3.8+
- **Paradigm**: Object-Oriented Programming
- **Patterns**: Singleton, Factory Method, Abstract Factory, Template Method, Observer
- **Architecture**: Modular with separation of concerns

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
- Design pattern implementation (5 patterns)
- Modular architecture and separation of concerns
- Object-oriented design best practices
- Code maintainability and scalability

**Learning Outcomes**:
- ✅ Transformed monolithic code into modular architecture
- ✅ Implemented 5 industry-standard design patterns
- ✅ Improved code maintainability
- ✅ Enhanced scalability and testability

Learning advanced Python concepts, software design patterns, and refactoring techniques

---
