"""
title: ASTx Data Types module.
"""

from __future__ import annotations

from public import public

from astx.tools.typing import typechecked
from astx.types.base import AnyType


@public
@typechecked
class Temporal(AnyType):
    """
    title: >-
      Base class for temporal data types (date, time, timestamp, datetime).
    """


@public
@typechecked
class Date(Temporal):
    """
    title: Date data type expression.
    """


@public
@typechecked
class Time(Temporal):
    """
    title: Time data type expression.
    """


@public
@typechecked
class Timestamp(Temporal):
    """
    title: Timestamp data type expression.
    """


@public
@typechecked
class DateTime(Temporal):
    """
    title: DateTime data type expression.
    """
