"""ASTx class for With Statement (Context Manager)."""

from __future__ import annotations

from typing import Dict, List, Optional, cast

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    DataTypesStruct,
    Expr,
    Identifier,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.blocks import Block


@public
class WithItem:
    """AST class representing an item inside a `with` statement."""

    def __init__(
        self, context_expr: Expr, instance_name: Optional[Identifier] = None
    ) -> None:
        """Initialize a WithItem instance."""
        self.context_expr = context_expr
        self.instance_name = instance_name

    def __str__(self) -> str:
        """Return string representation of the WithItem."""
        if self.instance_name:
            return f"{self.context_expr} as {self.instance_name}"
        return str(self.context_expr)

    def _prepare_struct(
        self, key: str, value: DataTypesStruct, simplified: bool = False
    ) -> Dict[str, DataTypesStruct]:
        """Prepare structural representation."""
        return {key: value} if simplified else {"WithItem": {key: value}}

    def get_struct(
        self, simplified: bool = False
    ) -> Dict[str, DataTypesStruct]:
        """Get structural representation of the WithItem."""
        key = (
            "CONTEXT"
            if not self.instance_name
            else f"CONTEXT[{self.context_expr!s}]"
        )
        value = cast(DataTypesStruct, self.context_expr.get_struct(simplified))
        return self._prepare_struct(key, value, simplified)


class WithStmt(StatementType):
    """AST class for the `with` statement (context manager)."""

    def __init__(
        self,
        items: List[WithItem],
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize WithStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.items = items
        self.body = body
        self.kind = ASTKind.WithStmtKind

    def __str__(self) -> str:
        """Return string representation of the WithStmt."""
        items_str = ", ".join(str(item) for item in self.items)
        return f"WithStmt[{items_str}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Get structural representation of the WithStmt."""
        items_structs: List[Dict[str, DataTypesStruct]] = [
            item.get_struct(simplified) for item in self.items
        ]

        return cast(
            ReprStruct,
            {
                "WITH-STMT": {
                    "items": items_structs,
                    "body": self.body.get_struct(simplified),
                }
            },
        )
