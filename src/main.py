from .lexer import Lexer
from .parser import Parser
from .ast_printer import AstPrinter
from .interpreter import Interpreter


DEBUG_TOKENS = False
DEBUG_AST = False

def run(source: str):
    scanner = Lexer(source)
    tokens = scanner.scan_tokens()

    if DEBUG_TOKENS:
        for token in tokens:
            print(token)
        return
    
    parser = Parser(tokens)
    expr = parser.parse()

    if DEBUG_AST:
        printer = AstPrinter()
        print(printer.print(expr))
        return
    
    interpreter = Interpreter()
    result = interpreter.evaluate(expr)
    print(result)


def repl():
    try:
        while True:
            line = input("lox> ")
            if not line:
                continue
            run(line)
    except (EOFError, KeyboardInterrupt):
        print("\nbye")


def run_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        run(f.read())


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()
