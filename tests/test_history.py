import pytest
from app.history import History, AutoSaveObserver

@pytest.fixture
def history():
    """Create a fresh History object for each test."""
    return History()


def test_history_starts_empty(history):
    assert history.data.empty


def test_add_history(history):
    history.add(10, "add", 5, 15)

    assert len(history.data) == 1
    assert history.data.iloc[0]["a"] == 10
    assert history.data.iloc[0]["operation"] == "add"
    assert history.data.iloc[0]["b"] == 5
    assert history.data.iloc[0]["result"] == 15


def test_clear_history(history):
    history.add(10, "add", 5, 15)
    history.clear()

    assert history.data.empty

def test_save_history(history, tmp_path):
    """Test saving calculator history to a CSV file."""

    history.add(10, "add", 5, 15)

    file_path = tmp_path / "history.csv"
    history.save(file_path)

    assert file_path.exists()


def test_load_history(history, tmp_path):
    """Test loading calculator history from a CSV file."""

    history.add(10, "add", 5, 15)

    file_path = tmp_path / "history.csv"
    history.save(file_path)

    new_history = History()
    new_history.load(file_path)

    assert len(new_history.data) == 1
    assert new_history.data.iloc[0]["a"] == 10
    assert new_history.data.iloc[0]["operation"] == "add"
    assert new_history.data.iloc[0]["b"] == 5
    assert new_history.data.iloc[0]["result"] == 15


def test_auto_save_observer(history, tmp_path):
    """Test that history automatically saves when it changes."""

    file_path = tmp_path / "auto_history.csv"

    observer = AutoSaveObserver(file_path)
    history.add_observer(observer)

    history.add(10, "add", 5, 15)

    assert file_path.exists()


def test_logging_observer(caplog):
    """Test that LoggingObserver records calculations."""
    import logging
    from app.history import History, LoggingObserver

    history = History()
    history.add_observer(LoggingObserver())

    with caplog.at_level(logging.INFO):
        history.add(5, "add", 3, 8)

    assert "Calculation: 5" in caplog.text
    assert "add" in caplog.text
    assert "8" in caplog.text
