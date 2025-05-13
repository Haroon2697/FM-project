"""
Program parser and AST transformer implementation.
This module handles parsing of the custom language and converts it to an AST.
"""

from ssa_converter import SSAConverter, format_ssa_output
from smt_generator import SMTGenerator, check_program_equivalence
from typing import List, Tuple, Any

# Example programs for testing
EXAMPLE_PROGRAM = """
x = 10;
y = x + 5;
when (x > y) {
    z = x + y;
} otherwise {
    z = x - y;
}
verify(z > 0);
"""

EXAMPLE_PROGRAM_2 = """
a = 10;
b = a + 5;
when (a > b) {
    c = a + b;
} otherwise {
    c = a - b;
}
verify(c > 0);
"""

# Grammar definition
GRAMMAR = """
start: statement+

statement: assignment
        | if_statement
        | while_loop
        | for_loop
        | assert_stmt

assignment: NAME "=" expr ";"
if_statement: "when" "(" expr ")" block "otherwise" block
while_loop: "repeat" "(" expr ")" block
for_loop: "iterate" "(" assignment expr ";" assignment ")" block
assert_stmt: "verify" "(" expr ")" ";"

block: "{" statement* "}"

expr: term
    | expr "+" term -> add
    | expr "-" term -> sub

term: factor
    | term "*" factor -> mul
    | term "/" factor -> div

factor: NUMBER -> number
      | NAME -> var
      | "(" expr ")"
      | condition

condition: expr COMPARATOR expr

COMPARATOR: ">" | "<" | ">=" | "<=" | "==" | "!="

%import common.NUMBER
%import common.CNAME -> NAME
%import common.WS

%ignore WS
"""

class ASTTransformer:
    """Transforms parse tree into AST."""
    
    def start(self, statements):
        """Root node of AST."""
        return list(statements)
    
    def assignment(self, children):
        """Assignment statement: var = expr;"""
        var, expr = children
        return ('assign', var, expr)
    
    def if_statement(self, children):
        """If statement: when (cond) { ... } otherwise { ... }"""
        cond, then_block, else_block = children
        return ('if', cond, then_block, else_block)
    
    def while_loop(self, children):
        """While loop: repeat (cond) { ... }"""
        cond, body = children
        return ('while', cond, body)
    
    def for_loop(self, children):
        """For loop: iterate (init; cond; update) { ... }"""
        init, cond, update, body = children
        return ('for', init, cond, update, body)
    
    def assert_stmt(self, children):
        """Assertion: verify(cond);"""
        cond, = children
        return ('assert', cond)
    
    def block(self, statements):
        """Block of statements: { ... }"""
        return list(statements)
    
    def add(self, children):
        """Addition: expr + term"""
        left, right = children
        return ('add', left, right)
    
    def sub(self, children):
        """Subtraction: expr - term"""
        left, right = children
        return ('sub', left, right)
    
    def mul(self, children):
        """Multiplication: term * factor"""
        left, right = children
        return ('mul', left, right)
    
    def div(self, children):
        """Division: term / factor"""
        left, right = children
        return ('div', left, right)
    
    def number(self, children):
        """Number literal"""
        return ('number', int(children[0]))
    
    def var(self, children):
        """Variable reference"""
        return ('var', str(children[0]))
    
    def condition(self, children):
        """Condition: expr comparator expr"""
        left, op, right = children
        return ('cond', op, left, right)

def parse_and_transform(code: str) -> List[Tuple]:
    """
    Parse code and transform to AST.
    
    Args:
        code: Program code as string
        
    Returns:
        List of AST nodes
    """
    # Simple tokenizer and parser implementation
    tokens = tokenize(code)
    return parse(tokens)

def tokenize(code: str) -> List[str]:
    """Simple tokenizer implementation."""
    # This is a placeholder for the actual tokenizer implementation
    return code.split()

def parse(tokens: List[str]) -> List[Tuple]:
    """Simple parser implementation."""
    # This is a placeholder for the actual parser implementation
    return []

