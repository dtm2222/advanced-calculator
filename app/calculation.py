from dataclasses import dataclass
from app.operations import Operation


@dataclass
class Calculation:
    """Represents a single calculator calculation."""

    a: float
    b: float
    operation: Operation

    def execute(self) -> float:
        """Execute the calculation using the selected operation."""
        return self.operation.execute(self.a, self.b)