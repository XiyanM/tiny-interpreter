from __future__ import annotations # type: ignore
from typing import List
from .tokens import Token, TokenType
from .ast_nodes import Literal, Binary, Expr, Grouping, Unary
from .stmt_nodes import Statement, VarStmt, IfStmt, WhileStmt, BlockStmt, PrintStmt, FunctionStmt, ReturnStmt

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens: List[Token]):
        self.current = 0
        self.tokens = tokens

    def parse(self) -> List[Statement]:
        statements = []

        while not self.is_at_end():
            statements.append(self.declaration())

        return statements
    
    #statement grammar
    def declaration(self) -> Statement:
        if self.match(TokenType.VAR):
            return self.var_declaration()
        return self.statement()


    def statement(self) -> Statement:
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.LEFT_BRACE):
            return self.block()
        
        return self.expression_statement()

    def var_declaration(self) -> Statement:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name")

        initialiser = None
        if self.match(TokenType.EQUAL):
            initialiser = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expect ; after variable declaration")
        return VarStmt(name, initialiser)
    
    def print_statement(self) -> Statement:
        expression = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ; after value")

        return PrintStmt(expression)
    
    def if_statement(self) -> Statement:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        
        return IfStmt(condition, then_branch, else_branch)
    
    def while_statement(self) -> Statement:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition'.")

        body = self.statement()

        return WhileStmt(condition, body)
    
    def block(self) -> Statement:
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")

        return BlockStmt(statements)






    #expression grammar
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
    

    
