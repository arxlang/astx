from astx.blocks import Block
from astx.datatypes import Int32, Int32Literal
from astx.flows import ForCountLoop, ForRangeLoop, If
from astx.operators import BinaryOp, UnaryOp
from astx.variables import Variable


def test_if():
    op = BinaryOp(op_code=">", lhs=Int32Literal(1), rhs=Int32Literal(2))
    then_block = Block()
    If(condition=op, then=then_block)


def test_if_else():
    cond = BinaryOp(op_code=">", lhs=Int32Literal(1), rhs=Int32Literal(2))
    then_block = Block()
    else_block = Block()
    If(condition=cond, then=then_block, else_=else_block)


def test_for_range():
    var_a = Variable("a", type_=Int32, value=-1)
    start = Int32Literal(1)
    end = Int32Literal(10)
    step = Int32Literal(1)
    body = Block()
    body.append(Int32Literal(2))
    ForRangeLoop(variable=var_a, start=start, end=end, step=step, body=body)


def test_for_count():
    var_a = Variable("a", type_=Int32, value=0)
    cond = BinaryOp(op_code="<", lhs=var_a, rhs=Int32Literal(10))
    update = UnaryOp(op_code="++", operand=var_a)
    body = Block()
    body.append(Int32Literal(2))
    ForCountLoop(initializer=var_a, condition=cond, update=update, body=body)
