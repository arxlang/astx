"""ASTx Data Types module."""

from __future__ import annotations

from public import public
from typeguard import typechecked

from astx.types.base import AnyType


@public
@typechecked
class Boolean(AnyType):
    """Boolean data type expression."""
