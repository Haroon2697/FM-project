# Program Equivalence Checker

A formal methods tool that checks program equivalence using SSA form and SMT solving.

## Setup Instructions

1. Install required Python packages:
```bash
pip install lark-parser z3-solver
```

2. Run the program:
```bash
python gui.py
```

## Project Structure

- `gui.py`: Main GUI interface
- `parser.py`: Program parser and AST transformer
- `ssa_converter.py`: SSA form converter
- `smt_generator.py`: SMT constraint generator
- `loop_unroller.py`: Loop unrolling implementation
- `mini_lang.lark`: Language grammar definition

## Usage

1. Program Analysis:
   - Enter program in the input area
   - Click "Parse & Analyze" to see SSA form and SMT constraints

2. Equivalence Check:
   - Enter two programs
   - Click "Check Equivalence" to verify if they are equivalent

## Language Syntax

```python
# Variable Assignment
x = 10;
y = x + 5;

# Conditional Statements
when (x > y) {
    z = x + y;
} otherwise {
    z = x - y;
}

# Loops
repeat (x > 0) {
    x = x - 1;
}

iterate (i = 0; i < 10; i = i + 1) {
    sum = sum + i;
}

# Array Operations
arr[0] = 10;
x = arr[1];

# Assertions
verify(x > 0);
```

## Features

- Custom programming language parser using Lark
- Support for basic arithmetic operations (+, -, *, /)
- Conditional statements (if)
- Program assertions
- Conversion to SSA form
- SMT constraint generation
- Program equivalence verification using Z3 solver

## Requirements

- Python 3.x
- lark-parser
- z3-solver

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install lark-parser z3-solver
```

## Usage

Run the program with two input programs to check their equivalence:

```python
python parser.py program1.txt program2.txt
```

### Example Program Format

```
x := 10;
y := 5;
if (x > y) {
    z := x + y;
}
assert(z > 10);
```

## Project Structure

- `parser.py`: Main program and language parser
- `ssa_converter.py`: Converts programs to SSA form
- `smt_generator.py`: Generates and solves SMT constraints
