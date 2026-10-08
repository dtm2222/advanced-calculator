import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_default_config(monkeypatch):
    """Test the default calculator configuration."""

    monkeypatch.delenv("CALCULATOR_HISTORY_FILE", raising=False)
    monkeypatch.delenv("CALCULATOR_AUTO_SAVE", raising=False)
    monkeypatch.delenv("CALCULATOR_PRECISION", raising=False)

    config = CalculatorConfig()

    assert config.history_file == "history.csv"
    assert config.auto_save is True
    assert config.precision == 2


def test_custom_config(monkeypatch):
    """Test configuration using environment variables."""

    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", "my_history.csv")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "4")

    config = CalculatorConfig()

    assert config.history_file == "my_history.csv"
    assert config.auto_save is False
    assert config.precision == 4


def test_invalid_precision(monkeypatch):
    """Test that non-numeric precision raises an error."""

    monkeypatch.setenv("CALCULATOR_PRECISION", "hello")

    with pytest.raises(ConfigurationError):
        CalculatorConfig()


def test_negative_precision(monkeypatch):
    """Test that negative precision raises an error."""

    monkeypatch.setenv("CALCULATOR_PRECISION", "-2")

    with pytest.raises(ConfigurationError):
        CalculatorConfig()