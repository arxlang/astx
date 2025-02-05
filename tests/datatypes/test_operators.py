"""Module for testing operators."""

import pytest

from astx.base import ASTKind
from astx.literals.numeric import LiteralInt32
from astx.types.operators import BinaryOp, UnaryOp, WalrusOp

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


def test_walrus_op_init() -> None:
    """Test WalrusOp initialization and properties."""
    # Creating an test instance
    lhs = "x"
    rhs = lit_1  # Using existing LiteralInt32 instance
    walrus = WalrusOp(lhs=lhs, rhs=rhs)
    # Test basic properties
    assert walrus.op_code == ":="
    assert walrus.kind == ASTKind.WalrusOpKind
    assert walrus.lhs == lhs
    assert walrus.rhs == rhs
    # Test string representation
    assert str(walrus) == f"WalrusOp[:=]({lhs} := {rhs})"


def test_walrus_op_get_struct() -> None:
    """Test WalrusOp get_struct method."""
    lhs = "x"
    rhs = lit_1
    walrus = WalrusOp(lhs=lhs, rhs=rhs)
    # Test without simplification
    struct = walrus.get_struct(simplified=False)
    assert "WALRUS[:=]" in struct
    assert struct["WALRUS[:=]"]["lhs"] == lhs
    assert struct["WALRUS[:=]"]["rhs"] == rhs.get_struct(False)
    # Test with simplification
    simple_struct = walrus.get_struct(simplified=True)
    assert "WALRUS[:=]" in simple_struct
