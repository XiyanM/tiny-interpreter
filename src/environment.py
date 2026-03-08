from __future__ import annotations
from typing import Any, Optional
from .tokens import Token

class RuntimeError_(Exception):
    pass

class Environment:
    def __init__(self, enclosing: Optional[Environment] = None):
        self.values: dict[str, Any] = {}
        self.enclosing = enclosing

    def define(self, name:str, value: Any) -> None:
        self.values[name] = value

    def get(self, name_token:Token) -> Any:
        name = name_token.lexeme
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name_token)
        raise RuntimeError_(f"Undefined variable '{name}' at line {name_token.line}")

    
    def assign(self, name_token:Token, value:Any) -> None:
        name = name_token.lexeme
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name_token, value)
            return
        raise RuntimeError_(f"Undefined variable '{name}' at line {name_token.line}")

        
        
