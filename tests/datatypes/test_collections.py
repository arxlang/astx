"""Tests for List, Set, Map, Tuple, and Dictionary literals."""

from __future__ import annotations

from typing import Callable, Type

import astx
import pytest

from astx.literals.collection import (
    LiteralList,
    LiteralSet,
    LiteralMap,
    LiteralTuple,
    LiteralDictionary,
)
from astx.types.operators import BinaryOp, UnaryOp
from astx.variables import Variable

VAR_A = Variable("a")

COLLECTION_LITERAL_CLASSES = [
    LiteralList,
    LiteralSet,
    LiteralMap,
    LiteralTuple,
    LiteralDictionary,
]


def test_variable_collections() -> None:
    """Test variable declaration with collection types."""
    var_list = Variable("list_var")
    var_set = Variable("set_var")
    BinaryOp(op_code="+", lhs=var_list, rhs=var_set)


@pytest.mark.parametrize("literal_class", COLLECTION_LITERAL_CLASSES)
def test_literal_initialization(literal_class: Type[astx.Literal]) -> None:
    """Test collection literals initialization."""
    sample_data = {
        LiteralList: [1, 2, 3],
        LiteralSet: {1, 2, 3},
        LiteralMap: {"key1": "value1", "key2": "value2"},
        LiteralTuple: (1, 2, 3),
        LiteralDictionary: {"key1": "value1", "key2": 42},
    }
    literal_instance = literal_class(sample_data[literal_class])
    assert str(literal_instance) != ""
    assert repr(literal_instance) != ""
    assert literal_instance.get_struct() != {}
    assert literal_instance.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda literal_class: BinaryOp("+", VAR_A, literal_class([1, 2, 3])), "+"),
        (lambda literal_class: BinaryOp("==", VAR_A, literal_class([1, 2, 3])), "=="),
        (lambda literal_class: BinaryOp("!=", VAR_A, literal_class([1, 2, 3])), "!="),
        (lambda literal_class: BinaryOp(">", VAR_A, literal_class([1, 2, 3])), ">"),
        (lambda literal_class: BinaryOp(">=", VAR_A, literal_class([1, 2, 3])), ">="),
        (lambda literal_class: BinaryOp("<", VAR_A, literal_class([1, 2, 3])), "<"),
        (lambda literal_class: BinaryOp("<=", VAR_A, literal_class([1, 2, 3])), "<="),
    ],
)
@pytest.mark.parametrize("literal_class", COLLECTION_LITERAL_CLASSES)
def test_binary_operations(
    literal_class: Type[astx.Literal],
    fn_bin_op: Callable[[Type[astx.Literal]], BinaryOp],
    op_code: str,
) -> None:
    """Test binary operations on collection literals."""
    sample_data = {
        LiteralList: [1, 2, 3],
        LiteralSet: {1, 2, 3},
        LiteralMap: {"key1": "value1"},
        LiteralTuple: (1, 2, 3),
        LiteralDictionary: {"key1": "value1"},
    }
    bin_op = fn_bin_op(literal_class)
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda literal_class: UnaryOp("+", literal_class([1, 2, 3])), "+"),
        (lambda literal_class: UnaryOp("-", literal_class([1, 2, 3])), "-"),
    ],
)
@pytest.mark.parametrize("literal_class", COLLECTION_LITERAL_CLASSES)
def test_unary_operations(
    literal_class: Type[astx.Literal],
    fn_unary_op: Callable[[Type[astx.Literal]], UnaryOp],
    op_code: str,
) -> None:
    """Test unary operations on collection literals."""
    sample_data = {
        LiteralList: [1, 2, 3],
        LiteralSet: {1, 2, 3},
        LiteralMap: {"key1": "value1"},
        LiteralTuple: (1, 2, 3),
        LiteralDictionary: {"key1": "value1"},
    }
    unary_op = fn_unary_op(literal_class)
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}


def test_literal_list_format() -> None:
    """Test LiteralList format."""
    literal_list = LiteralList([1, 2, 3])
    assert literal_list.value == [1, 2, 3]
    assert isinstance(literal_list, LiteralList)


def test_literal_set_format() -> None:
    """Test LiteralSet format."""
    literal_set = LiteralSet({1, 2, 3})
    assert literal_set.value == {1, 2, 3}
    assert isinstance(literal_set, LiteralSet)


def test_literal_map_format() -> None:
    """Test LiteralMap format."""
    literal_map = LiteralMap({"key1": "value1", "key2": "value2"})
    assert literal_map.value == {"key1": "value1", "key2": "value2"}
    assert isinstance(literal_map, LiteralMap)


def test_literal_tuple_format() -> None:
    """Test LiteralTuple format."""
    literal_tuple = LiteralTuple((1, 2, 3))
    assert literal_tuple.value == (1, 2, 3)
    assert isinstance(literal_tuple, LiteralTuple)


def test_literal_dictionary_format() -> None:
    """Test LiteralDictionary format."""
    literal_dict = LiteralDictionary({"key1": "value1", "key2": 42})
    assert literal_dict.value == {"key1": "value1", "key2": 42}
    assert isinstance(literal_dict, LiteralDictionary)
