from __future__ import annotations # type: ignore
from typing import List
from .tokens import Token, TokenType
from .ast_nodes import Literal, Binary, Expr, Grouping

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens: List[Token]):
        self.current = 0
        self.tokens = tokens

    def parse(self) -> Expr:
        expr = self.expression()
        self.consume(TokenType.EOF, "Expect end of expression")
        return expr
    
    def expression(self) -> Expr:
        return self.term()

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous()
            right = self.factor()
            expr = Binary(expr, op, right)
        
        return expr

    def factor(self):
        expr = self.primary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.previous()
            right = self.primary()
            expr = Binary(expr, op, right)
        return expr

    def primary(self):
        if self.match(TokenType.NUMBER):
            value = self.previous().literal
            return Literal(value)
        
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ) after expression")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")
    
        

    #helper functions
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current-1]
    
    def advance(self):
        self.current+=1
        return self.previous()
    
    def is_at_end(self):
        return self.peek().type == TokenType.EOF
    
    def match(self, *types: TokenType) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, t: TokenType, message: str):
        if self.check(t):
            return self.advance()
        raise self.error(self.peek(), message)



    def error(self, token: Token, message: str) -> ParseError:
        where = "at end" if token.type == TokenType.EOF else f"at '{token.lexeme}'"
        return ParseError(f"[line {token.line}] Error {where}: {message}")

    
    def check(self, t: TokenType):
        return self.peek().type == t
    

    
