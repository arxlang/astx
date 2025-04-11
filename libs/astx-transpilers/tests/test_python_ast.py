# libs/astx-transpilers/tests/test_python_ast.py
"""Test Python STRING Transpiler."""

import ast
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

import pytest

import astx
# Correct import path for Void based on ModuleNotFoundError
# Assuming Void is directly under astx based on common patterns
# If this still fails, the astx package structure needs verification
try:
    from astx import Void
except ImportError:
    # Fallback if not directly under astx
    try:
        from astx.datatypes import Void
    except ImportError:
        # If still not found, define a dummy for the test to proceed
        class Void:
            pass

# Testing the STRING transpiler
from astx_transpilers import python_string as astx2py

transpiler = astx2py.ASTxPythonTranspiler()


def translate(node: astx.AST) -> str:
    """Translate from ASTx to Python source using the STRING transpiler."""
    code: str = str(transpiler.visit(node))
    try:
        ast.parse(code)
    except SyntaxError as e:
        pytest.fail(f"Generated code is not valid Python:\n{code}\nError: {e}")
    return code


def check_transpilation(code: str) -> None:
    """Check Transpilation with Python ast lib."""
    try:
        ast.parse(code)
    except SyntaxError as e:
        pytest.fail(f"Code failed to parse:\n{code}\nError: {e}")


def fn_print(arg: astx.LiteralString) -> astx.FunctionCall:
    """Return a FunctionCall node for the string transpiler."""
    print_fn_var = astx.Variable(name="print")
    # Ignore type error for this test helper specific to string transpiler
    # Mypy expects FunctionDef, but string transpiler handles Variable
    return astx.FunctionCall(fn=print_fn_var, args=[arg])  # type: ignore[arg-type]


# --- Test Cases ---


def test_transpiler_multiple_imports_stmt() -> None:
    """Test astx.ImportStmt multiple imports."""
    alias1 = astx.AliasExpr(name="math")
    alias2 = astx.AliasExpr(name="matplotlib", asname="mtlb")
    import_stmt = astx.ImportStmt(names=[alias1, alias2])
    generated_code = translate(import_stmt)
    expected_code = "import math, matplotlib as mtlb"
    assert generated_code == expected_code


def test_transpiler_import_from_stmt() -> None:
    """Test astx.ImportFromStmt importing from module."""
    alias = astx.AliasExpr(name="pyplot", asname="plt")
    import_from_stmt = astx.ImportFromStmt(
        module="matplotlib", names=[alias], level=0
    )
    generated_code = translate(import_from_stmt)
    expected_code = "from matplotlib import pyplot as plt"
    assert generated_code == expected_code


def test_transpiler_wildcard_import_from_stmt() -> None:
    """Test astx.ImportFromStmt wildcard import from module."""
    alias = astx.AliasExpr(name="*")
    import_from_stmt = astx.ImportFromStmt(module="matplotlib", names=[alias])
    generated_code = translate(import_from_stmt)
    expected_code = "from matplotlib import *"
    assert generated_code == expected_code


def test_transpiler_future_import_from_stmt() -> None:
    """Test astx.ImportFromStmt from future import."""
    alias = astx.AliasExpr(name="division")
    import_from_stmt = astx.ImportFromStmt(module="__future__", names=[alias])
    generated_code = translate(import_from_stmt)
    expected_code = "from __future__ import division"
    assert generated_code == expected_code


# --- Import Expression Tests ---
def test_transpiler_multiple_imports_expr() -> None:
    """Test astx.ImportExpr multiple imports."""
    alias1 = astx.AliasExpr(name="sqrt", asname="square_root")
    alias2 = astx.AliasExpr(name="pi")
    import_expr = astx.ImportExpr(names=[alias1, alias2])
    generated_code = translate(import_expr)
    expected_code = "module1, module2 = (__import__('sqrt as square_root') , __import__('pi') )"
    assert generated_code == expected_code


