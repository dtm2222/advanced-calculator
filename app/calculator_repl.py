from app.calculation import Calculation
from app.operations import OperationFactory
from app.history import History, AutoSaveObserver
from app.calculator_memento import MementoManager
from app.calculator_config import CalculatorConfig
from app.input_validators import validate_number, validate_operation
from app.history import History, AutoSaveObserver, LoggingObserver
import logging
from colorama import Fore, Style, init

class Calculator:
    """Facade that connects the calculator components."""

    def __init__(self):
        self.config = CalculatorConfig()
        self.history = History()
        self.memento_manager = MementoManager()
       
        logging.basicConfig(
            filename=self.config.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            force=True
        )


        # Add the auto-save observer if auto-save is enabled.
        if self.config.auto_save:
            observer = AutoSaveObserver(self.config.history_file)
            self.history.add_observer(observer)

        
        # Register the logging observer to record calculations.
        self.history.add_observer(LoggingObserver())
  

    def calculate(
        self,
        operation_name: str,
        first_value: str,
        second_value: str
    ):
        """Validate input, perform a calculation, and store the result."""

        # Validate the operation and numbers.
        operation_name = validate_operation(operation_name)

        a = validate_number(first_value)
        b = validate_number(second_value)

        # Factory creates the correct operation strategy.
        operation = OperationFactory.create_operation(operation_name)

        # Create the calculation.
        calculation = Calculation(a, b, operation)

        # Save the current history for undo.
        self.memento_manager.save_state(self.history.data)

        # Perform the calculation.
        result = calculation.execute()

        # Round using the configured precision.
        result = round(result, self.config.precision)

        # Store the calculation in history.
        self.history.add(
            a,
            operation_name,
            b,
            result
        )

        return result

    def undo(self):
        """Undo the most recent calculation."""

        self.history.data = self.memento_manager.undo(
            self.history.data
        )

        return self.history.data

    def redo(self):
        """Redo the most recently undone calculation."""

        self.history.data = self.memento_manager.redo(
            self.history.data
        )

        return self.history.data

    def clear(self):
        """Clear calculator history while saving the previous state."""

        # Save history first so clear can be undone.
        self.memento_manager.save_state(
            self.history.data
        )

        self.history.clear()

        return self.history.data

    def save(self):
        """Save calculator history to the configured CSV file."""

        self.history.save(
            self.config.history_file
        )

    def load(self):
        """Load calculator history from the configured CSV file."""

        # Save the current state so loading can be undone.
        self.memento_manager.save_state(
            self.history.data
        )

        self.history.load(
            self.config.history_file
        )

        return self.history.data


def run_repl():
    """Run the calculator read-evaluate-print loop."""

    init()
    calculator = Calculator()

    print("Welcome to the Advanced Calculator!")
    print("Type 'help' to see available commands.")

    while True:

        # Get a command from the user.
        user_input = input("Calculator> ").strip()

        # -------------------------
        # EXIT
        # -------------------------

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # -------------------------
        # HELP
        # -------------------------

        if user_input.lower() == "help":
         print(Fore.BLUE + "Available commands:" + Style.RESET_ALL)
         print("  add <a> <b>")
         print("  subtract <a> <b>")
         print("  multiply <a> <b>")
         print("  divide <a> <b>")
         print("  power <a> <b>")
         print("  root <a> <b>")
         print("  modulus <a> <b>")
         print("  int_divide <a> <b>")
         print("  percent <a> <b>")
         print("  abs_diff <a> <b>")
         print("  history")
         print("  undo")
         print("  redo")
         print("  clear")
         print("  save")
         print("  load")
         print("  exit")
         continue

        # -------------------------
        # HISTORY
        # -------------------------

        if user_input.lower() == "history":

            if calculator.history.data.empty:
                print("No calculation history.")

            else:
                print(
                    calculator.history.data.to_string(
                        index=False
                    )
                )

            continue

        # -------------------------
        # UNDO
        # -------------------------

        if user_input.lower() == "undo":
            calculator.undo()
            print("Undo complete.")
            continue

        # -------------------------
        # REDO
        # -------------------------

        if user_input.lower() == "redo":
            calculator.redo()
            print("Redo complete.")
            continue

        # -------------------------
        # CLEAR
        # -------------------------

        if user_input.lower() == "clear":
            calculator.clear()
            print("History cleared.")
            continue

        # -------------------------
        # SAVE
        # -------------------------

        if user_input.lower() == "save":
            calculator.save()
            print("History saved.")
            continue

        # -------------------------
        # LOAD
        # -------------------------

        if user_input.lower() == "load":

            try:
                calculator.load()
                print("History loaded.")

            except FileNotFoundError:
                print(
                    "Error: No saved history file was found."
                )

            continue

        # -------------------------
        # MATH COMMANDS
        # -------------------------

        parts = user_input.split()

        if len(parts) == 3:

            operation_name = parts[0]
            first_value = parts[1]
            second_value = parts[2]

            try:

                result = calculator.calculate(
                    operation_name,
                    first_value,
                    second_value
                )

                print(Fore.GREEN + f"Result: {result}" + Style.RESET_ALL)

            except Exception as error:
                print(Fore.RED + f"Error: {error}" + Style.RESET_ALL)

        else:

            print(
                "Invalid command. "
                "Type 'help' for instructions."
            )


if __name__ == "__main__":  # pragma: no cover
    run_repl()