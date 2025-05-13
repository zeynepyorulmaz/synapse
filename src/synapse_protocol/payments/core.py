"""
Core implementation of the A2A Payment Protocol
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from .types import PaymentRequest, PaymentResponse, PaymentStatus
from .exceptions import PaymentError, ValidationError

class PaymentProtocol:
    """Main class for handling A2A payment operations."""
    
    def __init__(self, api_key: str, environment: str = "sandbox", xrp_client: Optional[Any] = None):
        """
        Initialize the payment protocol.
        
        Args:
            api_key: API key for authentication
            environment: 'sandbox' or 'production'
            xrp_client: Optional XRP client instance for XRP payments
        """
        self.api_key = api_key
        self.environment = environment
        self._validate_environment()
        
        # Initialize XRP bridge if client is provided
        if xrp_client:
            from .xrp_bridge import XrpPaymentBridge
            self.xrp_bridge = XrpPaymentBridge(xrp_client)
        else:
            self.xrp_bridge = None
        
    def _validate_environment(self) -> None:
        """Validate the environment setting."""
        if self.environment not in ["sandbox", "production"]:
            raise ValidationError("Environment must be either 'sandbox' or 'production'")
            
    async def initiate_payment(
        self,
        payment_data: Dict[str, Any]
    ) -> PaymentResponse:
        """
        Initiate an A2A payment.
        
        Args:
            payment_data: Dictionary containing payment details
                - sender_account: Sender's account identifier
                - receiver_account: Receiver's account identifier
                - amount: Payment amount
                - currency: Payment currency (e.g., 'USD', 'EUR', 'XRP')
                - description: Optional payment description
                - metadata: Optional additional payment metadata
            
        Returns:
            PaymentResponse object containing payment details
        """
        # Validate input parameters
        if payment_data["amount"] <= 0:
            raise ValidationError("Amount must be greater than zero")
            
        # Create payment request
        payment_request = PaymentRequest(
            payment_id=str(uuid.uuid4()),
            sender_account=payment_data["sender_account"],
            receiver_account=payment_data["receiver_account"],
            amount=payment_data["amount"],
            currency=payment_data["currency"],
            description=payment_data.get("description"),
            metadata=payment_data.get("metadata"),
            status=PaymentStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        # Process payment based on currency
        if payment_data["currency"] == "XRP" and self.xrp_bridge:
            return await self.xrp_bridge.process_payment(payment_request)
        else:
            # TODO: Implement other payment methods
            raise PaymentError(f"Unsupported currency: {payment_data['currency']}")
        
    async def get_payment_status(self, payment_id: str) -> PaymentStatus:
        """
        Get the status of a payment.
        
        Args:
            payment_id: Unique identifier of the payment
            
        Returns:
            Current payment status
        """
        # TODO: Implement actual status checking logic
        return PaymentStatus.PENDING
        
    async def cancel_payment(self, payment_id: str) -> PaymentResponse:
        """
        Cancel a pending payment.
        
        Args:
            payment_id: Unique identifier of the payment
            
        Returns:
            PaymentResponse object with cancellation status
        """
        # TODO: Implement actual cancellation logic
        return PaymentResponse(
            payment_id=payment_id,
            status=PaymentStatus.CANCELLED,
            message="Payment cancelled successfully"
        )
        
    async def get_balance(self, account_id: str, currency: str = "XRP") -> float:
        """
        Get account balance.
        
        Args:
            account_id: Account identifier
            currency: Currency to check balance for
            
        Returns:
            Account balance
        """
        if currency == "XRP" and self.xrp_bridge:
            return await self.xrp_bridge.get_balance(account_id)
        else:
            raise PaymentError(f"Unsupported currency: {currency}")
            
    async def verify_transaction(self, tx_hash: str) -> bool:
        """
        Verify a transaction.
        
        Args:
            tx_hash: Transaction hash to verify
            
        Returns:
            True if transaction is valid and successful
        """
        if self.xrp_bridge:
            return await self.xrp_bridge.verify_transaction(tx_hash)
        else:
            raise PaymentError("XRP bridge not initialized") 