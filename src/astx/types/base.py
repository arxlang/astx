"""ASTx Data Types module."""

from __future__ import annotations

from public import public
from typeguard import typechecked

from astx.base import (
    DataType,
)


@public
@typechecked
class AnyType(DataType):
    """Generic data type expression."""
