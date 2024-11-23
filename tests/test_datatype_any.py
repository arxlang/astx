from typing import Dict, Any

import pytest
from astx.datatypes import AnyType
from astx.base import ASTKind, NO_SOURCE_LOCATION

def test_any_type_creation() -> None:
    """Test basic creation of AnyType."""
    any_type = AnyType()
    assert isinstance(any_type, AnyType)
    assert any_type.kind == ASTKind.AnyDTKind

def test_any_type_str_representation() -> None:
    """Test string representation of AnyType."""
    any_type = AnyType()
    assert str(any_type) == "Any"

def test_any_type_struct_representation() -> None:
    """Test struct representation of AnyType."""
    any_type = AnyType()
    
    # Test with simplified=False
    struct = any_type.get_struct(simplified=False)
    assert isinstance(struct, dict)
    assert struct["type"] == "Any"
    assert struct["value"] is None
    
    # Test with simplified=True
    simplified_struct = any_type.get_struct(simplified=True)
    assert isinstance(simplified_struct, dict)
    assert simplified_struct["type"] == "Any"
    assert simplified_struct["value"] is None

def test_any_type_equality() -> None:
    """Test equality comparison between AnyType instances."""
    any_type1 = AnyType()
    any_type2 = AnyType()
    
    # Same types should be equal
    assert any_type1 == any_type2