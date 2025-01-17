"""ASTx collection types module."""

from __future__ import annotations

from typing import List

from public import public

from astx.base import AST, DataType
from astx.tools.typing import typechecked


@public
@typechecked
class CollectionType(DataType):
    """Base class for collection types."""

    pass


@public
@typechecked
class ListType(CollectionType):
    """Type representation of a list of elements of a specific type."""

    def __init__(self, element_type: AST) -> None:
        super().__init__()
        self.element_type = element_type

    def __str__(self) -> str:
        return f"ListType[{self.element_type}]"

    def __repr__(self) -> str:
        return self.__str__()


@public
@typechecked
class SetType(CollectionType):
    """Type representation of a set of elements of a specific type."""

    def __init__(self, element_type: AST) -> None:
        super().__init__()
        self.element_type = element_type

    def __str__(self) -> str:
        return f"SetType[{self.element_type}]"

    def __repr__(self) -> str:
        return self.__str__()


@public
@typechecked
class MapType(CollectionType):
    """Type representation of a map/dictionary with specific key and value types."""

    def __init__(self, key_type: AST, value_type: AST) -> None:
        super().__init__()
        self.key_type = key_type
        self.value_type = value_type

    def __str__(self) -> str:
        return f"MapType[{self.key_type}, {self.value_type}]"

    def __repr__(self) -> str:
        return self.__str__()


@public
@typechecked
class TupleType(CollectionType):
    """Type representation of a tuple of elements of specific types."""

    def __init__(self, element_types: List[AST]) -> None:
        super().__init__()
        self.element_types = element_types

    def __str__(self) -> str:
        types_str = ", ".join(str(t) for t in self.element_types)
        return f"TupleType[{types_str}]"

    def __repr__(self) -> str:
        return self.__str__()
