"""Collection Literals Module."""

from __future__ import annotations

from typing import Any

from public import public

from astx.base import ReprStruct
from astx.literals.base import Literal
from astx.tools.typing import typechecked

@public
@typechecked
class LiteralList(Literal):
    """Represents a literal list."""

    def __init__(self, value: list[Any], loc: Any = None) -> None:
        """Initialize a LiteralLis."""
        self.value = value
        self.loc = loc

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

    def __init__(self, value: set[Any], loc: Any = None) -> None:
        """Initialize a LiteralSet."""
        self.value = value
        self.loc = loc

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

    def __init__(self, value: dict[Any, Any], loc: Any = None) -> None:
        """Initialize a LiteralMap."""
        self.value = value
        self.loc = loc

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

    def __init__(self, value: tuple[Any, ...], loc: Any = None) -> None:
        """Initialize a LiteralTuple."""
        self.value = value
        self.loc = loc

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

    def __init__(self, value: dict[Any, Any], loc: Any = None) -> None:
        """Initialize a LiteralDictionary."""
        self.value = value
        self.loc = loc

    def __str__(self) -> str:
        """Return a string representation."""
        return f"LiteralDictionary[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a structural representation."""
        key = f"LiteralDictionary: {self.value}"
        return self._prepare_struct(key, self.value, simplified)
