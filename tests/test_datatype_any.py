"""Tests for Any data type."""

from astx.base import ASTKind
from astx.datatypes import AnyType


def test_any_type_creation() -> None:
    """Test basic creation of AnyType."""
    any_type = AnyType()
    assert isinstance(any_type, AnyType)
    assert any_type.kind == ASTKind.AnyDTKind


def test_any_type_str_representation() -> None:
    """Test string representation of AnyType."""
    any_type = AnyType()
    assert str(any_type) == "Any"


def test_any_type_equality() -> None:
    """Test equality comparison between AnyType instances."""
    any_type1 = AnyType()
    any_type2 = AnyType()

    # Same types should be equal
    assert any_type1 == any_type2
