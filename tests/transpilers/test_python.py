"""Test Python Transpiler."""

import astx

from astx.transpilers import python as astx2py


def test_import() -> None:
    """Test astx.ImportStmt and astx.AliasExpr."""
    # Create alias
    alias1 = astx.AliasExpr(name="math")  # type: ignore[abstract]

    # Create an import statement
    import_stmt = astx.ImportStmt(names=[alias1])

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_stmt)

    expected_code = "import math"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_import_with_alias() -> None:
    """Test astx.ImportStmt and astx.AliasExpr using alias."""
    # Create aliases
    alias2 = astx.AliasExpr(name="os", asname="operating_system")  # type: ignore[abstract]

    # Create an import statement
    import_stmt = astx.ImportStmt(names=[alias2])

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_stmt)

    expected_code = "import os as operating_system"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_multiple_imports() -> None:  # CHECK THIS WITH IVAN
    """Test astx.ImportStmt and astx.AliasExpr with multiple imports."""
    # Create aliases
    alias1 = astx.AliasExpr(name="math")  # type: ignore[abstract]
    alias2 = astx.AliasExpr(name="os", asname="operating_system")  # type: ignore[abstract]

    # Create an import statement
    import_stmt = astx.ImportStmt(names=[alias1, alias2])

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_stmt)

    expected_code = "import math \nimport os as operating_system"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_import_from_no_module() -> None:
    """Test astx.ImportFromStmt with relative import."""
    alias3 = astx.AliasExpr(name="path")  # type: ignore[abstract]

    import_from_stmt = astx.ImportFromStmt(names=[alias3], level=1)
    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_from_stmt)

    expected_code = "from . import path"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_import_from_with_module_and_alias() -> None:
    """Test astx.ImportFromStmt importing from module."""
    # Create an import-from statement
    alias3 = astx.AliasExpr(name="path", asname="p")  # type: ignore[abstract]

    import_from_stmt = astx.ImportFromStmt(
        module="os", names=[alias3], level=0
    )
    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(import_from_stmt)

    # print generated code
    generated_code

    expected_code = "from os import path as p"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_function() -> None:
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
