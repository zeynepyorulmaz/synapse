"""
Multi-agent example for Synapse Protocol
"""

import asyncio
import os
from flask import Flask
from synapse_protocol import PaymentProtocol, WebSocketManager, AgentManager

async def main():
    # Initialize Flask app
    app = Flask(__name__)
    
    # Initialize payment protocol with test API key
    payment_protocol = PaymentProtocol(
        api_key="test_synapse_key_123",  # Test API key
        environment="sandbox"
    )
    
    # Initialize WebSocket manager
    websocket_manager = WebSocketManager(app)
    
    # Initialize agent manager with test API key
    agent_manager = AgentManager(
        api_key="test_openai_key_456",  # Test OpenAI API key
        environment="sandbox"
    )
    
    # Store instances in app context
    app.payment_protocol = payment_protocol
    app.websocket_manager = websocket_manager
    app.agent_manager = agent_manager
    
    try:
        # Create a payment request
        payment_data = {
            "sender_account": "test_sender_123",
            "receiver_account": "test_receiver_456",
            "amount": 1000.0,
            "currency": "XRP",
            "description": "Large payment for services"
        }
        
        # Create and execute risk assessment crew
        risk_crew = agent_manager.create_risk_assessment_crew()
        risk_assessment = agent_manager.execute_crew("risk_crew")
        print("Risk Assessment:", risk_assessment)
        
        # If risk assessment passes, create and execute payment crew
        if risk_assessment.get("risk_level", "high") != "high":
            payment_crew = agent_manager.create_payment_crew()
            payment_result = agent_manager.execute_crew("payment_crew")
            print("Payment Processing:", payment_result)
            
            # Create the payment
            payment = await payment_protocol.initiate_payment(payment_data)
            print(f"Payment created: {payment.id}")
            
            # Get payment status
            status = await payment_protocol.get_payment_status(payment.id)
            print(f"Payment status: {status.status}")
            
            # Get account balance
            balance = await payment_protocol.get_balance("test_sender_123")
            print(f"Account balance: {balance.amount} {balance.currency}")
        else:
            print("Payment rejected due to high risk level")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
    # Start WebSocket server
    websocket_manager.run(debug=True)

if __name__ == "__main__":
    asyncio.run(main()) 