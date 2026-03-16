"""
title: ASTx Data Types module.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ExprType,
    ReprStruct,
    SourceLocation,
)
from astx.tools.typing import typechecked
from astx.types.base import NoneType
from astx.types.operators import DataTypeOps


@public
@typechecked
class Literal(DataTypeOps):
    """
    title: Literal Data type.
    attributes:
      ref:
        type: str
      type_:
        type: ExprType
      loc:
        type: SourceLocation
      value:
        type: Any
    """

    ref: str

    type_: ExprType
    loc: SourceLocation
    value: Any

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*args, **kwargs)
        self.ref = uuid4().hex

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        class_name = self.__class__.__name__
        return f"{class_name}({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST representation for the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"Literal[{self.type_}]: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class LiteralNone(Literal):
    """
    title: LiteralNone data type.
    attributes:
      loc:
        type: SourceLocation
      ref:
        type: str
      value:
        type: None
      type_:
        type: NoneType
    """

    ref: str
    value: None

    type_: NoneType
    value = None

    def __init__(self, loc: SourceLocation = NO_SOURCE_LOCATION) -> None:
        """
        title: Initialize LiteralNone.
        parameters:
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = None
        self.type_ = NoneType()
