"""Module for testing operators."""

import pytest

from astx.base import ASTKind
from astx.literals.numeric import LiteralInt32
from astx.operators import CompareOp, WalrusOp
from astx.types.operators import BinaryOp, UnaryOp
from astx.variables import Variable

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
    lhs = Variable("x")
    rhs = lit_1
    walrus = WalrusOp(lhs=lhs, rhs=rhs)
    assert walrus.kind == ASTKind.WalrusOpKind
    assert walrus.lhs == lhs
    assert walrus.rhs == rhs
    assert str(walrus) == f"WalrusOp[:=]({lhs} := {rhs})"


def test_walrus_op_get_struct() -> None:
    """Test WalrusOp get_struct method."""
    lhs = Variable("x")
    rhs = lit_1
    walrus = WalrusOp(lhs=lhs, rhs=rhs)
    assert walrus.get_struct(simplified=False)
    assert walrus.get_struct(simplified=True)


def test_compare_op_init() -> None:
    """Test CompareOp initialization and properties."""
    compare = CompareOp(op_code="==", lhs=lit_1, rhs=lit_2)
    assert compare.kind == ASTKind.CompareOpKind
    assert compare.op_code == "=="
    assert compare.lhs == lit_1
    assert compare.rhs == lit_2
    assert str(compare) == f"CompareOp[==]({lit_1} == {lit_2})"


def test_compare_op_get_struct() -> None:
    """Test CompareOp get_struct method."""
    compare = CompareOp(op_code="==", lhs=lit_1, rhs=lit_2)
    assert compare.get_struct(simplified=False)
    assert compare.get_struct(simplified=True)


def test_compare_op_with_variables() -> None:
    """Test CompareOp with variables."""
    var = Variable("x")
    compare = CompareOp(op_code=">", lhs=var, rhs=lit_1)
    assert str(compare) == f"CompareOp[>]({var} > {lit_1})"
    assert compare.lhs == var
    assert compare.rhs == lit_1
