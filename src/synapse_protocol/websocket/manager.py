"""
WebSocket manager for handling server initialization and configuration
"""

from typing import Optional
from flask import Flask
from flask_socketio import SocketIO
from .handler import WebSocketHandler

class WebSocketManager:
    """Manages WebSocket server initialization and configuration."""
    
    def __init__(self, app: Flask, cors_allowed_origins: Optional[list] = None):
        """
        Initialize the WebSocket manager.
        
        Args:
            app: Flask application instance
            cors_allowed_origins: List of allowed CORS origins
        """
        self.app = app
        self.cors_allowed_origins = cors_allowed_origins or ['*']
        self.socketio = self._initialize_socketio()
        self.handler = WebSocketHandler(self.socketio)
        
    def _initialize_socketio(self) -> SocketIO:
        """
        Initialize SocketIO instance.
        
        Returns:
            SocketIO instance
        """
        return SocketIO(
            self.app,
            cors_allowed_origins=self.cors_allowed_origins,
            async_mode='eventlet',
            logger=True,
            engineio_logger=True
        )
        
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False) -> None:
        """
        Run the WebSocket server.
        
        Args:
            host: Host to bind to
            port: Port to bind to
            debug: Whether to run in debug mode
        """
        self.socketio.run(
            self.app,
            host=host,
            port=port,
            debug=debug,
            use_reloader=False
        )
        
    def emit_payment_update(self, payment_id: str, status: str, data: Optional[dict] = None) -> None:
        """
        Emit payment status update.
        
        Args:
            payment_id: Payment identifier
            status: New payment status
            data: Additional payment data
        """
        self.handler.emit_payment_update(payment_id, status, data)
        
    def emit_balance_update(self, account_id: str, balance: float, currency: str) -> None:
        """
        Emit balance update.
        
        Args:
            account_id: Account identifier
            balance: New balance
            currency: Currency
        """
        self.handler.emit_balance_update(account_id, balance, currency)
        
    def emit_error(self, error_type: str, message: str, data: Optional[dict] = None) -> None:
        """
        Emit error message.
        
        Args:
            error_type: Type of error
            message: Error message
            data: Additional error data
        """
        self.handler.emit_error(error_type, message, data) 