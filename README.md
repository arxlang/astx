# ASTx

**ASTx** is an agnostic expression structure for **AST**. It is agnostic because
it is not specific to any language, neither to the **ArxLang** project, although
its main focus is to provide all needed feature for **ArxLang**.

**ASTx** doesn't aim to be a `lexer` or a `parser`, although it could be used by
any programming language or parser in order to provide a high level
representation of the AST.

Note: this project is under active development and it is not ready for
production yet.

- License: BSD 3 Clause
- Documentation: https://astx.arxlang.org.

## Features

- Support for blocks of AST: `Module`, and `Block`
- Support for control flow: `if/else` statement and `for` loop
- Support for integer data types: Int8, Int16, Int32, Int64
- Support for Binary and Unary operators
- Support for object visibility: Public and Private
- Support for object scope: Global and Local
- Support for SymbolTable organized by scope
- Support for functions declaration and function call
