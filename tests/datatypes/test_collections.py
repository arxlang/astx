"""Tests for Collections data types."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Tuple, Type

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

SAMPLE_DATA: Dict[Type[astx.Literal], Any] = {
    LiteralList: [1, 2, 3],
    LiteralSet: {1, 2, 3},
    LiteralMap: {"key1": "value1", "key2": "value2"},
    LiteralTuple: (1, 2, 3),
    LiteralDictionary: {"key1": "value1", "key2": 42},
}

OPERATIONS_PER_CLASS: Dict[
    Type[astx.Literal],
    List[Tuple[Callable[[Type[astx.Literal]], BinaryOp], str]],
] = {
    LiteralList: [
        (lambda lc: VAR_A + lc(SAMPLE_DATA[lc]), "+"),
        (lambda lc: VAR_A == lc(SAMPLE_DATA[lc]), "=="),
        (lambda lc: VAR_A != lc(SAMPLE_DATA[lc]), "!="),
    ],
    LiteralTuple: [
        (lambda lc: VAR_A + lc(SAMPLE_DATA[lc]), "+"),
        (lambda lc: VAR_A == lc(SAMPLE_DATA[lc]), "=="),
        (lambda lc: VAR_A != lc(SAMPLE_DATA[lc]), "!="),
    ],
    LiteralSet: [
        (
            lambda lc: BinaryOp(
                op_code="|", lhs=VAR_A, rhs=lc(SAMPLE_DATA[lc])
            ),
            "|",
        ),
        (lambda lc: VAR_A == lc(SAMPLE_DATA[lc]), "=="),
        (lambda lc: VAR_A != lc(SAMPLE_DATA[lc]), "!="),
    ],
    LiteralMap: [
        (lambda lc: VAR_A == lc(SAMPLE_DATA[lc]), "=="),
        (lambda lc: VAR_A != lc(SAMPLE_DATA[lc]), "!="),
    ],
    LiteralDictionary: [
        (lambda lc: VAR_A == lc(SAMPLE_DATA[lc]), "=="),
        (lambda lc: VAR_A != lc(SAMPLE_DATA[lc]), "!="),
    ],
}


@pytest.mark.parametrize("literal_class", COLLECTION_LITERAL_CLASSES)
def test_initialization(literal_class: Type[astx.Literal]) -> None:
    """Test the initialization of collection literals."""
    literal = literal_class(SAMPLE_DATA[literal_class])
    assert literal.value == SAMPLE_DATA[literal_class]
    assert isinstance(literal, literal_class)


@pytest.mark.parametrize("literal_class", COLLECTION_LITERAL_CLASSES)
def test_binary_operations(literal_class: Type[astx.Literal]) -> None:
    """Test binary operations on collection literals."""
    operations = OPERATIONS_PER_CLASS.get(literal_class, [])
    for fn_bin_op, op_code in operations:
        try:
            bin_op = fn_bin_op(literal_class)
            assert isinstance(bin_op, BinaryOp)
            assert bin_op.op_code == op_code
            assert str(bin_op) != ""
            assert repr(bin_op) != ""
            struct = bin_op.get_struct()
            assert isinstance(
                struct, dict
            ), f"Expected struct to be a dict, got {type(struct)}"
            assert "op_code" in struct
            assert "lhs" in struct
            assert "rhs" in struct
        except Exception as e:
            pytest.fail(
                f"Binary operation '{op_code}' failed for"
                f"{literal_class.__name__}: {e}"
            )


@pytest.mark.parametrize("literal_class", COLLECTION_LITERAL_CLASSES)
def test_string_representation(literal_class: Type[astx.Literal]) -> None:
    """Test string representation of literals."""
    literal = literal_class(SAMPLE_DATA[literal_class])
    expected_str = f"{literal_class.__name__}[{SAMPLE_DATA[literal_class]}]"
    assert str(literal) == expected_str
    assert repr(literal) != ""


@pytest.mark.parametrize("literal_class", COLLECTION_LITERAL_CLASSES)
def test_get_struct(literal_class: Type[astx.Literal]) -> None:
    """Test the get_struct method of collection literals."""
    literal = literal_class(SAMPLE_DATA[literal_class])
    struct = literal.get_struct()
    simplified_struct = literal.get_struct(simplified=True)
    assert struct != {}
    assert simplified_struct != {}


def test_nested_collections() -> None:
    """Test literals with nested collections."""
    nested_list = [1, [2, 3], {"key": [4, 5]}]
    nested_literal = LiteralList(nested_list)
    assert nested_literal.value == nested_list
    assert isinstance(nested_literal, LiteralList)
    assert str(nested_literal) == f"LiteralList[{nested_list}]"
