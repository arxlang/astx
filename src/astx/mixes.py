from typing import Union

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

from astx.base import DataType
from astx.variables import Variable
from astx.callables import Function


__all__ = ["NamedExpr"]

NamedExpr: TypeAlias = Union[DataType, Function, Variable]
