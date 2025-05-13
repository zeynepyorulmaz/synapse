"""
API routes for payment operations
"""

from flask import Blueprint, request, jsonify, current_app
from ..payments.core import PaymentProtocol
from ..payments.exceptions import PaymentError, ValidationError

payment_bp = Blueprint('payments', __name__, url_prefix='/api/v1/payments')

@payment_bp.route('/create', methods=['POST'])
async def create_payment():
    """Create a new payment."""
    try:
        data = request.get_json()
        payment = await current_app.payment_protocol.initiate_payment(data)
        
        # Emit payment update
        current_app.websocket_manager.emit_payment_update(
            payment.id,
            payment.status,
            payment.to_dict()
        )
        
        return jsonify(payment.to_dict()), 201
    except ValidationError as e:
        current_app.websocket_manager.emit_error('validation_error', str(e))
        return jsonify({'error': str(e)}), 400
    except PaymentError as e:
        current_app.websocket_manager.emit_error('payment_error', str(e))
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.websocket_manager.emit_error('server_error', str(e))
        return jsonify({'error': 'Internal server error'}), 500

@payment_bp.route('/<payment_id>/status', methods=['GET'])
async def get_payment_status(payment_id):
    """Get payment status."""
    try:
        status = await current_app.payment_protocol.get_payment_status(payment_id)
        
        # Emit payment update
        current_app.websocket_manager.emit_payment_update(
            payment_id,
            status.status,
            status.to_dict()
        )
        
        return jsonify(status.to_dict())
    except PaymentError as e:
        current_app.websocket_manager.emit_error('payment_error', str(e))
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.websocket_manager.emit_error('server_error', str(e))
        return jsonify({'error': 'Internal server error'}), 500

@payment_bp.route('/<payment_id>/cancel', methods=['POST'])
async def cancel_payment(payment_id):
    """Cancel a payment."""
    try:
        result = await current_app.payment_protocol.cancel_payment(payment_id)
        
        # Emit payment update
        current_app.websocket_manager.emit_payment_update(
            payment_id,
            'CANCELLED',
            result.to_dict()
        )
        
        return jsonify(result.to_dict())
    except PaymentError as e:
        current_app.websocket_manager.emit_error('payment_error', str(e))
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.websocket_manager.emit_error('server_error', str(e))
        return jsonify({'error': 'Internal server error'}), 500

@payment_bp.route('/balance/<account_id>', methods=['GET'])
async def get_balance(account_id):
    """Get account balance."""
    try:
        balance = await current_app.payment_protocol.get_balance(account_id)
        
        # Emit balance update
        current_app.websocket_manager.emit_balance_update(
            account_id,
            balance.amount,
            balance.currency
        )
        
        return jsonify(balance.to_dict())
    except PaymentError as e:
        current_app.websocket_manager.emit_error('payment_error', str(e))
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.websocket_manager.emit_error('server_error', str(e))
        return jsonify({'error': 'Internal server error'}), 500

@payment_bp.route('/verify/<transaction_hash>', methods=['GET'])
async def verify_transaction(transaction_hash):
    """Verify a transaction."""
    try:
        result = await current_app.payment_protocol.verify_transaction(transaction_hash)
        return jsonify(result.to_dict())
    except PaymentError as e:
        current_app.websocket_manager.emit_error('payment_error', str(e))
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.websocket_manager.emit_error('server_error', str(e))
        return jsonify({'error': 'Internal server error'}), 500 