def check_program_equivalence(ssa1: List[Tuple], ssa2: List[Tuple]) -> str:
    """
    Check if two programs are equivalent based on their SSA forms.
    
    Args:
        ssa1: SSA form of first program
        ssa2: SSA form of second program
        
    Returns:
        String describing equivalence result
    """
    # Compare variable assignments
    vars1 = {v[0] for v in ssa1 if isinstance(v, tuple) and v[0] != 'if' and v[0] != 'assert'}
    vars2 = {v[0] for v in ssa2 if isinstance(v, tuple) and v[0] != 'if' and v[0] != 'assert'}
    
    if vars1 != vars2:
        return "Programs are not equivalent: Different variables used"
    
    # Compare control flow
    if_stmts1 = [v for v in ssa1 if isinstance(v, tuple) and v[0] == 'if']
    if_stmts2 = [v for v in ssa2 if isinstance(v, tuple) and v[0] == 'if']
    
    if len(if_stmts1) != len(if_stmts2):
        return "Programs are not equivalent: Different control flow"
    
    # Compare assertions
    asserts1 = [v for v in ssa1 if isinstance(v, tuple) and v[0] == 'assert']
    asserts2 = [v for v in ssa2 if isinstance(v, tuple) and v[0] == 'assert']
    
    if len(asserts1) != len(asserts2):
        return "Programs are not equivalent: Different assertions"
    
    return "Programs are equivalent"

def main():
    print("\nProgram Analysis Options:")
    print("----------------------------------------")
    print("1. Input Program")
    print("2. Parse Tree")
    print("3. Abstract Syntax Tree (AST)")
    print("4. Static Single Assignment (SSA) Form")
    print("5. Verify Program (SMT)")
    print("6. Check Program Equivalence")
    print("0. Exit Program")
    print("----------------------------------------")
    
    while True:
        try:
            choice = input("Enter numbers (e.g., 123456 to see all): ").strip()
            if choice == '0':
                break
                
            if '1' in choice:
                print("\nInput Program:")
                print("----------------------------------------")
                print(EXAMPLE_PROGRAM)
            
            if '2' in choice:
                print("\nParse Tree:")
                print("----------------------------------------")
                tokens = tokenize(EXAMPLE_PROGRAM)
                print(tokens)
            
            if '3' in choice:
                print("\nAbstract Syntax Tree (AST):")
                print("----------------------------------------")
                ast = parse_and_transform(EXAMPLE_PROGRAM)
                print(ast)
            
            if '4' in choice:
                print("\nStatic Single Assignment (SSA) Form:")
                print("----------------------------------------")
                ast = parse_and_transform(EXAMPLE_PROGRAM)
                ssa = SSAConverter().convert(ast)
                print(format_ssa_output(ssa))
            
            if '5' in choice:
                print("\nProgram Verification (SMT):")
                print("----------------------------------------")
                ast = parse_and_transform(EXAMPLE_PROGRAM)
                ssa = SSAConverter().convert(ast)
                smt = SMTGenerator(ssa)
                smt.to_smt()
                print(smt.check_assertions())
            
            if '6' in choice:
                print("\nProgram Equivalence Check:")
                print("----------------------------------------")
                # Parse and convert first program
                ast1 = parse_and_transform(EXAMPLE_PROGRAM)
                ssa1 = SSAConverter().convert(ast1)
                
                # Parse and convert second program
                print("\nSecond Program:")
                print(EXAMPLE_PROGRAM_2)
                ast2 = parse_and_transform(EXAMPLE_PROGRAM_2)
                ssa2 = SSAConverter().convert(ast2)
                
                print("\nProgram 1 SSA:")
                print(format_ssa_output(ssa1))
                print("\nProgram 2 SSA:")
                print(format_ssa_output(ssa2))
                
                print("\nEquivalence Result:")
                result = check_program_equivalence(ssa1, ssa2)
                print(result)
                
        except Exception as e:
            print(f"\nError: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()