# Synapse Protocol

A powerful framework for A2A (Account-to-Account) Payment Protocol with XRP Integration, featuring real-time WebSocket updates and AI-powered payment processing.

## Installation

You can install the package using pip:

```bash
pip install synapse-protocol
```

For development installation with additional tools:

```bash
pip install synapse-protocol[dev]
```

## Quick Start

```python
from synapse_protocol import PaymentProtocol, WebSocketManager, AgentManager
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Initialize payment protocol
payment_protocol = PaymentProtocol(
    api_key="your_api_key",
    environment="sandbox"  # or "production"
)

# Initialize WebSocket manager
websocket_manager = WebSocketManager(app)

# Initialize agent manager
agent_manager = AgentManager(
    api_key="your_openai_api_key",
    environment="sandbox"
)

# Store instances in app context
app.payment_protocol = payment_protocol
app.websocket_manager = websocket_manager
app.agent_manager = agent_manager

# Create a payment with AI agents
payment_data = {
    "sender_account": "sender123",
    "receiver_account": "receiver456",
    "amount": 100.0,
    "currency": "XRP",
    "description": "Payment for services"
}

# Create and execute risk assessment crew
risk_crew = agent_manager.create_risk_assessment_crew()
risk_assessment = agent_manager.execute_crew("risk_crew")

# If risk assessment passes, process payment
if risk_assessment.get("risk_level", "high") != "high":
    payment_crew = agent_manager.create_payment_crew()
    payment_result = agent_manager.execute_crew("payment_crew")
    
    # Create the payment
    payment = await payment_protocol.initiate_payment(payment_data)
```

## Multi-Agent System

The Synapse Protocol includes a powerful multi-agent system powered by CrewAI:

### Available Agents

1. **Payment Validator**
   - Validates payment requests
   - Ensures compliance with requirements
   - Performs initial risk assessment

2. **Payment Processor**
   - Handles payment execution
   - Manages transaction flow
   - Ensures successful completion

3. **Payment Auditor**
   - Audits completed payments
   - Verifies compliance
   - Generates audit reports

4. **Risk Analyzer**
   - Analyzes payment risks
   - Provides risk assessment
   - Detects potential fraud

5. **Compliance Checker**
   - Verifies regulatory compliance
   - Checks policy adherence
   - Ensures legal requirements

### Creating Custom Agents

```python
# Create a custom agent
custom_agent = agent_manager.create_agent(
    name="custom_agent",
    role="Custom Role",
    goal="Custom Goal",
    backstory="Custom Backstory"
)

# Create a task for the agent
task = agent_manager.create_task(
    description="Task description",
    agent_name="custom_agent",
    expected_output="Expected output format"
)

# Create a crew with the agent
crew = agent_manager.create_crew(
    name="custom_crew",
    agent_names=["custom_agent"],
    tasks=[task]
)

# Execute the crew
result = agent_manager.execute_crew("custom_crew")
```

## WebSocket Integration

```javascript
// Client-side JavaScript
const socket = io('http://your-server:5000');

// Connect to WebSocket
socket.on('connect', () => {
    console.log('Connected to WebSocket server');
});

// Join payment room
socket.emit('join_room', { room: 'payment_123' });

// Listen for payment updates
socket.on('payment_update', (data) => {
    console.log('Payment update:', data);
});

// Listen for balance updates
socket.on('balance_update', (data) => {
    console.log('Balance update:', data);
});

// Listen for errors
socket.on('error', (data) => {
    console.error('Error:', data);
});
```

## Features

- A2A Payment Protocol implementation
- XRP integration
- Real-time WebSocket updates
- AI-powered payment processing with CrewAI
- Multi-agent system for payment handling
- Risk assessment and compliance checking
- Comprehensive error handling
- RESTful API endpoints
- WebSocket support for real-time updates
- Payment validation and verification
- Balance checking
- Transaction verification

## Documentation

For detailed documentation, visit [https://synapseprotocol.com/docs](https://synapseprotocol.com/docs)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 