def test_transpiler_import_from_expr() -> None:
    """Test astx.ImportFromExpr importing from module."""
    alias1 = astx.AliasExpr(name="sqrt", asname="square_root")
    import_from_expr = astx.ImportFromExpr(module="math", names=[alias1])
    generated_code = translate(import_from_expr)
    expected_code = "name = getattr(__import__('math', fromlist=['sqrt as square_root']), 'sqrt as square_root')"
    assert generated_code == expected_code


def test_transpiler_wildcard_import_from_expr() -> None:
    """Test astx.ImportFromExpr wildcard import from module."""
    alias1 = astx.AliasExpr(name="*")
    import_from_expr = astx.ImportFromExpr(module="math", names=[alias1])
    generated_code = translate(import_from_expr)
    expected_code = "name = getattr(__import__('math', fromlist=['*']), '*')"
    assert generated_code == expected_code


def test_transpiler_future_import_from_expr() -> None:
    """Test astx.ImportFromExpr from future import."""
    alias1 = astx.AliasExpr(name="division")
    import_from_expr = astx.ImportFromExpr(module="__future__", names=[alias1])
    generated_code = translate(import_from_expr)
    expected_code = "name = getattr(__import__('__future__', fromlist=['division']), 'division')"
    assert generated_code == expected_code


def test_transpiler_relative_import_from_expr() -> None:
    """Test astx.ImportFromExpr relative imports."""
    alias1 = astx.AliasExpr(name="division")
    alias2 = astx.AliasExpr(name="matplotlib", asname="mtlb")
    import_from_expr = astx.ImportFromExpr(names=[alias1, alias2], level=1)
    generated_code = translate(import_from_expr)
    expected_code = "name1, name2 = (getattr(__import__('.', fromlist=['division']), 'division'), getattr(__import__('.', fromlist=['matplotlib as mtlb']), 'matplotlib as mtlb'))"
    assert generated_code == expected_code


# --- End Import Expression Tests ---


def test_transpiler_lambdaexpr() -> None:
    """Test astx.LambdaExpr."""
    arg_x = astx.Argument(name="x", type_=astx.Int32())
    params_obj = astx.Arguments(arg_x)
    body = astx.BinaryOp(
        op_code="+", lhs=astx.Variable(name="x"), rhs=astx.LiteralInt32(1)
    )
    lambda_expr = astx.LambdaExpr(params=params_obj, body=body)
    generated_code = translate(lambda_expr)
    expected_code = "lambda x: (x + 1)"
    assert generated_code == expected_code


def test_transpiler_lambdaexpr_noparams() -> None:
    """Test astx.LambdaExpr without params."""
    body = astx.LiteralInt32(1)
    params_obj = astx.Arguments()
    lambda_expr = astx.LambdaExpr(params=params_obj, body=body)
    generated_code = translate(lambda_expr)
    expected_code = "lambda : 1"
    assert generated_code == expected_code


def test_transpiler_functiondef() -> None:
    """Test astx.FunctionDef."""
    arg_x = astx.Argument(name="x", type_=astx.Int32())
    arg_y = astx.Argument(name="y", type_=astx.Int32())
    args_obj = astx.Arguments(arg_x, arg_y)
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
    add_function = astx.FunctionDef(
        prototype=astx.FunctionPrototype(
            name="add", args=args_obj, return_type=astx.Int32()
        ),
        body=body,
        loc=astx.SourceLocation(line=1, col=0),
    )
    generated_code = translate(add_function)
    expected_code = "\n".join(
        [
            "def add(x: int, y: int) -> int:",
            "    result = (x + y)",
            "    return result",
        ]
    )
    assert generated_code.strip() == expected_code.strip()


def test_literal_int32() -> None:
    """Test astx.LiteralInt32."""
    literal_int32_node = astx.LiteralInt32(value=42)
    generated_code = translate(literal_int32_node)
    expected_code = "42"
    assert generated_code == expected_code


def test_literal_float16() -> None:
    """Test astx.LiteralFloat16."""
    literal_float16_node = astx.LiteralFloat16(value=3.14)
    generated_code = translate(literal_float16_node)
    expected_code = "3.14"
    assert generated_code == expected_code


