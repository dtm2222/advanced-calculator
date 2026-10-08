import pandas as pd

from app.calculator_memento import CalculatorMemento, MementoManager

def test_memento_saves_history():
    """Test that the memento stores a history snapshot."""

    history = pd.DataFrame([
        {
            "a": 10,
            "operation": "add",
            "b": 5,
            "result": 15,
        }
    ])

    memento = CalculatorMemento(history)
    saved_history = memento.get_history()

    assert len(saved_history) == 1
    assert saved_history.iloc[0]["result"] == 15


def test_memento_is_independent():
    """Test that changing current history does not change the snapshot."""

    history = pd.DataFrame([
        {
            "a": 10,
            "operation": "add",
            "b": 5,
            "result": 15,
        }
    ])

    memento = CalculatorMemento(history)

    history.loc[1] = [20, "multiply", 2, 40]

    saved_history = memento.get_history()

    assert len(history) == 2
    assert len(saved_history) == 1


def test_undo():
    """Test restoring the previous history state."""

    manager = MementoManager()

    history = pd.DataFrame([
        {
            "a": 10,
            "operation": "add",
            "b": 5,
            "result": 15,
        }
    ])

    manager.save_state(history)

    history.loc[1] = [20, "multiply", 2, 40]

    restored_history = manager.undo(history)

    assert len(restored_history) == 1
    assert restored_history.iloc[0]["result"] == 15


def test_redo():
    """Test restoring a history state after undo."""

    manager = MementoManager()

    history = pd.DataFrame([
        {
            "a": 10,
            "operation": "add",
            "b": 5,
            "result": 15,
        }
    ])

    manager.save_state(history)

    history.loc[1] = [20, "multiply", 2, 40]

    history = manager.undo(history)
    history = manager.redo(history)

    assert len(history) == 2
    assert history.iloc[1]["result"] == 40


def test_undo_with_empty_stack():
    """Test undo when there is no previous state."""

    manager = MementoManager()
    history = pd.DataFrame()

    result = manager.undo(history)

    assert result.equals(history)


def test_redo_with_empty_stack():
    """Test redo when there is no state to restore."""

    manager = MementoManager()
    history = pd.DataFrame()

    result = manager.redo(history)

    assert result.equals(history)