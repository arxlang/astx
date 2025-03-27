"""AST types module."""

from __future__ import annotations

from typing import Optional

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    DataType,
    Expr,
    ReprStruct,
    SourceLocation,
)
from astx.tools.typing import typechecked


@public
@typechecked
class TypeCastExpr(Expr):
    """AST class for type casting expressions."""

    expr: Expr
    target_type: DataType

    def __init__(
        self,
        expr: Expr,
        target_type: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.expr = expr
        self.target_type = target_type
        self.kind = ASTKind.TypeCastExprKind

    def __str__(self) -> str:
        """Return a string representation of the TypeCast expression."""
        return f"TypeCastExpr ({self.expr}, {self.target_type})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the TypeCast expression."""
        key = "TypeCastExpr"
        value: ReprStruct = {
            "expression": self.expr.get_struct(simplified),
            "target_type": self.target_type.get_struct(simplified),
        }

        return self._prepare_struct(key, value, simplified)
