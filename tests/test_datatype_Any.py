"""Tests for Any data type."""
from __future__ import annotations
from typing import Any as TypeAny
import pytest
from astx.datatypes import Any as AnyDataType
from astx.variables import VariableDeclaration
from astx.variables import Variable

VAR_A = Variable("a")

def test_variable_any() -> None:
    """Test variable Any."""
    any_instance = AnyDataType("SomeValue")
    decl_a = VariableDeclaration(
        name="a", type_=AnyDataType, value=any_instance
    )
    assert decl_a.type_ == AnyDataType.__mro__[0]  # astx.datatypes.Any
    assert decl_a.get_struct()

@pytest.mark.parametrize("value", [
    "StringValue",
    123,
    45.67,
    True,
    [1, 2, 3],
    {"key": "value"},
    (1, 2, 3),
    None,
])
def test_any_literal(value: TypeAny) -> None:
    """Test Any literal initialization."""
    any_instance = AnyDataType(value)
    assert isinstance(any_instance, AnyDataType)
    assert any_instance.value == value
    assert str(any_instance) == f"Any({value})"
    assert any_instance.get_struct() != {}
    assert any_instance.get_struct(simplified=True) != {}

@pytest.mark.parametrize(
    "fn_bin_op, op_code",
    [
        (lambda value: VAR_A + AnyDataType(value), "+"),
        (lambda value: VAR_A == AnyDataType(value), "=="),
        (lambda value: VAR_A != AnyDataType(value), "!="),
    ],
)
@pytest.mark.parametrize("value", [
    "StringValue",
    123,
    45.67,
    True,
    [1, 2, 3],
    {"key": "value"},
    (1, 2, 3),
    None,
])
def test_bin_ops_any(value: TypeAny, fn_bin_op: Callable[[TypeAny], AnyDataType], op_code: str) -> None:
    """Test binary operations on Any data type."""
    bin_op = fn_bin_op(value)
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}

@pytest.mark.parametrize(
    "fn_unary_op, op_code",
    [
        (lambda value: +AnyDataType(value), "+"),
        (lambda value: -AnyDataType(value), "-"),
    ],
)
@pytest.mark.parametrize("value", [
    123,
    -45.67,
])
def test_unary_ops_any(value: TypeAny, fn_unary_op: Callable[[TypeAny], AnyDataType], op_code: str) -> None:
    """Test unary operations on Any data type."""
    unary_op = fn_unary_op(value)
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}

def test_any_struct() -> None:
    """Test the structure of Any instances."""
    any_instance = AnyDataType("Hello")
    struct = any_instance.get_struct()
    assert struct['key'] == "Any"
    assert struct['value'] == "Hello"

    any_instance = AnyDataType([1, 2, 3])
    struct = any_instance.get_struct()
    assert struct['key'] == "Any"
    assert struct['value'] == [1, 2, 3]
