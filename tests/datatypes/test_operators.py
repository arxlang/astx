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
    """Test CompareOp initialization with single operator."""
    compare = CompareOp(left=lit_1, ops=["=="], comparators=[lit_2])
    assert compare.kind == ASTKind.CompareOpKind
    assert compare.ops == ["=="]
    assert compare.left == lit_1
    assert compare.comparators == [lit_2]
    assert str(compare) == "Compare[==]"


def test_compare_op_get_struct() -> None:
    """Test CompareOp get_struct returns correct structure."""
    compare = CompareOp(left=lit_1, ops=["=="], comparators=[lit_2])
    struct = compare.get_struct(simplified=False)
    assert struct["type"] == "COMPARE[==]"
    assert "left" in struct["content"]
    assert "comparators" in struct["content"]
    assert "ops" not in struct["content"]


def test_compare_op_with_variables() -> None:
    """Test CompareOp with variables."""
    var = Variable("x")
    compare = CompareOp(left=var, ops=[">"], comparators=[lit_1])
    assert str(compare) == f"CompareOp(x > {lit_1})"
    assert compare.left == var
    assert compare.comparators[0] == lit_1


def test_chained_compare_op() -> None:
    """Test CompareOp with multiple chained comparisons."""
    var_a = Variable("a")
    var_b = Variable("b") 
    var_c = Variable("c")
    
    compare = CompareOp(
        left=var_a,
        ops=["<", "<"],
        comparators=[var_b, var_c]
    )
    
    assert compare.kind == ASTKind.CompareOpKind
    assert compare.left == var_a
    assert compare.ops == ["<", "<"]
    assert compare.comparators == [var_b, var_c]
    assert str(compare) == "Compare[<, <]"
    
    struct = compare.get_struct(simplified=False)
    assert struct["type"] == "COMPARE[<, <]"
    assert "left" in struct["content"]
    assert "comparators" in struct["content"]
    assert len(struct["content"]["comparators"]) == 2

