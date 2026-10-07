import pytest

from app.input_validators import validate_number, validate_operation
from app.exceptions import InvalidInputError, InvalidOperationError


def test_validate_number():
    """Test that valid numeric input is converted to a float."""
    assert validate_number("10") == 10.0
    assert validate_number("5.5") == 5.5
    assert validate_number("-3") == -3.0


def test_validate_invalid_number():
    """Test that invalid input raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        validate_number("hello")


def test_validate_operation():
    """Test that valid operations are accepted."""
    assert validate_operation("add") == "add"
    assert validate_operation("subtract") == "subtract"
    assert validate_operation("multiply") == "multiply"
    assert validate_operation("divide") == "divide"
    assert validate_operation("power") == "power"
    assert validate_operation("root") == "root"


def test_validate_operation_case_insensitive():
    """Test that operation names are not case sensitive."""
    assert validate_operation("ADD") == "add"
    assert validate_operation("Multiply") == "multiply"


def test_validate_invalid_operation():
    """Test that an unsupported operation raises an error."""
    with pytest.raises(InvalidOperationError):
        validate_operation("banana")