from __future__ import annotations
from .ast_nodes import Literal, Grouping, Binary, Expr, Unary
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

        if isinstance(expr, Unary):
            op = expr.op.type
            right = self._eval(expr.right)

            if op == TokenType.MINUS:
                self._check_number_operand(op, right)
                return -right
                
            if op == TokenType.BANG:
                return not self._is_truthy(right)

            raise RuntimeError_(f"Unknown unary operator: {expr.op.lexeme}")



        if isinstance(expr, Binary):
            left = self._eval(expr.left)
            op = expr.op.type
            right = self._eval(expr.right)

            #equality
            if op == TokenType.EQUAL_EQUAL:
                return self._is_equal(left, right)
            if op == TokenType.BANG_EQUAL:
                return not self._is_equal(left,right)
            
            #comparison
            if op == TokenType.GREATER:
                self._check_number_operands(op, left, right)
                return left > right
            if op == TokenType.GREATER_EQUAL:
                self._check_number_operands(op, left, right)
                return left >= right
            if op == TokenType.LESS:
                self._check_number_operands(op, left, right)
                return left < right
            if op == TokenType.LESS_EQUAL:
                self._check_number_operands(op, left, right)
                return left <= right
            

            #arithmetic
            if op == TokenType.PLUS:
                if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                raise RuntimeError_("Operands to '+' must be either both numbers or both strings")
            
            if op == TokenType.MINUS:
                self._check_number_operands(op, left, right)
                return left - right
            if op == TokenType.STAR:
                self._check_number_operands(op, left, right)
                return left * right
            if op == TokenType.SLASH:
                self._check_number_operands(op, left, right)
                if right == 0:
                    raise RuntimeError_("Division by zero.")
                return left / right

            raise RuntimeError_(f"Unknown binary operator: {expr.op.lexeme}")
    
        raise RuntimeError_(f"Unknown Expr node: {type(expr)}")
    
    def _check_number_operand(self, op_token, value:Any) -> None:
        if not isinstance(value, (int, float)):
            raise RuntimeError_(f"Operand must be a number for {op_token.name}")

    def _check_number_operands(self, op_token, left:Any, right:Any) -> None:
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise RuntimeError_(f"Operands must be a number for {op_token.name}")
        
    def _is_equal(self, a:Any, b:Any) -> bool:
        #in lox: nil == nil is true, nil == anything else is false
        return a == b
    
    def _is_truthy(self, value:Any) -> bool:
        #in lox: false and nil are falsey, anything else is truthy
        if value is None:
            return False
        if value is False:
            return False
        return True



