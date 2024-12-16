"""ASTx Data Types module."""

from __future__ import annotations

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ReprStruct,
    SourceLocation,
)
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.string import UTF8Char, UTF8String


@public
@typechecked
class LiteralUTF8String(Literal):
    """Literal class for UTF-8 strings."""

    value: str

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        super().__init__(loc)
        self.value = value
        self.type_ = UTF8String()
        self.loc = loc

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"LiteralUTF8String({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the object in a simplified."""
        key = f"LiteralUTF8String: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class LiteralUTF8Char(Literal):
    """Literal class for UTF-8 characters."""

    value: str

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        super().__init__(loc)
        self.value = value
        self.type_ = UTF8Char()
        self.loc = loc

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"LiteralUTF8Char({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the object in a simplified."""
        key = f"LiteralUTF8Char: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)
