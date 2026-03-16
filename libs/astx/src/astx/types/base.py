"""
title: ASTx Data Types module.
"""

from __future__ import annotations

from public import public

from astx.base import (
    DataType,
)
from astx.tools.typing import typechecked


@public
@typechecked
class AnyType(DataType):
    """
    title: Generic data type expression.
    """


@public
@typechecked
class NoneType(AnyType):
    """
    title: NoneType data type expression.
    """
