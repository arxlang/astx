"""Test cases for collection data types."""

from __future__ import annotations

from typing import Dict, List, Sequence, Set, Tuple

from astx.literals.base import Literal
from astx.literals.collections import (
    LiteralDict,
    LiteralList,
    LiteralSet,
    LiteralTuple,
    SetComp,
)
from astx.literals.numeric import LiteralInt32
from astx.types.collections import DictType, ListType, SetType, TupleType
from astx.types.operators import BinaryOp, UnaryOp

# Test constants
GENERATOR_COUNT = 3  # Number of generators in set comprehension


def test_literal_list_creation() -> None:
    """Test creation of LiteralList."""
    elements: List[Literal] = [
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    ]
    lit_list = LiteralList(elements)
    assert isinstance(lit_list, LiteralList)
    assert isinstance(lit_list.type_, ListType)
    assert lit_list.elements == elements


def test_literal_tuple_creation() -> None:
    """Test creation of LiteralTuple."""
    elements: Tuple[Literal, ...] = (
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    )
    lit_tuple = LiteralTuple(elements)
    assert isinstance(lit_tuple, LiteralTuple)
    assert isinstance(lit_tuple.type_, TupleType)
    assert lit_tuple.elements == elements


def test_literal_set_creation() -> None:
    """Test creation of LiteralSet."""
    elements: Set[Literal] = {
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    }
    lit_set = LiteralSet(elements)
    assert isinstance(lit_set, LiteralSet)
    assert isinstance(lit_set.type_, SetType)
    assert lit_set.elements == elements


def test_literal_dict_creation() -> None:
    """Test creation of LiteralDict."""
    elements: Dict[Literal, Literal] = {
        LiteralInt32(1): LiteralInt32(10),
        LiteralInt32(2): LiteralInt32(20),
    }
    lit_dict = LiteralDict(elements)
    assert isinstance(lit_dict, LiteralDict)
    assert isinstance(lit_dict.type_, DictType)
    assert lit_dict.elements == elements


def test_literal_list_binary_addition() -> None:
    """Test binary addition operation on LiteralList."""
    elements1: List[Literal] = [LiteralInt32(1), LiteralInt32(2)]
    elements2: List[Literal] = [LiteralInt32(3), LiteralInt32(4)]
    lit_list1 = LiteralList(elements1)
    lit_list2 = LiteralList(elements2)
    combined = BinaryOp("+", lit_list1, lit_list2)
    assert isinstance(combined, BinaryOp)
    assert combined.op_code == "+"
    assert combined.lhs == lit_list1
    assert combined.rhs == lit_list2


def test_literal_list_unary_negation() -> None:
    """Test unary negation operation on LiteralList."""
    elements: List[Literal] = [
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    ]
    lit_list = LiteralList(elements)
    negated = UnaryOp("-", lit_list)
    assert isinstance(negated, UnaryOp)
    assert negated.op_code == "-"
    assert negated.operand == lit_list


def test_literal_set_binary_union() -> None:
    """Test binary union operation on LiteralSet."""
    elements1: Set[Literal] = {LiteralInt32(1), LiteralInt32(2)}
    elements2: Set[Literal] = {LiteralInt32(3), LiteralInt32(4)}
    lit_set1 = LiteralSet(elements1)
    lit_set2 = LiteralSet(elements2)
    union_set = BinaryOp("|", lit_set1, lit_set2)
    assert isinstance(union_set, BinaryOp)
    assert union_set.op_code == "|"
    assert union_set.lhs == lit_set1
    assert union_set.rhs == lit_set2


def test_literal_dict_binary_merge() -> None:
    """Test binary merge operation on LiteralDict."""
    elements1: Dict[Literal, Literal] = {LiteralInt32(1): LiteralInt32(10)}
    elements2: Dict[Literal, Literal] = {LiteralInt32(2): LiteralInt32(20)}
    lit_dict1 = LiteralDict(elements1)
    lit_dict2 = LiteralDict(elements2)
    merged_dict = BinaryOp("**", lit_dict1, lit_dict2)
    assert isinstance(merged_dict, BinaryOp)
    assert merged_dict.op_code == "**"
    assert merged_dict.lhs == lit_dict1
    assert merged_dict.rhs == lit_dict2


def test_set_comp_creation() -> None:
    """Test creation of set comprehension."""
    elt = LiteralInt32(5)
    generators: Sequence[Literal] = [LiteralInt32(1)]
    set_comp = SetComp(elt, generators)

    assert isinstance(set_comp, SetComp)
    assert isinstance(set_comp.type_, SetType)
    assert set_comp.elt == elt
    assert set_comp.generators == generators


def test_set_comp_with_complex_generators() -> None:
    """Test set comprehension with multiple generators."""
    elt = LiteralInt32(5)
    generators: Sequence[Literal] = [
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    ]
    set_comp = SetComp(elt, generators)
    assert len(set_comp.generators) == GENERATOR_COUNT
    assert all(isinstance(gen, LiteralInt32) for gen in set_comp.generators)


def test_set_comp_type_inference() -> None:
    """Test type inference in set comprehension."""
    elt = LiteralInt32(5)
    generators: Sequence[Literal] = [LiteralInt32(1)]
    set_comp = SetComp(elt, generators)
    assert isinstance(set_comp.type_, SetType)
    assert set_comp.type_.element_type == elt.type_
