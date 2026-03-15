# Tiny Lox Interpreter

A small tree-walk interpreter for a Lox-like language written in Python.

## What it supports

- Lexing into tokens
- Recursive-descent parsing into AST nodes
- Expression evaluation
  - literals
  - grouping
  - unary operators (`!`, `-`)
  - binary operators (`+`, `-`, `*`, `/`, comparisons, equality)
- Statements
  - expression statements
  - `print`
  - `var` declarations
  - blocks
  - `if` / `else`
  - `while`
- Variables and assignment
- Nested lexical environments
- Strings and multiline string lexing
- Functions
  - `fun` declarations
  - call expressions
  - `return`
  - closures
  - recursion

## Project structure

```text
src/
  main.py              # entry point, REPL / file runner
  tokens.py            # TokenType enum and Token dataclass
  lexer.py             # source text -> tokens
  parser.py            # tokens -> statements / expressions (AST)
  ast_nodes.py         # expression AST nodes
  stmt_nodes.py        # statement AST nodes
  interpreter.py       # tree-walk interpreter
  environment.py       # lexical scope chain
  lox_function.py      # runtime function object
  runtime_control.py   # internal control-flow exceptions (e.g. return)
  ast_printer.py       # optional AST debug printer
```

## How it works

### 1. Lexing
The lexer scans raw source code and produces a list of tokens.

Examples of tokens:
- keywords: `var`, `print`, `if`, `while`, `fun`, `return`
- literals: numbers, strings, identifiers
- symbols: `(` `)` `{` `}` `;` `,`
- operators: `+ - * / ! == != < <= > >= =`

### 2. Parsing
The parser consumes tokens and builds an AST.

- Top level parsing returns a `List[Statement]`
- Statement grammar handles declarations, control flow, blocks, and returns
- Expression grammar handles precedence and associativity
- Function calls are parsed as expressions

### 3. Interpreting
The interpreter walks the AST and evaluates it.

- Variables are stored in environments
- Blocks create nested environments
- Functions are runtime values stored as `LoxFunction`
- Returns are implemented using an internal control-flow exception
- Closures work by capturing the environment where a function was declared

## Running the interpreter

From the project root:

```bash
python3 -m src.main
```

To run a file:

```bash
python3 -m src.main program.lox
```

## REPL

Running without a file starts a simple REPL:

```text
lox> print 1 + 2;
3
```

Note: the current REPL is line-based, so multi-line programs are better run from a file.

## Example programs

### Variables

```lox
var x = 10;
print x;
x = x + 5;
print x;
```

### Blocks and scope

```lox
var x = "global";
{
  var x = "local";
  print x;
}
print x;
```

### If / while

```lox
var x = 0;
while (x < 3) {
  print x;
  x = x + 1;
}
```

### Functions

```lox
fun add(a, b) {
  return a + b;
}

print add(1, 2);
```

### Closures

```lox
fun makeCounter() {
  var x = 0;

  fun inc() {
    x = x + 1;
    return x;
  }

  return inc;
}

var c = makeCounter();
print c();
print c();
```

### Recursion

```lox
fun fact(n) {
  if (n <= 1) return 1;
  return n * fact(n - 1);
}

print fact(5);
```

## Debugging

`main.py` includes optional debug flags:

- `DEBUG_TOKENS` to print tokens
- `DEBUG_AST` to print the parsed AST

## Current limitations

This project stops at a strong tree-walk interpreter milestone. It does not currently include:

- logical `and` / `or`
- native functions such as `clock()`
- classes / methods / inheritance
- parser error recovery / synchronization

## Why this project matters

This interpreter demonstrates:

- recursive-descent parsing
- AST design
- lexical scoping
- closures
- runtime environments
- control-flow handling for `return`
- function calls and recursion

## Future improvements

Possible next steps:

- add logical operators
- add native functions
- improve runtime / parse errors
- add comments support
- add classes and methods
- add tests

## License

Personal learning project.

