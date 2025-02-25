"""Test cases for collections data types."""

from __future__ import annotations

from typing import Dict, List, Set, Tuple
from public import public
from astx.base import NO_SOURCE_LOCATION, SourceLocation
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.collections import ListType, TupleType, SetType, DictType
from astx.types.numeric import Int32
import pytest
from astx.literals.collections import LiteralList, LiteralTuple, LiteralSet, LiteralDict
from astx.literals.numeric import LiteralInt32

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
