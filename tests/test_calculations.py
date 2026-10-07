import pytest

from app.calculation import Calculation
from app.operations import (
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
)


@pytest.mark.parametrize(
    "a,b,operation,expected",
    [
        (10, 5, Addition(), 15),
        (10, 5, Subtraction(), 5),
        (10, 5, Multiplication(), 50),
        (10, 5, Division(), 2),
        (2, 3, Power(), 8),
        (16, 2, Root(), 4),
    ],
)
def test_calculation_execute(a, b, operation, expected):
    calculation = Calculation(a, b, operation)

    assert calculation.execute() == pytest.approx(expected)