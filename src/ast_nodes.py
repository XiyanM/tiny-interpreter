from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List
from .tokens import Token


class Expr:
    pass


@dataclass(frozen=True)
class Literal(Expr):
    value: Any


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    op: Token
    right: Expr


@dataclass(frozen=True)
class Grouping(Expr):
    expression: Expr


@dataclass(frozen=True)
class Unary(Expr):
    op: Token
    right: Expr


@dataclass(frozen=True)
class Variable(Expr):
    name: Token


@dataclass(frozen=True)
class Assign(Expr):
    name: Token
    value: Expr


@dataclass(frozen=True)
class Call(Expr):
    callee: Expr  # Variable() which holds the function name
    paren: Token  # closing RIGHT_PAREN token, used for error handling
    args: List[Expr]
