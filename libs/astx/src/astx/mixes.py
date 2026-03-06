"""Module for mixing ASTx types from different modules."""

from typing import TypeAlias, Union

from astx.base import DataType
from astx.callables import FunctionDef
from astx.data import Variable

__all__ = ["NamedExpr"]

NamedExpr: TypeAlias = Union[DataType, FunctionDef, Variable]