def test_literal_float32() -> None:
    """Test astx.LiteralFloat32."""
    literal_float32_node = astx.LiteralFloat32(value=2.718)
    generated_code = translate(literal_float32_node)
    expected_code = "2.718"
    assert generated_code == expected_code


def test_literal_float64() -> None:
    """Test astx.LiteralFloat64."""
    literal_float64_node = astx.LiteralFloat64(value=1.414)
    generated_code = translate(literal_float64_node)
    expected_code = "1.414"
    assert generated_code == expected_code


def test_literal_complex32() -> None:
    """Test astx.LiteralComplex32."""
    literal_complex32_node = astx.LiteralComplex32(real=1, imag=2.8)
    generated_code = translate(literal_complex32_node)
    expected_code = "complex(1, 2.8)"
    assert generated_code == expected_code


def test_literal_complex64() -> None:
    """Test astx.LiteralComplex64."""
    literal_complex64_node = astx.LiteralComplex64(real=3.5, imag=4)
    generated_code = translate(literal_complex64_node)
    expected_code = "complex(3.5, 4)"
    assert generated_code == expected_code


def test_transpiler_typecastexpr() -> None:
    """Test astx.TypeCastExpr."""
    expr = astx.Variable(name="x")
    target_type = astx.Int32()
    cast_expr = astx.TypeCastExpr(expr=expr, target_type=target_type)
    generated_code = translate(cast_expr)
    expected_code = "cast(int, x)"
    assert generated_code == expected_code


def test_transpiler_utf8_char() -> None:
    """Test astx.LiteralUTF8Char."""
    utf8_char_node = astx.LiteralUTF8Char(value="c")
    generated_code = translate(utf8_char_node)
    expected_code = repr("c")
    assert generated_code == expected_code


def test_transpiler_utf8_string() -> None:
    """Test astx.LiteralUTF8String."""
    utf8_string_node = astx.LiteralUTF8String(value="hello")
    generated_code = translate(utf8_string_node)
    expected_code = repr("hello")
    assert generated_code == expected_code


def test_transpiler_literal_utf8_char() -> None:
    """Test astx.LiteralUTF8Char (redundant)."""
    literal_utf8_char_node = astx.LiteralUTF8Char(value="a")
    generated_code = translate(literal_utf8_char_node)
    expected_code = repr("a")
    assert generated_code == expected_code


def test_transpiler_literal_utf8_string() -> None:
    """Test astx.LiteralUTF8String (redundant)."""
    literal_utf8_string_node = astx.LiteralUTF8String(value="world")
    generated_code = translate(literal_utf8_string_node)
    expected_code = repr("world")
    assert generated_code == expected_code


