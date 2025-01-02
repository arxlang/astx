"""ASTx Collection Literal Data Types module."""

from __future__ import annotations

from typing import List as TypingList, Set as TypingSet, Dict as TypingDict, Tuple as TypingTuple, Any
from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ReprStruct,
    SourceLocation,
)
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.collection import (
    List,
    Set,
    Map,
    Tuple,
    Dictionary,
)


@public
@typechecked
class LiteralList(Literal):
    """LiteralList data type class."""

    def __init__(self, value: TypingList[Any], loc: SourceLocation = NO_SOURCE_LOCATION) -> None:
        """Initialize LiteralList."""
        super().__init__(loc)
        self.value = value
        self.type_ = List()
        self.loc = loc

    def __str__(self) -> str:
        return f"LiteralList[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        key = f"LiteralList: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralSet(Literal):
    """LiteralSet data type class."""

    def __init__(self, value: TypingSet[Any], loc: SourceLocation = NO_SOURCE_LOCATION) -> None:
        """Initialize LiteralSet."""
        super().__init__(loc)
        self.value = value
        self.type_ = Set()
        self.loc = loc

    def __str__(self) -> str:
        return f"LiteralSet[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        key = f"LiteralSet: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralMap(Literal):
    """LiteralMap data type class."""

    def __init__(self, value: TypingDict[Any, Any], loc: SourceLocation = NO_SOURCE_LOCATION) -> None:
        """Initialize LiteralMap."""
        super().__init__(loc)
        self.value = value
        self.type_ = Map()
        self.loc = loc

    def __str__(self) -> str:
        return f"LiteralMap[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        key = f"LiteralMap: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralTuple(Literal):
    """LiteralTuple data type class."""

    def __init__(self, value: TypingTuple[Any, ...], loc: SourceLocation = NO_SOURCE_LOCATION) -> None:
        """Initialize LiteralTuple."""
        super().__init__(loc)
        self.value = value
        self.type_ = Tuple()
        self.loc = loc

    def __str__(self) -> str:
        return f"LiteralTuple[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        key = f"LiteralTuple: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralDictionary(Literal):
    """LiteralDictionary data type class."""

    def __init__(self, value: TypingDict[Any, Any], loc: SourceLocation = NO_SOURCE_LOCATION) -> None:
        """Initialize LiteralDictionary."""
        super().__init__(loc)
        self.value = value
        self.type_ = Dictionary()
        self.loc = loc

    def __str__(self) -> str:
        return f"LiteralDictionary[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        key = f"LiteralDictionary: {self.value}"
        return self._prepare_struct(key, self.value, simplified)
