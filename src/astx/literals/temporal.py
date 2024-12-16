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
from astx.types.temporal import (
    Date,
    DateTime,
    Time,
    Timestamp,
)


@public
@typechecked
class LiteralDate(Literal):
    """LiteralDate data type class."""

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralDate."""
        super().__init__(loc)
        self.value = value
        self.type_ = Date()
        self.loc = loc

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"LiteralDate[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the LiteralDate object."""
        key = f"LiteralDate: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralTime(Literal):
    """LiteralTime data type class."""

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralTime."""
        super().__init__(loc)
        self.value = value
        self.type_ = Time()
        self.loc = loc

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"LiteralTime[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the LiteralTime object."""
        key = f"LiteralTime: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralTimestamp(Literal):
    """LiteralTimestamp data type class."""

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralTimestamp."""
        super().__init__(loc)
        self.value = value
        self.type_ = Timestamp()
        self.loc = loc

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"LiteralTimestamp[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the LiteralTimestamp object."""
        key = f"LiteralTimestamp: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralDateTime(Literal):
    """LiteralDateTime data type class."""

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralDateTime."""
        super().__init__(loc)
        self.value = value
        self.type_ = DateTime()
        self.loc = loc

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"LiteralDateTime[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the LiteralDateTime object."""
        key = f"LiteralDateTime: {self.value}"
        return self._prepare_struct(key, self.value, simplified)
