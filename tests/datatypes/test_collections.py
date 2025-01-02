"""Tests for the collection literals."""

import astx
import pytest

from astx.literals.collection import (
    LiteralDictionary,
    LiteralList,
    LiteralMap,
    LiteralSet,
    LiteralTuple,
)
from astx.types.operators import BinaryOp
from astx.variables import Variable

VAR_A = Variable("a")

COLLECTION_LITERAL_CLASSES = [
    LiteralList,
    LiteralSet,
    LiteralMap,
    LiteralTuple,
    LiteralDictionary,
]

SAMPLE_DATA = dict[type[astx.Literal], object] = {
    LiteralList: [1, 2, 3],
    LiteralSet: {1, 2, 3},
    LiteralMap: {"key1": "value1", "key2": "value2"},
    LiteralTuple: (1, 2, 3),
    LiteralDictionary: {"key1": "value1", "key2": 42},
}


@pytest.mark.parametrize("literal_class", COLLECTION_LITERAL_CLASSES)
def test_initialization(literal_class: type[astx.Literal]) -> None:
    """Test the initialization of collection literals."""
    literal = literal_class(SAMPLE_DATA[literal_class])
    assert literal.value == SAMPLE_DATA[literal_class]
    assert isinstance(literal, literal_class)


@pytest.mark.parametrize("literal_class", COLLECTION_LITERAL_CLASSES)
def test_binary_operations(literal_class: type[astx.Literal]) -> None:
    """Test binary operations on collection literals."""
    literal = literal_class(SAMPLE_DATA[literal_class])
    bin_op = BinaryOp(op_code="+", lhs=VAR_A, rhs=literal)
    assert bin_op.op_code == "+"
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    struct = bin_op.get_struct()
    assert "op_code" in struct
    assert "lhs" in struct
    assert "rhs" in struct


@pytest.mark.parametrize("literal_class", COLLECTION_LITERAL_CLASSES)
def test_empty_initialization(literal_class: type[astx.Literal]) -> None:
    """Test initialization with empty values."""
    empty_value = type(SAMPLE_DATA[literal_class])()
    literal = literal_class(empty_value)
    assert literal.value == empty_value


@pytest.mark.parametrize("literal_class", COLLECTION_LITERAL_CLASSES)
def test_string_representation(literal_class: type[astx.Literal]) -> None:
    """Test string representation of literals."""
    literal = literal_class(SAMPLE_DATA[literal_class])
    assert (
        str(literal)
        == f"{literal_class.__name__}[{SAMPLE_DATA[literal_class]}]"
    )
    assert repr(literal) != ""
