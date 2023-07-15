from astx.datatypes import Int32Literal
from astx.operators import BinaryOp, UnaryOp


def test_binary_op():
    lit_a = Int32Literal(1)
    lit_b = Int32Literal(2)
    BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)


def test_unary_op():
    lit_a = Int32Literal(1)
    UnaryOp(op_code="+", operand=lit_a)
