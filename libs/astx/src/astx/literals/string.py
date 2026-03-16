"""
title: ASTx Data Types module.
"""

from __future__ import annotations

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ReprStruct,
    SourceLocation,
)
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.string import String, UTF8Char, UTF8String


@public
@typechecked
class LiteralString(Literal):
    """
    title: LiteralString data type class.
    attributes:
      type_:
        type: String
      loc:
        type: SourceLocation
      value:
        type: str
    """

    type_: String
    loc: SourceLocation

    value: str

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralString.
        parameters:
          value:
            type: str
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = String()
        self.loc = loc

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        return f"LiteralString({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"LiteralString: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class LiteralUTF8String(LiteralString):
    """
    title: Literal class for UTF-8 strings.
    attributes:
      loc:
        type: SourceLocation
      type_:
        type: UTF8String
      value:
        type: str
    """

    loc: SourceLocation
    type_: UTF8String

    value: str

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        super().__init__(value=value, loc=loc)
        self.type_ = UTF8String()

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        return f"LiteralUTF8String({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the structure of the object in a simplified.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"LiteralUTF8String: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class LiteralUTF8Char(LiteralString):
    """
    title: Literal class for UTF-8 characters.
    attributes:
      loc:
        type: SourceLocation
      type_:
        type: UTF8Char
      value:
        type: str
    """

    loc: SourceLocation
    type_: UTF8Char

    value: str

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        super().__init__(value=value, loc=loc)
        self.type_ = UTF8Char()

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        return f"LiteralUTF8Char({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the structure of the object in a simplified.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"LiteralUTF8Char: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)
