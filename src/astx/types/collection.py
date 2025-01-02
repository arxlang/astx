"""ASTx Collection Data Types module."""

from __future__ import annotations

from public import public

from astx.tools.typing import typechecked
from astx.types.base import AnyType


@public
@typechecked
class Collection(AnyType):
    """Base class for collection data types (list, set, map, tuple)."""


@public
@typechecked
class List(Collection):
    """List data type expression."""
    

@public
@typechecked
class Set(Collection):
    """Set data type expression."""
    

@public
@typechecked
class Map(Collection):
    """Map data type expression."""
    

@public
@typechecked
class Tuple(Collection):
    """Tuple data type expression."""


@public
@typechecked
class Dictionary(Collection):
    """Dictionary data type expression."""