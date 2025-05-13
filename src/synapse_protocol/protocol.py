"""
Core protocol implementation for Synapse Protocol.
"""

import asyncio
import json
import websockets
from typing import Dict, Any, Optional

class SynapseProtocol:
    """Main protocol class for handling blockchain interactions."""
    
    def __init__(self, websocket_url: str = "ws://localhost:8765"):
        """Initialize the protocol with a WebSocket connection URL."""
        self.websocket_url = websocket_url
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        
    async def connect(self) -> None:
        """Establish WebSocket connection."""
        self.websocket = await websockets.connect(self.websocket_url)
        
    async def disconnect(self) -> None:
        """Close the WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            
    async def send_message(self, message: Dict[str, Any]) -> None:
        """Send a message through the WebSocket connection."""
        if not self.websocket:
            raise ConnectionError("Not connected to WebSocket server")
        await self.websocket.send(json.dumps(message))
        
    async def receive_message(self) -> Dict[str, Any]:
        """Receive a message from the WebSocket connection."""
        if not self.websocket:
            raise ConnectionError("Not connected to WebSocket server")
        message = await self.websocket.recv()
        return json.loads(message) 