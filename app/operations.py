from abc import ABC, abstractmethod
import math


class Operation(ABC):
    """Abstract base class for calculator operations."""

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Perform the operation using two numbers."""
        pass  # pragma: no cover


class Addition(Operation):
    """Strategy for addition."""

    def execute(self, a: float, b: float) -> float:
        return a + b


class Subtraction(Operation):
    """Strategy for subtraction."""

    def execute(self, a: float, b: float) -> float:
        return a - b


class Multiplication(Operation):
    """Strategy for multiplication."""

    def execute(self, a: float, b: float) -> float:
        return a * b


class Division(Operation):
    """Strategy for division."""

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b


class Power(Operation):
    """Strategy for exponentiation."""

    def execute(self, a: float, b: float) -> float:
        return a ** b


class Root(Operation):
    """Strategy for calculating the nth root."""

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Root degree cannot be zero.")
        if a < 0:
            raise ValueError("Cannot calculate the root of a negative number.")
        return math.pow(a, 1 / b)


class OperationFactory:
    """Factory for creating calculator operation objects."""

    _operations = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,
    }

    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        """Create and return the requested operation."""

        operation_class = cls._operations.get(operation_name.lower())

        if operation_class is None:
            raise ValueError(f"Unknown operation: {operation_name}")

        return operation_class()