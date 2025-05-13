"""
Main application module for Synapse Protocol
"""

import os
from flask import Flask
from flask_cors import CORS
from .api.routes import payment_bp
from .websocket import WebSocketManager
from .payments.core import PaymentProtocol
from .payments.xrp_bridge import XrpPaymentBridge

def create_app(test_config=None):
    """
    Create and configure the Flask application.
    
    Args:
        test_config: Test configuration dictionary
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
            API_KEY=os.environ.get('API_KEY'),
            ENVIRONMENT=os.environ.get('ENVIRONMENT', 'sandbox')
        )
    else:
        app.config.update(test_config)
        
    # Initialize CORS
    CORS(app)
    
    # Initialize payment protocol
    xrp_client = XrpPaymentBridge()  # Initialize with your XRP client configuration
    payment_protocol = PaymentProtocol(
        api_key=app.config['API_KEY'],
        environment=app.config['ENVIRONMENT'],
        xrp_client=xrp_client
    )
    
    # Initialize WebSocket manager
    websocket_manager = WebSocketManager(app)
    
    # Register blueprints
    app.register_blueprint(payment_bp)
    
    # Store instances in app context
    app.payment_protocol = payment_protocol
    app.websocket_manager = websocket_manager
    
    return app

def main():
    """Run the application."""
    app = create_app()
    app.websocket_manager.run(
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') == 'development'
    )

if __name__ == '__main__':
    main() 