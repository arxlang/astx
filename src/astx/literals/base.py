"""ASTx Data Types module."""

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
    """Literal Data type."""

    type_: ExprType
    loc: SourceLocation
    value: Any

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*args, **kwargs)
        self.ref = uuid4().hex

    def __str__(self) -> str:
        """Return a string that represents the object."""
        klass = self.__class__.__name__
        return f"{klass}({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST representation for the object."""
        key = f"Literal[{self.type_}]: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class LiteralNone(Literal):
    """LiteralNone data type."""

    type_: NoneType
    value = None

    def __init__(self, loc: SourceLocation = NO_SOURCE_LOCATION) -> None:
        """Initialize LiteralNone."""
        super().__init__(loc)
        self.value = None
        self.type_ = NoneType()
