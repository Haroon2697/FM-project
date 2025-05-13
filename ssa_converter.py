"""
Static Single Assignment (SSA) form converter implementation.
This module converts AST into SSA form by tracking variable versions.
"""

class SSAConverter:
    """Converts AST to SSA form."""
    
    def __init__(self):
        """Initialize SSA converter with empty state."""
        self.counter = {}  # Tracks variable versions: {'x': 3}
        self.env = {}      # Current version mapping: {'x': 'x_3'}
        self.ssa = []      # List of SSA statements
    
    def new_version(self, var):
        """
        Create a new version of a variable.
        
        Args:
            var: Variable name
            
        Returns:
            New version name (e.g., 'x_3')
        """
        n = self.counter.get(var, 0) + 1
        self.counter[var] = n
        vname = f"{var}_{n}"
        self.env[var] = vname
        return vname
    
    def current(self, var):
        """
        Get current version of a variable.
        
        Args:
            var: Variable name
            
        Returns:
            Current version name
        """
        return self.env.get(var, var)
    
    def convert(self, ast):
        """
        Convert AST to SSA form.
        
        Args:
            ast: Abstract Syntax Tree
            
        Returns:
            List of SSA statements
        """
        for stmt in ast:
            if stmt[0] == 'assign':
                self.handle_assignment(stmt)
            elif stmt[0] == 'if':
                self.handle_if(stmt)
            elif stmt[0] == 'while':
                self.handle_while(stmt)
            elif stmt[0] == 'for':
                self.handle_for(stmt)
            elif stmt[0] == 'assert':
                self.handle_assert(stmt)
        return self.ssa
    
    def handle_assignment(self, stmt):
        """
        Handle assignment statement.
        
        Args:
            stmt: Assignment statement tuple
        """
        _, var, expr = stmt
        new_var = self.new_version(var)
        new_expr = self.transform_expr(expr)
        self.ssa.append((new_var, '=', new_expr))
    
    def handle_if(self, stmt):
        """
        Handle if statement.
        
        Args:
            stmt: If statement tuple
        """
        _, cond, true_block, false_block = stmt
        new_cond = self.transform_expr(cond)
        self.ssa.append(('if', new_cond))
        
        if true_block:
            for s in true_block:
                if s[0] == 'assign':
                    self.handle_assignment(s)
        
        if false_block:
            for s in false_block:
                if s[0] == 'assign':
                    self.handle_assignment(s)
    
    def handle_while(self, stmt):
        """
        Handle while loop.
        
        Args:
            stmt: While loop tuple
        """
        _, cond, body = stmt
        new_cond = self.transform_expr(cond)
        self.ssa.append(('while', new_cond))
        
        for s in body:
            if s[0] == 'assign':
                self.handle_assignment(s)
    
    def handle_for(self, stmt):
        """
        Handle for loop.
        
        Args:
            stmt: For loop tuple
        """
        _, init, cond, update, body = stmt
        self.handle_assignment(init)
        new_cond = self.transform_expr(cond)
        self.ssa.append(('for', new_cond))
        
        for s in body:
            if s[0] == 'assign':
                self.handle_assignment(s)
        
        self.handle_assignment(update)
    
    def handle_assert(self, stmt):
        """
        Handle assert statement.
        
        Args:
            stmt: Assert statement tuple
        """
        _, cond = stmt
        new_cond = self.transform_expr(cond)
        self.ssa.append(('assert', new_cond))
    
    def transform_expr(self, expr):
        """
        Transform expression to use SSA variables.
        
        Args:
            expr: Expression tuple
            
        Returns:
            Transformed expression
        """
        if isinstance(expr, tuple):
            if expr[0] == 'var':
                return ('var', self.current(expr[1]))
            elif expr[0] == 'cond':
                op = expr[1].value if hasattr(expr[1], 'value') else expr[1]
                left = self.transform_expr(expr[2])
                right = self.transform_expr(expr[3])
                return ('cond', op, left, right)
            elif expr[0] in ('add', 'sub', 'mul', 'div'):
                left = self.transform_expr(expr[1])
                right = self.transform_expr(expr[2])
                return (expr[0], left, right)
        return expr

def format_ssa_output(ssa_list):
    """
    Format SSA statements into readable code.
    
    Args:
        ssa_list: List of SSA statements
        
    Returns:
        Formatted string representation
    """
    def format_expr(expr):
        if isinstance(expr, tuple):
            if expr[0] == 'var':
                return expr[1]
            elif expr[0] == 'cond':
                return f"{format_expr(expr[2])} {expr[1]} {format_expr(expr[3])}"
            elif expr[0] in ('add', 'sub', 'mul', 'div'):
                ops = {
                    'add': '+', 'sub': '-',
                    'mul': '*', 'div': '/'
                }
                return f"{format_expr(expr[1])} {ops[expr[0]]} {format_expr(expr[2])}"
        return str(expr)
    
    output = []
    for stmt in ssa_list:
        if isinstance(stmt, tuple):
            if stmt[0] == 'if':
                output.append(f"if {format_expr(stmt[1])}")
            elif stmt[0] == 'while':
                output.append(f"while {format_expr(stmt[1])}")
            elif stmt[0] == 'for':
                output.append(f"for {format_expr(stmt[1])}")
            elif stmt[0] == 'assert':
                output.append(f"assert({format_expr(stmt[1])})")
            else:
                var, op, rhs = stmt
                output.append(f"{var} := {format_expr(rhs)}")
    return "\n".join(output)
