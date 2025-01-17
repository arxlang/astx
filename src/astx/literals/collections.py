"""Collection Literals Module."""

from __future__ import annotations

from typing import Any

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ReprStruct,
    SourceLocation,
)
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types import Dictionary, List, Set, Tuple


@public
@typechecked
class LiteralList(Literal):
    """Represents a literal list."""

    def __init__(
        self, value: list[Any], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize a LiteralLis."""
        super().__init__(loc)
        self.value = value
        self.loc = loc
        self.type_ = List()

    def __str__(self) -> str:
        """Return a string representatin."""
        return f"LiteralList[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a structural representation."""
        key = f"LiteralList: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralSet(Literal):
    """Represents a literal set."""

    def __init__(
        self, value: set[Any], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize a LiteralSet."""
        self.value = value
        self.loc = loc
        self.type_ = Set()

    def __str__(self) -> str:
        """Return a string representation."""
        return f"LiteralSet[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a structural representation."""
        key = f"LiteralSet: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralMap(Literal):
    """Represents a literal map."""

    def __init__(
        self, value: dict[Any, Any], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize a LiteralMap."""
        self.value = value
        self.loc = loc
        self.type_ = Dictionary()

    def __str__(self) -> str:
        """Return a string representation."""
        return f"LiteralMap[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a structural representation."""
        key = f"LiteralMap: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralTuple(Literal):
    """Represents a literal tuple."""

    def __init__(
        self, value: tuple[Any, ...], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize a LiteralTuple."""
        self.value = value
        self.loc = loc
        self.type_ = Tuple()

    def __str__(self) -> str:
        """Return a string representation."""
        return f"LiteralTuple[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a structural representation."""
        key = f"LiteralTuple: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralDictionary(Literal):
    """Represents a literal dictionary."""

    def __init__(
        self, value: dict[Any, Any], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize a LiteralDictionary."""
        self.value = value
        self.loc = loc
        self.type_ = Dictionary()

    def __str__(self) -> str:
        """Return a string representation."""
        return f"LiteralDictionary[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a structural representation."""
        key = f"LiteralDictionary: {self.value}"
        return self._prepare_struct(key, self.value, simplified)
