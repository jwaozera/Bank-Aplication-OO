"""
Adapter Pattern - Adaptadores de Métodos de Pagamento
Correções:
1. PIX valida chaves existentes
2. Pagamentos deduzem saldo corretamente
3. Bills são individuais por usuário
4. Credit card valida CVV e expiry
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from models.users import User
from models.bill import Bill
from datetime import datetime
import re


# ==================== INTERFACE DO SISTEMA ====================

class PaymentProcessor(ABC):
    """Interface padrão para processamento de pagamentos no sistema"""
    
    @abstractmethod
    def process_payment(self, amount: float, description: str, 
                       destination: str = None) -> Dict[str, any]:
        pass
    
    @abstractmethod
    def check_balance(self) -> float:
        pass
    
    @abstractmethod
    def get_transaction_history(self, limit: int = 10) -> list:
        pass


# ==================== SISTEMAS EXTERNOS (APIs de terceiros) ====================

class PixAPI:
    """Sistema externo PIX (simulado com validação)"""
    
    def __init__(self):
        self.transactions = []
        # Simula chaves PIX registradas no sistema
        self.registered_keys = {
            "user@example.com": {"name": "User Example", "type": "email"},
            "123456789": {"name": "Phone User", "type": "phone"},
            "test@test.com": {"name": "Test User", "type": "email"},
        }
    
    def validate_pix_key(self, pix_key: str) -> bool:
        """Valida se a chave PIX existe"""
        # Aceita chaves registradas OU chaves do padrão email/phone válido
        if pix_key in self.registered_keys:
            return True
        
        # Valida formato de email
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', pix_key):
            # Auto-registra email válido
            self.registered_keys[pix_key] = {"name": "New User", "type": "email"}
            return True
        
        # Valida formato de telefone (números)
        if pix_key.isdigit() and 10 <= len(pix_key) <= 11:
            self.registered_keys[pix_key] = {"name": "New Phone", "type": "phone"}
            return True
        
        return False
    
    def send_pix(self, value: float, pix_key: str, message: str) -> Dict[str, any]:
        """API do PIX com validação"""
        print(f"🔷 PIX API: Processing transaction...")
        
        if value <= 0:
            return {"status": "failed", "error": "Invalid amount"}
        
        # VALIDAÇÃO DE CHAVE PIX
        if not self.validate_pix_key(pix_key):
            return {
                "status": "failed", 
                "error": f"Invalid PIX key: {pix_key}. Key not found in PIX system."
            }
        
        transaction_id = f"PIX{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        result = {
            "status": "approved",
            "transaction_id": transaction_id,
            "pix_key": pix_key,
            "recipient": self.registered_keys[pix_key]["name"],
            "amount": value,
            "timestamp": datetime.now().isoformat()
        }
        
        self.transactions.append(result)
        print(f"✅ PIX sent: R$ {value:.2f} to {pix_key}")
        print(f"   Recipient: {result['recipient']}")
        return result
    
    def register_key(self, pix_key: str, name: str, key_type: str):
        """Registra uma nova chave PIX"""
        self.registered_keys[pix_key] = {"name": name, "type": key_type}
        print(f"✅ PIX key registered: {pix_key} ({name})")
    
    def list_transactions(self) -> list:
        return self.transactions


class CreditCardGateway:
    """Gateway de cartão de crédito com validação"""
    
    def __init__(self):
        self.transactions = []
    
    def validate_card(self, card_number: str, cvv: str, expiry: str) -> tuple[bool, str]:
        """Valida dados do cartão"""
        # Valida número do cartão (deve ter 16 dígitos)
        if not card_number.replace(" ", "").isdigit():
            return False, "Card number must contain only digits"
        
        card_clean = card_number.replace(" ", "")
        if len(card_clean) != 16:
            return False, "Card number must have 16 digits"
        
        # Valida CVV (3 ou 4 dígitos)
        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            return False, "CVV must be 3 or 4 digits"
        
        # Valida expiry (MM/YY)
        try:
            month, year = expiry.split("/")
            if not (1 <= int(month) <= 12):
                return False, "Invalid expiry month"
            
            current_year = datetime.now().year % 100
            if int(year) < current_year:
                return False, "Card expired"
        except:
            return False, "Invalid expiry format (use MM/YY)"
        
        return True, "Card valid"
    
    def charge_card(self, card_number: str, cvv: str, expiry: str, 
                   amount: float, merchant_id: str) -> Dict[str, any]:
        """API de cartão com validação"""
        print(f"💳 Credit Card Gateway: Processing charge...")
        
        # VALIDAÇÃO DO CARTÃO
        valid, message = self.validate_card(card_number, cvv, expiry)
        if not valid:
            return {"approved": False, "reason": message}
        
        if amount <= 0:
            return {"approved": False, "reason": "Invalid amount"}
        
        transaction_id = f"CC{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        result = {
            "approved": True,
            "transaction_id": transaction_id,
            "card_last4": card_number[-4:],
            "amount": amount,
            "authorization_code": f"AUTH{transaction_id[-6:]}",
            "timestamp": datetime.now().isoformat()
        }
        
        self.transactions.append(result)
        print(f"✅ Card charged: R$ {amount:.2f} (Card ending in {card_number[-4:]})")
        return result
    
    def refund_transaction(self, transaction_id: str) -> bool:
        print(f"🔄 Refunding transaction {transaction_id}")
        return True
    
    def get_statement(self) -> list:
        return self.transactions


class CryptoExchangeAPI:
    """API de exchange de criptomoedas"""
    
    def __init__(self):
        self.balances = {}  # Balances por usuário
        self.exchange_rates = {"BTC": 300000.00, "ETH": 15000.00}
        self.transactions = []
    
    def buy_crypto(self, crypto: str, amount_brl: float, user_id: str) -> Dict[str, any]:
        """Compra criptomoeda"""
        print(f"₿ Crypto API: Buying {crypto}...")
        
        if crypto not in self.exchange_rates:
            return {"success": False, "error": "Unsupported cryptocurrency"}
        
        crypto_amount = amount_brl / self.exchange_rates[crypto]
        
        # Inicializa balance do usuário se não existir
        if user_id not in self.balances:
            self.balances[user_id] = {"BTC": 0, "ETH": 0}
        
        result = {
            "success": True,
            "crypto": crypto,
            "crypto_amount": crypto_amount,
            "brl_amount": amount_brl,
            "rate": self.exchange_rates[crypto],
            "tx_hash": f"0x{datetime.now().strftime('%Y%m%d%H%M%S')}abcdef",
            "timestamp": datetime.now().isoformat()
        }
        
        self.balances[user_id][crypto] = self.balances[user_id].get(crypto, 0) + crypto_amount
        self.transactions.append(result)
        
        print(f"✅ Bought {crypto_amount:.8f} {crypto} for R$ {amount_brl:.2f}")
        return result
    
    def sell_crypto(self, crypto: str, crypto_amount: float, user_id: str) -> Dict[str, any]:
        """Vende criptomoeda"""
        print(f"₿ Crypto API: Selling {crypto}...")
        
        if user_id not in self.balances:
            return {"success": False, "error": "No crypto balance"}
        
        if self.balances[user_id].get(crypto, 0) < crypto_amount:
            return {"success": False, "error": "Insufficient crypto balance"}
        
        brl_amount = crypto_amount * self.exchange_rates[crypto]
        
        result = {
            "success": True,
            "crypto": crypto,
            "crypto_amount": crypto_amount,
            "brl_amount": brl_amount,
            "rate": self.exchange_rates[crypto],
            "tx_hash": f"0x{datetime.now().strftime('%Y%m%d%H%M%S')}fedcba",
            "timestamp": datetime.now().isoformat()
        }
        
        self.balances[user_id][crypto] -= crypto_amount
        self.transactions.append(result)
        
        print(f"✅ Sold {crypto_amount:.8f} {crypto} for R$ {brl_amount:.2f}")
        return result
    
    def get_balance(self, crypto: str, user_id: str) -> float:
        """Retorna saldo de uma criptomoeda"""
        if user_id not in self.balances:
            return 0
        return self.balances[user_id].get(crypto, 0)


class InternationalBankingAPI:
    """API de transferência bancária internacional (SWIFT)"""
    
    def __init__(self):
        self.transactions = []
        # Simula códigos SWIFT válidos
        self.valid_swift_codes = {
            "BOFAUS3N": "Bank of America",
            "CITIUS33": "Citibank",
            "CHASUS33": "JP Morgan Chase",
            "DEUTDEFF": "Deutsche Bank",
            "HSBCGB2L": "HSBC UK",
        }
    
    def validate_swift(self, swift_code: str) -> bool:
        """Valida código SWIFT (8 ou 11 caracteres)"""
        if swift_code in self.valid_swift_codes:
            return True
        # Aceita formato SWIFT básico
        return len(swift_code) in [8, 11] and swift_code[:4].isalpha()
    
    def send_international_transfer(self, amount: float, currency: str,
                                   swift_code: str, account_number: str,
                                   beneficiary_name: str) -> Dict[str, any]:
        """Envia transferência internacional"""
        print(f"🌍 SWIFT: Processing international transfer...")
        
        # VALIDAÇÃO SWIFT
        if not self.validate_swift(swift_code):
            return {
                "status": "failed",
                "error": f"Invalid SWIFT code: {swift_code}"
            }
        
        fee_percentage = 0.03  # 3% de taxa
        fee = amount * fee_percentage
        total = amount + fee
        
        bank_name = self.valid_swift_codes.get(swift_code, "International Bank")
        
        result = {
            "status": "processing",
            "reference": f"SWIFT{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "amount": amount,
            "currency": currency,
            "fee": fee,
            "total": total,
            "swift_code": swift_code,
            "bank_name": bank_name,
            "estimated_days": 3,
            "timestamp": datetime.now().isoformat()
        }
        
        self.transactions.append(result)
        
        print(f"✅ Transfer initiated: {amount:.2f} {currency} + {fee:.2f} fee")
        print(f"   Destination: {bank_name}")
        print(f"   Estimated arrival: 3 business days")
        return result
    
    def track_transfer(self, reference: str) -> Dict[str, any]:
        return {
            "reference": reference,
            "status": "completed",
            "current_location": "Destination bank"
        }


# ==================== ADAPTERS (CORRIGIDOS) ====================

class PixAdapter(PaymentProcessor):
    """Adapter PIX com dedução de saldo CORRIGIDA"""
    
    def __init__(self, pix_api: PixAPI, user: User, user_pix_key: str):
        self.pix_api = pix_api
        self.user = user
        self.pix_key = user_pix_key
        
        # Registra a chave do usuário no sistema PIX
        self.pix_api.register_key(user_pix_key, user.get_name(), "user")
    
    def process_payment(self, amount: float, description: str, 
                       destination: str = None) -> Dict[str, any]:
        """Processa pagamento PIX com dedução de saldo"""
        if not destination:
            return {
                "success": False,
                "transaction_id": None,
                "message": "PIX key required for destination"
            }
        
        # VERIFICA SALDO ANTES
        if self.user.get_balance() < amount:
            return {
                "success": False,
                "transaction_id": None,
                "message": f"Insufficient balance. Available: R$ {self.user.get_balance():.2f}"
            }
        
        # Processa no PIX
        result = self.pix_api.send_pix(amount, destination, description)
        
        # SE APROVADO, DEDUZ SALDO
        if result["status"] == "approved":
            self.user.set_balance(self.user.get_balance() - amount)
            print(f"💰 Balance deducted: R$ {amount:.2f}")
            print(f"   New balance: R$ {self.user.get_balance():.2f}")
        
        return {
            "success": result["status"] == "approved",
            "transaction_id": result.get("transaction_id"),
            "message": f"PIX payment successful to {result.get('recipient')}" 
                      if result["status"] == "approved" 
                      else result.get("error", "Payment failed"),
            "method": "PIX",
            "details": result
        }
    
    def check_balance(self) -> float:
        """PIX usa o saldo do usuário"""
        return self.user.get_balance()
    
    def get_transaction_history(self, limit: int = 10) -> list:
        pix_transactions = self.pix_api.list_transactions()
        # Filtra apenas transações deste usuário
        user_transactions = [t for t in pix_transactions if t.get("pix_key") == self.pix_key]
        return user_transactions[-limit:]


class CreditCardAdapter(PaymentProcessor):
    """Adapter de cartão com dedução de saldo CORRIGIDA"""
    
    def __init__(self, gateway: CreditCardGateway, user: User,
                 card_number: str, cvv: str, expiry: str, cardholder: str):
        self.gateway = gateway
        self.user = user
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry
        self.cardholder = cardholder
        self.merchant_id = "NORTH_FRONTIER_BANK"
        self.credit_limit = 10000.00  # Limite do cartão
        self.used_credit = 0.00
    
    def process_payment(self, amount: float, description: str, 
                       destination: str = None) -> Dict[str, any]:
        """Processa pagamento com cartão"""
        
        # Verifica limite do cartão
        available_credit = self.credit_limit - self.used_credit
        if amount > available_credit:
            return {
                "success": False,
                "transaction_id": None,
                "message": f"Credit limit exceeded. Available: R$ {available_credit:.2f}"
            }
        
        # Processa no gateway
        result = self.gateway.charge_card(
            self.card_number,
            self.cvv,
            self.expiry,
            amount,
            self.merchant_id
        )
        
        # Se aprovado, contabiliza crédito usado
        if result.get("approved"):
            self.used_credit += amount
            print(f"💳 Credit used: R$ {amount:.2f}")
            print(f"   Available credit: R$ {self.credit_limit - self.used_credit:.2f}")
        
        return {
            "success": result.get("approved", False),
            "transaction_id": result.get("transaction_id"),
            "message": "Card payment successful" if result.get("approved") 
                      else result.get("reason", "Payment failed"),
            "method": "Credit Card",
            "card_last4": result.get("card_last4"),
            "authorization": result.get("authorization_code"),
            "details": result
        }
    
    def check_balance(self) -> float:
        """Retorna crédito disponível"""
        return self.credit_limit - self.used_credit
    
    def get_transaction_history(self, limit: int = 10) -> list:
        statement = self.gateway.get_statement()
        return statement[-limit:]
    
    def pay_invoice(self, amount: float) -> bool:
        """Paga fatura do cartão usando saldo do usuário"""
        if self.user.get_balance() < amount:
            print(f"❌ Insufficient balance to pay invoice")
            return False
        
        self.user.set_balance(self.user.get_balance() - amount)
        self.used_credit -= amount
        print(f"✅ Invoice paid: R$ {amount:.2f}")
        return True


class CryptoAdapter(PaymentProcessor):
    """Adapter crypto com ID do usuário"""
    
    def __init__(self, crypto_api: CryptoExchangeAPI, user: User):
        self.crypto_api = crypto_api
        self.user = user
        self.user_id = user.get_name()  # Usa nome como ID único
    
    def process_payment(self, amount: float, description: str, 
                       destination: str = None) -> Dict[str, any]:
        """Compra crypto com saldo BRL"""
        
        crypto = destination if destination in ["BTC", "ETH"] else "BTC"
        
        # VERIFICA SALDO
        if self.user.get_balance() < amount:
            return {
                "success": False,
                "message": f"Insufficient balance. Available: R$ {self.user.get_balance():.2f}"
            }
        
        # Compra crypto
        result = self.crypto_api.buy_crypto(crypto, amount, self.user_id)
        
        # DEDUZ SALDO
        if result["success"]:
            self.user.set_balance(self.user.get_balance() - amount)
            print(f"💰 Balance deducted: R$ {amount:.2f}")
        
        return {
            "success": result["success"],
            "transaction_id": result.get("tx_hash"),
            "message": f"Bought {result.get('crypto_amount', 0):.8f} {crypto}" 
                      if result["success"] else result.get("error"),
            "method": "Cryptocurrency",
            "crypto": crypto,
            "crypto_amount": result.get("crypto_amount"),
            "details": result
        }
    
    def check_balance(self) -> float:
        """Retorna saldo BRL equivalente"""
        btc_balance = self.crypto_api.get_balance("BTC", self.user_id)
        eth_balance = self.crypto_api.get_balance("ETH", self.user_id)
        
        btc_brl = btc_balance * self.crypto_api.exchange_rates["BTC"]
        eth_brl = eth_balance * self.crypto_api.exchange_rates["ETH"]
        
        return btc_brl + eth_brl
    
    def get_transaction_history(self, limit: int = 10) -> list:
        return self.crypto_api.transactions[-limit:]
    
    def sell_crypto(self, crypto: str, amount: float) -> Dict[str, any]:
        """Vende crypto e adiciona BRL"""
        result = self.crypto_api.sell_crypto(crypto, amount, self.user_id)
        
        if result["success"]:
            self.user.set_balance(self.user.get_balance() + result["brl_amount"])
        
        return result


class InternationalBankAdapter(PaymentProcessor):
    """Adapter internacional com validação SWIFT"""
    
    def __init__(self, swift_api: InternationalBankingAPI, user: User):
        self.swift_api = swift_api
        self.user = user
    
    def process_payment(self, amount: float, description: str, 
                       destination: str = None) -> Dict[str, any]:
        
        if not destination:
            return {
                "success": False,
                "message": "SWIFT code and account required (format: SWIFT:ACCOUNT:NAME)"
            }
        
        try:
            swift_code, account, name = destination.split(":")
        except:
            return {
                "success": False,
                "message": "Invalid format. Use: SWIFTCODE:ACCOUNT:NAME"
            }
        
        # Envia transferência
        result = self.swift_api.send_international_transfer(
            amount, "BRL", swift_code, account, name
        )
        
        if result["status"] == "failed":
            return {
                "success": False,
                "message": result.get("error")
            }
        
        # DEDUZ SALDO (valor + taxa)
        total_cost = result["total"]
        if self.user.get_balance() >= total_cost:
            self.user.set_balance(self.user.get_balance() - total_cost)
            success = True
            message = f"Transfer initiated (ref: {result['reference']})"
            print(f"💰 Deducted: R$ {total_cost:.2f} (amount + fee)")
        else:
            success = False
            message = f"Insufficient balance. Need: R$ {total_cost:.2f}"
        
        return {
            "success": success,
            "transaction_id": result.get("reference"),
            "message": message,
            "method": "International Transfer (SWIFT)",
            "fee": result["fee"],
            "total": result["total"],
            "estimated_days": result["estimated_days"],
            "details": result
        }
    
    def check_balance(self) -> float:
        return self.user.get_balance()
    
    def get_transaction_history(self, limit: int = 10) -> list:
        return self.swift_api.transactions[-limit:]


# ==================== PAYMENT MANAGER ====================

class PaymentManager:
    """Gerenciador unificado de métodos de pagamento"""
    
    def __init__(self, user: User):
        self.user = user
        self.payment_methods: Dict[str, PaymentProcessor] = {}
    
    def add_payment_method(self, name: str, processor: PaymentProcessor):
        self.payment_methods[name] = processor
        print(f"✅ Payment method '{name}' added")
    
    def list_payment_methods(self) -> List[str]:
        return list(self.payment_methods.keys())
    
    def pay_with(self, method_name: str, amount: float, 
                description: str, destination: str = None) -> Dict[str, any]:
        
        if method_name not in self.payment_methods:
            return {
                "success": False,
                "message": f"Payment method '{method_name}' not found"
            }
        
        processor = self.payment_methods[method_name]
        result = processor.process_payment(amount, description, destination)
        
        return result
    
    def pay_bill_with_method(self, bill: Bill, method_name: str) -> bool:
        """Paga boleto usando método específico"""
        
        print(f"\n💳 Paying bill with {method_name}")
        print(f"Bill: {bill.get_description()}")
        print(f"Amount: R$ {bill.get_value():.2f}")
        
        # Para PIX, precisa de chave destino (simulada)
        destination = None
        if method_name == "PIX":
            destination = "merchant@bank.com"  # Chave do beneficiário
        
        result = self.pay_with(
            method_name,
            bill.get_value(),
            f"Bill payment: {bill.get_description()}",
            destination
        )
        
        if result["success"]:
            bill.set_paid(True)
            # Registra no histórico do usuário
            from models.history import History_bill
            history = History_bill(
                "Bill Payment via " + method_name,
                f"Paid {bill.get_description()} using {method_name}",
                bill.get_value(),
                bill.get_due_date()
            )
            self.user.add_history(history)
            
            print(f"✅ Bill paid successfully via {method_name}")
            print(f"   Transaction ID: {result.get('transaction_id')}")
            return True
        else:
            print(f"❌ Payment failed: {result.get('message')}")
            return False
    
    def get_all_balances(self) -> Dict[str, float]:
        balances = {}
        for name, processor in self.payment_methods.items():
            try:
                balances[name] = processor.check_balance()
            except:
                balances[name] = 0.0
        return balances
    
    def print_payment_summary(self):
        print("\n" + "="*50)
        print("💳 PAYMENT METHODS SUMMARY")
        print("="*50)
        
        methods = self.list_payment_methods()
        print(f"📋 Available methods: {len(methods)}")
        
        balances = self.get_all_balances()
        
        for method in methods:
            balance = balances.get(method, 0)
            if balance == float('inf'):
                balance_str = "Unlimited"
            else:
                balance_str = f"R$ {balance:.2f}"
            
            print(f"\n💳 {method}")
            print(f"   Balance/Credit: {balance_str}")
        
        print("="*50)
