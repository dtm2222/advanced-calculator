import pandas as pd


class History:
    """Manage calculator history using a pandas DataFrame."""

    def __init__(self):
        self.data = pd.DataFrame(
            columns=["a", "operation", "b", "result"]
        )

    def add(self, a: float, operation: str, b: float, result: float):
        """Add a calculation to history."""

        new_entry = pd.DataFrame(
            [{
                "a": a,
                "operation": operation,
                "b": b,
                "result": result,
            }]
        )

        self.data = pd.concat(
            [self.data, new_entry],
            ignore_index=True
        )

    def clear(self):
        """Clear all calculation history."""
        self.data = self.data.iloc[0:0]

    def save(self, file_path: str):
     """Save calculation history to a CSV file."""
     self.data.to_csv(file_path, index=False)

    def load(self, file_path: str):
     """Load calculation history from a CSV file."""
     self.data = pd.read_csv(file_path)