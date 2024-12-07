"""ASTx Data Types module."""

from __future__ import annotations

from public import public
from typeguard import typechecked

from astx.types.base import AnyType


@public
@typechecked
class Collection(AnyType):
    """Base class for collection data types."""


@public
@typechecked
class Set(Collection):
    """Set data type expression."""


@public
@typechecked
class List(Collection):
    """List data type expression."""
