"""Tests for complex data types."""

from __future__ import annotations

from typing import Callable, Type

import astx
import pytest

from astx.operators import BinaryOp, UnaryOp
from astx.variables import Variable

VAR_A = Variable("a")

COMPLEX_LITERAL_CLASSES = [
    astx.datatypes.LiteralComplex64,
    astx.datatypes.LiteralComplex32,
]


def test_complex_variable() -> None:
    """Test variable complex."""
    var_a = Variable("a")
    var_b = Variable("b")

    BinaryOp(op_code="+", lhs=var_a, rhs=var_b)


@pytest.mark.parametrize("literal_class", COMPLEX_LITERAL_CLASSES)
def test_complex_literal(literal_class: Type[astx.Literal]) -> None:
    """Test complex literals."""
    lit_a = literal_class(1.23 + 2.34j)
    lit_b = literal_class(3.45 + 4.56j)
    BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda literal_class: VAR_A + literal_class(1.23 + 2.34j), "+"),
        (lambda literal_class: VAR_A - literal_class(1.23 + 2.34j), "-"),
        (lambda literal_class: VAR_A / literal_class(1.23 + 2.34j), "/"),
    ],
)
@pytest.mark.parametrize("literal_class", COMPLEX_LITERAL_CLASSES)
def test_complex_bin_ops(
    literal_class: Type[astx.Literal],
    fn_bin_op: Callable[[Type[astx.Literal]], BinaryOp],
    op_code: str,
) -> None:
    """Test complex binary operations."""
    bin_op = fn_bin_op(literal_class)
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda literal_class: +literal_class(1.23 + 2.34j), "+"),
        (lambda literal_class: -literal_class(1.23 + 2.34j), "-"),
    ],
)
@pytest.mark.parametrize("literal_class", COMPLEX_LITERAL_CLASSES)
def test_complex_unary_ops(
    literal_class: Type[astx.Literal],
    fn_unary_op: Callable[[Type[astx.Literal]], UnaryOp],
    op_code: str,
) -> None:
    """Test complex unary operations."""
    unary_op = fn_unary_op(literal_class)
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}
