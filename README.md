# Advanced Calculator — IS 601 Midterm Project

## Project Overview

This project is a Python command-line calculator developed for IS 601.


## Features

The Advanced Calculator supports 10 arithmetic operations:

- Addition, subtraction, multiplication, and division
- Power and root
- Modulus and integer division
- Percentage and absolute difference

Additional features include:
- Calculation history managed with pandas
- Timestamps for each calculation
- Undo and redo functionality
- Automatic CSV history saving
- Logging of calculations
- Color-coded terminal output
- Automated testing with pytest and GitHub Actions

## Installation

Clone the repository:

```bash
git clone git@github.com:dtm2222/advanced-calculator.git
cd advanced-calculator
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it in Git Bash on Windows:

```bash
source venv/Scripts/activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## Running the Calculator

Start the calculator using:

```bash
python -m app.calculator_repl
```

Example commands:

```text
add 5 3
subtract 10 4
multiply 6 2
divide 10 2
power 2 3
root 16 2
modulus 10 3
int_divide 10 3
percent 2 5
abs_diff 5 9
```

Other available commands:

- `help` — Display available commands
- `history` — Display calculation history
- `undo` — Undo the previous change
- `redo` — Redo an undone change
- `clear` — Clear calculation history
- `save` — Save history to CSV
- `load` — Load history from CSV
- `exit` — Close the calculator

## Design Patterns

**Factory Pattern:** The OperationFactory creates the correct arithmetic operation based on the user's input.

**Memento Pattern:** Stores previous history states, allowing users to undo and redo changes.

**Observer Pattern:** The AutoSaveObserver automatically saves calculation history, while the LoggingObserver records calculations in a log file.

## Configuration

The calculator uses environment variables through python-dotenv.

| Variable | Default | Description |
|---|---|---|
| `CALCULATOR_HISTORY_FILE` | `history.csv` | History CSV location |
| `CALCULATOR_LOG_FILE` | `calculator.log` | Application log location |
| `CALCULATOR_AUTO_SAVE` | `true` | Enables automatic saving |
| `CALCULATOR_PRECISION` | `2` | Decimal places for results |

These settings can be customized using a `.env` file.

## Testing

The project uses pytest and pytest-cov.

Run the tests:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

GitHub Actions automatically runs the tests when code is pushed to the main branch or when a pull request is opened.

The workflow requires at least 90% test coverage.

## Optional Feature — Color-Coded Output

Colorama improves readability in the command-line interface.

- Green: Successful calculations
- Red: Error messages
- Blue: Help menu heading

## Technologies Used

Python, pandas, python-dotenv, Colorama, pytest, pytest-cov, Git, GitHub, and GitHub Actions.