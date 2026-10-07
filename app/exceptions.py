class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class InvalidInputError(CalculatorError):
    """Raised when the user enters invalid input."""
    pass


class InvalidOperationError(CalculatorError):
    """Raised when the user enters an unsupported operation."""
    pass