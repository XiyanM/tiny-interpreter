from __future__ import annotations # type: ignore
from typing import List
from .tokens import Token, TokenType
from .ast_nodes import Literal, Binary, Expr, Grouping, Unary

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
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            op = self.previous()
            right = self.comparison()
            expr = Binary(expr, op, right)
        
        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(TokenType.GREATER_EQUAL, TokenType.GREATER, TokenType.LESS, TokenType.LESS_EQUAL):
            op = self.previous()
            right = self.term()
            expr = Binary(expr, op, right)
        
        return expr
        

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous()
            right = self.factor()
            expr = Binary(expr, op, right)
        
        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.previous()
            right = self.unary()
            expr = Binary(expr, op, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.previous()
            right = self.unary()
            return Unary(op, right)
        return self.primary()
        


    def primary(self):
        if self.match(TokenType.NUMBER, TokenType.STRING):
            value = self.previous().literal
            return Literal(value)

        if self.match(TokenType.TRUE):
            return Literal(True)
        
        if self.match(TokenType.FALSE):
            return Literal(False)
    
        if self.match(TokenType.NIL):
            return Literal(None)
        
        
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
    

    
