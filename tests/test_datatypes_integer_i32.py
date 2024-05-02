"""Tests for i32 data type."""

from astx.datatypes import LiteralInt32
from astx.operators import BinaryOp
from astx.variables import Variable


def test_variable_i32() -> None:
    """Test variable i32."""
    var_a = Variable("a")
    var_b = Variable("b")

    BinaryOp(op_code="+", lhs=var_a, rhs=var_b)


def test_literal_i32() -> None:
    """Test literal i32."""
    lit_a = LiteralInt32(value=1)
    lit_b = LiteralInt32(value=2)
    BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)


def test_bin_ops() -> None:
    var_a = Variable("a")
    lit_2 = LiteralInt32(value=2)

    bin_ops_chain = var_a + var_a - var_a * var_a / var_a**lit_2
    mod_2 = bin_ops_chain % LiteralInt32(value=2)

    ne_op = var_a != lit_2
    neg_op = not var_a
    eq_op = var_a == lit_2

    ge_op = var_a >= lit_2
    gt_op = var_a > lit_2
    le_op = var_a <= lit_2
    lt_op = var_a < lit_2


def test_unary_ops() -> None:
    lit_2 = -LiteralInt32(value=2)
