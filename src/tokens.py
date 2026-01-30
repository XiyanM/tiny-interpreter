from enum import Enum, auto

class TokenType(Enum):
    #Keywords
    VAR = auto()
    PRINT = auto()

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


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal, line: int):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.lexeme!r}, {self.literal!r})"
    
    def __str__(self):
        return self.__repr__

        

