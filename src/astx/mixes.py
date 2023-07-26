from typing import TypeAlias, Union

from astx.datatypes import Variable
from astx.callables import Function


__all__ = ["NamedExpr"]

NamedExpr: TypeAlias = Union[Function, Variable]
