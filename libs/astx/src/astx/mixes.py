"""Module for mixing ASTx types from different modules."""

from typing import Union

try:
    from typing import TypeAlias  # type: ignore
except ImportError:
    from typing_extensions import TypeAlias

from astx.base import DataType
from astx.callables import FunctionDef
from astx.variables import Variable

__all__ = ["NamedExpr"]

NamedExpr: TypeAlias = Union[DataType, FunctionDef, Variable]
