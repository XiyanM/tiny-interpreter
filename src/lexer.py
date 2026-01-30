from typing import List
from .tokens import TokenType, Token

class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens: List[Token] = []

        self.start = 0
        self.current = 0
        self.line = 1

        self.keywords = {
            "var": TokenType.VAR,
            "print": TokenType.PRINT
        }

    def is_at_end(self) -> bool:
        return self.current >= len(self.text) 
    
    def advance(self):
        ch = self.text(self.current)
        self.current += 1
        return ch
    
    def add_token(self, TokenType, lexeme, literal=None):
        lexeme = self.text[self.start:self.current]
        return Token(TokenType, lexeme, literal, self.line)

    def scan_token(self):
        ch = self.advance()

        if ch == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif ch == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif ch == "{":
            self.add_token(TokenType.LEFT_BRAcE)
        elif ch == "}":
            self.add_token(TokenType.RIGHT_BRAcE)
        elif ch == ",":
            self.add_token(TokenType.cOMMA)
        elif ch == ".":
            self.add_token(TokenType.DOT)
        elif ch == "-":
            self.add_token(TokenType.MINUS)
        elif ch == "+":
            self.add_token(TokenType.PLUS)
        elif ch == ";":
            self.add_token(TokenType.SEMIcOLON)
        elif ch == "*":
            self.add_token(TokenType.STAR)
        elif ch == "/":
            self.add_token(TokenType.SLASH)
        elif ch in (" ", "\r", "\t"):
            pass
        elif ch == "\n":
            self.line += 1
        elif ch.isdigit():
            self.number()
        elif ch.isalpha() or c == "_":
            self.identifier()
        else:
            raise SyntaxError(f"Unexpected character on line {self.line}")
        
        def scan_tokens(self) -> List[Token]:
            while not self.is_at_end():
                self.start = self.current
                self.scan_token()
  
            self.tokens.append(Token(TokenType.EOF, "", None, self.line))






    



    



