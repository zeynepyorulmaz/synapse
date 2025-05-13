"""
Custom exceptions for the A2A Payment Protocol
"""

class PaymentError(Exception):
    """Base exception for payment-related errors."""
    pass

class ValidationError(PaymentError):
    """Raised when payment validation fails."""
    pass

class AuthenticationError(PaymentError):
    """Raised when authentication fails."""
    pass

class InsufficientFundsError(PaymentError):
    """Raised when there are insufficient funds for a payment."""
    pass

class AccountNotFoundError(PaymentError):
    """Raised when an account is not found."""
    pass

class PaymentNotFoundError(PaymentError):
    """Raised when a payment is not found."""
    pass

class PaymentProcessingError(PaymentError):
    """Raised when there's an error processing a payment."""
    pass

class PaymentCancellationError(PaymentError):
    """Raised when there's an error cancelling a payment."""
    pass

class RateLimitError(PaymentError):
    """Raised when API rate limits are exceeded."""
    pass

class NetworkError(PaymentError):
    """Raised when there's a network-related error."""
    pass 