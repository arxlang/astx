from astx.blocks import Block, Module
from astx.operators import BinaryOp
from astx.datatypes import Variable, Int32


def test_block():
    block = Block()
    var_a = Variable("a", Int32)
    var_b = Variable("b", Int32)
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)
    block.append(sum_op)


def test_module():
    module = Module()
    var_a = Variable("a", Int32)
    var_b = Variable("b", Int32)
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)
    module.append(sum_op)
