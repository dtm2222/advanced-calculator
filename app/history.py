import pandas as pd
import logging 
from datetime import datetime

from abc import ABC, abstractmethod

class HistoryObserver(ABC):
    """Base class for history observers."""

    @abstractmethod
    def update(self, history):
        """Respond when calculator history changes."""
        pass  # pragma: no cover


class AutoSaveObserver(HistoryObserver):
    """Automatically save history when it changes."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def update(self, history):
        """Save the updated history to a CSV file."""
        history.save(self.file_path)


class LoggingObserver(HistoryObserver):
    """Log the latest calculation when history changes."""

    def update(self, history):
        """Record the latest calculation in the application log."""
        if history.data.empty:
            return

        latest = history.data.iloc[-1]

        logging.info(
            "Calculation: %s %s %s = %s",
            latest["a"],
            latest["operation"],
            latest["b"],
            latest["result"]
        )


class History:
    """Manage calculator history using a pandas DataFrame."""

    def __init__(self):
        self.data = pd.DataFrame(
    columns=["a", "operation", "b", "result", "timestamp"]
)

        self.observers = []

    def add_observer(self, observer: HistoryObserver):
      """Add an observer to the observer list."""
      self.observers.append(observer)


    def notify_observers(self):
     """Notify all observers that history has changed."""
     for observer in self.observers:
         observer.update(self)




    def add(self, a: float, operation: str, b: float, result: float):
        """Add a calculation to history."""

        new_entry = pd.DataFrame(
            [{
                "a": a,
                "operation": operation,
                "b": b,
                "result": result,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            }]
        )

        self.data = pd.concat(
            [self.data, new_entry],
            ignore_index=True
        )

        self.notify_observers()


    def clear(self):
        """Clear all calculation history."""
        self.data = self.data.iloc[0:0]

    def save(self, file_path: str):
     """Save calculation history to a CSV file."""
     self.data.to_csv(file_path, index=False)

    def load(self, file_path: str):
     """Load calculation history from a CSV file."""
     self.data = pd.read_csv(file_path)