"""Tests for control flow statements."""

from astx.blocks import Block
from astx.datatypes import Int32, LiteralInt32
from astx.flows import ForCountLoop, ForRangeExpr, ForRangeLoop, If
from astx.modifiers import MutabilityKind
from astx.operators import BinaryOp, UnaryOp
from astx.variables import InlineVariableDeclaration, Variable
from astx.viz import visualize


def test_if() -> None:
    """Test `if` statement."""
    op = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    if_stmt = If(condition=op, then=then_block)

    assert str(if_stmt)
    assert if_stmt.get_struct()
    assert if_stmt.get_struct(simplified=True)
    visualize(if_stmt.get_struct())


def test_if_else() -> None:
    """Test `if`/`else` statement."""
    cond = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    else_block = Block()
    if_stmt = If(condition=cond, then=then_block, else_=else_block)

    assert str(if_stmt)
    assert if_stmt.get_struct()
    assert if_stmt.get_struct(simplified=True)
    visualize(if_stmt.get_struct())


def test_for_range_expr() -> None:
    """Test `For Range` expression`."""
    range_expr = ForRangeExpr(
        start=LiteralInt32(0), end=LiteralInt32(10), step=LiteralInt32(1)
    )

    assert str(range_expr)
    assert range_expr.get_struct()
    assert range_expr.get_struct(simplified=True)
    visualize(range_expr.get_struct())


def test_for_range_loop_stmt() -> None:
    """Test `For Range Loop` statement."""
    # Create a range expression from 0 to 10 with step 1
    range_expr = ForRangeExpr(
        start=LiteralInt32(0), end=LiteralInt32(10), step=LiteralInt32(1)
    )

    # Variable declaration for the loop variable
    loop_var = InlineVariableDeclaration(
        name="i",
        type_=Int32,
        mutability=MutabilityKind.mutable,
        value=LiteralInt32(0),
    )

    # Loop body
    loop_body = Block(name="loop_body")

    # Create the ForRangeLoop using the range expression
    for_loop_stmt = ForRangeLoop(
        variable=loop_var,
        range_expr=range_expr,
        body=loop_body,
    )

    assert str(for_loop_stmt)
    assert for_loop_stmt.get_struct()
    assert for_loop_stmt.get_struct(simplified=True)
    visualize(for_loop_stmt.get_struct())


def test_for_count() -> None:
    """Test `For Count Loop` statement."""
    decl_a = InlineVariableDeclaration("a", type_=Int32, value=LiteralInt32(0))
    var_a = Variable("a")
    cond = BinaryOp(op_code="<", lhs=var_a, rhs=LiteralInt32(10))
    update = UnaryOp(op_code="++", operand=var_a)
    body = Block()
    body.append(LiteralInt32(2))
    for_stmt = ForCountLoop(
        initializer=decl_a, condition=cond, update=update, body=body
    )

    assert str(for_stmt)
    assert for_stmt.get_struct()
    assert for_stmt.get_struct(simplified=True)
    visualize(for_stmt.get_struct())
