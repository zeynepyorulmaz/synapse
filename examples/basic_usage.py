"""
Basic usage example for Synapse Protocol
"""

import asyncio
import os
from flask import Flask
from synapse_protocol import PaymentProtocol, WebSocketManager

async def main():
    # Initialize Flask app
    app = Flask(__name__)
    
    # Initialize payment protocol
    payment_protocol = PaymentProtocol(
        api_key=os.getenv("SYNAPSE_API_KEY", "your_api_key"),
        environment="sandbox"
    )
    
    # Initialize WebSocket manager
    websocket_manager = WebSocketManager(app)
    
    # Store instances in app context
    app.payment_protocol = payment_protocol
    app.websocket_manager = websocket_manager
    
    try:
        # Create a payment
        payment = await payment_protocol.initiate_payment({
            "sender_account": "sender123",
            "receiver_account": "receiver456",
            "amount": 100.0,
            "currency": "XRP",
            "description": "Test payment"
        })
        print(f"Payment created: {payment.id}")
        
        # Get payment status
        status = await payment_protocol.get_payment_status(payment.id)
        print(f"Payment status: {status.status}")
        
        # Get account balance
        balance = await payment_protocol.get_balance("sender123")
        print(f"Account balance: {balance.amount} {balance.currency}")
        
        # Verify transaction (if available)
        if payment.transaction_hash:
            result = await payment_protocol.verify_transaction(payment.transaction_hash)
            print(f"Transaction verification: {result.is_valid}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
    # Start WebSocket server
    websocket_manager.run(debug=True)

if __name__ == "__main__":
    asyncio.run(main()) 