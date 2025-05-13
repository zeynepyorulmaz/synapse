"""
Synapse Protocol - A2A Payment Protocol with XRP Integration
"""

from .payments.core import PaymentProtocol
from .websocket import WebSocketManager
from .agents.agent_manager import AgentManager

__version__ = "0.1.0"

__all__ = [
    'PaymentProtocol',
    'WebSocketManager',
    'AgentManager'
] 