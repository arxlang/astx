"""Test Python Transpiler."""

import ast
import sys

import astx
import pytest

from astx_transpilers import python_string as astx2py

transpiler = astx2py.ASTxPythonTranspiler()


def translate(node: astx.AST) -> str:
    """Translate from ASTx to Python source."""
    code = str(transpiler.visit(node))
    # check if the code is a valid python code
    ast.parse(code)
    return code


def check_transpilation(code: str) -> None:
    """Check Transpilation with Python ast lib."""
    ast.parse(code)


def test_transpiler_multiple_imports_stmt() -> None:
    """Test astx.ImportStmt multiple imports."""
    alias1 = astx.AliasExpr(name="math")
    alias2 = astx.AliasExpr(name="matplotlib", asname="mtlb")

    # Create an import statement
    import_stmt = astx.ImportStmt(names=[alias1, alias2])

    # Generate Python code
    generated_code = translate(import_stmt)

    expected_code = "import math, matplotlib as mtlb"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_import_from_stmt() -> None:
    """Test astx.ImportFromStmt importing from module."""
    alias = astx.AliasExpr(name="pyplot", asname="plt")

    import_from_stmt = astx.ImportFromStmt(
        module="matplotlib", names=[alias], level=0
    )

    # Generate Python code
    generated_code = translate(import_from_stmt)

    expected_code = "from matplotlib import pyplot as plt"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_wildcard_import_from_stmt() -> None:
    """Test astx.ImportFromStmt wildcard import from module."""
    alias = astx.AliasExpr(name="*")

    import_from_stmt = astx.ImportFromStmt(module="matplotlib", names=[alias])

    # Generate Python code
    generated_code = translate(import_from_stmt)

    expected_code = "from matplotlib import *"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_future_import_from_stmt() -> None:
    """Test astx.ImportFromStmt from future import."""
    alias = astx.AliasExpr(name="division")

    import_from_stmt = astx.ImportFromStmt(module="__future__", names=[alias])

    # Generate Python code
    generated_code = translate(import_from_stmt)

    expected_code = "from __future__ import division"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_multiple_imports_expr() -> None:
    """Test astx.ImportExpr multiple imports."""
    alias1 = astx.AliasExpr(name="sqrt", asname="square_root")
    alias2 = astx.AliasExpr(name="pi")

    import_expr = astx.ImportExpr([alias1, alias2])

    # Generate Python code
    generated_code = translate(import_expr)

    expected_code = (
        "module1, module2 = "
        "(__import__('sqrt as square_root') , "
        "__import__('pi') )"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_import_from_expr() -> None:
    """Test astx.ImportFromExpr importing from module."""
    alias1 = astx.AliasExpr(name="sqrt", asname="square_root")

    import_from_expr = astx.ImportFromExpr(module="math", names=[alias1])

    # Generate Python code
    generated_code = translate(import_from_expr)

    expected_code = (
        "name = "
        "getattr(__import__('math', "
        "fromlist=['sqrt as square_root']), "
        "'sqrt as square_root')"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_wildcard_import_from_expr() -> None:
    """Test astx.ImportFromExpr wildcard import from module."""
    alias1 = astx.AliasExpr(name="*")

    import_from_expr = astx.ImportFromExpr(module="math", names=[alias1])

    # Generate Python code
    generated_code = translate(import_from_expr)

    expected_code = "name = getattr(__import__('math', fromlist=['*']), '*')"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_future_import_from_expr() -> None:
    """Test astx.ImportFromExpr from future import."""
    alias1 = astx.AliasExpr(name="division")

    import_from_expr = astx.ImportFromExpr(module="__future__", names=[alias1])

    # Generate Python code
    generated_code = translate(import_from_expr)

    expected_code = (
        "name = "
        "getattr(__import__('__future__', "
        "fromlist=['division']), "
        "'division')"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_relative_import_from_expr() -> None:
    """Test astx.ImportFromExpr relative imports."""
    alias1 = astx.AliasExpr(name="division")
    alias2 = astx.AliasExpr(name="matplotlib", asname="mtlb")

    import_from_expr = astx.ImportFromExpr(names=[alias1, alias2], level=1)

    # Generate Python code
    generated_code = translate(import_from_expr)

    expected_code = (
        "name1, name2 = "
        "(getattr("
        "__import__('.', fromlist=['division']), "
        "'division'), "
        "getattr("
        "__import__('.', fromlist=['matplotlib as mtlb']), "
        "'matplotlib as mtlb'))"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_lambdaexpr() -> None:
    """Test astx.LambdaExpr."""
    params = astx.Arguments(astx.Argument(name="x", type_=astx.Int32()))
    body = astx.BinaryOp(
        op_code="+", lhs=astx.Variable(name="x"), rhs=astx.LiteralInt32(1)
    )

    lambda_expr = astx.LambdaExpr(params=params, body=body)

    # Generate Python code
    generated_code = translate(lambda_expr)

    expected_code = "lambda x: (x + 1)"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_lambdaexpr_noparams() -> None:
    """Test astx.LambdaExpr without params."""
    body = astx.LiteralInt32(1)

    lambda_expr = astx.LambdaExpr(body=body)

    # Generate Python code
    generated_code = translate(lambda_expr)

    expected_code = "lambda : 1"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_functiondef() -> None:
    """Test astx.FunctionDef."""
    # Function parameters
    args = astx.Arguments(
        astx.Argument(name="x", type_=astx.Int32()),
        astx.Argument(name="y", type_=astx.Int32()),
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
    add_function = astx.FunctionDef(
        prototype=astx.FunctionPrototype(
            name="add",
            args=args,
            return_type=astx.Int32(),
        ),
        body=body,
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Generate Python code
    generated_code = translate(add_function)
    expected_code = "\n".join(
        [
            "def add(x: int, y: int) -> int:",
            "    result = (x + y)",
            "    return result",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_literal_int32() -> None:
    """Test astx.LiteralInt32."""
    # Create a LiteralInt32 node
    literal_int32_node = astx.LiteralInt32(value=42)

    # Generate Python code
    generated_code = translate(literal_int32_node)
    expected_code = "42"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_literal_float16() -> None:
    """Test astx.LiteralFloat16."""
    # Create a LiteralFloat16 node
    literal_float16_node = astx.LiteralFloat16(value=3.14)

    # Generate Python code
    generated_code = translate(literal_float16_node)
    expected_code = "3.14"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_literal_float32() -> None:
    """Test astx.LiteralFloat32."""
    # Create a LiteralFloat32 node
    literal_float32_node = astx.LiteralFloat32(value=2.718)

    # Generate Python code
    generated_code = translate(literal_float32_node)
    expected_code = "2.718"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_literal_float64() -> None:
    """Test astx.LiteralFloat64."""
    # Create a LiteralFloat64 node
    literal_float64_node = astx.LiteralFloat64(value=1.414)

    # Generate Python code
    generated_code = translate(literal_float64_node)
    expected_code = "1.414"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_literal_complex32() -> None:
    """Test astx.LiteralComplex32."""
    # Create a LiteralComplex32 node
    literal_complex32_node = astx.LiteralComplex32(real=1, imag=2.8)

    # Generate Python code
    generated_code = translate(literal_complex32_node)
    expected_code = "complex(1, 2.8)"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_literal_complex64() -> None:
    """Test astx.LiteralComplex64."""
    # Create a LiteralComplex64 node
    literal_complex64_node = astx.LiteralComplex64(real=3.5, imag=4)

    # Generate Python code
    generated_code = translate(literal_complex64_node)
    expected_code = "complex(3.5, 4)"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_typecastexpr() -> None:
    """Test astx.TypeCastExpr."""
    # Expression to cast
    expr = astx.Variable(name="x")
    # Target type for casting
    target_type = astx.Int32()
    # Create the TypeCastExpr
    cast_expr = astx.TypeCastExpr(expr=expr, target_type=target_type)

    generated_code = translate(cast_expr)
    expected_code = "cast(int, x)"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_utf8_char() -> None:
    """Test astx.Utf8Char."""
    # Create a Utf8Char node
    utf8_char_node = astx.LiteralUTF8Char(value="c")

    # Generate Python code
    generated_code = translate(utf8_char_node)
    expected_code = repr("c")

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_utf8_string() -> None:
    """Test astx.Utf8String."""
    # Create a Utf8String node
    utf8_string_node = astx.LiteralUTF8String(value="hello")

    # Generate Python code
    generated_code = translate(utf8_string_node)
    expected_code = repr("hello")

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_utf8_char() -> None:
    """Test astx.LiteralUtf8Char."""
    # Create a LiteralUtf8Char node
    literal_utf8_char_node = astx.LiteralUTF8Char(value="a")

    # Generate Python code
    generated_code = translate(literal_utf8_char_node)
    expected_code = repr("a")

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_utf8_string() -> None:
    """Test astx.LiteralUtf8String."""
    # Create a LiteralUtf8String node
    literal_utf8_string_node = astx.LiteralUTF8String(value="world")

    # Generate Python code
    generated_code = translate(literal_utf8_string_node)
    expected_code = repr("world")

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_for_range_loop_expr() -> None:
    """Test `For Range Loop` expression`."""
    decl_a = astx.InlineVariableDeclaration(
        "a", type_=astx.Int32(), value=astx.LiteralInt32(-1)
    )
    start = astx.LiteralInt32(0)
    end = astx.LiteralInt32(10)
    step = astx.LiteralInt32(1)
    body = astx.Block()
    body.append(astx.LiteralInt32(2))

    for_expr = astx.ForRangeLoopExpr(
        variable=decl_a, start=start, end=end, step=step, body=body
    )

    generated_code = translate(for_expr)
    expected_code = "result = [2 for a in range(0, 10, 1)]"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_async_for_range_loop_expr() -> None:
    """Test `Async For Range Loop` expression`."""
    decl_a = astx.InlineVariableDeclaration(
        "a", type_=astx.Int32(), value=astx.LiteralInt32(-1)
    )
    start = astx.LiteralInt32(0)
    end = astx.LiteralInt32(10)
    step = astx.LiteralInt32(1)
    body = astx.Block()
    body.append(astx.LiteralInt32(2))

    for_expr = astx.AsyncForRangeLoopExpr(
        variable=decl_a, start=start, end=end, step=step, body=body
    )

    generated_code = translate(for_expr)
    expected_code = "result = [2 async for a in range(0, 10, 1)]"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_break_stmt() -> None:
    """Test astx.BreakStmt transpilation."""
    # Create a simple loop structure (e.g., WhileStmt)
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(op_code="<", lhs=x_var, rhs=astx.LiteralInt32(5))

    # Create the loop body with a break statement
    body_block = astx.Block(name="while_body")
    body_block.append(astx.BreakStmt())

    while_stmt = astx.WhileStmt(condition=condition, body=body_block)

    # Generate Python code
    generated_code = translate(while_stmt)

    # Expected code for the WhileStmt with break
    expected_code = "\n".join(
        [
            "while (x < 5):",
            "    break",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_continue_stmt() -> None:
    """Test astx.ContinueStmt transpilation."""
    # Create a simple loop structure (e.g., WhileStmt)
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(op_code="<", lhs=x_var, rhs=astx.LiteralInt32(5))

    # Create the loop body with a continue statement
    body_block = astx.Block(name="while_body")
    body_block.append(astx.ContinueStmt())

    while_stmt = astx.WhileStmt(condition=condition, body=body_block)

    # Generate Python code
    generated_code = translate(while_stmt)

    # Expected code for the WhileStmt with continue
    expected_code = "\n".join(
        [
            "while (x < 5):",
            "    continue",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_binary_op() -> None:
    """Test astx.BinaryOp for addition operation."""
    # Create a BinaryOp node for the expression "x + y"
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    binary_op = astx.BinaryOp(op_code="+", lhs=lhs, rhs=rhs)

    # Generate Python code
    generated_code = translate(binary_op)

    # Expected code for the binary operation
    expected_code = "(x + y)"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_while_stmt() -> None:
    """Test astx.WhileStmt."""
    # Define a condition: x < 5
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=astx.LiteralInt32(5),
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Define the loop body: x = x + 1
    update_expr = astx.VariableAssignment(
        name="x",
        value=astx.BinaryOp(
            op_code="+",
            lhs=x_var,
            rhs=astx.LiteralInt32(1),
            loc=astx.SourceLocation(line=2, col=4),
        ),
        loc=astx.SourceLocation(line=2, col=4),
    )

    # Create the body block
    body_block = astx.Block(name="while_body")
    body_block.append(update_expr)

    while_stmt = astx.WhileStmt(
        condition=condition,
        body=body_block,
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Generate Python code
    generated_code = translate(while_stmt)

    # Expected code for the WhileStmt
    expected_code = "\n".join(
        [
            "while (x < 5):",
            "    x = (x + 1)",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_ifexpr_with_else() -> None:
    """Test astx.IfExpr with else block."""
    # determine condition
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )

    # define literals
    lit_2 = astx.LiteralInt32(2)
    lit_3 = astx.LiteralInt32(3)

    # Add statements to the then and else blocks
    then_ = astx.Block()
    else_ = astx.Block()
    then_.append(lit_2)
    else_.append(lit_3)

    # define if Expr
    if_expr = astx.IfExpr(condition=cond, then=then_, else_=else_)

    # Generate Python code
    generated_code = translate(if_expr)
    expected_code = "2 if (1 > 2) else 3"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_while_expr() -> None:
    """Test astx.WhileExpr."""
    # Define a condition: x < 5
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=astx.LiteralInt32(5),
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Define the loop body: x = x + 1
    update_expr = astx.WalrusOp(
        lhs=x_var,
        rhs=astx.BinaryOp(
            op_code="+",
            lhs=x_var,
            rhs=astx.LiteralInt32(1),
        ),
    )

    # Create the body block
    body = astx.Block()
    body.append(update_expr)

    while_stmt = astx.WhileExpr(
        condition=condition,
        body=body,
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Generate Python code
    generated_code = translate(while_stmt)
    expected_code = "[(x := (x + 1)) for _ in iter(lambda: (x < 5), False)]"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_ifexpr_without_else() -> None:
    """Test astx.IfExpr without else block."""
    # determine condition
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )

    # define literals
    lit_2 = astx.LiteralInt32(2)

    # Add statement to the then block
    then_ = astx.Block()
    then_.append(lit_2)

    # define if Expr
    if_expr = astx.IfExpr(condition=cond, then=then_)

    # Generate Python code
    generated_code = translate(if_expr)

    # Expected code for the binary operation
    expected_code = "2 if (1 > 2) else None"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_ifstmt_with_else() -> None:
    """Test astx.IfStmt with else block."""
    # determine condition
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )

    # create then and else blocks
    then_block = astx.Block()
    else_block = astx.Block()

    # define literals
    lit_2 = astx.LiteralInt32(2)
    lit_3 = astx.LiteralInt32(3)

    # define operations
    op1 = lit_2 + lit_3
    op2 = lit_2 - lit_3

    # Add statements to the then and else blocks
    then_block.append(op1)
    else_block.append(op2)

    # define if Stmt
    if_stmt = astx.IfStmt(condition=cond, then=then_block, else_=else_block)

    # Generate Python code
    generated_code = translate(if_stmt)

    # Expected code for the binary operation
    expected_code = "\n".join(
        [
            "if (1 > 2):",
            "    (2 + 3)",
            "else:",
            "    (2 - 3)",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_ifstmt_without_else() -> None:
    """Test astx.IfStmt without else block."""
    # determine condition
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )

    # create then block
    then_block = astx.Block()

    # define literals
    lit_2 = astx.LiteralInt32(2)
    lit_3 = astx.LiteralInt32(3)

    # define operation
    op1 = lit_2 + lit_3

    # Add statement to the then block
    then_block.append(op1)

    # define if Stmt
    if_stmt = astx.IfStmt(condition=cond, then=then_block)

    # Generate Python code
    generated_code = translate(if_stmt)

    # Expected code for the binary operation
    expected_code = "\n".join(
        [
            "if (1 > 2):",
            "    (2 + 3)",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_date_type() -> None:
    """Test Type[astx.Date]."""
    # Generate Python code for the type
    generated_code = translate(astx.Date())
    expected_code = "date"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_time_type() -> None:
    """Test Type[astx.Time]."""
    # Generate Python code for the type
    generated_code = translate(astx.Time())
    expected_code = "time"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_timestamp_type() -> None:
    """Test Type[astx.Timestamp]."""
    # Generate Python code for the type
    generated_code = translate(astx.Timestamp())
    expected_code = "timestamp"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_datetime_type() -> None:
    """Test Type[astx.DateTime]."""
    # Generate Python code for the type
    generated_code = translate(astx.DateTime())
    expected_code = "datetime"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_date() -> None:
    """Test astx.LiteralDate."""
    # Create a LiteralDate node
    literal_date_node = astx.LiteralDate(value="2024-11-24")

    # Generate Python code
    generated_code = translate(literal_date_node)
    expected_code = "datetime.strptime('2024-11-24', '%Y-%m-%d').date()"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_time() -> None:
    """Test astx.LiteralTime."""
    # Create a LiteralTime node
    literal_time_node = astx.LiteralTime(value="14:30:00")

    # Generate Python code
    generated_code = translate(literal_time_node)
    expected_code = "datetime.strptime('14:30:00', '%H:%M:%S').time()"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_timestamp() -> None:
    """Test astx.LiteralTimestamp."""
    # Create a LiteralTimestamp node
    literal_timestamp_node = astx.LiteralTimestamp(value="2024-11-24 14:30:00")

    # Generate Python code
    generated_code = translate(literal_timestamp_node)
    expected_code = (
        "datetime.strptime('2024-11-24 14:30:00', '%Y-%m-%d %H:%M:%S')"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_datetime() -> None:
    """Test astx.LiteralDateTime."""
    # Create a LiteralDateTime node
    literal_datetime_node = astx.LiteralDateTime(value="2024-11-24T14:30:00")

    # Generate Python code
    generated_code = translate(literal_datetime_node)
    expected_code = (
        "datetime.strptime('2024-11-24T14:30:00', '%Y-%m-%dT%H:%M:%S')"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_classdefstmt() -> None:
    """Test astx.ClassDefStmt."""
    # Create a class body
    class_body = astx.Block(name="MyClass_body")
    var1 = astx.Variable(name="var1")
    class_body.append(var1)

    # Create a class definition
    class_def = astx.ClassDefStmt(
        name="MyClass",
        body=class_body,
    )

    # Generate Python code
    generated_code = translate(class_def)
    expected_code = "\n".join(
        [
            "class MyClass:",
            "    var1",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_enumdeclstmt() -> None:
    """Test astx.ClassDeclStmt."""
    # Enum attributes
    var_r = astx.VariableDeclaration(
        name="RED",
        type_=astx.DataType(),
        value=astx.LiteralInt32(1),
    )

    var_g = astx.VariableDeclaration(
        name="GREEN",
        type_=astx.DataType(),
        value=astx.LiteralInt32(2),
    )

    enum_decl = astx.EnumDeclStmt(
        name="Color",
        attributes=[var_r, var_g],
    )

    # Generate Python code
    generated_code = translate(enum_decl)
    expected_code = "\n".join(
        [
            "class Color(Enum):",
            "    RED: Int32 = 1",
            "    GREEN: Int32 = 2",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_variabledeclaration() -> None:
    """Test astx.VariableDeclaration."""
    var_r = astx.VariableDeclaration(
        name="RED",
        type_=astx.DataType(),
        value=astx.LiteralInt32(1),
    )

    # Generate Python code
    generated_code = translate(var_r)
    expected_code = "RED: Int32 = 1"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_structdeclstmt() -> None:
    """Test astx.StructDeclStmt."""
    # Define struct attributes
    attr1 = astx.VariableDeclaration(
        name="id",
        type_=astx.DataType(),
        value=astx.LiteralInt32(3),
    )

    attr2 = astx.VariableDeclaration(
        name="value",
        type_=astx.DataType(),
        value=astx.LiteralInt32(1),
    )

    decorator1 = astx.Variable(name="decorator_one")

    # Create struct declaration
    struct_decl = astx.StructDeclStmt(
        name="DataPoint",
        attributes=[attr1, attr2],
        decorators=[decorator1],
    )

    # Generate Python code
    generated_code = translate(struct_decl)
    expected_code = "\n".join(
        [
            "@dataclass ",
            "class DataPoint:",
            "    id: Int32 = 3",
            "    value: Int32 = 1",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_structdefstmt() -> None:
    """Test astx.StructDefStmt."""
    # Define struct attributes
    attr1 = astx.VariableDeclaration(
        name="id",
        type_=astx.DataType(),
        value=astx.LiteralInt32(3),
    )

    attr2 = astx.VariableDeclaration(
        name="value",
        type_=astx.DataType(),
        value=astx.LiteralInt32(1),
    )

    decorator1 = astx.Variable(name="decorator_one")

    # Create struct declaration
    struct_def = astx.StructDefStmt(
        name="DataPoint",
        attributes=[attr1, attr2],
        decorators=[decorator1],
    )

    # Generate Python code
    generated_code = translate(struct_def)
    expected_code = "\n".join(
        [
            "@dataclass ",
            "class DataPoint:",
            "    id: Int32 = 3",
            "    value: Int32 = 1",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_subscriptexpr_upper_lower() -> None:
    """Test astx.SubscriptExpr (slice)."""
    # Variable
    a_var = astx.Variable(name="a")

    # SubscriptExpr
    subscr_expr = astx.SubscriptExpr(
        value=a_var,
        lower=astx.LiteralInt32(0),
        upper=astx.LiteralInt32(10),
        step=astx.LiteralInt32(2),
    )

    # Generate Python code
    generated_code = translate(subscr_expr)
    expected_code = "a[0:10:2]"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_subscriptexpr_index() -> None:
    """Test astx.SubscriptExpr (index)."""
    # Variable
    a_var = astx.Variable(name="a")

    # SubscriptExpr
    subscr_expr = astx.SubscriptExpr(
        value=a_var,
        index=astx.LiteralInt32(0),
    )

    # Generate Python code
    generated_code = translate(subscr_expr)
    expected_code = "a[0]"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def fn_print(
    arg: astx.LiteralString,
) -> astx.FunctionCall:
    """Return a FunctionCall to print a string."""
    proto = astx.FunctionPrototype(
        name="print",
        args=astx.Arguments(astx.Argument("_", type_=astx.String())),
        return_type=astx.String(),
    )
    fn = astx.FunctionDef(prototype=proto, body=astx.Block())
    return astx.FunctionCall(
        fn=fn,
        args=[arg],
    )


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python>=3.10")
def test_transpiler_switchstmt() -> None:
    """Test astx.SwitchStmt (2 cases + default)."""
    # The expression to match
    value_expr = astx.Variable(name="x")

    # Patterns and corresponding expressions
    condition1 = astx.LiteralInt32(value=1)
    body1 = astx.Block()
    body1.append(fn_print(astx.LiteralString(value="one")))

    condition2 = astx.LiteralInt32(value=2)
    body2 = astx.Block()
    body2.append(fn_print(astx.LiteralString(value="two")))

    body_default = astx.Block()
    body_default.append(fn_print(astx.LiteralString(value="other")))

    # create branches
    case1 = astx.CaseStmt(condition=condition1, body=body1)
    case2 = astx.CaseStmt(condition=condition2, body=body2)
    case_default = astx.CaseStmt(default=True, body=body_default)

    # Create the SwitchStmt
    switch_stmt = astx.SwitchStmt(
        value=value_expr,
        cases=[case1, case2, case_default],
    )

    # Generate Python code
    generated_code = translate(switch_stmt)
    expected_code = "\n".join(
        [
            "match x:",
            "    case 1:",
            "        print('one')",
            "    case 2:",
            "        print('two')",
            "    case _:",
            "        print('other')",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_yieldexpr_whilestmt() -> None:
    """Test astx.YieldExpr (using WhileStmt)."""
    # Create the `while True` loop
    while_cond = astx.LiteralBoolean(True)
    while_body = astx.Block()

    # Create the `yield` expression
    yield_expr = astx.YieldExpr(value=astx.LiteralInt32(1))

    # Assign the result of `yield` back to `value`
    assign_value = astx.VariableAssignment(name="value", value=yield_expr)

    # Add the assignment to the loop body
    while_body.append(assign_value)

    # Define the `while` loop and add it to the function body
    while_stmt = astx.WhileStmt(condition=while_cond, body=while_body)

    # Generate Python code
    generated_code = translate(while_stmt)
    expected_code = "\n".join(
        [
            "while True:",
            "    value = yield 1",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_yieldstmt_whilestmt() -> None:
    """Test astx.YieldStmt (using WhileStmt)."""
    # Create the `while True` loop
    while_cond = astx.LiteralBoolean(True)
    while_body = astx.Block()

    yield_stmt = astx.YieldExpr(value=astx.LiteralInt32(1))

    assign_value = astx.VariableAssignment(name="value", value=yield_stmt)

    while_body.append(assign_value)

    while_stmt = astx.WhileStmt(condition=while_cond, body=while_body)

    # Generate Python code
    generated_code = translate(while_stmt)
    expected_code = "\n".join(
        [
            "while True:",
            "    value = yield 1",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_yieldfromexpr_whilestmt() -> None:
    """Test astx.YieldFromExpr (using WhileStmt)."""
    # Create the `while True` loop
    while_cond = astx.LiteralBoolean(True)
    while_body = astx.Block()

    # Create the `yieldfrom` expression
    yieldfrom_expr = astx.YieldFromExpr(value=astx.Variable("x"))

    # Assign the result of `yieldfrom` back to `value`
    assign_value = astx.VariableAssignment(name="value", value=yieldfrom_expr)

    # Add the assignment to the loop body
    while_body.append(assign_value)

    # Define the `while` loop and add it to the function body
    while_stmt = astx.WhileStmt(condition=while_cond, body=while_body)

    # Generate Python code
    generated_code = translate(while_stmt)
    expected_code = "\n".join(
        [
            "while True:",
            "    value = yield from x",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_assignmentexpr() -> None:
    """Test astx.AssignmentExpr."""
    var_a = astx.Variable(name="a")
    var_b = astx.Variable(name="b")

    # create assignment expression
    assign_expr = astx.AssignmentExpr(
        targets=[var_a, var_b], value=astx.LiteralInt32(1)
    )

    # Generate Python code
    generated_code = translate(assign_expr)
    expected_code = "a = b = 1"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_delete_stmt() -> None:
    """Test astx.DeleteStmt transpilation."""
    # Create identifiers to be deleted
    var1 = astx.Identifier(value="x")
    var2 = astx.Identifier(value="y")

    # Create a DeleteStmt with multiple targets
    delete_stmt = astx.DeleteStmt(value=[var1, var2])

    # Generate Python code
    generated_code = translate(delete_stmt)
    expected_code = "del x, y"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )

    # Test single target deletion
    single_delete = astx.DeleteStmt(value=[var1])
    generated_code = translate(single_delete)
    expected_code = "del x"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_throwstmt() -> None:
    """Test astx.ThrowStmt."""
    # create throw statement
    throw_stmt = astx.ThrowStmt()

    # Generate Python code
    generated_code = translate(throw_stmt)
    expected_code = "raise"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_exception_handler_stmt() -> None:
    """Test astx.ExceptionHandlerStmt."""
    # Create the "try" block
    try_body = astx.Block()
    try_body.append(fn_print(astx.LiteralString(value="passed")))

    # Create the "except" block
    exception_types = [astx.Identifier("A")]
    except_body1 = astx.Block()
    except_body1.append(fn_print(astx.LiteralString(value="failed")))

    handler1 = astx.CatchHandlerStmt(
        name=astx.Identifier("e"), types=exception_types, body=except_body1
    )

    try_except_stmt = astx.ExceptionHandlerStmt(
        body=try_body, handlers=[handler1]
    )

    # Generate Python code
    generated_code = translate(try_except_stmt)
    expected_code = "\n".join(
        [
            "try:",
            "    print('passed')",
            "except (A) as e:",
            "    print('failed')",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_exception_handler_stmt_with_finally() -> None:
    """Test astx.ExceptionHandlerStmt with FinallyHandler."""
    # Create the "try" block
    try_body = astx.Block()
    try_body.append(fn_print(astx.LiteralString(value="passed")))

    # Create the "except" block
    exception_types = [astx.Identifier("A"), astx.Identifier("B")]
    except_body = astx.Block()
    except_body.append(fn_print(astx.LiteralString(value="failed")))

    handler1 = astx.CatchHandlerStmt(
        name=astx.Identifier("e"), types=exception_types, body=except_body
    )

    # Create the "finally" block
    finally_body = astx.Block()
    finally_body.append(fn_print(astx.LiteralString(value="run complete")))

    finally_handler = astx.FinallyHandlerStmt(body=finally_body)

    # Construct the full "try-except" statement
    try_except_stmt = astx.ExceptionHandlerStmt(
        body=try_body,
        handlers=[handler1],
        finally_handler=finally_handler,
    )

    # Generate Python code
    generated_code = translate(try_except_stmt)
    expected_code = "\n".join(
        [
            "try:",
            "    print('passed')",
            "except (A ,B) as e:",
            "    print('failed')",
            "finally:",
            "    print('run complete')",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_and_op() -> None:
    """Test transpiler for AndOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.AndOp(lhs=lhs, rhs=rhs)

    generated_code = translate(op)

    expected_code = "x and y"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_or_op() -> None:
    """Test transpiler for OrOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.OrOp(lhs=lhs, rhs=rhs)

    generated_code = translate(op)

    expected_code = "x or y"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_xor_op() -> None:
    """Test transpiler for XorOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.XorOp(lhs=lhs, rhs=rhs)

    generated_code = translate(op)

    expected_code = "x ^ y"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_nand_op() -> None:
    """Test transpiler for NandOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.NandOp(lhs=lhs, rhs=rhs)

    generated_code = translate(op)

    expected_code = "not (x and y)"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_nor_op() -> None:
    """Test transpiler for NorOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.NorOp(lhs=lhs, rhs=rhs)

    generated_code = translate(op)

    expected_code = "not (x or y)"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_xnor_op() -> None:
    """Test transpiler for XnorOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.XnorOp(lhs=lhs, rhs=rhs)

    generated_code = translate(op)

    expected_code = "not (x ^ y)"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_group_expr() -> None:
    """Test struct representation."""
    grp = astx.ParenthesizedExpr(
        astx.AndOp(astx.LiteralBoolean(True), astx.LiteralBoolean(False))
    )
    generated_code = translate(grp)
    expected_code = "(True and False)"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_functionasyncdef() -> None:
    """Test astx.FunctionAsyncDef."""
    arg_a = astx.Argument(
        "a", type_=astx.Int32(), default=astx.LiteralInt32(1)
    )
    proto = astx.FunctionPrototype(
        name="aget",
        args=astx.Arguments(arg_a),
        return_type=astx.Int32(),
    )
    var_a = astx.Variable("a")

    return_stmt = astx.FunctionReturn(value=var_a)

    fn_block = astx.Block()
    fn_block.append(return_stmt)

    fn_a = astx.FunctionAsyncDef(prototype=proto, body=fn_block)

    # Generate Python code
    generated_code = translate(fn_a)
    expected_code = "\n".join(
        [
            "async def aget(a: int) -> int:",
            "    return a",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_await_expr_() -> None:
    """Test astx.AwaitExpr."""
    var_a = astx.Variable("a")
    await_expr = astx.AwaitExpr(value=var_a)

    # Generate Python code
    generated_code = translate(await_expr)
    expected_code = "await a"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_list() -> None:
    """Test astx.LiteralList."""
    lit_list = astx.LiteralList(
        [astx.LiteralInt32(1), astx.LiteralInt32(2), astx.LiteralInt32(3)]
    )
    generated_code = translate(lit_list)
    expected_code = "[1, 2, 3]"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_tuple() -> None:
    """Test astx.LiteralTuple."""
    lit_tuple = astx.LiteralTuple((astx.LiteralInt32(1), astx.LiteralInt32(2)))

    generated_code = translate(lit_tuple)
    expected_code = "(1, 2)"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_set() -> None:
    """Test astx.LiteralSet."""
    lit_set = astx.LiteralSet(
        {astx.LiteralInt32(1), astx.LiteralInt32(2), astx.LiteralInt32(3)}
    )

    generated_code = translate(lit_set)
    expected_code = "{1, 2, 3}"

    # We need to eval the string because generated_code
    # can contain a permuted version of the set
    assert ast.literal_eval(generated_code) == ast.literal_eval(
        expected_code
    ), f"@Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_dict() -> None:
    """Test astx.LiteralDict."""
    lit_dict = astx.LiteralDict(
        {
            astx.LiteralInt32(1): astx.LiteralInt32(10),
            astx.LiteralInt32(2): astx.LiteralInt32(20),
        }
    )

    generated_code = translate(lit_dict)
    expected_code = "{1: 10, 2: 20}"

    # We need to eval the string because generated_code
    # can contain a permuted version of the dict
    assert ast.literal_eval(generated_code) == ast.literal_eval(
        expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_do_while_stmt() -> None:
    """Test astx.DoWhileStmt."""
    # Define a condition: x < 5
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=astx.LiteralInt32(5),
        loc=astx.SourceLocation(line=2, col=4),
    )

    # Define the loop body: x = x + 1
    update_expr = astx.VariableAssignment(
        name="x",
        value=astx.BinaryOp(
            op_code="+",
            lhs=x_var,
            rhs=astx.LiteralInt32(1),
            loc=astx.SourceLocation(line=1, col=0),
        ),
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Create the body block
    body_block = astx.Block(name="do_while_body")
    body_block.append(update_expr)

    do_while_stmt = astx.DoWhileStmt(
        body=body_block,
        condition=condition,
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(do_while_stmt)

    # Expected code for DoWhileStmt
    expected_code = "\n".join(
        [
            "while True:",
            "    x = (x + 1)",
            "    if not (x < 5):",
            "        break",
        ]
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_do_while_expr() -> None:
    """Test astx.DoWhileExpr."""
    # Define a condition: x < 5
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=astx.LiteralInt32(5),
        loc=astx.SourceLocation(line=2, col=4),
    )

    # Define the loop body: x = x + 1
    update_expr = astx.WalrusOp(
        lhs=x_var,
        rhs=astx.BinaryOp(
            op_code="+",
            lhs=x_var,
            rhs=astx.LiteralInt32(1),
        ),
    )

    # Create the body block
    body = astx.Block()
    body.append(update_expr)

    do_while_expr = astx.DoWhileExpr(
        body=body,
        condition=condition,
    )

    # Generate Python code
    generated_code = translate(do_while_expr)
    expected_code = (
        "[(x := (x + 1)) for _ in iter(lambda: True, False) if ((x < 5))]"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_generator_expr() -> None:
    """Test astx.GeneratorExpr."""
    # Create the conditions for the generators
    condition_1 = astx.BoolBinaryOp(
        op_code="==",
        lhs=astx.BinaryOp(
            op_code="%",
            lhs=astx.Variable("x"),
            rhs=astx.LiteralInt32(2),
        ),
        rhs=astx.LiteralInt32(1),
    )

    condition_2 = astx.BoolBinaryOp(
        op_code="==",
        lhs=astx.BinaryOp(
            op_code="%",
            lhs=astx.Variable("y"),
            rhs=astx.LiteralInt32(2),
        ),
        rhs=astx.LiteralInt32(0),
    )

    # Create the generators
    generator_1 = astx.ComprehensionClause(
        target=astx.Variable("x"),
        iterable=astx.Variable("list_1"),
        conditions=[condition_1],
    )

    generator_2 = astx.ComprehensionClause(
        target=astx.Variable("y"),
        iterable=astx.Variable("list_2"),
        conditions=[condition_2],
    )

    # Create the generator expression
    gen_expr = astx.GeneratorExpr(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("y")
        ),
        generators=[generator_1, generator_2],
    )

    generated_code = translate(gen_expr)
    expected_code = (
        "((x + y) "
        "for x in list_1 if ((x % 2) == 1) "
        "for y in list_2 if ((y % 2) == 0))"
    )
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_list_comprehension() -> None:
    """Test ListComprehension."""
    # Create the conditions for the generator
    condition_1 = astx.BinaryOp(
        op_code=">",
        lhs=astx.Variable("x"),
        rhs=astx.LiteralInt32(3),
    )

    condition_2 = astx.BinaryOp(
        op_code="<",
        lhs=astx.Variable("x"),
        rhs=astx.LiteralInt32(7),
    )

    # Create the generator
    generator = astx.ComprehensionClause(
        target=astx.Variable("x"),
        iterable=astx.Identifier("range(10)"),
        conditions=[condition_1, condition_2],
    )

    # Create the generator expression
    gen_expr = astx.ListComprehension(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("x")
        ),
        generators=[generator],
    )

    generated_code = translate(gen_expr)
    expected_code = "[(x + x) for x in range(10) if (x > 3) if (x < 7)]"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_set_comprehension() -> None:
    """Test SetComprehension code generation."""
    # Create the conditions for the generator
    condition_1 = astx.BinaryOp(
        op_code=">",
        lhs=astx.Variable("x"),
        rhs=astx.LiteralInt32(3),
    )

    condition_2 = astx.BinaryOp(
        op_code="<",
        lhs=astx.Variable("x"),
        rhs=astx.LiteralInt32(7),
    )

    # Create the generator
    generator = astx.ComprehensionClause(
        target=astx.Variable("x"),
        iterable=astx.Identifier("range(10)"),
        conditions=[condition_1, condition_2],
    )

    # Create the set comprehension
    set_comp = astx.SetComprehension(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("x")
        ),
        generators=[generator],
    )

    generated_code = translate(set_comp)
    expected_code = "{(x + x) for x in range(10) if (x > 3) if (x < 7)}"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_set_comprehension_no_conditions() -> None:
    """Test SetComprehension without conditions."""
    # Create the generator
    generator = astx.ComprehensionClause(
        target=astx.Variable("x"),
        iterable=astx.Identifier("range(10)"),
    )

    # Create the set comprehension
    set_comp = astx.SetComprehension(
        element=astx.Variable("x"),
        generators=[generator],
    )

    generated_code = translate(set_comp)
    expected_code = "{x for x in range(10)}"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_nested_set_comprehension() -> None:
    """Test nested SetComprehension."""
    # Create the generators
    generator_1 = astx.ComprehensionClause(
        target=astx.Variable("x"), iterable=astx.Identifier("range(5)")
    )

    generator_2 = astx.ComprehensionClause(
        target=astx.Variable("y"), iterable=astx.Identifier("range(3)")
    )

    # Create the set comprehension
    set_comp = astx.SetComprehension(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("y")
        ),
        generators=[generator_1, generator_2],
    )

    generated_code = translate(set_comp)
    expected_code = "{(x + y) for x in range(5) for y in range(3)}"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_set_comprehension_with_multiple_conditions() -> None:
    """Test SetComprehension with multiple conditions."""
    # Create the conditions for the generator
    condition_1 = astx.BinaryOp(
        op_code="%",
        lhs=astx.Variable("x"),
        rhs=astx.LiteralInt32(2),
    )

    condition_2 = astx.BinaryOp(
        op_code="<",
        lhs=astx.Variable("x"),
        rhs=astx.LiteralInt32(50),
    )

    # Create the generator fot the set comprehension
    generator = astx.ComprehensionClause(
        target=astx.Variable("x"),
        iterable=astx.Identifier("range(100)"),
        conditions=[condition_1, condition_2],
    )

    # Create the set comprehension
    set_comp = astx.SetComprehension(
        element=astx.Variable("x"),
        generators=[generator],
    )

    generated_code = translate(set_comp)
    expected_code = "{x for x in range(100) if (x % 2) if (x < 50)}"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_ellipsis() -> None:
    """Test transpilation of Ellipsis nodes."""
    ellipsis = astx.Ellipsis()

    generated_code = translate(ellipsis)
    expected_code = "..."

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_ellipsis_in_context() -> None:
    """Test Ellipsis transpilation within expressions."""
    ellipsis = astx.Ellipsis()

    value = astx.Variable(name="x")
    subscript = astx.SubscriptExpr(value=value, index=ellipsis)

    generated_code = translate(subscript)
    expected_code = "x[...]"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_starred_simple() -> None:
    """Test simple starred expression transpilation."""
    value = astx.Variable(name="args")
    starred = astx.Starred(value=value)

    generated_code = translate(starred)
    expected_code = "*args"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )
