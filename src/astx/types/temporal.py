"""ASTx Data Types module."""

from __future__ import annotations

from public import public

from astx.tools.typing import typechecked
from astx.types.base import AnyType


@public
@typechecked
class Temporal(AnyType):
    """Base class for temporal data types (date, time, timestamp, datetime)."""


@public
@typechecked
class Date(Temporal):
    """Date data type expression."""


@public
@typechecked
class Time(Temporal):
    """Time data type expression."""


@public
@typechecked
class Timestamp(Temporal):
    """Timestamp data type expression."""


@public
@typechecked
class DateTime(Temporal):
    """DateTime data type expression."""
