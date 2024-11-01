"""Tests for Any data type."""

from __future__ import annotations

from typing import Callable

import pytest

from astx.datatypes import AnyType
from astx.operators import UnaryOp
from astx.variables import Variable

VAR_A = Variable("a")


def test_variable_any() -> None:
    """Test variable with AnyType."""
    var_a = AnyType(5)
    var_b = AnyType(10)

    assert str(var_a) == "Any(5)"
    assert str(var_b) == "Any(10)"


@pytest.mark.parametrize(
    "literal_value",
    [AnyType(5), AnyType(10.5), AnyType(3.14), AnyType(-7), AnyType(0)],
)
def test_any_literal(literal_value: AnyType) -> None:
    """Test AnyType with various literal values."""
    assert str(literal_value) == f"Any({literal_value.value})"
    assert literal_value.get_struct() != {}
    assert literal_value.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda value: +value, "+"),
        (lambda value: -value, "-"),
    ],
)
@pytest.mark.parametrize(
    "value", [AnyType(5), AnyType(10.5), AnyType(-3.14), AnyType(7)]
)
def test_unary_ops_any(
    fn_unary_op: Callable[[AnyType], UnaryOp],
    value: AnyType,
    op_code: str,
) -> None:
    """Test unary operations on AnyType."""
    unary_op = fn_unary_op(value)
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}
