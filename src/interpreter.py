from __future__ import annotations
from .ast_nodes import Literal, Grouping, Binary, Expr
from typing import Any
from .tokens import TokenType


class RuntimeError_(Exception):
    pass 

class Interpreter:
    def evaluate(self, expr: Expr) -> Any:
        return self._eval(expr)

    def _eval(self, expr: Expr) -> Any:
        if isinstance(expr, Literal):
            return expr.value
        
        if isinstance(expr, Grouping):
            return self._eval(expr.expression)
    
        if isinstance(expr, Binary):
            left = self._eval(expr.left)
            op = expr.op.type
            right = self._eval(expr.right)

            if op == TokenType.PLUS:
                return left + right
            if op == TokenType.MINUS:
                return left - right
            if op == TokenType.STAR:
                return left * right
            if op == TokenType.SLASH:
                if right == 0:
                    raise RuntimeError_("Division by zero.")
                return left / right

            raise RuntimeError_(f"Unknown binary operator: {expr.op.lexeme}")
    
        raise RuntimeError_(f"Unknown Expr node: {type(expr)}")


