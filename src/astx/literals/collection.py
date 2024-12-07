"""ASTx Data Types module."""

from __future__ import annotations

from public import public
from typeguard import typechecked
from typing import Any

from astx.base import (
    NO_SOURCE_LOCATION,
    ReprStruct,
    SourceLocation,
)
from astx.literals.base import Literal
from astx.types.collection import (
    Set,
    List,
)


@public
@typechecked
class LiteralSet(Literal):
    """LiteralSet data type class."""

    value: Set[Any]

    def __init__(
        self, value: Set[Any], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralSet."""
        super().__init__(loc)
        self.value = value
        self.type_ = Set
        self.loc = loc

    def __str__(self) -> str:
        """Return a string representation of the LiteralSet."""
        return f"LiteralSet({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST representation for the Set literal."""
        key = "Set"
        value = list(self.value)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class LiteralList(Literal):
    """LiteralList data type class."""

    value: List[Any]

    def __init__(
        self, value: List[Any], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralList."""
        super().__init__(loc)
        self.value = value
        self.type_ = List
        self.loc = loc

    def __str__(self) -> str:
        """Return a string representation of the LiteralList."""
        return f"LiteralList({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST representation for the List literal."""
        key = "List"
        value = self.value
        return self._prepare_struct(key, value, simplified)