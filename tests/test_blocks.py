from arxast.blocks import Block, Module
from arxast.operators import BinaryOp
from arxast.datatypes import Variable, Int32


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
