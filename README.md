![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow.svg)


# Bank-Aplication-OO


## 🔄 Principais Destaques da Refatoração:


1. Design Patterns Implementados

- Singleton Pattern: Para gerenciar uma única instância do sistema bancário
- Factory Method Pattern: Para criação de diferentes tipos de usuários
- Abstract Factory Pattern: Para criar famílias de objetos de histórico de transações

2. Arquitetura Modular

- Antes: Um arquivo main.py com muitas linhas
- Depois: Estrutura modular com separação clara de responsabilidades

3. Melhorias Significativas

- Interface de usuário aprimorada visual + formatação
- Sistema completo de atendimento ao cliente
- Tratamento robusto de erros
- Gerenciamento avançado de contas


## Objetos para se utilizar
 - Cliente - Tudo que tem relação com o usuário, desde saldo e nome até histórico
 - Nó do histórico - É o objeto que define uma ação do histórico (transferências, pagamentos, etc)
 - Transferência - Para transferir dinheiro entre contas
 - Boleto - Valor, data de vencimento e funções relacionadas a juros
 - Empréstimo - Para manipular cada valor, juros e prazos de um empréstimo
 - Investimento - Manipular e atribuir os investimentos de cada usuário


# North Frontier Bank System - Refactored Edition

A comprehensive banking system simulation built in Python featuring advanced **Object-Oriented Design Patterns**, complete user account management, transactions, loans, bills, and investment goals.

## 🔄 Major Refactoring & Design Pattern Implementation

This version represents a **complete architectural overhaul** of the original banking system, implementing industry-standard **Creational Design Patterns** for better maintainability, scalability, and code organization.

### 🏗️ Design Patterns Implemented

#### 1. **Singleton Pattern**
- **Location**: `core/bank_singleton.py`
- **Purpose**: Ensures only one instance of the banking system exists throughout the application
- **Benefits**: 
  - Centralized state management
  - Prevents data inconsistencies
  - Global access point for system-wide data
  
```python
# Before: Multiple scattered lists and variables
accounts = []
bills_list = []
exchange_rate = 5.25

# After: Centralized Singleton management
bank_system = BankSystem()  # Always returns the same instance
```

#### 2. **Factory Method Pattern**
- **Location**: `core/user_factory.py`
- **Purpose**: Creates different types of users (Regular/Investor) without exposing instantiation logic
- **Benefits**:
  - Simplified object creation
  - Easy to extend with new user types
  - Separation of concerns

```python
# Before: Direct instantiation with conditional logic
if user_type == "investor":
    user = Investor(name, password, balance)
else:
    user = User(name, password, balance)

# After: Factory pattern
factory = UserFactoryProvider.get_factory("investor")
user = factory.create_user(name, password, balance)
```

#### 3. **Abstract Factory Pattern**
- **Location**: `core/transaction_factory.py`
- **Purpose**: Creates families of related transaction history objects
- **Benefits**:
  - Consistent object creation across user types
  - Enhanced history tracking for different user categories
  - Easier maintenance and extension

```python
# Before: Direct history creation
history = History_transaction(action, description, amount, balance)

# After: Context-aware factory creation
factory = TransactionFactoryProvider.get_factory(user)
history = factory.create_transaction_history(action, description, amount, balance)
```

### 📁 New Modular Architecture

#### **Before (Monolithic Structure)**:
```
bank_application/
├── main.py (800+ lines of mixed responsibilities)
├── users.py
├── bill.py
├── history.py
├── loan.py
└── goal.py
```

#### **After (Modular Pattern-Based Structure)**:
```
north_frontier_bank/
├── main.py (Clean, focused entry point)
├── core/                          # 🆕 Core business logic
│   ├── bank_singleton.py          # Singleton pattern
│   ├── user_factory.py           # Factory Method pattern
│   ├── transaction_factory.py    # Abstract Factory pattern
│   ├── menu_manager.py          # Menu operations manager
│   └── customer_service.py      # Modularized customer service
└── models/                       # Enhanced model classes
    ├── users.py
    ├── bill.py
    ├── history.py
    ├── loan.py
    └── goal.py
```


## System Architecture

### Core Modules

#### `users.py`
- `User` class: Base user functionality
- `Investor` class: Extended user with investment capabilities
- Transaction handling between accounts
- Balance and history management

#### `bill.py`
- `Bill` class: Bill management system
- Due date tracking and overdue detection
- Payment processing with balance validation
- Integration with user history

#### `loan.py`
- `Loan` class: Loan creation and management
- Automatic history entry generation
- Integration with user account system

