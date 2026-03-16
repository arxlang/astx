"""
title: Module for mixing ASTx types from different modules.
"""

from typing import TypeAlias

from astx.base import DataType
from astx.callables import FunctionDef
from astx.data import Variable

__all__ = ["NamedExpr"]

NamedExpr: TypeAlias = DataType | FunctionDef | Variable
