"""Test callable ASTx objects."""

import pytest

from astx.blocks import Block
from astx.callables import (
    Argument,
    Arguments,
    AwaitExpr,
    FunctionAsyncDef,
    FunctionCall,
    FunctionDef,
    FunctionPrototype,
    FunctionReturn,
    LambdaExpr,
    YieldExpr,
    YieldFromExpr,
    YieldStmt,
)
from astx.flows import WhileStmt
from astx.literals.numeric import LiteralInt32
from astx.modifiers import ScopeKind, VisibilityKind
from astx.types.numeric import Int32
from astx.types.operators import BinaryOp, UnaryOp
from astx.variables import InlineVariableDeclaration, Variable
from astx.viz import visualize_image


def test_functiondef_creation_with_no_modifiers() -> None:
    """Test function creation with no modifiers."""
    var_a = Argument("a", type_=Int32(), default=LiteralInt32(1))
    var_b = Argument("b", type_=Int32(), default=LiteralInt32(1))

    proto = FunctionPrototype(
        name="add",
        args=Arguments(var_a, var_b),
        return_type=Int32(),
    )

    with pytest.raises(Exception):
        proto.get_struct()

    fn_block = Block()
    fn = FunctionDef(prototype=proto, body=fn_block)

    assert str(fn)
    assert fn.get_struct()
    assert fn.get_struct(simplified=True)

    visualize_image(fn.get_struct())


def test_functiondef_creation_with_modifiers() -> None:
    """Test function creation with modifiers."""
    var_a = Argument("a", type_=Int32(), default=LiteralInt32(1))
    var_b = Argument("b", type_=Int32(), default=LiteralInt32(1))
    proto = FunctionPrototype(
        name="add",
        args=Arguments(var_a, var_b),
        return_type=Int32(),
        visibility=VisibilityKind.public,
        scope=ScopeKind.global_,
    )
    fn_block = Block()
    fn = FunctionDef(prototype=proto, body=fn_block)

    assert str(fn)
    assert fn.get_struct()
    assert fn.get_struct(simplified=True)

    visualize_image(fn.get_struct())


def test_function_call() -> None:
    """Test the FunctionCall class."""
    var_a = Argument("a", type_=Int32(), default=LiteralInt32(1))
    var_b = Argument("b", type_=Int32(), default=LiteralInt32(1))
    proto = FunctionPrototype(
        name="add",
        args=Arguments(var_a, var_b),
        return_type=Int32(),
        visibility=VisibilityKind.public,
        scope=ScopeKind.global_,
    )
    fn_block = Block()
    fn = FunctionDef(prototype=proto, body=fn_block)

    lit_int32_1 = LiteralInt32(1)

    fn_call = FunctionCall(fn=fn, args=(lit_int32_1,))

    assert hash(fn_call) == hash(fn(args=(lit_int32_1,)))
    assert fn_call.get_struct()
    assert fn_call.get_struct(simplified=True)


def test_function_return() -> None:
    """Test the FunctionReturn class."""
    fn_return = FunctionReturn(LiteralInt32(0))

    assert str(fn_return)
    assert fn_return.get_struct()
    assert fn_return.get_struct(simplified=True)


def test_lambdaexpr() -> None:
    """Test the LambdaExpr class."""
    params = Arguments(Argument(name="x", type_=Int32()))
    body = BinaryOp(op_code="+", lhs=Variable(name="x"), rhs=LiteralInt32(1))
    lambda_expr = LambdaExpr(params=params, body=body)

    assert str(lambda_expr)
    assert lambda_expr.get_struct()
    assert lambda_expr.get_struct(simplified=True)


def test_lambdaexpr_noparams() -> None:
    """Test the LambdaExpr class without params."""
    body = LiteralInt32(1)
    lambda_expr = LambdaExpr(body=body)

    assert str(lambda_expr)
    assert lambda_expr.get_struct()
    assert lambda_expr.get_struct(simplified=True)


def test_functionasync_creation_with_no_modifiers() -> None:
    """Test async function creation with no modifiers."""
    var_a = Argument("a", type_=Int32(), default=LiteralInt32(1))
    var_b = Argument("b", type_=Int32(), default=LiteralInt32(1))

    proto = FunctionPrototype(
        name="add",
        args=Arguments(var_a, var_b),
        return_type=Int32(),
    )

    with pytest.raises(Exception):
        proto.get_struct()

    fn_block = Block()
    fn = FunctionAsyncDef(prototype=proto, body=fn_block)

    assert str(fn)
    assert fn.get_struct()
    assert fn.get_struct(simplified=True)

    visualize_image(fn.get_struct())


def test_await_expr() -> None:
    """Test `AwaitExpr` class."""
    await_expr = AwaitExpr(value=LiteralInt32(1))

    assert str(await_expr)
    assert await_expr.get_struct()
    assert await_expr.get_struct(simplified=True)
    visualize_image(await_expr.get_struct())


def test_yield_expr() -> None:
    """Test `YieldExpr` class."""
    yield_expr = YieldExpr(value=LiteralInt32(1))

    assert str(yield_expr)
    assert yield_expr.get_struct()
    assert yield_expr.get_struct(simplified=True)
    visualize_image(yield_expr.get_struct())


def test_yieldfrom_expr() -> None:
    """Test `YieldFromExpr` class."""
    yieldfrom_expr = YieldFromExpr(value=LiteralInt32(1))

    assert str(yieldfrom_expr)
    assert yieldfrom_expr.get_struct()
    assert yieldfrom_expr.get_struct(simplified=True)
    visualize_image(yieldfrom_expr.get_struct())


def test_yield_stmt_basic() -> None:
    """Test basic YieldStmt without a value."""
    yield_stmt = YieldStmt()

    assert str(yield_stmt) == "YieldStmt"
    assert yield_stmt.get_struct()
    assert yield_stmt.get_struct(simplified=True)
    visualize_image(yield_stmt.get_struct())


def test_yield_stmt_with_value() -> None:
    """Test YieldStmt with a literal value."""
    yield_stmt = YieldStmt(value=LiteralInt32(42))

    assert str(yield_stmt)
    assert yield_stmt.get_struct()
    assert yield_stmt.get_struct(simplified=True)
    visualize_image(yield_stmt.get_struct())


def test_yield_stmt_with_expression() -> None:
    """Test YieldStmt with a complex expression."""
    var_x = Variable("x")
    expr = BinaryOp(op_code="+", lhs=var_x, rhs=LiteralInt32(1))
    yield_stmt = YieldStmt(value=expr)

    assert str(yield_stmt)
    assert yield_stmt.get_struct()
    assert yield_stmt.get_struct(simplified=True)
    visualize_image(yield_stmt.get_struct())


def test_yield_stmt_in_generator_block() -> None:
    """Test YieldStmt as part of a generator function block."""
    EXPECTED_BLOCK_LENGTH = 2

    gen_block = Block(name="generator_body")

    counter_decl = InlineVariableDeclaration(
        "i", type_=Int32(), value=LiteralInt32(0)
    )
    gen_block.append(counter_decl)

    i_var = Variable("i")
    condition = BinaryOp(
        op_code="<",
        lhs=i_var,
        rhs=LiteralInt32(5),
    )

    while_block = Block()
    while_block.append(YieldStmt(i_var))
    while_block.append(UnaryOp("++", i_var))

    while_stmt = WhileStmt(condition=condition, body=while_block)
    gen_block.append(while_stmt)

    assert len(gen_block) == EXPECTED_BLOCK_LENGTH
    assert isinstance(gen_block[1], WhileStmt)
    assert str(gen_block[1].body[0])
    visualize_image(gen_block.get_struct())
