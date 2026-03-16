"""
title: ASTx Data Types module.
"""

from __future__ import annotations

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    SourceLocation,
)
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.boolean import Boolean


@public
@typechecked
class LiteralBoolean(Literal):
    """
    title: LiteralBoolean data type class.
    attributes:
      type_:
        type: Boolean
      loc:
        type: SourceLocation
      value:
        type: bool
    """

    type_: Boolean
    loc: SourceLocation

    value: bool

    def __init__(
        self, value: bool, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralBoolean.
        parameters:
          value:
            type: bool
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Boolean()
        self.loc = loc
