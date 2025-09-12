# ASTx Transpiler Tutorial

This guide walks you through using ASTx's transpiler system to convert your AST
structures into Python code. We've redesigned the transpiler with a cleaner
architecture that's easier to use and maintain.

## How the Transpiler Works

The transpiler follows a straightforward two-step approach:

### Step 1: ASTx → Python AST Objects

The `ASTxPythonASTTranspiler` converts your ASTx nodes into Python's built-in
AST objects. This is useful when you need to work with the AST programmatically.

```python
from astx_transpilers.python_to_ast import ASTxPythonASTTranspiler

# Get a Python AST object
ast_transpiler = ASTxPythonASTTranspiler()
python_ast = ast_transpiler.visit(your_astx_node)
```

### Step 2: ASTx → Python Source Code

The `ASTxPythonTranspiler` takes your ASTx nodes and produces clean, readable
Python source code. Behind the scenes, it uses the AST transpiler and then
converts to string format.

```python
from astx_transpilers.python_string import ASTxPythonTranspiler

# Get Python source code as a string
string_transpiler = ASTxPythonTranspiler()
python_code = string_transpiler.visit(your_astx_node)
```

## What's Better About This Approach

- **No more circular imports**: Each component has a single, clear job
- **Easier debugging**: Problems in AST generation don't affect string
  formatting
- **More flexible**: Use AST objects directly or get formatted strings
- **Cleaner code**: Each module focuses on one thing and does it well

## Testing Your Setup

Make sure everything works by running the test suite:

```bash
python -m pytest libs/astx-transpilers/tests/ -v
```

## Usage Examples

### Example 1: Simple Integer Literal

**Code:**

```python
import astx
from astx_transpilers.python_to_ast import ASTxPythonASTTranspiler
from astx_transpilers.python_string import ASTxPythonTranspiler

# Create an ASTx integer literal
astx_node = astx.LiteralInt32(value=42)

# Convert to Python AST
python_ast = ASTxPythonASTTranspiler().visit(astx_node)
print(python_ast)

# Convert to Python source code string
code_str = ASTxPythonTranspiler().visit(astx_node)
print(code_str)
```

**Output:**

```
<_ast.Constant value=42>
42
```

---

### Example 2: Lambda Expression

**Code:**

```python
import astx
from astx_transpilers.python_string import ASTxPythonTranspiler

# Create lambda: lambda x: x + 1
params = astx.Arguments(astx.Argument(name="x", type_=astx.Int32()))
body = astx.BinaryOp(op_code="+", lhs=astx.Variable(name="x"), rhs=astx.LiteralInt32(1))
lambda_node = astx.LambdaExpr(params=params, body=body)

# Convert to Python source code
transpiler = ASTxPythonTranspiler()
code_str = transpiler.visit(lambda_node)
print(code_str)
```

**Output:**

```python
lambda x: x + 1
```

---

### Example 3: Mathematical Expression

**Code:**

```python
import astx
from astx_transpilers.python_string import ASTxPythonTranspiler

# Create: (5 + 3) * 2
left_expr = astx.BinaryOp(
    op_code="+",
    lhs=astx.LiteralInt32(5),
    rhs=astx.LiteralInt32(3)
)
math_expr = astx.BinaryOp(
    op_code="*",
    lhs=left_expr,
    rhs=astx.LiteralInt32(2)
)

transpiler = ASTxPythonTranspiler()
result = transpiler.visit(math_expr)
print(result)
```

**Output:**

```
((5 + 3) * 2)
```

---

### Example 4: Function Definition

**Code:**

```python
import astx
from astx_transpilers.python_string import ASTxPythonTranspiler

# Create function: def add(x, y): return x + y
args = astx.Arguments(
    astx.Argument(name="x", type_=astx.Int32()),
    astx.Argument(name="y", type_=astx.Int32()),
)
fn_body = astx.Block()
fn_body.append(
    astx.FunctionReturn(
        value=astx.BinaryOp(
            op_code="+",
            lhs=astx.Variable("x"),
            rhs=astx.Variable("y")
        )
    )
)
add_function = astx.FunctionDef(
    prototype=astx.FunctionPrototype(
        name="add",
        args=args,
        return_type=astx.Int32()
    ),
    body=fn_body,
)

transpiler = ASTxPythonTranspiler()
code_str = transpiler.visit(add_function)
print(code_str)
```

**Output:**

```python
def add(x: int, y: int) -> int:
    return (x + y)
```

---

### Example 5: Import Statement

**Code:**

```python
import astx
from astx_transpilers.python_string import ASTxPythonTranspiler

# Create: import os, sys
import_stmt = astx.ImportStmt(
    names=[
        astx.AliasExpr(name="os"),
        astx.AliasExpr(name="sys")
    ]
)

transpiler = ASTxPythonTranspiler()
code_str = transpiler.visit(import_stmt)
print(code_str)
```

**Output:**

```python
import os, sys
```

## What You Get

- **AST Output:** Valid Python AST objects that can be further processed
- **String Output:** Clean Python source code ready to execute or save to files

## Implementation Details

The refactored transpiler provides better code organization and eliminates
previous circular dependency issues. Each component now has a single, clear
purpose.

---

**Source Files:**

- `libs/astx-transpilers/src/astx_transpilers/python_to_ast.py`
- `libs/astx-transpilers/src/astx_transpilers/python_string.py`

**Tests:**

- `libs/astx-transpilers/tests/test_python_to_ast.py`
- `libs/astx-transpilers/tests/test_python_string.py`
