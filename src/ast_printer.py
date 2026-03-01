from __future__ import annotations
from .ast_nodes import Expr, Literal, Grouping, Binary, Unary

class AstPrinter:
    def print(self, expr: Expr):
        return self.parenthesize(expr)
    
    def parenthesize(self, expr: Expr):
        if isinstance(expr, Literal):
            return str(expr.value)


        if isinstance(expr, Binary):
            op = expr.op.lexeme
            return f"({op} {self.parenthesize(expr.left)} {self.parenthesize(expr.right)})"


        if isinstance(expr, Grouping):
            return f"(group {self.parenthesize(expr.expression)})"
        
        if isinstance(expr, Unary):
            op = expr.op.lexeme
            return f"({op} {self.parenthesize(expr.right)})"
        
        print("DEBUG:", expr, type(expr), expr.__class__.__module__)
        raise TypeError(f"Unknown Expr type: {type(expr)}")