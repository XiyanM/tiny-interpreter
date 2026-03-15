from .environment import Environment
from .runtime_control import ReturnSignal


class LoxFunction:
    def __init__(self, declaration, closure):
        self.declaration = (
            declaration  # entire FunctionStmt including body, param, name token
        )
        self.closure = closure  # environment where function was declared

    def arity(self):
        return len(self.declaration.param)

    def call(self, interpreter, arguments):
        prev = interpreter.env  # environment where function was called
        interpreter.env = Environment(enclosing=self.closure)

        try:
            for i in range(len(self.declaration.param)):
                param_name = self.declaration.param[i].lexeme
                interpreter.env.define(param_name, arguments[i])

            for stmt in self.declaration.body:
                interpreter._execute(stmt)

        except ReturnSignal as returned:
            return returned.value

        finally:
            interpreter.env = prev

        return None
