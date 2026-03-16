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
from astx.types.temporal import (
    Date,
    DateTime,
    Time,
    Timestamp,
)


@public
@typechecked
class LiteralDate(Literal):
    """
    title: LiteralDate data type class.
    attributes:
      value:
        type: str
      type_:
        type: Date
      loc:
        type: SourceLocation
    """

    value: str
    type_: Date
    loc: SourceLocation

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralDate.
        parameters:
          value:
            type: str
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Date()
        self.loc = loc

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"LiteralDate[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the structure of the LiteralDate object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"LiteralDate: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralTime(Literal):
    """
    title: LiteralTime data type class.
    attributes:
      value:
        type: str
      type_:
        type: Time
      loc:
        type: SourceLocation
    """

    value: str
    type_: Time
    loc: SourceLocation

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralTime.
        parameters:
          value:
            type: str
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Time()
        self.loc = loc

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"LiteralTime[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the structure of the LiteralTime object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"LiteralTime: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralTimestamp(Literal):
    """
    title: LiteralTimestamp data type class.
    attributes:
      value:
        type: str
      type_:
        type: Timestamp
      loc:
        type: SourceLocation
    """

    value: str
    type_: Timestamp
    loc: SourceLocation

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralTimestamp.
        parameters:
          value:
            type: str
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Timestamp()
        self.loc = loc

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"LiteralTimestamp[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the structure of the LiteralTimestamp object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"LiteralTimestamp: {self.value}"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class LiteralDateTime(Literal):
    """
    title: LiteralDateTime data type class.
    attributes:
      value:
        type: str
      type_:
        type: DateTime
      loc:
        type: SourceLocation
    """

    value: str
    type_: DateTime
    loc: SourceLocation

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralDateTime.
        parameters:
          value:
            type: str
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = DateTime()
        self.loc = loc

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"LiteralDateTime[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the structure of the LiteralDateTime object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"LiteralDateTime: {self.value}"
        return self._prepare_struct(key, self.value, simplified)
