"""ASTx Collection Data Types."""

from __future__ import annotations

from typing import List, Type
from public import public
from astx.tools.typing import typechecked
from astx.types.base import AnyType
from astx.base import ExprType


@public
@typechecked
class CollectionType(AnyType):
    """Base class for collection data types."""


@public
@typechecked
class ListType(CollectionType):
    """List data type expression."""

    def __init__(self, element_types: List[ExprType]) -> None:
        """Initialize ListType with an element type."""
        self.element_types = element_types

    def __str__(self) -> str:
        types_str = ", ".join(str(t) for t in self.element_types)
        return f"ListType[{types_str}]"


@public
@typechecked
class SetType(CollectionType):
    """Set data type expression."""

    def __init__(self, element_type: ExprType) -> None:
        """Initialize SetType with an element type."""
        self.element_type = element_type

    def __str__(self) -> str:
        return f"SetType[{self.element_type}]"


@public
@typechecked
class DictType(CollectionType):
    """Dictionary data type expression."""

    def __init__(self, key_type: ExprType, value_type: ExprType) -> None:
        """Initialize DictType with key-value types."""
        self.key_type = key_type
        self.value_type = value_type

    def __str__(self) -> str:
        return f"DictType[{self.key_type}, {self.value_type}]"


@public
@typechecked
class TupleType(CollectionType):
    """Tuple data type expression."""

    def __init__(self, element_types: List[ExprType]) -> None:
        """Initialize TupleType with multiple element types."""
        self.element_types = element_types

    def __str__(self) -> str:
        types_str = ", ".join(str(t) for t in self.element_types)
        return f"TupleType[{types_str}]"