#### `goal.py`
- `Goal` class: Investment goal tracking
- Progress monitoring and completion detection
- Automatic removal upon goal achievement

#### `history.py`
- Abstract `History` class with specialized subclasses:
  - `History_transaction`: Deposits, withdrawals, transfers
  - `History_loan`: Loan records
  - `History_bill`: Bill payments
  - `History_investment`: Investment activities
  - `History_cheque_book`: Checkbook orders

#### `main.py`
- Main application loop and user interface
- Menu system
- Account management and navigation
- Integration of all system components

## Getting Started

## Requirements

- **Python Version**: Python 3.6 or higher
- **Storage**: 10 MB free disk space

### Python Libraries

This project uses only **Python Standard Library** modules - no external packages need to be installed!

#### Required Standard Libraries (included with Python):
```python
# Built-in modules used:
from abc import ABC, abstractmethod  # Abstract base classes
from datetime import datetime, timedelta  # Date and time handling
```

### Installation Commands

Since the project only uses standard library modules, **no pip installations are required**:

```bash
# No need to run any of these commands:
# pip install requirements.txt  ❌ (not needed)
# pip install datetime          ❌ (built-in)
# pip install abc               ❌ (built-in)
```

### Verifying Your Python Installation

Check if your Python installation includes the required modules:

```bash
python -c "import datetime, abc; print('All required modules available!')"
```

If this command runs without errors, you're ready to use the banking system.

### Installation and Setup

#### Step 1: Download the Files
1. Download all the Python files to your computer
2. Create a new folder called `north_frontier_bank`
3. Place all files in the same directory:
   ```
  north_frontier_bank/
   ├── main.py (Clean, focused entry point)
   ├── core/                          # 🆕 Core business logic
   │   ├── bank_singleton.py          # Singleton pattern
   │   ├── user_factory.py           # Factory Method pattern
   │   ├── transaction_factory.py    # Abstract Factory pattern
   │   ├── menu_manager.py          # Menu operations manager
   │   └── customer_service.py      # Modularized customer service
   └── models/                       # Enhanced model classes
      ├── users.py
      ├── bill.py
      ├── history.py
      ├── loan.py
      └── goal.py
   ```

#### Step 2: Verify Python Installation
1. Open terminal/command prompt
2. Check if Python is installed:
   ```bash
   python --version
   ```
   or
   ```bash
   python3 --version
   ```
3. You should see something like: `Python 3.8.0` or higher

#### Step 3: Navigate to Project Directory
```bash
cd path/to/north_frontier_bank
```

#### Step 4: Run the Application
```bash
python main.py
```

If `python` doesn't work, try:
```bash
python3 main.py
```

### Alternative Installation Methods

#### Using Git (if project is in a repository)
```bash
git clone github.com/jwaozera/Bank-Aplication-OO
cd north_frontier_bank
python main.py
```

#### Using ZIP Download
1. Download ZIP file from repository
2. Extract to desired location
3. Navigate to extracted folder in terminal
4. Run: `python main.py`

## Default Accounts

The system comes with pre-configured test accounts:

### Regular Users
- **Kris**: Password `1234`, Balance: R$ 1,000.00
- **Susie**: Password `9876`, Balance: R$ 1,500.00

### Investor Users
- **Aubrey**: Password `4567`, Balance: R$ 2,500.00
- **Kel**: Password `999`, Balance: R$ 99,999.00
- **Mari**: Password `4444`, Balance: R$ 0.00

### Sample Bills
- Font installation: R$ 100.00 (Due: 2023-10-31)
- Stair railing: R$ 200.00 (Due: 2023-11-15)

## Usage Guide

### Login Process
1. Enter username and password
2. If account doesn't exist, a new regular account will be created
3. Access the main menu with full banking functionality

### Main Menu Options
1. **Balance**: View current Real and Dollar balances
2. **Withdraw**: Remove funds from account
3. **Deposit**: Add funds to account
4. **View History**: Complete transaction history
5. **Transfer**: Send money to other accounts
6. **Change Account**: Switch between user accounts
7. **Pay Bills**: Manage and pay outstanding bills
8 and 9. **Currency Exchange**: Convert between Real and Dollar
10. **Loan**: Apply for financial assistance
11. **Checkbook**: Order checkbooks
12. **Create Investment Goal**: Set financial targets (Investor only)
13. **Deposit in Goal**: Fund investment goals (Investor only)
14. **Customer Service**: Access help and support
15. **Exit**: Close the application

### Investment Goals (Investor Accounts)
- Create multiple financial targets
- View all active goals and their status


