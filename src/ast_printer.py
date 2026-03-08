from __future__ import annotations
from typing import List

from .ast_nodes import Expr, Literal, Grouping, Binary, Unary, Variable, Assign
from .stmt_nodes import (
    Statement, PrintStmt, VarStmt, ExprStmt, BlockStmt, IfStmt, WhileStmt
)

class AstPrinter:
    def print_program(self, statements: List[Statement]) -> str:
        return "\n".join(self.print_stmt(stmt) for stmt in statements)

    # -------- statements --------
    def print_stmt(self, stmt: Statement) -> str:
        if isinstance(stmt, PrintStmt):
            return f"(print {self.print_expr(stmt.expression)})"

        if isinstance(stmt, ExprStmt):
            return f"(expr {self.print_expr(stmt.expression)})"

        if isinstance(stmt, VarStmt):
            if stmt.initialiser is None:
                return f"(var {stmt.name.lexeme})"
            return f"(var {stmt.name.lexeme} {self.print_expr(stmt.initialiser)})"

        if isinstance(stmt, BlockStmt):
            inner = " ".join(self.print_stmt(s) for s in stmt.statements)
            return f"(block {inner})"

        if isinstance(stmt, IfStmt):
            then_part = self.print_stmt(stmt.then_branch)
            else_part = self.print_stmt(stmt.else_branch) if stmt.else_branch else "nil"
            return f"(if {self.print_expr(stmt.condition)} {then_part} {else_part})"

        if isinstance(stmt, WhileStmt):
            return f"(while {self.print_expr(stmt.condition)} {self.print_stmt(stmt.body)})"

        raise TypeError(f"Unknown Statement type: {type(stmt)}")

    # -------- expressions --------
    def print_expr(self, expr: Expr) -> str:
        if isinstance(expr, Literal):
            return str(expr.value)

        if isinstance(expr, Grouping):
            return f"(group {self.print_expr(expr.expression)})"

        if isinstance(expr, Unary):
            op = expr.op.lexeme
            return f"({op} {self.print_expr(expr.right)})"

        if isinstance(expr, Binary):
            op = expr.op.lexeme
            return f"({op} {self.print_expr(expr.left)} {self.print_expr(expr.right)})"

        if isinstance(expr, Variable):
            return f"(varref {expr.name.lexeme})"

        if isinstance(expr, Assign):
            return f"(assign {expr.name.lexeme} {self.print_expr(expr.value)})"

        raise TypeError(f"Unknown Expr type: {type(expr)}")