"""Test Python Transpiler."""

import astx

from astx.transpilers import python as astx2py


def test_transpiler_multiple_imports_stmt() -> None:
    """Test astx.ImportStmt multiple imports."""
    alias1 = astx.AliasExpr(name="math")
    alias2 = astx.AliasExpr(name="matplotlib", asname="mtlb")

    # Create an import statement
    import_stmt = astx.ImportStmt(names=[alias1, alias2])

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_stmt)

    expected_code = "import math, matplotlib as mtlb"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_import_from_stmt() -> None:
    """Test astx.ImportFromStmt importing from module."""
    alias = astx.AliasExpr(name="pyplot", asname="plt")

    import_from_stmt = astx.ImportFromStmt(
        module="matplotlib", names=[alias], level=0
    )

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_from_stmt)

    expected_code = "from matplotlib import pyplot as plt"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_wildcard_import_from_stmt() -> None:
    """Test astx.ImportFromStmt wildcard import from module."""
    alias = astx.AliasExpr(name="*")

    import_from_stmt = astx.ImportFromStmt(module="matplotlib", names=[alias])

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_from_stmt)

    expected_code = "from matplotlib import *"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_future_import_from_stmt() -> None:
    """Test astx.ImportFromStmt from future import."""
    alias = astx.AliasExpr(name="division")

    import_from_stmt = astx.ImportFromStmt(module="__future__", names=[alias])

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_from_stmt)

    expected_code = "from __future__ import division"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_multiple_imports_expr() -> None:
    """Test astx.ImportExpr multiple imports."""
    alias1 = astx.AliasExpr(name="sqrt", asname="square_root")
    alias2 = astx.AliasExpr(name="pi")

    import_expr = astx.ImportExpr([alias1, alias2])

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_expr)

    expected_code = (
        "module1, module2 = "
        "(__import__('sqrt as square_root') , "
        "__import__('pi') )"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_import_from_expr() -> None:
    """Test astx.ImportFromExpr importing from module."""
    alias1 = astx.AliasExpr(name="sqrt", asname="square_root")

    import_from_expr = astx.ImportFromExpr(module="math", names=[alias1])

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_from_expr)

    expected_code = (
        "name = "
        "getattr(__import__('math', "
        "fromlist=['sqrt as square_root']), "
        "'sqrt as square_root')"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_wildcard_import_from_expr() -> None:
    """Test astx.ImportFromExpr wildcard import from module."""
    alias1 = astx.AliasExpr(name="*")

    import_from_expr = astx.ImportFromExpr(module="math", names=[alias1])

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_from_expr)

    expected_code = "name = getattr(__import__('math', fromlist=['*']), '*')"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_future_import_from_expr() -> None:
    """Test astx.ImportFromExpr from future import."""
    alias1 = astx.AliasExpr(name="division")

    import_from_expr = astx.ImportFromExpr(module="__future__", names=[alias1])

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_from_expr)

    expected_code = (
        "name = "
        "getattr(__import__('__future__', "
        "fromlist=['division']), "
        "'division')"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_relative_import_from_expr() -> None:
    """Test astx.ImportFromExpr relative imports."""
    alias1 = astx.AliasExpr(name="division")
    alias2 = astx.AliasExpr(name="matplotlib", asname="mtlb")

    import_from_expr = astx.ImportFromExpr(names=[alias1, alias2], level=1)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_from_expr)

    expected_code = (
        "name1, name2 = "
        "(getattr("
        "__import__('.', fromlist=['division']), "
        "'division'), "
        "getattr("
        "__import__('.', fromlist=['matplotlib as mtlb']), "
        "'matplotlib as mtlb'))"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_function() -> None:
    """Test astx.Function."""
    # Function parameters
    args = astx.Arguments(
        astx.Argument(name="x", type_=astx.Int32),
        astx.Argument(name="y", type_=astx.Int32),
    )

    # Function body
    body = astx.Block()
    body.append(
        astx.VariableAssignment(
            name="result",
            value=astx.BinaryOp(
                op_code="+",
                lhs=astx.Variable(name="x"),
                rhs=astx.Variable(name="y"),
                loc=astx.SourceLocation(line=2, col=8),
            ),
            loc=astx.SourceLocation(line=2, col=4),
        )
    )
    body.append(
        astx.FunctionReturn(
            value=astx.Variable(name="result"),
            loc=astx.SourceLocation(line=3, col=4),
        )
    )

    # Function definition
    add_function = astx.Function(
        prototype=astx.FunctionPrototype(
            name="add",
            args=args,
            return_type=astx.Int32,
        ),
        body=body,
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(add_function)
    expected_code = "\n".join(
        [
            "def add(x: int, y: int) -> int:",
            "    result = (x + y)",
            "    return result",
        ]
    )

    assert generated_code == expected_code, "generated_code != expected_code"
