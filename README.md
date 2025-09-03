# Bank-Aplication-OO

## Objetos para se utilizar
 - Cliente - Tudo que tem relação com o usuário, desde saldo e nome até histórico
 - Nó do histórico - É o objeto que define uma ação do histórico (transferências, pagamentos, etc)
 - Transferência - Para transferir dinheiro entre contas
 - Boleto - Valor, data de vencimento e funções relacionadas a juros
 - Empréstimo - Para manipular cada valor, juros e prazos de um empréstimo
 - Investimento - Manipular e atribuir os investimentos de cada usuário

# North Frontier Bank System

A comprehensive banking system simulation built in Python featuring user account management, transactions, loans, bills, and investment goals.

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

### System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Python Version**: Python 3.6 or higher
- **Memory**: Minimum 128 MB RAM
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
   ├── main.py
   ├── users.py
   ├── bill.py
   ├── loan.py
   ├── goal.py
   └── history.py
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
git clone [repository-url]
cd north_frontier_bank
python main.py
```

#### Using ZIP Download
1. Download ZIP file from repository
2. Extract to desired location
3. Navigate to extracted folder in terminal
4. Run: `python main.py`

### Troubleshooting

#### Common Issues and Solutions

**"python is not recognized as an internal or external command"**
- Solution: Install Python from [python.org](https://python.org) or use `python3` command

**"No module named 'users'"**
- Solution: Ensure all Python files are in the same directory and you're running from that directory

**Permission denied errors**
- Solution: Make sure you have read/write permissions in the directory

**Import errors**
- Solution: Check that all files are present and properly named (case-sensitive on some systems)

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

## Technical Features

### Object-Oriented Design
- Inheritance: `Investor` extends `User`
- Abstraction: Abstract `History` class with concrete implementations
- Encapsulation: Private attributes with getter/setter methods
- Polymorphism: Different history types with unified interface
