"""Tests for Any data type."""

from __future__ import annotations

from typing import Any, Callable

import pytest

from astx.datatypes import AnyType  # Import the AnyType class here
from astx.operators import BinaryOp, UnaryOp
from astx.variables import Variable

VAR_A = Variable("a")


def test_variable_any() -> None:
    """Test variable with AnyType."""
    var_a = AnyType(5)
    var_b = AnyType("Hello")

    assert str(var_a) == "Any(5)"
    assert str(var_b) == "Any(Hello)"

    # Test binary operation with AnyType
    result = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)
    assert result.op_code == "+"
    assert str(result) != ""
    assert repr(result) != ""
    assert result.get_struct() != {}
    assert result.get_struct(simplified=True) != {}


@pytest.mark.parametrize("literal_value", [5, "Hello", 3.14, True, None])
def test_any_literal(literal_value: Any) -> None:
    """Test AnyType with various literal values."""
    lit_any = AnyType(literal_value)
    assert str(lit_any) == f"Any({literal_value})"
    assert lit_any.value == literal_value
    assert lit_any.get_struct() != {}
    assert lit_any.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda literal_value: VAR_A + AnyType(literal_value), "+"),
        (lambda literal_value: VAR_A == AnyType(literal_value), "=="),
        (lambda literal_value: VAR_A != AnyType(literal_value), "!="),
    ],
)
def test_bin_ops_any(
    fn_bin_op: Callable[[AnyType], BinaryOp],
    op_code: str,
) -> None:
    """Test binary operations on AnyType."""
    bin_op = fn_bin_op(5)  # Pass an integer to the function
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda value: +AnyType(value), "+"),
        (lambda value: -AnyType(value), "-"),
    ],
)
@pytest.mark.parametrize("value", [5, "Hello", 3.14, True, None])
def test_unary_ops_any(
    fn_unary_op: Callable[[AnyType], UnaryOp],
    value: AnyType,
    op_code: str,
) -> None:
    """Test unary operations on AnyType."""
    unary_op = fn_unary_op(value)  # Test with the specified value
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}
