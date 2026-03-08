from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from .ast_nodes import Expr
from .tokens import Token


class Statement:
    pass

@dataclass(frozen=True)
class ExprStmt(Statement):
    expression: Expr

@dataclass(frozen=True)
class VarStmt(Statement):
    name: Token
    initialiser: Optional[Expr]

@dataclass(frozen=True)
class PrintStmt(Statement):
    expression: Expr

@dataclass(frozen=True)
class BlockStmt(Statement):
    statements: List[Statement]

@dataclass(frozen=True)
class IfStmt(Statement):
    condition: Expr
    then_branch: Statement
    else_branch: Optional[Statement]

@dataclass(frozen=True)
class WhileStmt(Statement):
    condition: Expr
    body: Statement

@dataclass(frozen=True)
class FunctionStmt(Statement):
    name: Token
    param: List[Token]
    body: List[Statement]

@dataclass(frozen=True)
class ReturnStmt(Statement):
    keyword: Token
    value: Optional[Expr]



