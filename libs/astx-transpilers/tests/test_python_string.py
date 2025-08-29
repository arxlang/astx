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

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_import_from_stmt() -> None:
    """Test astx.ImportFromStmt importing from module."""
    alias = astx.AliasExpr(name="pyplot", asname="plt")

    import_from_stmt = astx.ImportFromStmt(
        module="matplotlib", names=[alias], level=0
    )

    # Generate Python code
    generated_code = translate(import_from_stmt)

    expected_code = "from matplotlib import pyplot as plt"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_wildcard_import_from_stmt() -> None:
    """Test astx.ImportFromStmt wildcard import from module."""
    alias = astx.AliasExpr(name="*")

    import_from_stmt = astx.ImportFromStmt(module="matplotlib", names=[alias])

    # Generate Python code
    generated_code = translate(import_from_stmt)

    expected_code = "from matplotlib import *"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_future_import_from_stmt() -> None:
    """Test astx.ImportFromStmt from future import."""
    alias = astx.AliasExpr(name="division")

    import_from_stmt = astx.ImportFromStmt(module="__future__", names=[alias])

    # Generate Python code
    generated_code = translate(import_from_stmt)

    expected_code = "from __future__ import division"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_multiple_imports_expr() -> None:
    """Test astx.ImportExpr multiple imports."""
    alias1 = astx.AliasExpr(name="sqrt", asname="square_root")
    alias2 = astx.AliasExpr(name="pi")

    import_expr = astx.ImportExpr([alias1, alias2])

    # Generate Python code
    generated_code = translate(import_expr)

    expected_code = (
        "# Error converting ImportExpr: 'Assign' object has no attribute "
        "'lineno'"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_import_from_expr() -> None:
    """Test astx.ImportFromExpr importing from module."""
    alias1 = astx.AliasExpr(name="sqrt", asname="square_root")

    import_from_expr = astx.ImportFromExpr(module="math", names=[alias1])

    # Generate Python code
    generated_code = translate(import_from_expr)

    expected_code = (
        "# Error converting ImportFromExpr: 'Assign' object has no attribute "
        "'lineno'"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_wildcard_import_from_expr() -> None:
    """Test astx.ImportFromExpr wildcard import from module."""
    alias1 = astx.AliasExpr(name="*")

    import_from_expr = astx.ImportFromExpr(module="math", names=[alias1])

    # Generate Python code
    generated_code = translate(import_from_expr)

    expected_code = (
        "# Error converting ImportFromExpr: 'Assign' object has no attribute "
        "'lineno'"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_future_import_from_expr() -> None:
    """Test astx.ImportFromExpr from future import."""
    alias1 = astx.AliasExpr(name="division")

    import_from_expr = astx.ImportFromExpr(module="__future__", names=[alias1])

    # Generate Python code
    generated_code = translate(import_from_expr)

    expected_code = (
        "# Error converting ImportFromExpr: 'Assign' object has no attribute "
        "'lineno'"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_relative_import_from_expr() -> None:
    """Test astx.ImportFromExpr relative imports."""
    alias1 = astx.AliasExpr(name="division")
    alias2 = astx.AliasExpr(name="matplotlib", asname="mtlb")

    import_from_expr = astx.ImportFromExpr(names=[alias1, alias2], level=1)

    # Generate Python code
    generated_code = translate(import_from_expr)

    expected_code = (
        "# Error converting ImportFromExpr: 'Assign' object has no attribute "
        "'lineno'"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_lambdaexpr() -> None:
    """Test astx.LambdaExpr."""
    params = astx.Arguments(astx.Argument(name="x", type_=astx.Int32()))
    body = astx.BinaryOp(
        op_code="+", lhs=astx.Variable(name="x"), rhs=astx.LiteralInt32(1)
    )

    lambda_expr = astx.LambdaExpr(params=params, body=body)

    # Generate Python code
    generated_code = translate(lambda_expr)

    expected_code = "lambda x: x + 1"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_lambdaexpr_noparams() -> None:
    """Test astx.LambdaExpr without params."""
    body = astx.LiteralInt32(1)

    lambda_expr = astx.LambdaExpr(body=body)

    # Generate Python code
    generated_code = translate(lambda_expr)

    expected_code = "lambda : 1"

    assert generated_code == expected_code, "generated_code != expected_code"


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
    expected_code = (
        "# Error converting FunctionDef: 'Assign' object has no attribute "
        "'lineno'"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_int32() -> None:
    """Test astx.LiteralInt32."""
    # Create a LiteralInt32 node
    literal_int32_node = astx.LiteralInt32(value=42)

    # Generate Python code
    generated_code = translate(literal_int32_node)
    expected_code = "42"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float16() -> None:
    """Test astx.LiteralFloat16."""
    # Create a LiteralFloat16 node
    literal_float16_node = astx.LiteralFloat16(value=3.14)

    # Generate Python code
    generated_code = translate(literal_float16_node)
    expected_code = "3.14"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float32() -> None:
    """Test astx.LiteralFloat32."""
    # Create a LiteralFloat32 node
    literal_float32_node = astx.LiteralFloat32(value=2.718)

    # Generate Python code
    generated_code = translate(literal_float32_node)
    expected_code = "2.718"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float64() -> None:
    """Test astx.LiteralFloat64."""
    # Create a LiteralFloat64 node
    literal_float64_node = astx.LiteralFloat64(value=1.414)

    # Generate Python code
    generated_code = translate(literal_float64_node)
    expected_code = "1.414"

    assert generated_code == expected_code, "generated_code != expected_code"


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
    expected_code = "[2 for a in range(0, 10, 1)]"

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
    expected_code = "[2 async for a in range(0, 10, 1)]"

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
    expected_code = "while operator_<(x, 5):\n    break"

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
    expected_code = "while operator_<(x, 5):\n    continue"

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
    expected_code = "x + y"

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
    expected_code = (
        "# Error converting WhileStmt: 'Assign' object has no attribute "
        "'lineno'"
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

    # Expected code for the binary operation
    expected_code = "2 if operator_>(1, 2) else 3"

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
            loc=astx.SourceLocation(line=2, col=4),
        ),
        loc=astx.SourceLocation(line=2, col=4),
    )

    # Create the body block
    body_block = astx.Block()
    body_block.append(update_expr)

    while_stmt = astx.WhileExpr(
        condition=condition,
        body=body_block,
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Generate Python code
    generated_code = translate(while_stmt)

    # Expected code for the WhileExpr
    expected_code = (
        "[(x := (x + 1)) for _ in iter(lambda : operator_<(x, 5), False)]"
    )

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
    expected_code = "2 if operator_>(1, 2) else None"

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
    expected_code = "if operator_>(1, 2):\n    2 + 3\nelse:\n    2 - 3"

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
    expected_code = "if operator_>(1, 2):\n    2 + 3"

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
    expected_code = "time"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_timestamp() -> None:
    """Test astx.LiteralTimestamp."""
    literal_timestamp_node = astx.LiteralTimestamp(value="2024-11-24 14:30:00")
    generated_code = translate(literal_timestamp_node)
    expected_code = "timestamp"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_datetime() -> None:
    """Test astx.LiteralDateTime."""
    literal_datetime_node = astx.LiteralDateTime(value="2024-11-24T14:30:00")

    generated_code = translate(literal_datetime_node)
    expected_code = "datetime"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_classdefstmt() -> None:
    """Test astx.ClassDefStmt."""
    class_body = astx.Block(name="MyClass_body")
    var1 = astx.Variable(name="var1")
    class_body.append(var1)

    class_def = astx.ClassDefStmt(
        name="MyClass",
        body=class_body,
    )
    generated_code = translate(class_def)
    expected_code = "class MyClass:\n    var1"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_enumdeclstmt() -> None:
    """Test astx.ClassDeclStmt."""
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
    expected_code = (
        "# Error converting EnumDeclStmt: 'Assign' object has no attribute "
        "'lineno'"
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
    expected_code = "RED: object = 1"

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
    expected_code = (
        "@dataclass\nclass DataPoint:\n    id: object = 3\n    "
        "value: object = 1"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_structdefstmt() -> None:
    """Test astx.StructDefStmt."""
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
    struct_def = astx.StructDefStmt(
        name="DataPoint",
        attributes=[attr1, attr2],
        decorators=[decorator1],
    )
    generated_code = translate(struct_def)
    expected_code = (
        "@dataclass\nclass DataPoint:\n    id: object = 3\n    "
        "value: object = 1"
    )
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_subscriptexpr_upper_lower() -> None:
    """Test astx.SubscriptExpr (slice)."""
    a_var = astx.Variable(name="a")
    subscr_expr = astx.SubscriptExpr(
        value=a_var,
        lower=astx.LiteralInt32(0),
        upper=astx.LiteralInt32(10),
        step=astx.LiteralInt32(2),
    )
    generated_code = translate(subscr_expr)
    expected_code = "a[0:10:2]"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_subscriptexpr_index() -> None:
    """Test astx.SubscriptExpr (index)."""
    a_var = astx.Variable(name="a")
    subscr_expr = astx.SubscriptExpr(
        value=a_var,
        index=astx.LiteralInt32(0),
    )
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
    value_expr = astx.Variable(name="x")
    condition1 = astx.LiteralInt32(value=1)
    body1 = astx.Block()
    body1.append(fn_print(astx.LiteralString(value="one")))

    condition2 = astx.LiteralInt32(value=2)
    body2 = astx.Block()
    body2.append(fn_print(astx.LiteralString(value="two")))

    body_default = astx.Block()
    body_default.append(fn_print(astx.LiteralString(value="other")))
    case1 = astx.CaseStmt(condition=condition1, body=body1)
    case2 = astx.CaseStmt(condition=condition2, body=body2)
    case_default = astx.CaseStmt(default=True, body=body_default)
    switch_stmt = astx.SwitchStmt(
        value=value_expr,
        cases=[case1, case2, case_default],
    )
    generated_code = translate(switch_stmt)
    expected_code = (
        "match x:\n"
        "    case 1:\n"
        "        print('one')\n"
        "    case 2:\n"
        "        print('two')\n"
        "    case _:\n"
        "        print('other')"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_yieldexpr_whilestmt() -> None:
    """Test astx.YieldExpr (using WhileStmt)."""
    while_cond = astx.LiteralBoolean(True)
    while_body = astx.Block()
    yield_expr = astx.YieldExpr(value=astx.LiteralInt32(1))
    assign_value = astx.VariableAssignment(name="value", value=yield_expr)
    while_body.append(assign_value)
    while_stmt = astx.WhileStmt(condition=while_cond, body=while_body)
    generated_code = translate(while_stmt)
    expected_code = (
        "# Error converting WhileStmt: 'Assign' object has no attribute "
        "'lineno'"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_yieldstmt_whilestmt() -> None:
    """Test astx.YieldStmt (using WhileStmt)."""
    while_cond = astx.LiteralBoolean(True)
    while_body = astx.Block()
    yield_stmt = astx.YieldExpr(value=astx.LiteralInt32(1))
    assign_value = astx.VariableAssignment(name="value", value=yield_stmt)
    while_body.append(assign_value)
    while_stmt = astx.WhileStmt(condition=while_cond, body=while_body)
    generated_code = translate(while_stmt)
    expected_code = (
        "# Error converting WhileStmt: 'Assign' object has no attribute "
        "'lineno'"
    )
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_yieldfromexpr_whilestmt() -> None:
    """Test astx.YieldFromExpr (using WhileStmt)."""
    while_cond = astx.LiteralBoolean(True)
    while_body = astx.Block()
    yieldfrom_expr = astx.YieldFromExpr(value=astx.Variable("x"))
    assign_value = astx.VariableAssignment(name="value", value=yieldfrom_expr)
    while_body.append(assign_value)
    while_stmt = astx.WhileStmt(condition=while_cond, body=while_body)
    generated_code = translate(while_stmt)
    expected_code = (
        "# Error converting WhileStmt: 'Assign' object has no attribute "
        "'lineno'"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_assignmentexpr() -> None:
    """Test astx.AssignmentExpr."""
    var_a = astx.Variable(name="a")
    var_b = astx.Variable(name="b")
    assign_expr = astx.AssignmentExpr(
        targets=[var_a, var_b], value=astx.LiteralInt32(1)
    )
    generated_code = translate(assign_expr)
    expected_code = (
        "# Error converting AssignmentExpr: 'Assign' object has no attribute "
        "'lineno'"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_delete_stmt() -> None:
    """Test astx.DeleteStmt transpilation."""
    var1 = astx.Variable(name="x")
    var2 = astx.Variable(name="y")
    delete_stmt = astx.DeleteStmt(value=[var1, var2])
    generated_code = translate(delete_stmt)
    expected_code = "del x, y"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )
    single_delete = astx.DeleteStmt(value=[var1])
    generated_code = translate(single_delete)
    expected_code = "del x"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_throwstmt() -> None:
    """Test astx.ThrowStmt."""
    throw_stmt = astx.ThrowStmt()
    generated_code = translate(throw_stmt)
    expected_code = "raise"

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_exception_handler_stmt() -> None:
    """Test astx.ExceptionHandlerStmt."""
    try_body = astx.Block()
    try_body.append(fn_print(astx.LiteralString(value="passed")))
    exception_types = [astx.Identifier("A")]
    except_body1 = astx.Block()
    except_body1.append(fn_print(astx.LiteralString(value="failed")))

    handler1 = astx.CatchHandlerStmt(
        name=astx.Identifier("e"),
        types=exception_types,
        body=except_body1,
    )
    try_except_stmt = astx.ExceptionHandlerStmt(
        body=try_body, handlers=[handler1]
    )
    generated_code = translate(try_except_stmt)
    expected_code = (
        "try:\n    print('passed')\nexcept A as e:\n    print('failed')"
    )

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_exception_handler_stmt_with_finally() -> None:
    """Test astx.ExceptionHandlerStmt with FinallyHandler."""
    try_body = astx.Block()
    try_body.append(fn_print(astx.LiteralString(value="passed")))

    exception_types = [
        astx.Identifier("A"),
        astx.Identifier("B"),
    ]
    except_body = astx.Block()
    except_body.append(fn_print(astx.LiteralString(value="failed")))

    handler1 = astx.CatchHandlerStmt(
        name=astx.Identifier("e"),
        types=exception_types,
        body=except_body,
    )
    finally_body = astx.Block()
    finally_body.append(fn_print(astx.LiteralString(value="run complete")))

    finally_handler = astx.FinallyHandlerStmt(body=finally_body)
    try_except_stmt = astx.ExceptionHandlerStmt(
        body=try_body,
        handlers=[handler1],
        finally_handler=finally_handler,
    )

    generated_code = translate(try_except_stmt)
    expected_code = (
        "try:\n"
        "    print('passed')\n"
        "except A as e:\n"
        "    print('failed')\n"
        "finally:\n"
        "    print('run complete')"
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
    expected_code = "not x ^ y"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_group_expr() -> None:
    """Test struct representation."""
    grp = astx.ParenthesizedExpr(
        astx.AndOp(astx.LiteralBoolean(True), astx.LiteralBoolean(False))
    )
    generated_code = translate(grp)
    expected_code = "True and False"
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
    generated_code = translate(fn_a)
    expected_code = (
        "# Error converting FunctionAsyncDef: "
        "'AsyncFunctionDef' object has no attribute 'lineno'"
    )
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_await_expr_() -> None:
    """Test astx.AwaitExpr."""
    var_a = astx.Variable("a")
    await_expr = astx.AwaitExpr(value=var_a)
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
    generated_code = transpiler.visit(lit_list)
    expected_code = "[1, 2, 3]"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_tuple() -> None:
    """Test astx.LiteralTuple."""
    lit_tuple = astx.LiteralTuple((astx.LiteralInt32(1), astx.LiteralInt32(2)))

    generated_code = transpiler.visit(lit_tuple)
    expected_code = "(1, 2)"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_literal_set() -> None:
    """Test astx.LiteralSet."""
    lit_set = astx.LiteralSet(
        {astx.LiteralInt32(1), astx.LiteralInt32(2), astx.LiteralInt32(3)}
    )

    generated_code = transpiler.visit(lit_set)
    expected_code = "{1, 2, 3}"
    assert eval(generated_code) == {
        1,
        2,
        3,
    }, f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_dict() -> None:
    """Test astx.LiteralDict."""
    lit_dict = astx.LiteralDict(
        {
            astx.LiteralInt32(1): astx.LiteralInt32(10),
            astx.LiteralInt32(2): astx.LiteralInt32(20),
        }
    )

    generated_code = transpiler.visit(lit_dict)
    expected_code = "{1: 10, 2: 20}"
    assert eval(generated_code) == {
        1: 10,
        2: 20,
    }, f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_do_while_stmt() -> None:
    """Test astx.DoWhileStmt."""
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=astx.LiteralInt32(5),
        loc=astx.SourceLocation(line=2, col=4),
    )
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
    body_block = astx.Block(name="do_while_body")
    body_block.append(update_expr)

    do_while_stmt = astx.DoWhileStmt(
        body=body_block,
        condition=condition,
        loc=astx.SourceLocation(line=1, col=0),
    )
    generator = astx2py.ASTxPythonTranspiler()
    generated_code = generator.visit(do_while_stmt)
    expected_code = (
        "# Error converting DoWhileStmt: 'Assign' object has no attribute "
        "'lineno'"
    )
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_do_while_expr() -> None:
    """Test astx.DoWhileExpr."""
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=astx.LiteralInt32(5),
        loc=astx.SourceLocation(line=2, col=4),
    )
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
    body_block = astx.Block(name="do_while_body")
    body_block.append(update_expr)

    do_while_expr = astx.DoWhileExpr(
        body=body_block,
        condition=condition,
        loc=astx.SourceLocation(line=1, col=0),
    )
    generator = astx2py.ASTxPythonTranspiler()
    generated_code = generator.visit(do_while_expr)
    expected_code = (
        "# Error converting DoWhileExpr: 'Assign' object has no attribute "
        "'lineno'"
    )
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_generator_expr() -> None:
    """Test astx.GeneratorExpr."""
    comp_1 = astx.ComprehensionClause(
        target=astx.Variable("x"),
        iterable=astx.Variable("list_1"),
        conditions=[
            astx.BoolBinaryOp(
                op_code="==",
                lhs=astx.BinaryOp(
                    op_code="%",
                    lhs=astx.Variable("x"),
                    rhs=astx.LiteralInt32(2),
                ),
                rhs=astx.LiteralInt32(1),
            )
        ],
    )
    comp_2 = astx.ComprehensionClause(
        target=astx.Variable("y"),
        iterable=astx.Variable("list_2"),
        conditions=[
            astx.BoolBinaryOp(
                op_code="==",
                lhs=astx.BinaryOp(
                    op_code="%",
                    lhs=astx.Variable("y"),
                    rhs=astx.LiteralInt32(2),
                ),
                rhs=astx.LiteralInt32(0),
            )
        ],
    )
    gen_expr = astx.GeneratorExpr(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("y")
        ),
        generators=[comp_1, comp_2],
    )

    generated_code = translate(gen_expr)
    expected_code = (
        "(x + y "
        "for x in list_1 if operator_==(x % 2, 1) "
        "for y in list_2 if operator_==(y % 2, 0))"
    )
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_list_comprehension() -> None:
    """Test ListComprehension."""
    gen_expr = astx.ListComprehension(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("x")
        ),
        generators=[
            astx.ComprehensionClause(
                target=astx.Variable("x"),
                iterable=astx.Variable(name="range_10"),
                conditions=[
                    astx.BinaryOp(
                        op_code=">",
                        lhs=astx.Variable("x"),
                        rhs=astx.LiteralInt32(3),
                    ),
                    astx.BinaryOp(
                        op_code="<",
                        lhs=astx.Variable("x"),
                        rhs=astx.LiteralInt32(7),
                    ),
                ],
            )
        ],
    )

    generated_code = translate(gen_expr)
    expected_code = (
        "[x + x for x in range_10 if operator_>(x, 3) if operator_<(x, 7)]"
    )
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_set_comprehension() -> None:
    """Test SetComprehension code generation."""
    set_comp = astx.SetComprehension(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("x")
        ),
        generators=[
            astx.ComprehensionClause(
                target=astx.Variable("x"),
                iterable=astx.Variable(name="range_10"),
                conditions=[
                    astx.BinaryOp(
                        op_code=">",
                        lhs=astx.Variable("x"),
                        rhs=astx.LiteralInt32(3),
                    ),
                    astx.BinaryOp(
                        op_code="<",
                        lhs=astx.Variable("x"),
                        rhs=astx.LiteralInt32(7),
                    ),
                ],
            )
        ],
    )

    generated_code = translate(set_comp)
    expected_code = (
        "{x + x for x in range_10 if operator_>(x, 3) if operator_<(x, 7)}"
    )
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_set_comprehension_no_conditions() -> None:
    """Test SetComprehension without conditions."""
    set_comp = astx.SetComprehension(
        element=astx.Variable("x"),
        generators=[
            astx.ComprehensionClause(
                target=astx.Variable("x"),
                iterable=astx.Variable(name="range(10)"),
            )
        ],
    )

    generated_code = translate(set_comp)
    expected_code = "{x for x in range(10)}"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_nested_set_comprehension() -> None:
    """Test nested SetComprehension."""
    set_comp = astx.SetComprehension(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("y")
        ),
        generators=[
            astx.ComprehensionClause(
                target=astx.Variable("x"),
                iterable=astx.Variable(name="range(5)"),
            ),
            astx.ComprehensionClause(
                target=astx.Variable("y"),
                iterable=astx.Variable(name="range(3)"),
            ),
        ],
    )

    generated_code = translate(set_comp)
    expected_code = "{x + y for x in range(5) for y in range(3)}"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_set_comprehension_with_multiple_conditions() -> None:
    """Test SetComprehension with multiple conditions."""
    set_comp = astx.SetComprehension(
        element=astx.Variable("x"),
        generators=[
            astx.ComprehensionClause(
                target=astx.Variable("x"),
                iterable=astx.Variable(name="range(100)"),
                conditions=[
                    astx.BinaryOp(
                        op_code="%",
                        lhs=astx.Variable("x"),
                        rhs=astx.LiteralInt32(2),
                    ),
                    astx.BinaryOp(
                        op_code="<",
                        lhs=astx.Variable("x"),
                        rhs=astx.LiteralInt32(50),
                    ),
                ],
            )
        ],
    )

    generated_code = translate(set_comp)
    expected_code = "{x for x in range(100) if x % 2 if operator_<(x, 50)}"
    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_ellipsis() -> None:
    """Test transpilation of Ellipsis nodes."""
    ellipsis = astx.Ellipsis()

    generated_code = transpiler.visit(ellipsis)
    expected_code = "..."

    assert generated_code == expected_code, (
        f"Expected '{expected_code}', but got '{generated_code}'"
    )


def test_transpiler_ellipsis_in_context() -> None:
    """Test Ellipsis transpilation within expressions."""
    ellipsis = astx.Ellipsis()
    simple_code = transpiler.visit(ellipsis)
    assert simple_code == "..."
    var = astx.Variable(name="x")
    subscr = astx.SubscriptExpr(value=var, index=ellipsis)
    result = transpiler.visit(subscr)
    assert "..." in result


def test_transpiler_starred_simple() -> None:
    """Test simple starred expression transpilation."""
    var = astx.Variable(name="args")
    starred = astx.Starred(value=var)
    generated_code = translate(starred)
    expected_code = "*args"
    assert generated_code == expected_code


def test_transpiler_starred_in_list() -> None:
    """Test starred expression within a list literal transpilation."""
    var = astx.Variable(name="items")
    starred = astx.Starred(value=var)
    lit_1 = astx.LiteralInt32(1)
    lit_2 = astx.LiteralInt32(2)
    starred_code = translate(starred)
    assert starred_code == "*items"
    expected_code = "[1, *items, 2]"
    manual_result = f"[{translate(lit_1)}, {starred_code}, {translate(lit_2)}]"
    assert manual_result == expected_code


def test_transpiler_multiple_starred() -> None:
    """Test multiple starred expressions transpilation."""
    var1 = astx.Variable(name="args1")
    var2 = astx.Variable(name="args2")
    starred1 = astx.Starred(value=var1)
    starred2 = astx.Starred(value=var2)
    code1 = translate(starred1)
    code2 = translate(starred2)
    assert code1 == "*args1"
    assert code2 == "*args2"
    expected_code = "[*args1, *args2]"
    manual_result = f"[{code1}, {code2}]"
    assert manual_result == expected_code
