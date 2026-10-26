import pytest

from app.operations import (
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    OperationFactory,
)


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        (Addition(), 5, 3, 8),
        (Subtraction(), 5, 3, 2),
        (Multiplication(), 5, 3, 15),
        (Division(), 6, 3, 2),
        (Power(), 2, 3, 8),
        (Root(), 9, 2, 3),
    ],
)
def test_operations(operation, a, b, expected):
    assert operation.execute(a, b) == pytest.approx(expected)


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        Division().execute(10, 0)


@pytest.mark.parametrize(
    "a,b",
    [
        (9, 0),
        (-9, 2),
    ],
)
def test_invalid_roots(a, b):
    with pytest.raises(ValueError):
        Root().execute(a, b)


@pytest.mark.parametrize(
    "name,expected_class",
    [
        ("add", Addition),
        ("subtract", Subtraction),
        ("multiply", Multiplication),
        ("divide", Division),
        ("power", Power),
        ("root", Root),
    ],
)
def test_operation_factory(name, expected_class):
    operation = OperationFactory.create_operation(name)

    assert isinstance(operation, expected_class)


def test_operation_factory_invalid():
    with pytest.raises(ValueError):
        OperationFactory.create_operation("invalid")


@pytest.mark.parametrize(
    "operation_name, a, b, expected",
    [
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 25, 100, 25),
        ("abs_diff", 5, 10, 5),
        ("abs_diff", 10, 5, 5),
    ],
)
def test_new_operations(operation_name, a, b, expected):
    operation = OperationFactory.create_operation(operation_name)
    assert operation.execute(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "operation_name",
    ["modulus", "int_divide", "percent"],
)
def test_new_operations_division_by_zero(operation_name):
    operation = OperationFactory.create_operation(operation_name)

    with pytest.raises(ZeroDivisionError):
        operation.execute(10, 0)