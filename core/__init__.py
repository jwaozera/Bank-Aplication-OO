# package initialization file for core

# import dos pattern estruturais para facilitar o uso
from core.decorators import (
    UserDecorator,
    PremiumAccountDecorator,
    InsuranceDecorator,
    NotificationDecorator,
    StudentAccountDecorator,
    VIPDecorator,
    decorate_user
)

from core.adapters import (
    PaymentProcessor,
    PixAdapter,
    CreditCardAdapter,
    CryptoAdapter,
    InternationalBankAdapter,
    PaymentManager,
    # APIs externas
    PixAPI,
    CreditCardGateway,
    CryptoExchangeAPI,
    InternationalBankingAPI
)

__all__ = [
    # Decorators
    'UserDecorator',
    'PremiumAccountDecorator',
    'InsuranceDecorator',
    'NotificationDecorator',
    'StudentAccountDecorator',
    'VIPDecorator',
    'decorate_user',
    # Facades
    'BankingFacade',
    'InvestmentFacade',
    'ReportFacade',
    'get_facades',
    # Adapters
    'PaymentProcessor',
    'PixAdapter',
    'CreditCardAdapter',
    'CryptoAdapter',
    'InternationalBankAdapter',
    'PaymentManager',
    # External APIs
    'PixAPI',
    'CreditCardGateway',
    'CryptoExchangeAPI',
    'InternationalBankingAPI'
]
