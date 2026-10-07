from app.exceptions import InvalidInputError, InvalidOperationError




def validate_number(value: str) -> float:
    """Validate that the user's input can be converted to a number."""

    try:
        return float(value)
    except ValueError as exc:
        raise InvalidInputError(
            f"Invalid number: {value}"
        ) from exc

VALID_OPERATIONS = {
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "root",
}


def validate_operation(operation: str) -> str:
    """Validate that the requested operation is supported."""

    operation = operation.lower()

    if operation not in VALID_OPERATIONS:
        raise InvalidOperationError(
            f"Invalid operation: {operation}"
        )

    return operation

