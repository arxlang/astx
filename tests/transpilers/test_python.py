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


def test_transpiler_lambdaexpr() -> None:
    """Test astx.LambdaExpr."""
    params = astx.Arguments(astx.Argument(name="x", type_=astx.Int32))
    body = astx.BinaryOp(
        op_code="+", lhs=astx.Variable(name="x"), rhs=astx.LiteralInt32(1)
    )

    lambda_expr = astx.LambdaExpr(params=params, body=body)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(lambda_expr)

    expected_code = "lambda x: (x + 1)"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_lambdaexpr_noparams() -> None:
    """Test astx.LambdaExpr without params."""
    body = astx.LiteralInt32(1)

    lambda_expr = astx.LambdaExpr(body=body)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(lambda_expr)

    expected_code = "lambda : 1"

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


def test_literal_int32() -> None:
    """Test astx.LiteralInt32."""
    # Create a LiteralInt32 node
    literal_int32_node = astx.LiteralInt32(value=42)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_int32_node)
    expected_code = "42"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float16() -> None:
    """Test astx.LiteralFloat16."""
    # Create a LiteralFloat16 node
    literal_float16_node = astx.LiteralFloat16(value=3.14)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_float16_node)
    expected_code = "3.14"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float32() -> None:
    """Test astx.LiteralFloat32."""
    # Create a LiteralFloat32 node
    literal_float32_node = astx.LiteralFloat32(value=2.718)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_float32_node)
    expected_code = "2.718"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float64() -> None:
    """Test astx.LiteralFloat64."""
    # Create a LiteralFloat64 node
    literal_float64_node = astx.LiteralFloat64(value=1.414)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_float64_node)
    expected_code = "1.414"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_complex32() -> None:
    """Test astx.LiteralComplex32."""
    # Create a LiteralComplex32 node
    literal_complex32_node = astx.LiteralComplex32(real=1, imag=2.8)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_complex32_node)
    expected_code = "complex(1, 2.8)"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_literal_complex64() -> None:
    """Test astx.LiteralComplex64."""
    # Create a LiteralComplex64 node
    literal_complex64_node = astx.LiteralComplex64(real=3.5, imag=4)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_complex64_node)
    expected_code = "complex(3.5, 4)"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_typecastexpr() -> None:
    """Test astx.TypeCastExpr."""
    # Expression to cast
    expr = astx.Variable(name="x")
    # Target type for casting
    target_type = astx.Int32()
    # Create the TypeCastExpr
    cast_expr = astx.TypeCastExpr(expr=expr, target_type=target_type)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    generated_code = generator.visit(cast_expr)
    expected_code = "cast(int, x)"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_utf8_char() -> None:
    """Test astx.Utf8Char."""
    # Create a Utf8Char node
    utf8_char_node = astx.UTF8Char(value="c")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(utf8_char_node)
    expected_code = repr("c")

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_utf8_string() -> None:
    """Test astx.Utf8String."""
    # Create a Utf8String node
    utf8_string_node = astx.UTF8String(value="hello")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(utf8_string_node)
    expected_code = repr("hello")

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_utf8_char() -> None:
    """Test astx.LiteralUtf8Char."""
    # Create a LiteralUtf8Char node
    literal_utf8_char_node = astx.LiteralUTF8Char(value="a")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_utf8_char_node)
    expected_code = repr("a")

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_utf8_string() -> None:
    """Test astx.LiteralUtf8String."""
    # Create a LiteralUtf8String node
    literal_utf8_string_node = astx.LiteralUTF8String(value="world")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_utf8_string_node)
    expected_code = repr("world")

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_date() -> None:
    """Test astx.Date."""
    date_node = astx.Date(value="2024-10-31")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(date_node)

    expected_code = "date('2024-10-31')"
    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_time() -> None:
    """Test astx.Time."""
    time_node = astx.Time(value="15:30:00")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(time_node)

    expected_code = "time('15:30:00')"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_timestamp() -> None:
    """Test astx.Timestamp."""
    timestamp_node = astx.Timestamp(value="2024-10-31T15:30:00")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(timestamp_node)

    expected_code = "timestamp('2024-10-31T15:30:00')"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_datetime() -> None:
    """Test astx.DateTime."""
    datetime_node = astx.DateTime(value="2024-10-31T15:30:00")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(datetime_node)

    expected_code = "datetime('2024-10-31T15:30:00')"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_date() -> None:
    """Test astx.LiteralDate."""
    literal_date_node = astx.LiteralDate(value="2024-10-31")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_date_node)

    expected_code = repr("2024-10-31")

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_time() -> None:
    """Test astx.LiteralTime."""
    literal_time_node = astx.LiteralTime(value="15:30:00")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_time_node)

    expected_code = repr("15:30:00")

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_timestamp() -> None:
    """Test astx.LiteralTimestamp."""
    literal_timestamp_node = astx.LiteralTimestamp(value="2024-10-31T15:30:00")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_timestamp_node)

    expected_code = repr("2024-10-31T15:30:00")
    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_datetime() -> None:
    """Test astx.LiteralDateTime."""
    literal_datetime_node = astx.LiteralDateTime(value="2024-10-31T15:30:00")

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_datetime_node)

    expected_code = repr("2024-10-31T15:30:00")

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"
