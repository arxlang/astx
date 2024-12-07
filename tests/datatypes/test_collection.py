"""Tests for List and Set data types."""

from __future__ import annotations

from typing import Callable, Type

import astx
import pytest

from astx.types.operators import BinaryOp
from astx.variables import Variable

VAR_A = Variable("a")

LIST_LITERAL_CLASSES = [
    astx.LiteralList,
]

SET_LITERAL_CLASSES = [
    astx.LiteralSet,
]


def test_variable() -> None:
    """Test variable for List and Set."""
    var_a = Variable("a")
    var_b = Variable("b")

    BinaryOp(op_code="+", lhs=var_a, rhs=var_b)


@pytest.mark.parametrize("literal_class", LIST_LITERAL_CLASSES)
def test_list_literal(literal_class: Type[astx.Literal]) -> None:
    """Test List literals."""
    lit_a = literal_class([1, 2, 3])
    lit_b = literal_class([4, 5, 6])
    BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)


@pytest.mark.parametrize("literal_class", SET_LITERAL_CLASSES)
def test_set_literal(literal_class: Type[astx.Literal]) -> None:
    """Test Set literals."""
    lit_a = literal_class({1, 2, 3})
    lit_b = literal_class({4, 5, 6})
    BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda literal_class: VAR_A + literal_class([1, 2, 3]), "+"),
        (lambda literal_class: VAR_A == literal_class([1, 2, 3]), "=="),
        (lambda literal_class: VAR_A != literal_class([1, 2, 3]), "!="),
    ],
)
@pytest.mark.parametrize("literal_class", LIST_LITERAL_CLASSES)
def test_bin_ops_list(
    literal_class: Type[astx.Literal],
    fn_bin_op: Callable[[Type[astx.Literal]], BinaryOp],
    op_code: str,
) -> None:
    """Test binary operations on List literals."""
    bin_op = fn_bin_op(literal_class)
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda literal_class: VAR_A + literal_class({1, 2, 3}), "+"),
        (lambda literal_class: VAR_A == literal_class({1, 2, 3}), "=="),
        (lambda literal_class: VAR_A != literal_class({1, 2, 3}), "!="),
    ],
)
@pytest.mark.parametrize("literal_class", SET_LITERAL_CLASSES)
def test_bin_ops_set(
    literal_class: Type[astx.Literal],
    fn_bin_op: Callable[[Type[astx.Literal]], BinaryOp],
    op_code: str,
) -> None:
    """Test binary operations on Set literals."""
    bin_op = fn_bin_op(literal_class)
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda literal_class: +literal_class([1, 2, 3]), "+"),
    ],
)
@pytest.mark.parametrize("literal_class", LIST_LITERAL_CLASSES)
def test_unary_ops_list(
    literal_class: Type[astx.Literal],
    fn_unary_op: Callable[[Type[astx.Literal]], BinaryOp],
    op_code: str,
) -> None:
    """Test unary operations on List literals."""
    unary_op = fn_unary_op(literal_class)
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda literal_class: +literal_class({1, 2, 3}), "+"),
    ],
)
@pytest.mark.parametrize("literal_class", SET_LITERAL_CLASSES)
def test_unary_ops_set(
    literal_class: Type[astx.Literal],
    fn_unary_op: Callable[[Type[astx.Literal]], BinaryOp],
    op_code: str,
) -> None:
    """Test unary operations on Set literals."""
    unary_op = fn_unary_op(literal_class)
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}
