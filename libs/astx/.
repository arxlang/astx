# ASTx: Abstract Syntax Tree Framework

![CI](https://img.shields.io/github/actions/workflow/status/arxlang/astx/main.yaml?logo=github&label=CI)
[![Python Versions](https://img.shields.io/pypi/pyversions/astx)](https://pypi.org/project/astx/)
[![Package Version](https://img.shields.io/pypi/v/astx?color=blue)](https://pypi.org/project/astx/)
![License](https://img.shields.io/pypi/l/astx?color=blue)
![Discord](https://img.shields.io/discord/966124290464428042?logo=discord&color=blue)

ASTx is a versatile and extensible library for representing, manipulating, and
analyzing Abstract Syntax Trees (ASTs). It provides a unified interface for
working with ASTs in various contexts, such as compilers, interpreters, and
transpilers.

ASTx makes it easy to model programming languages, apply transformations,
generate code, and build custom tools for static and dynamic analysis.

**ASTx** doesn't aim to be a `lexer` or a `parser`, although it could be used by
any programming language or parser in order to provide a high level
representation of the AST.

It integrates with [IRx](https://github.com/arxlang/irx), enabling code
generation with **LLVM**. Currently, only a small subset of **ASTx** nodes is
supported, but active development is underway, with full support expected soon.

**Note**: this project is under active development and it is not ready for
production yet.

---

## 🚀 Features

- **Language-Agnostic Design**: Model and manipulate ASTs for different
  programming languages.
- **Extensibility**: Easily add support for new language features or custom AST
  nodes.
- **Code Generation**: Transform ASTs into target code for various backends or
  target languages.
- **Rich Node Set**: Support for common constructs like variables, expressions,
  functions, classes, and control flow.
- **Python Integration**: Built with Python, making it easy to integrate into
  Python-based projects.
- **Symbol Table**: Support for an initial implementation of Symbol Table.

---

## 📦 Installation

Install ASTx from PyPI:

```bash
pip install astx
```

---

## 📖 Overview

ASTx is designed around two primary concepts:

1. **Nodes**: Each node represents a language construct (e.g., `Variable`,
   `Function`, `IfStmt`).
2. **Tree**: Nodes are organized hierarchically, forming an abstract
   representation of the program structure.

Additionally, ASTx provides a simple transpiler for converting ASTx nodes to
Python code (in text format). This feature is intended solely for educational
purposes, demonstrating how a transpiler from ASTx to any other language can be
implemented.

---

## ✨ Usage

### 1. Create an AST

```python
import astx

# Define a simple function `add(x, y): return x + y`
args = astx.Arguments(
    astx.Argument(name="x", type_=astx.Int32()),
    astx.Argument(name="y", type_=astx.Int32()),
)
fn_body = astx.Block()
fn_body.append(
    astx.FunctionReturn(
        value=astx.BinaryOp(op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("y"))
    )
)
add_function = astx.FunctionDef(
    prototype=astx.FunctionPrototype(name="add", args=args, return_type=astx.Int32()),
    body=fn_body,
)
```

### 2. Generate Code

Use a transpiler to convert the AST to Python code:

```python
from astx_transpilers.python_string import ASTxPythonTranspiler

# Transpile the AST to Python
transpiler = ASTxPythonTranspiler()
python_code = transpiler.visit(add_function)

print(python_code)
```

Output:

```python
def add(x: int, y: int) -> int:
    return (x + y)
```

### 3. ASTx Visualization Features

**ASTx** offers multiple ways to visualize the AST structure:

- YAML
- JSON
- Graphical visualization (PNG or ASCII)

In a Jupyter Notebook, the default graphical visualization is **PNG**, while in
a console, the default is **ASCII**.

You can also print the AST structure in **JSON** or **YAML** format. For
example:

```python
>>> print(add_function.to_json())
>>> print(add_function.to_yaml())
```

---

## 📚 Documentation

Detailed documentation and examples can be found in the
[official documentation](https://arxlang.github.io/astx).

---

## 🛠️ Contributing

Contributions are welcome! Please check out our
[Contributing Guide](https://astx.arxlang.org/contributing/) for more
information.

---

## 📝 License

ASTx is open-source software licensed under the BSD-3-Clause License. See
[LICENSE](LICENSE) for details.
