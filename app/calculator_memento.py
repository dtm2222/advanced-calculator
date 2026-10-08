import pandas as pd


class CalculatorMemento:
    """Stores a snapshot of the calculator's history."""

    def __init__(self, history: pd.DataFrame):
        self._history = history.copy()

    def get_history(self) -> pd.DataFrame:
        """Return a copy of the saved history."""
        return self._history.copy()



class MementoManager:
    """Manage undo and redo history snapshots."""

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def save_state(self, history: pd.DataFrame):
        """Save the current state for a future undo."""
        self.undo_stack.append(CalculatorMemento(history))
        self.redo_stack.clear()

    def undo(self, current_history: pd.DataFrame):
        """Restore the previous history state."""

        if not self.undo_stack:
            return current_history

        self.redo_stack.append(CalculatorMemento(current_history))

        memento = self.undo_stack.pop()

        return memento.get_history()

    def redo(self, current_history: pd.DataFrame):
        """Restore a previously undone history state."""

        if not self.redo_stack:
            return current_history

        self.undo_stack.append(CalculatorMemento(current_history))

        memento = self.redo_stack.pop()

        return memento.get_history()