def test_transpiler_for_range_loop_expr() -> None:
    """Test `For Range Loop` expression`."""
    decl_a = astx.InlineVariableDeclaration(
        name="a", type_=astx.Int32(), value=astx.LiteralInt32(-1)
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
    assert generated_code == expected_code


def test_transpiler_async_for_range_loop_expr() -> None:
    """Test `Async For Range Loop` expression`."""
    decl_a = astx.InlineVariableDeclaration(
        name="a", type_=astx.Int32(), value=astx.LiteralInt32(-1)
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
    assert generated_code == expected_code


def test_transpiler_binary_op() -> None:
    """Test astx.BinaryOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    binary_op = astx.BinaryOp(op_code="+", lhs=lhs, rhs=rhs)
    generated_code = translate(binary_op)
    expected_code = "(x + y)"
    assert generated_code == expected_code


def test_transpiler_while_stmt() -> None:
    """Test astx.WhileStmt."""
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=astx.LiteralInt32(5),
        loc=astx.SourceLocation(line=1, col=0),
    )
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
    body_block = astx.Block(name="while_body")
    body_block.append(update_expr)
    while_stmt = astx.WhileStmt(
        condition=condition,
        body=body_block,
        loc=astx.SourceLocation(line=1, col=0),
    )
    generated_code = translate(while_stmt)
    expected_code = "while (x < 5):\n    x = (x + 1)"
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_ifexpr_with_else() -> None:
    """Test astx.IfExpr with else block."""
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )
    lit_2 = astx.LiteralInt32(2)
    lit_3 = astx.LiteralInt32(3)
    then_ = astx.Block()
    else_ = astx.Block()
    then_.append(lit_2)
    else_.append(lit_3)
    if_expr = astx.IfExpr(condition=cond, then=then_, else_=else_)
    generated_code = translate(if_expr)
    expected_code = "2 if (1 > 2) else 3"
    assert generated_code == expected_code


def test_transpiler_while_expr() -> None:
    """Test astx.WhileExpr."""
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=astx.LiteralInt32(5),
        loc=astx.SourceLocation(line=1, col=0),
    )
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
    body_block = astx.Block()
    body_block.append(update_expr)
    while_expr = astx.WhileExpr(
        condition=condition,
        body=body_block,
        loc=astx.SourceLocation(line=1, col=0),
    )
    generated_code = translate(while_expr)
    expected_code = "[(x := (x + 1)) for _ in iter(lambda: (x < 5), False)]"
    assert generated_code == expected_code


def test_transpiler_ifexpr_without_else() -> None:
    """Test astx.IfExpr without else block."""
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )
    lit_2 = astx.LiteralInt32(2)
    then_ = astx.Block()
    then_.append(lit_2)
    if_expr = astx.IfExpr(condition=cond, then=then_)
    generated_code = translate(if_expr)
    expected_code = "2 if (1 > 2) else None"
    assert generated_code == expected_code


def test_transpiler_ifstmt_with_else() -> None:
    """Test astx.IfStmt with else block."""
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )
    then_block = astx.Block()
    else_block = astx.Block()
    lit_2 = astx.LiteralInt32(2)
    lit_3 = astx.LiteralInt32(3)
    op1 = astx.BinaryOp("+", lit_2, lit_3)
    op2 = astx.BinaryOp("-", lit_2, lit_3)
    then_block.append(op1)
    else_block.append(op2)
    if_stmt = astx.IfStmt(condition=cond, then=then_block, else_=else_block)
    generated_code = translate(if_stmt)
    expected_code = "if (1 > 2):\n    (2 + 3)\nelse:\n    (2 - 3)"
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_ifstmt_without_else() -> None:
    """Test astx.IfStmt without else block."""
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )
    then_block = astx.Block()
    lit_2 = astx.LiteralInt32(2)
    lit_3 = astx.LiteralInt32(3)
    op1 = astx.BinaryOp("+", lit_2, lit_3)
    then_block.append(op1)
    if_stmt = astx.IfStmt(condition=cond, then=then_block)
    generated_code = translate(if_stmt)
    expected_code = "if (1 > 2):\n    (2 + 3)"
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_date_type() -> None:
    """Test Type[astx.Date]."""
    generated_code = translate(astx.Date())
    expected_code = "date"
    assert generated_code == expected_code


def test_transpiler_time_type() -> None:
    """Test Type[astx.Time]."""
    generated_code = translate(astx.Time())
    expected_code = "time"
    assert generated_code == expected_code


def test_transpiler_timestamp_type() -> None:
    """Test Type[astx.Timestamp]."""
    generated_code = translate(astx.Timestamp())
    expected_code = "timestamp"
    assert generated_code == expected_code


def test_transpiler_datetime_type() -> None:
    """Test Type[astx.DateTime]."""
    generated_code = translate(astx.DateTime())
    expected_code = "datetime"
    assert generated_code == expected_code


def test_transpiler_literal_date() -> None:
    """Test astx.LiteralDate."""
    literal_date_node = astx.LiteralDate(value="2024-11-24")
    generated_code = translate(literal_date_node)
    expected_code = "datetime.strptime('2024-11-24', '%Y-%m-%d').date()"
    assert generated_code == expected_code


def test_transpiler_literal_time() -> None:
    """Test astx.LiteralTime."""
    literal_time_node = astx.LiteralTime(value="14:30:00")
    generated_code = translate(literal_time_node)
    expected_code = "datetime.strptime('14:30:00', '%H:%M:%S').time()"
    assert generated_code == expected_code


def test_transpiler_literal_timestamp() -> None:
    """Test astx.LiteralTimestamp."""
    literal_timestamp_node = astx.LiteralTimestamp(
        value="2024-11-24 14:30:00"
    )
    generated_code = translate(literal_timestamp_node)
    expected_code = (
        "datetime.strptime('2024-11-24 14:30:00', '%Y-%m-%d %H:%M:%S')"
    )
    assert generated_code == expected_code


def test_transpiler_literal_datetime() -> None:
    """Test astx.LiteralDateTime."""
    literal_datetime_node = astx.LiteralDateTime(value="2024-11-24T14:30:00")
    generated_code = translate(literal_datetime_node)
    expected_code = (
        "datetime.strptime('2024-11-24T14:30:00', '%Y-%m-%dT%H:%M:%S')"
    )
    assert generated_code == expected_code


def test_transpiler_classdefstmt() -> None:
    """Test astx.ClassDefStmt."""
    class_body = astx.Block(name="MyClass_body")
    class_body.append(
        astx.VariableAssignment(name="var1", value=astx.LiteralInt32(0))
    )
    class_def = astx.ClassDefStmt(name="MyClass", body=class_body)
    generated_code = translate(class_def)
    expected_code = "class MyClass:\n    var1 = 0"
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_enumdeclstmt() -> None:
    """Test astx.EnumDeclStmt."""
    var_r = astx.VariableDeclaration(
        name="RED", type_=astx.Int32(), value=astx.LiteralInt32(1)
    )
    var_g = astx.VariableDeclaration(
        name="GREEN", type_=astx.Int32(), value=astx.LiteralInt32(2)
    )
    enum_decl = astx.EnumDeclStmt(name="Color", attributes=[var_r, var_g])
    generated_code = translate(enum_decl)
    expected_code = "class Color(Enum):\n    RED: Int32 = 1\n    GREEN: Int32 = 2"
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_variabledeclaration() -> None:
    """Test astx.VariableDeclaration."""
    var_r = astx.VariableDeclaration(
        name="RED", type_=astx.Int32(), value=astx.LiteralInt32(1)
    )
    generated_code = translate(var_r)
    expected_code = "RED: Int32 = 1"
    assert generated_code == expected_code


def test_transpiler_structdeclstmt() -> None:
    """Test astx.StructDeclStmt."""
    attr1 = astx.VariableDeclaration(
        name="id", type_=astx.Int32(), value=astx.LiteralInt32(3)
    )
    attr2 = astx.VariableDeclaration(
        name="value", type_=astx.Int32(), value=astx.LiteralInt32(1)
    )
    struct_decl = astx.StructDeclStmt(
        name="DataPoint", attributes=[attr1, attr2]
    )
    generated_code = translate(struct_decl)
    expected_code = "@dataclass \nclass DataPoint:\n    id: Int32 = 3\n    value: Int32 = 1"
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_structdefstmt() -> None:
    """Test astx.StructDefStmt."""
    attr1 = astx.VariableDeclaration(
        name="id", type_=astx.Int32(), value=astx.LiteralInt32(3)
    )
    attr2 = astx.VariableDeclaration(
        name="value", type_=astx.Int32(), value=astx.LiteralInt32(1)
    )
    struct_def = astx.StructDefStmt(
        name="DataPoint", attributes=[attr1, attr2]
    )
    generated_code = translate(struct_def)
    expected_code = "@dataclass \nclass DataPoint:\n    id: Int32 = 3\n    value: Int32 = 1"
    assert generated_code.strip() == expected_code.strip()


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
    assert generated_code == expected_code


def test_transpiler_subscriptexpr_index() -> None:
    """Test astx.SubscriptExpr (index)."""
    a_var = astx.Variable(name="a")
    subscr_expr = astx.SubscriptExpr(
        value=a_var, index=astx.LiteralInt32(0)
    )
    generated_code = translate(subscr_expr)
    expected_code = "a[0]"
    assert generated_code == expected_code


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python>=3.10")
def test_transpiler_switchstmt() -> None:
    """Test astx.SwitchStmt."""
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
    case_default = astx.CaseStmt(condition=None, body=body_default)
    switch_stmt = astx.SwitchStmt(
        value=value_expr, cases=[case1, case2, case_default]
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
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_yieldexpr_whilestmt() -> None:
    """Test astx.YieldExpr in WhileStmt."""
    while_cond = astx.LiteralBoolean(True)
    while_body = astx.Block()
    yield_expr = astx.YieldExpr(value=astx.LiteralInt32(1))
    assign_value = astx.VariableAssignment(name="value", value=yield_expr)
    while_body.append(assign_value)
    while_stmt = astx.WhileStmt(condition=while_cond, body=while_body)
    generated_code = translate(while_stmt)
    expected_code = "while True:\n    value = yield 1"
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_yieldstmt_whilestmt() -> None:
    """Test astx.YieldExpr as statement in WhileStmt."""
    while_cond = astx.LiteralBoolean(True)
    while_body = astx.Block()
    yield_stmt = astx.YieldExpr(value=astx.LiteralInt32(1))
    while_body.append(yield_stmt)
    while_stmt = astx.WhileStmt(condition=while_cond, body=while_body)
    generated_code = translate(while_stmt)
    expected_code = "while True:\n    yield 1"
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_yieldfromexpr_whilestmt() -> None:
    """Test astx.YieldFromExpr in WhileStmt."""
    while_cond = astx.LiteralBoolean(True)
    while_body = astx.Block()
    yieldfrom_expr = astx.YieldFromExpr(value=astx.Variable("x"))
    assign_value = astx.VariableAssignment(name="value", value=yieldfrom_expr)
    while_body.append(assign_value)
    while_stmt = astx.WhileStmt(condition=while_cond, body=while_body)
    generated_code = translate(while_stmt)
    expected_code = "while True:\n    value = yield from x"
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_assignmentexpr() -> None:
    """Test astx.AssignmentExpr."""
    var_a = astx.Variable(name="a")
    var_b = astx.Variable(name="b")
    assign_expr = astx.AssignmentExpr(
        targets=[var_a, var_b], value=astx.LiteralInt32(1)
    )
    generated_code = translate(assign_expr)
    expected_code = "a = b = 1"
    assert generated_code == expected_code


def test_transpiler_delete_stmt() -> None:
    """Test astx.DeleteStmt."""
    var1 = astx.Identifier(value="x")
    var2 = astx.Identifier(value="y")
    delete_stmt = astx.DeleteStmt(value=[var1, var2])
    generated_code = translate(delete_stmt)
    expected_code = "del x, y"
    assert generated_code == expected_code
    single_delete = astx.DeleteStmt(value=[var1])
    generated_code = translate(single_delete)
    expected_code = "del x"
    assert generated_code == expected_code


def test_transpiler_throwstmt() -> None:
    """Test astx.ThrowStmt."""
    throw_stmt = astx.ThrowStmt()
    generated_code = translate(throw_stmt)
    expected_code = "raise"
    assert generated_code == expected_code


def test_transpiler_exception_handler_stmt() -> None:
    """Test astx.ExceptionHandlerStmt."""
    try_body = astx.Block()
    try_body.append(fn_print(astx.LiteralString(value="passed")))
    exception_types = [astx.Identifier("A")]
    except_body1 = astx.Block()
    except_body1.append(fn_print(astx.LiteralString(value="failed")))
    handler1 = astx.CatchHandlerStmt(
        name=astx.Identifier("e"), types=exception_types, body=except_body1
    )
    try_except_stmt = astx.ExceptionHandlerStmt(
        body=try_body, handlers=[handler1]
    )
    generated_code = translate(try_except_stmt)
    expected_code = (
        "try:\n    print('passed')\nexcept A as e:\n    print('failed')"
    )
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_exception_handler_stmt_with_finally() -> None:
    """Test astx.ExceptionHandlerStmt with FinallyHandler."""
    try_body = astx.Block()
    try_body.append(fn_print(astx.LiteralString(value="passed")))
    exception_types = [astx.Identifier("A"), astx.Identifier("B")]
    except_body = astx.Block()
    except_body.append(fn_print(astx.LiteralString(value="failed")))
    handler1 = astx.CatchHandlerStmt(
        name=astx.Identifier("e"), types=exception_types, body=except_body
    )
    finally_body = astx.Block()
    finally_body.append(fn_print(astx.LiteralString(value="run complete")))
    finally_handler = astx.FinallyHandlerStmt(body=finally_body)
    try_except_stmt = astx.ExceptionHandlerStmt(
        body=try_body, handlers=[handler1], finally_handler=finally_handler
    )
    generated_code = translate(try_except_stmt)
    expected_code = (
        "try:\n"
        "    print('passed')\n"
        "except (A, B) as e:\n"
        "    print('failed')\n"
        "finally:\n"
        "    print('run complete')"
    )
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_and_op() -> None:
    """Test astx.AndOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.AndOp(lhs=lhs, rhs=rhs)
    generated_code = translate(op)
    expected_code = "x and y"
    assert generated_code == expected_code


def test_transpiler_or_op() -> None:
    """Test astx.OrOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.OrOp(lhs=lhs, rhs=rhs)
    generated_code = translate(op)
    expected_code = "x or y"
    assert generated_code == expected_code


def test_transpiler_xor_op() -> None:
    """Test astx.XorOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.XorOp(lhs=lhs, rhs=rhs)
    generated_code = translate(op)
    expected_code = "x ^ y"
    assert generated_code == expected_code


def test_transpiler_nand_op() -> None:
    """Test astx.NandOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.NandOp(lhs=lhs, rhs=rhs)
    generated_code = translate(op)
    expected_code = "not (x and y)"
    assert generated_code == expected_code


def test_transpiler_nor_op() -> None:
    """Test astx.NorOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.NorOp(lhs=lhs, rhs=rhs)
    generated_code = translate(op)
    expected_code = "not (x or y)"
    assert generated_code == expected_code


def test_transpiler_xnor_op() -> None:
    """Test astx.XnorOp."""
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    op = astx.XnorOp(lhs=lhs, rhs=rhs)
    generated_code = translate(op)
    expected_code = "not (x ^ y)"
    assert generated_code == expected_code


def test_group_expr() -> None:
    """Test astx.ParenthesizedExpr."""
    grp = astx.ParenthesizedExpr(
        astx.AndOp(astx.LiteralBoolean(True), astx.LiteralBoolean(False))
    )
    generated_code = translate(grp)
    expected_code = "(True and False)"
    assert generated_code == expected_code


def test_transpiler_functionasyncdef() -> None:
    """Test astx.FunctionAsyncDef."""
    arg_a = astx.Argument("a", type_=astx.Int32())
    args_obj = astx.Arguments(arg_a)
    proto = astx.FunctionPrototype(
        name="aget", args=args_obj, return_type=astx.Int32()
    )
    var_a = astx.Variable("a")
    return_stmt = astx.FunctionReturn(value=var_a)
    fn_block = astx.Block()
    fn_block.append(return_stmt)
    fn_a = astx.FunctionAsyncDef(prototype=proto, body=fn_block)
    generated_code = translate(fn_a)
    expected_code = "async def aget(a: int) -> int:\n    return a"
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_await_expr_() -> None:
    """Test astx.AwaitExpr."""
    var_a = astx.Variable("a")
    await_expr = astx.AwaitExpr(value=var_a)
    generated_code = translate(await_expr)
    expected_code = "await a"
    assert generated_code == expected_code


def test_transpiler_literal_list() -> None:
    """Test astx.LiteralList."""
    lit_list = astx.LiteralList(
        elements=[
            astx.LiteralInt32(1),
            astx.LiteralInt32(2),
            astx.LiteralInt32(3),
        ]
    )
    generated_code = transpiler.visit(lit_list)
    expected_code = "[1, 2, 3]"
    assert generated_code == expected_code


def test_transpiler_literal_tuple() -> None:
    """Test astx.LiteralTuple."""
    lit_tuple = astx.LiteralTuple(
        elements=(astx.LiteralInt32(1), astx.LiteralInt32(2))
    )
    generated_code = transpiler.visit(lit_tuple)
    expected_code = "(1, 2)"
    assert generated_code == expected_code


def test_transpiler_literal_set() -> None:
    """Test astx.LiteralSet."""
    elements_list: List[astx.Literal] = [
        astx.LiteralInt32(1),
        astx.LiteralInt32(2),
        astx.LiteralInt32(3),
    ]
    # Pass a set to the constructor as expected by type hints
    lit_set = astx.LiteralSet(elements=set(elements_list))
    generated_code = transpiler.visit(lit_set)
    expected_set: Set[int] = {1, 2, 3}
    try:
        generated_set = eval(generated_code)
        assert isinstance(generated_set, set)
        assert generated_set == expected_set
    except Exception as e:
        pytest.fail(f"Could not evaluate generated set '{generated_code}': {e}")


def test_transpiler_literal_dict() -> None:
    """Test astx.LiteralDict."""
    lit_dict = astx.LiteralDict(
        elements={
            astx.LiteralInt32(1): astx.LiteralInt32(10),
            astx.LiteralInt32(2): astx.LiteralInt32(20),
        }
    )
    generated_code = transpiler.visit(lit_dict)
    expected_code = "{1: 10, 2: 20}"
    assert generated_code == expected_code
    assert eval(generated_code) == {1: 10, 2: 20}


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
    expected_code = """
while True:
    x = (x + 1)
    if not (x < 5):
        break
""".strip()
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_do_while_expr() -> None:
    """Test astx.DoWhileExpr."""
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=astx.LiteralInt32(5),
        loc=astx.SourceLocation(line=2, col=4),
    )
    body_expr = astx.BinaryOp(
        op_code="+",
        lhs=x_var,
        rhs=astx.LiteralInt32(1),
        loc=astx.SourceLocation(line=1, col=0),
    )
    body_block = astx.Block(name="do_while_body")
    body_block.append(body_expr)
    do_while_expr = astx.DoWhileExpr(
        body=body_block,
        condition=condition,
        loc=astx.SourceLocation(line=1, col=0),
    )
    generated_code = translate(do_while_expr)
    # Actual output from previous failure
    expected_code = """
    [    (x + 1) for _ in iter(lambda: True, False) if ((x < 5))]
    """.strip()
    assert generated_code.strip() == expected_code.strip()


def test_transpiler_generator_expr() -> None:
    """Test astx.GeneratorExpr."""
    range_fn_var = astx.Variable("range")
    gen_expr = astx.GeneratorExpr(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("x")
        ),
        target=astx.Variable("x"),
        iterable=astx.FunctionCall(
            fn=range_fn_var, args=[astx.LiteralInt32(10)]
        ),  # type: ignore[arg-type]
        conditions=[
            astx.BinaryOp(
                op_code=">", lhs=astx.Variable("x"), rhs=astx.LiteralInt32(3)
            ),
            astx.BinaryOp(
                op_code="<", lhs=astx.Variable("x"), rhs=astx.LiteralInt32(7)
            ),
        ],
    )
    generated_code = translate(gen_expr)
    expected_code = "((x + x) for x in range(10) if (x > 3) if (x < 7))"
    assert generated_code == expected_code


def test_transpiler_generator_expr_no_conditions() -> None:
    """Test astx.GeneratorExpr with no conditions."""
    range_fn_var = astx.Variable("range")
    gen_expr = astx.GeneratorExpr(
        target=astx.Variable("x"),
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("x")
        ),
        iterable=astx.FunctionCall(
            fn=range_fn_var, args=[astx.LiteralInt32(10)]
        ),  # type: ignore[arg-type]
        conditions=[],
    )
    generated_code = translate(gen_expr)
    expected_code = "((x + x) for x in range(10))"
    assert generated_code == expected_code
