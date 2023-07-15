from arxast.datatypes import Int32, Int32Literal, Variable
from arxast.operators import BinaryOp


def test_variable_i32():
    var_a = Variable("a", Int32)
    var_b = Variable("b", Int32)
    BinaryOp(op_code="+", lhs=var_a, rhs=var_b)


def test_literal_i32():
    lit_a = Int32Literal(value=1)
    lit_b = Int32Literal(value=2)
    BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)
