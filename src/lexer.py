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
        ch = self.text[self.current]
        self.current += 1
        return ch
    
    def add_token(self, token_type: TokenType , literal=None):
        lexeme = self.text[self.start:self.current]
        self.tokens.append(Token(token_type, lexeme, literal, self.line))

    def scan_token(self):
        ch = self.advance()

        if ch == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif ch == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif ch == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif ch == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif ch == ",":
            self.add_token(TokenType.COMMA)
        elif ch == ".":
            self.add_token(TokenType.DOT)
        elif ch == "-":
            self.add_token(TokenType.MINUS)
        elif ch == "+":
            self.add_token(TokenType.PLUS)
        elif ch == ";":
            self.add_token(TokenType.SEMICOLON)
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
        elif ch.isalpha() or ch == "_":
            self.identifier()
        else:
            raise SyntaxError(f"Unexpected character on line {self.line}")
        
    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))  
        return self.tokens
    
    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.text[self.current]

    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == ".":
            self.advance()
            while self.peek().isdigit():
                self.advance()
        lexeme = self.text[self.start:self.current]
        value = float(lexeme)
        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        value = self.text[self.start:self.current]
        token_type = self.keywords.get(value, TokenType.IDENTIFIER)
        self.add_token(token_type)






    



    



