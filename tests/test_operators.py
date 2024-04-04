"""Module for testing operators."""

import pytest

from astx.datatypes import LiteralInt32
from astx.operators import BinaryOp, UnaryOp

lit_1 = LiteralInt32(1)
lit_2 = LiteralInt32(2)
lit_3 = LiteralInt32(3)


@pytest.mark.parametrize(
    "explicit,implicit",
    [
        (BinaryOp(op_code="+", lhs=lit_1, rhs=lit_2), lit_1 + lit_2),
        (
            BinaryOp(
                op_code="+",
                lhs=lit_1,
                rhs=BinaryOp(op_code="+", lhs=lit_2, rhs=lit_3),
            ),
            lit_1 + (lit_2 + lit_3),
        ),
        (
            BinaryOp(
                op_code="+",
                lhs=BinaryOp(op_code="+", lhs=lit_1, rhs=lit_2),
                rhs=lit_3,
            ),
            lit_1 + lit_2 + lit_3,
        ),
    ],
)
def test_binary_op(explicit: BinaryOp, implicit: BinaryOp) -> None:
    """Test binary operator."""
    assert implicit.get_struct() == explicit.get_struct()


def test_unary_op() -> None:
    """Test unary operator."""
    lit_a = LiteralInt32(1)
    UnaryOp(op_code="+", operand=lit_a)
