# core/observers.py
from abc import ABC, abstractmethod

class Observer(ABC):
    """Interface para observadores"""
    @abstractmethod
    def update(self, subject, event_type: str, data: dict):
        pass

class Subject:
    """Classe base para objetos observáveis"""
    def __init__(self):
        self._observers = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self, event_type: str, data: dict):
        for observer in self._observers:
            observer.update(self, event_type, data)

# Observadores concretos
class BillNotificationObserver(Observer):
    """Observador para notificações de boletos"""
    def update(self, subject, event_type: str, data: dict):
        if event_type == "BILL_OVERDUE":
            print(f"🔔 ALERT: Bill '{data['description']}' is overdue!")
            print(f"   Amount: R$ {data['amount']:.2f}")
        elif event_type == "BILL_PAID":
            print(f"✅ Bill '{data['description']}' paid successfully!")

class BalanceObserver(Observer):
    """Observador para mudanças de saldo"""
    def update(self, subject, event_type: str, data: dict):
        if event_type == "LOW_BALANCE":
            print(f"⚠️ WARNING: Low balance detected!")
            print(f"   Current balance: R$ {data['balance']:.2f}")
        elif event_type == "NEGATIVE_BALANCE":
            print(f"🚨 CRITICAL: Negative balance!")

class GoalProgressObserver(Observer):
    """Observador para progresso de metas"""
    def update(self, subject, event_type: str, data: dict):
        if event_type == "GOAL_PROGRESS":
            progress = (1 - data['remaining']/data['target']) * 100
            print(f"📊 Goal '{data['description']}' progress: {progress:.1f}%")
        elif event_type == "GOAL_ACHIEVED":
            print(f"🎉 Goal '{data['description']}' achieved!")
