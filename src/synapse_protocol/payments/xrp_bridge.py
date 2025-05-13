"""
Bridge module to connect XRP implementation with A2A payment protocol
"""

import json
from typing import Dict, Any, Optional
from datetime import datetime
from .core import PaymentProtocol
from .models import PaymentRequest, PaymentResponse, PaymentStatus
from .exceptions import PaymentError, ValidationError

class XrpPaymentBridge:
    """Bridge class to handle XRP payments within the A2A protocol."""
    
    def __init__(self, xrp_client: Any):
        """
        Initialize the XRP bridge.
        
        Args:
            xrp_client: Instance of the XRP client from the frontend
        """
        self.xrp_client = xrp_client
        
    async def process_payment(
        self,
        payment_request: PaymentRequest
    ) -> PaymentResponse:
        """
        Process a payment using XRP.
        
        Args:
            payment_request: Payment request to process
            
        Returns:
            PaymentResponse with the result
        """
        try:
            # Convert A2A payment request to XRP transaction request
            xrp_request = {
                "fromAgentId": payment_request.sender_account,
                "toAgentId": payment_request.receiver_account,
                "amount": payment_request.amount,
                "currency": "XRP",
                "memo": payment_request.description
            }
            
            # Execute the XRP transaction
            xrp_response = await self.xrp_client.sendPayment(xrp_request)
            
            # Convert XRP response to A2A payment response
            return PaymentResponse(
                payment_id=payment_request.payment_id,
                status=PaymentStatus.COMPLETED if xrp_response["success"] else PaymentStatus.FAILED,
                message="XRP payment processed successfully" if xrp_response["success"] else "XRP payment failed",
                error_code=None if xrp_response["success"] else "XRP_ERROR",
                error_message=None if xrp_response["success"] else xrp_response.get("error", "Unknown error"),
                completed_at=datetime.utcnow() if xrp_response["success"] else None
            )
            
        except Exception as e:
            return PaymentResponse(
                payment_id=payment_request.payment_id,
                status=PaymentStatus.FAILED,
                message="Error processing XRP payment",
                error_code="XRP_BRIDGE_ERROR",
                error_message=str(e),
                completed_at=None
            )
            
    async def get_balance(self, account_id: str) -> float:
        """
        Get XRP balance for an account.
        
        Args:
            account_id: Account identifier
            
        Returns:
            Account balance in XRP
        """
        try:
            return await self.xrp_client.getBalance(account_id)
        except Exception as e:
            raise PaymentError(f"Failed to get XRP balance: {str(e)}")
            
    async def verify_transaction(self, tx_hash: str) -> bool:
        """
        Verify an XRP transaction.
        
        Args:
            tx_hash: Transaction hash to verify
            
        Returns:
            True if transaction is valid and successful
        """
        try:
            return await self.xrp_client.verifyTransaction(tx_hash)
        except Exception as e:
            raise PaymentError(f"Failed to verify XRP transaction: {str(e)}") 