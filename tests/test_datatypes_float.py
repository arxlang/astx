"""Tests for float data types."""

from __future__ import annotations

from typing import Callable, Type

import astx
import pytest

from astx.operators import BinaryOp, UnaryOp
from astx.variables import Variable

VAR_A = Variable("a")

FLOAT_LITERAL_CLASSES = [
    astx.LiteralFloat64,
    astx.LiteralFloat32,
    astx.LiteralFloat16,
]


def test_variable() -> None:
    """Test variable float."""
    var_a = Variable("a")
    var_b = Variable("b")

    BinaryOp(op_code="+", lhs=var_a, rhs=var_b)


@pytest.mark.parametrize("literal_class", FLOAT_LITERAL_CLASSES)
def test_literal(literal_class: Type[astx.Literal]) -> None:
    """Test float literals."""
    lit_a = literal_class(1.23)
    lit_b = literal_class(4.56)
    BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda literal_class: VAR_A + literal_class(1.23), "+"),
        (lambda literal_class: VAR_A - literal_class(1.23), "-"),
        (lambda literal_class: VAR_A / literal_class(1.23), "/"),
        (lambda literal_class: VAR_A // literal_class(1.23), "//"),
        (lambda literal_class: VAR_A * literal_class(1.23), "*"),
        (lambda literal_class: VAR_A ** literal_class(1.23), "^"),
        (lambda literal_class: VAR_A >= literal_class(1.23), ">="),
        (lambda literal_class: VAR_A > literal_class(1.23), ">"),
        (lambda literal_class: VAR_A <= literal_class(1.23), "<="),
        (lambda literal_class: VAR_A < literal_class(1.23), "<"),
        (lambda literal_class: VAR_A == literal_class(1.23), "=="),
        (lambda literal_class: VAR_A != literal_class(1.23), "!="),
        (lambda literal_class: VAR_A % literal_class(1.23), "%"),
    ],
)
@pytest.mark.parametrize("literal_class", FLOAT_LITERAL_CLASSES)
def test_bin_ops(
    literal_class: Type[astx.Literal],
    fn_bin_op: Callable[[Type[astx.Literal]], BinaryOp],
    op_code: str,
) -> None:
    """Test binary operations."""
    bin_op = fn_bin_op(literal_class)
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda literal_class: +literal_class(1.23), "+"),
        (lambda literal_class: -literal_class(1.23), "-"),
    ],
)
@pytest.mark.parametrize("literal_class", FLOAT_LITERAL_CLASSES)
def test_unary_ops(
    literal_class: Type[astx.Literal],
    fn_unary_op: Callable[[Type[astx.Literal]], UnaryOp],
    op_code: str,
) -> None:
    """Test unary operations."""
    unary_op = fn_unary_op(literal_class)
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}