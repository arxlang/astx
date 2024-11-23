"""Tests for control flow statements."""

from astx.base import SourceLocation
from astx.blocks import Block
from astx.datatypes import Int32, LiteralInt32
from astx.flows import (
    ForCountLoopExpr,
    ForCountLoopStmt,
    ForRangeLoopExpr,
    ForRangeLoopStmt,
    IfExpr,
    IfStmt,
    WhileExpr,
    WhileStmt,
)
from astx.operators import BinaryOp, UnaryOp
from astx.variables import InlineVariableDeclaration, Variable
from astx.viz import visualize


def test_if_stmt() -> None:
    """Test `if` statement."""
    op = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    if_stmt = IfStmt(condition=op, then=then_block)

    assert str(if_stmt)
    assert if_stmt.get_struct()
    assert if_stmt.get_struct(simplified=True)
    visualize(if_stmt.get_struct())


def test_if_else_stmt() -> None:
    """Test `if`/`else` statement."""
    cond = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    else_block = Block()
    if_stmt = IfStmt(condition=cond, then=then_block, else_=else_block)

    assert str(if_stmt)
    assert if_stmt.get_struct()
    assert if_stmt.get_struct(simplified=True)
    visualize(if_stmt.get_struct())


def test_if_expr() -> None:
    """Test `if` expression."""
    op = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    if_expr = IfExpr(condition=op, then=then_block)

    assert str(if_expr)
    assert if_expr.get_struct()
    assert if_expr.get_struct(simplified=True)
    visualize(if_expr.get_struct())


def test_if_else_expr() -> None:
    """Test `if`/`else` expression."""
    cond = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    else_block = Block()
    if_expr = IfExpr(condition=cond, then=then_block, else_=else_block)

    assert str(if_expr)
    assert if_expr.get_struct()
    assert if_expr.get_struct(simplified=True)
    visualize(if_expr.get_struct())


def test_for_range_loop_expr() -> None:
    """Test `For Range Loop` expression`."""
    decl_a = InlineVariableDeclaration(
        "a", type_=Int32, value=LiteralInt32(-1)
    )
    start = LiteralInt32(1)
    end = LiteralInt32(10)
    step = LiteralInt32(1)
    body = Block()
    body.append(LiteralInt32(2))
    for_expr = ForRangeLoopExpr(
        variable=decl_a, start=start, end=end, step=step, body=body
    )

    assert str(for_expr)
    assert for_expr.get_struct()
    assert for_expr.get_struct(simplified=True)
    visualize(for_expr.get_struct())


def test_for_range_loop_stmt() -> None:
    """Test `For Range Loop` statement."""
    decl_a = InlineVariableDeclaration(
        "a", type_=Int32, value=LiteralInt32(-1)
    )
    start = LiteralInt32(1)
    end = LiteralInt32(10)
    step = LiteralInt32(1)
    body = Block()
    body.append(LiteralInt32(2))
    for_stmt = ForRangeLoopStmt(
        variable=decl_a, start=start, end=end, step=step, body=body
    )

    assert str(for_stmt)
    assert for_stmt.get_struct()
    assert for_stmt.get_struct(simplified=True)
    visualize(for_stmt.get_struct())


def test_for_count_loop_stmt() -> None:
    """Test `For Count Loop` statement."""
    decl_a = InlineVariableDeclaration("a", type_=Int32, value=LiteralInt32(0))
    var_a = Variable("a")
    cond = BinaryOp(op_code="<", lhs=var_a, rhs=LiteralInt32(10))
    update = UnaryOp(op_code="++", operand=var_a)
    body = Block()
    body.append(LiteralInt32(2))
    for_stmt = ForCountLoopStmt(
        initializer=decl_a, condition=cond, update=update, body=body
    )

    assert str(for_stmt)
    assert for_stmt.get_struct()
    assert for_stmt.get_struct(simplified=True)
    visualize(for_stmt.get_struct())


def test_for_count_loop_expr() -> None:
    """Test `For Count Loop` expression."""
    decl_a = InlineVariableDeclaration("a", type_=Int32, value=LiteralInt32(0))
    var_a = Variable("a")
    cond = BinaryOp(op_code="<", lhs=var_a, rhs=LiteralInt32(10))
    update = UnaryOp(op_code="++", operand=var_a)
    body = Block()
    body.append(LiteralInt32(2))
    for_expr = ForCountLoopExpr(
        initializer=decl_a, condition=cond, update=update, body=body
    )

    assert str(for_expr)
    assert for_expr.get_struct()
    assert for_expr.get_struct(simplified=True)
    visualize(for_expr.get_struct())


def test_while_expr() -> None:
    """Test `WhileExpr` class."""
    # Define a condition: x < 5
    x_var = Variable(name="x")
    condition = BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=LiteralInt32(5),
        loc=SourceLocation(line=1, col=0),
    )

    body_block = Block(name="while_body")

    # Create the WhileExpr
    while_expr = WhileExpr(
        condition=condition, body=body_block, loc=SourceLocation(line=1, col=0)
    )

    assert str(while_expr)
    assert while_expr.get_struct()
    assert while_expr.get_struct(simplified=True)
    visualize(while_expr.get_struct())


def test_while_stmt() -> None:
    """Test `WhileStmt` class."""
    # Define a condition: x < 5
    x_var = Variable(name="x")
    condition = BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=LiteralInt32(5),
        loc=SourceLocation(line=1, col=0),
    )

    body_block = Block(name="while_body")

    # Create the WhileStmt
    while_stmt = WhileStmt(
        condition=condition, body=body_block, loc=SourceLocation(line=1, col=0)
    )

    assert str(while_stmt)
    assert while_stmt.get_struct()
    assert while_stmt.get_struct(simplified=True)
    visualize(while_stmt.get_struct())
