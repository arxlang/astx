"""Tests for data types."""
from astx.datatypes import Int32, Int32Literal
from astx.operators import BinaryOp
from astx.variables import Variable


def test_variable_i32() -> None:
    """Test variable i32."""
    var_a = Variable("a", Int32, value=Int32Literal(1))
    var_b = Variable("b", Int32, value=Int32Literal(1))
    BinaryOp(op_code="+", lhs=var_a, rhs=var_b)


def test_literal_i32() -> None:
    """Test literal i32."""
    lit_a = Int32Literal(value=1)
    lit_b = Int32Literal(value=2)
    BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)
