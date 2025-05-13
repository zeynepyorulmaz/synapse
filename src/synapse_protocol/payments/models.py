"""
Data models for the A2A Payment Protocol
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass

class PaymentStatus(str, Enum):
    """Enumeration of possible payment statuses."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

@dataclass
class PaymentRequest:
    """Model for payment request data."""
    payment_id: str
    sender_account: str
    receiver_account: str
    amount: float
    currency: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: datetime = datetime.utcnow()
    
    def validate(self) -> None:
        """Validate the payment request data."""
        if not self.sender_account or not self.receiver_account:
            raise ValueError("Both sender and receiver accounts must be specified")
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero")
        if not self.currency or len(self.currency) != 3:
            raise ValueError("Currency must be a valid 3-letter code")

@dataclass
class PaymentResponse:
    """Model for payment response data."""
    payment_id: str
    status: PaymentStatus
    message: str
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None
    
    @property
    def is_successful(self) -> bool:
        """Check if the payment was successful."""
        return self.status in [PaymentStatus.COMPLETED, PaymentStatus.REFUNDED]
        
    @property
    def is_failed(self) -> bool:
        """Check if the payment failed."""
        return self.status in [PaymentStatus.FAILED, PaymentStatus.CANCELLED]

@dataclass
class AccountBalance:
    """Model for account balance information."""
    account_id: str
    currency: str
    available_balance: float
    pending_balance: float
    last_updated: datetime = datetime.utcnow()
    
    @property
    def total_balance(self) -> float:
        """Calculate total balance including pending transactions."""
        return self.available_balance + self.pending_balance 