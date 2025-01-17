"""Tests for Collections number data types."""

from typing import Dict, List, Set, Tuple

from astx.literals.base import Literal
from astx.literals.collections import (
    LiteralList,
    LiteralMap,
    LiteralSet,
    LiteralTuple,
)
from astx.literals.numeric import LiteralInt32
from astx.types.collections import ListType, MapType, SetType, TupleType
from astx.types.numeric import Int32


def test_literal_list_creation() -> None:
    elements: List[Literal] = [
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    ]
    lit_list = LiteralList(elements)
    assert isinstance(lit_list, LiteralList)
    assert isinstance(lit_list.type_, ListType)
    assert isinstance(lit_list.type_.element_type, Int32)
    assert lit_list.elements == elements


def test_literal_list_binary_operation_addition() -> None:
    elements1: List[Literal] = [LiteralInt32(1), LiteralInt32(2)]
    elements2: List[Literal] = [LiteralInt32(3), LiteralInt32(4)]
    lit_list1 = LiteralList(elements1)
    lit_list2 = LiteralList(elements2)
    combined_list = lit_list1 + lit_list2
    assert isinstance(combined_list, LiteralList)
    assert combined_list.elements == elements1 + elements2
    assert isinstance(combined_list.type_, ListType)
    assert isinstance(combined_list.type_.element_type, Int32)


def test_literal_list_unary_operation_negation() -> None:
    elements: List[Literal] = [
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    ]
    lit_list = LiteralList(elements)
    reversed_list = -lit_list
    assert isinstance(reversed_list, LiteralList)
    assert reversed_list.elements == list(reversed(elements))
    assert isinstance(reversed_list.type_, ListType)
    assert isinstance(reversed_list.type_.element_type, Int32)


def test_literal_set_creation() -> None:
    elements: Set[Literal] = set(
        [LiteralInt32(1), LiteralInt32(2), LiteralInt32(3)]
    )
    lit_set = LiteralSet(elements)
    assert isinstance(lit_set, LiteralSet)
    assert isinstance(lit_set.type_, SetType)
    assert isinstance(lit_set.type_.element_type, Int32)
    assert lit_set.elements == elements


def test_literal_set_binary_operation_union() -> None:
    elements1: Set[Literal] = set([LiteralInt32(1), LiteralInt32(2)])
    elements2: Set[Literal] = set([LiteralInt32(2), LiteralInt32(3)])
    lit_set1 = LiteralSet(elements1)
    lit_set2 = LiteralSet(elements2)
    union_set = lit_set1 + lit_set2
    assert isinstance(union_set, LiteralSet)
    expected_elements = elements1.union(elements2)
    assert union_set.elements == expected_elements
    assert isinstance(union_set.type_, SetType)
    assert isinstance(union_set.type_.element_type, Int32)


def test_literal_tuple_creation() -> None:
    elements: Tuple[Literal, ...] = (
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    )
    lit_tuple = LiteralTuple(elements)
    assert isinstance(lit_tuple, LiteralTuple)
    assert isinstance(lit_tuple.type_, TupleType)
    assert all(isinstance(t, Int32) for t in lit_tuple.type_.element_types)
    assert lit_tuple.elements == elements


def test_literal_tuple_unary_operation_negation() -> None:
    elements: Tuple[Literal, ...] = (
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    )
    lit_tuple = LiteralTuple(elements)
    reversed_tuple = -lit_tuple
    assert isinstance(reversed_tuple, LiteralTuple)
    assert reversed_tuple.elements == tuple(reversed(elements))
    assert isinstance(reversed_tuple.type_, TupleType)
    assert all(
        isinstance(t, Int32) for t in reversed_tuple.type_.element_types
    )


def test_literal_map_creation() -> None:
    elements: Dict[Literal, Literal] = {
        LiteralInt32(1): LiteralInt32(10),
        LiteralInt32(2): LiteralInt32(20),
    }
    lit_map = LiteralMap(elements)
    assert isinstance(lit_map, LiteralMap)
    assert isinstance(lit_map.type_, MapType)
    assert isinstance(lit_map.type_.key_type, Int32)
    assert isinstance(lit_map.type_.value_type, Int32)
    assert lit_map.elements == elements


def test_literal_map_binary_operation_merge() -> None:
    elements1: Dict[Literal, Literal] = {
        LiteralInt32(1): LiteralInt32(10),
        LiteralInt32(2): LiteralInt32(20),
    }
    elements2: Dict[Literal, Literal] = {
        LiteralInt32(2): LiteralInt32(200),
        LiteralInt32(3): LiteralInt32(30),
    }
    lit_map1 = LiteralMap(elements1)
    lit_map2 = LiteralMap(elements2)
    merged_map = lit_map1 + lit_map2
    assert isinstance(merged_map, LiteralMap)
    expected_elements = {**elements1, **elements2}
    assert merged_map.elements == expected_elements
    assert isinstance(merged_map.type_, MapType)
    assert isinstance(merged_map.type_.key_type, Int32)
    assert isinstance(merged_map.type_.value_type, Int32)
