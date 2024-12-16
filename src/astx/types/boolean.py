"""ASTx Data Types module."""

from __future__ import annotations

from public import public

from astx.tools.typing import typechecked
from astx.types.base import AnyType


@public
@typechecked
class Boolean(AnyType):
    """Boolean data type expression."""
