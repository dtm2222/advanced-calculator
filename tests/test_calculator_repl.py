import builtins
from app.history import LoggingObserver
from app.calculator_repl import Calculator, run_repl


def setup_calculator(monkeypatch, tmp_path):
    """Configure calculator tests to use a temporary history file."""

    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        str(tmp_path / "history.csv")
    )

    return Calculator()


def test_calculator_addition(monkeypatch, tmp_path):
    """Test performing a calculation through the facade."""

    calculator = setup_calculator(monkeypatch, tmp_path)

    result = calculator.calculate("add", "10", "5")

    assert result == 15
    assert len(calculator.history.data) == 1


def test_calculator_undo_redo(monkeypatch, tmp_path):
    """Test undo and redo through the facade."""

    calculator = setup_calculator(monkeypatch, tmp_path)

    calculator.calculate("add", "10", "5")
    calculator.calculate("multiply", "5", "5")

    calculator.undo()

    assert len(calculator.history.data) == 1

    calculator.redo()

    assert len(calculator.history.data) == 2


def test_calculator_clear(monkeypatch, tmp_path):
    """Test clearing calculator history."""

    calculator = setup_calculator(monkeypatch, tmp_path)

    calculator.calculate("add", "10", "5")
    calculator.clear()

    assert calculator.history.data.empty


def test_calculator_save_load(monkeypatch, tmp_path):
    """Test saving and loading calculator history."""

    calculator = setup_calculator(monkeypatch, tmp_path)

    calculator.calculate("add", "10", "5")
    calculator.save()

    calculator.clear()

    assert calculator.history.data.empty

    calculator.load()

    assert len(calculator.history.data) == 1


def test_repl_commands(monkeypatch, tmp_path, capsys):
    """Test the main REPL commands."""

    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        str(tmp_path / "history.csv")
    )

    commands = iter([
        "help",
        "history",
        "add 10 5",
        "history",
        "undo",
        "redo",
        "save",
        "clear",
        "load",
        "history",
        "exit",
    ])

    monkeypatch.setattr(
        builtins,
        "input",
        lambda _: next(commands)
    )

    run_repl()

    output = capsys.readouterr().out

    assert "Welcome to the Advanced Calculator!" in output
    assert "Available commands:" in output
    assert "No calculation history." in output
    assert "Result: 15.0" in output
    assert "Undo complete." in output
    assert "Redo complete." in output
    assert "History saved." in output
    assert "History cleared." in output
    assert "History loaded." in output
    assert "Goodbye!" in output


def test_repl_invalid_command(monkeypatch, tmp_path, capsys):
    """Test an invalid REPL command."""

    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        str(tmp_path / "history.csv")
    )

    commands = iter([
        "banana",
        "exit",
    ])

    monkeypatch.setattr(
        builtins,
        "input",
        lambda _: next(commands)
    )

    run_repl()

    output = capsys.readouterr().out

    assert "Invalid command." in output


def test_repl_calculation_error(monkeypatch, tmp_path, capsys):
    """Test an error while performing a calculation."""

    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        str(tmp_path / "history.csv")
    )

    commands = iter([
        "divide 10 0",
        "exit",
    ])

    monkeypatch.setattr(
        builtins,
        "input",
        lambda _: next(commands)
    )

    run_repl()

    output = capsys.readouterr().out

    assert "Error:" in output


def test_repl_load_missing_file(monkeypatch, tmp_path, capsys):
    """Test loading when no saved history file exists."""

    missing_file = tmp_path / "missing.csv"

    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        str(missing_file)
    )

    commands = iter([
        "load",
        "exit",
    ])

    monkeypatch.setattr(
        builtins,
        "input",
        lambda _: next(commands)
    )

    run_repl()

    output = capsys.readouterr().out

    assert "Error: No saved history file was found." in output

def test_calculator_without_auto_save(monkeypatch, tmp_path):
    """Test calculator when automatic history saving is disabled."""

    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        str(tmp_path / "history.csv")
    )

    monkeypatch.setenv(
        "CALCULATOR_AUTO_SAVE",
        "false"
    )

    calculator = Calculator()

    assert calculator.config.auto_save is False
    assert len(calculator.history.observers) == 1
    assert isinstance(calculator.history.observers[0], LoggingObserver)