from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .tokens import Token 



class Expr:
    pass

@dataclass(frozen=True)
class Literal(Expr):
    value: Any

@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    op : Token
    right : Expr

@dataclass(frozen=True)
class Grouping(Expr):
    expression: Expr

@dataclass(frozen=True)
class Unary(Expr):
    op: Token
    right: Expr



