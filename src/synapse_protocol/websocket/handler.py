"""
WebSocket handler for real-time updates
"""

from typing import Dict, Any, Optional
from flask_socketio import SocketIO, emit, join_room, leave_room
from ..payments import PaymentStatus

class WebSocketHandler:
    """Handles WebSocket connections and real-time updates."""
    
    def __init__(self, socketio: SocketIO):
        """
        Initialize the WebSocket handler.
        
        Args:
            socketio: Flask-SocketIO instance
        """
        self.socketio = socketio
        self.setup_handlers()
        
    def setup_handlers(self) -> None:
        """Set up WebSocket event handlers."""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection."""
            emit('connection_response', {'data': 'Connected'})
            
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection."""
            pass
            
        @self.socketio.on('join_room')
        def handle_join_room(data: Dict[str, Any]):
            """Handle room joining."""
            room = data.get('room')
            if room:
                join_room(room)
                emit('room_joined', {'room': room}, room=room)
                
        @self.socketio.on('leave_room')
        def handle_leave_room(data: Dict[str, Any]):
            """Handle room leaving."""
            room = data.get('room')
            if room:
                leave_room(room)
                emit('room_left', {'room': room}, room=room)
                
    def emit_payment_update(self, payment_id: str, status: PaymentStatus, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Emit payment status update.
        
        Args:
            payment_id: Payment identifier
            status: New payment status
            data: Additional payment data
        """
        self.socketio.emit(
            'payment_update',
            {
                'payment_id': payment_id,
                'status': status,
                'data': data or {}
            },
            room=f'payment_{payment_id}'
        )
        
    def emit_balance_update(self, account_id: str, balance: float, currency: str) -> None:
        """
        Emit balance update.
        
        Args:
            account_id: Account identifier
            balance: New balance
            currency: Currency
        """
        self.socketio.emit(
            'balance_update',
            {
                'account_id': account_id,
                'balance': balance,
                'currency': currency
            },
            room=f'account_{account_id}'
        )
        
    def emit_error(self, error_type: str, message: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Emit error message.
        
        Args:
            error_type: Type of error
            message: Error message
            data: Additional error data
        """
        self.socketio.emit(
            'error',
            {
                'type': error_type,
                'message': message,
                'data': data or {}
            }
        ) 