"""Tests for control flow statements."""
from astx.blocks import Block
from astx.datatypes import Int32, LiteralInt32
from astx.flows import ForCountLoop, ForRangeLoop, If
from astx.operators import BinaryOp, UnaryOp
from astx.variables import Variable


def test_if() -> None:
    """Test `if` statement."""
    op = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    If(condition=op, then=then_block)


def test_if_else() -> None:
    """Test `if`/`else` statement."""
    cond = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    else_block = Block()
    If(condition=cond, then=then_block, else_=else_block)


def test_for_range() -> None:
    """Test `For Range Loop` statement."""
    var_a = Variable("a", type_=Int32, value=LiteralInt32(-1))
    start = LiteralInt32(1)
    end = LiteralInt32(10)
    step = LiteralInt32(1)
    body = Block()
    body.append(LiteralInt32(2))
    ForRangeLoop(variable=var_a, start=start, end=end, step=step, body=body)


def test_for_count() -> None:
    """Test `For Count Loop` statement."""
    var_a = Variable("a", type_=Int32, value=LiteralInt32(0))
    cond = BinaryOp(op_code="<", lhs=var_a, rhs=LiteralInt32(10))
    update = UnaryOp(op_code="++", operand=var_a)
    body = Block()
    body.append(LiteralInt32(2))
    ForCountLoop(initializer=var_a, condition=cond, update=update, body=body)
