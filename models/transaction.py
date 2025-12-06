"""
Transaction model
"""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    """Represents a single currency conversion transaction"""
    from_currency: str
    to_currency: str
    amount: float
    result: float
    rate: float
    timestamp: datetime

    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            "from_currency": self.from_currency,
            "to_currency": self.to_currency,
            "amount": self.amount,
            "result": self.result,
            "rate": self.rate,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        """Create from dictionary"""
        return cls(
            from_currency=data["from_currency"],
            to_currency=data["to_currency"],
            amount=data["amount"],
            result=data["result"],
            rate=data["rate"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
