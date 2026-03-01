from __future__ import annotations
from enum import Enum, auto
from typing import Any
from dataclasses import dataclass

class TokenType(Enum):
    #Keywords
    VAR = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()
    NIL = auto()

    #Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    #Single-Character Tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()
    BANG = auto() #!
    LESS = auto() #<
    GREATER = auto() #>

    #one or two char tokens
    BANG_EQUAL = auto() # !=
    EQUAL_EQUAL = auto() # ==
    LESS_EQUAL = auto() #<=
    GREATER_EQUAL = auto() #>=
    
    EOF = auto()

@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    literal: Any
    line: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.lexeme!r}, {self.literal!r})"
    
    def __str__(self):
        return self.__repr__()

        

