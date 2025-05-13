"""
Shared types for the payment protocol
"""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class PaymentRequest:
    def __init__(
        self,
        payment_id: str,
        sender_account: str,
        receiver_account: str,
        amount: float,
        currency: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        status: PaymentStatus = PaymentStatus.PENDING,
        created_at: Optional[datetime] = None
    ):
        self.payment_id = payment_id
        self.sender_account = sender_account
        self.receiver_account = receiver_account
        self.amount = amount
        self.currency = currency
        self.description = description
        self.metadata = metadata or {}
        self.status = status
        self.created_at = created_at or datetime.utcnow()

class PaymentResponse:
    def __init__(
        self,
        payment_id: str,
        status: PaymentStatus,
        message: Optional[str] = None,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
        completed_at: Optional[datetime] = None
    ):
        self.payment_id = payment_id
        self.status = status
        self.message = message
        self.error_code = error_code
        self.error_message = error_message
        self.completed_at = completed_at 