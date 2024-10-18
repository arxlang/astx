"""AST types module."""

from __future__ import annotations
<<<<<<< HEAD
=======

from typing import Dict, List, Optional, Union

try:
    from typing_extensions import TypeAlias
except ImportError:
    from typing import TypeAlias  # type: ignore[no-redef,attr-defined]

from public import public
from typeguard import typechecked

from astx.base import (
    ASTKind,
    ASTNodes,
    DataType,
    Expr,
    SourceLocation,
)

PrimitivesStruct: TypeAlias = Union[int, str, float, bool]
DataTypesStruct: TypeAlias = Union[
    PrimitivesStruct, Dict[str, "DataTypesStruct"], List["DataTypesStruct"]
]
DictDataTypesStruct: TypeAlias = Dict[str, DataTypesStruct]
ReprStruct: TypeAlias = Union[List[DataTypesStruct], DictDataTypesStruct]


@public
class TypeCastExpr(Expr):
    """AST class for type casting expressions."""

    expr: Expr
    target_type: DataType

    @typechecked
    def __init__(
        self,
        expr: Expr,
        target_type: DataType,
        loc: SourceLocation = SourceLocation(-1, -1),
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.expr = expr
        self.target_type = target_type
        self.kind = ASTKind.TypeCastExprKind
>>>>>>> 01275a9 (create TypeCastExpr class)
