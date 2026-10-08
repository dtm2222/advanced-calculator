import os

from dotenv import load_dotenv

from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manage calculator configuration settings."""

    def __init__(self):
        load_dotenv()

        self.history_file = os.getenv(
            "CALCULATOR_HISTORY_FILE",
            "history.csv"
        )

        self.auto_save = os.getenv(
            "CALCULATOR_AUTO_SAVE",
            "true"
        ).lower() == "true"

        self.precision = self._get_precision()

    def _get_precision(self) -> int:
        """Get and validate calculator precision."""

        try:
            precision = int(
                os.getenv("CALCULATOR_PRECISION", "2")
            )
        except ValueError as exc:
            raise ConfigurationError(
                "CALCULATOR_PRECISION must be an integer."
            ) from exc

        if precision < 0:
            raise ConfigurationError(
                "CALCULATOR_PRECISION cannot be negative."
            )

        return precision