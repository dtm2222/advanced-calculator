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

class Modulus(Operation):
    """Calculate the remainder of division."""

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a % b


class IntegerDivision(Operation):
    """Calculate the integer quotient."""

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a // b


class Percentage(Operation):
    """Calculate a as a percentage of b."""

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot calculate percentage with zero denominator.")
        return (a / b) * 100


class AbsoluteDifference(Operation):
    """Calculate the absolute difference between two numbers."""

    def execute(self, a: float, b: float) -> float:
        return abs(a - b)


class OperationFactory:
    """Factory for creating calculator operation objects."""

    _operations = {
    "add": Addition,
    "subtract": Subtraction,
    "multiply": Multiplication,
    "divide": Division,
    "power": Power,
    "root": Root,
    "modulus": Modulus,
    "int_divide": IntegerDivision,
    "percent": Percentage,
    "abs_diff": AbsoluteDifference,
}

    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        """Create and return the requested operation."""

        operation_class = cls._operations.get(operation_name.lower())

        if operation_class is None:
            raise ValueError(f"Unknown operation: {operation_name}")

        return operation_class()