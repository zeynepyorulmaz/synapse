"""
Basic usage example for Synapse Protocol with real XRP client
"""

import asyncio
import os
from flask import Flask
from synapse_protocol import PaymentProtocol, WebSocketManager
from xrp_client import XrpClient

async def main():
    # Initialize Flask app
    app = Flask(__name__)
    
    # Initialize real XRP client (using testnet)
    xrp_client = XrpClient(testnet=True)
    
    # Create test wallets
    print("Creating test wallets...")
    sender_wallet = XrpClient.create_test_wallet()
    receiver_wallet = XrpClient.create_test_wallet()
    
    print(f"Sender wallet: {sender_wallet['address']}")
    print(f"Receiver wallet: {receiver_wallet['address']}")
    
    # Initialize payment protocol with test API key and real XRP client
    payment_protocol = PaymentProtocol(
        api_key="test_synapse_key_123",  # Test API key
        environment="sandbox",
        xrp_client=xrp_client
    )
    
    # Initialize WebSocket manager
    websocket_manager = WebSocketManager(app)
    
    # Store instances in app context
    app.payment_protocol = payment_protocol
    app.websocket_manager = websocket_manager
    
    try:
        # Create a payment
        payment = await payment_protocol.initiate_payment({
            "sender_account": sender_wallet["address"],
            "receiver_account": receiver_wallet["address"],
            "amount": 10.0,  # 10 XRP
            "currency": "XRP",
            "description": "Test payment using real XRP client"
        })
        print(f"Payment created: {payment.payment_id}")
        print(f"Payment status: {payment.status}")
        print(f"Payment message: {payment.message}")
        
        # Get payment status
        status = await payment_protocol.get_payment_status(payment.payment_id)
        print(f"Payment status: {status}")
        
        # Get account balance
        balance = await payment_protocol.get_balance(sender_wallet["address"])
        print(f"Sender account balance: {balance} XRP")
        
        # Get receiver balance
        receiver_balance = await payment_protocol.get_balance(receiver_wallet["address"])
        print(f"Receiver account balance: {receiver_balance} XRP")
        
        # Verify transaction (if available)
        if hasattr(payment, 'transaction_hash'):
            result = await payment_protocol.verify_transaction(payment.transaction_hash)
            print(f"Transaction verification: {result}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
    # Start WebSocket server on a different port
    try:
        websocket_manager.run(debug=True, port=5001)
    except OSError as e:
        if "Address already in use" in str(e):
            print("Port 5001 is in use, trying port 5002...")
            websocket_manager.run(debug=True, port=5002)
        else:
            raise

if __name__ == "__main__":
    asyncio.run(main()) 