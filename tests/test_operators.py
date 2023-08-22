"""Module for testing operators."""
from astx.datatypes import Int32Literal
from astx.operators import BinaryOp, UnaryOp


def test_binary_op() -> None:
    """Test binary operator."""
    lit_a = Int32Literal(1)
    lit_b = Int32Literal(2)
    BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)


def test_unary_op() -> None:
    """Test unary operator."""
    lit_a = Int32Literal(1)
    UnaryOp(op_code="+", operand=lit_a)
