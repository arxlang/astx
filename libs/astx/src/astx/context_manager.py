"""
title: ASTx class for With Statement (Context Manager).
"""

from __future__ import annotations

from typing import Optional, cast

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    DataTypesStruct,
    Expr,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.blocks import Block
from astx.data import Identifier


@public
class WithItem:
    """
    title: AST class representing an item inside a `with` statement.
    attributes:
      context_expr:
        type: Expr
      instance_name:
        type: Optional[Identifier]
    """

    context_expr: Expr
    instance_name: Optional[Identifier]

    def __init__(
        self, context_expr: Expr, instance_name: Optional[Identifier] = None
    ) -> None:
        """
        title: Initialize a WithItem instance.
        parameters:
          context_expr:
            type: Expr
          instance_name:
            type: Optional[Identifier]
        """
        self.context_expr = context_expr
        self.instance_name = instance_name

    def __str__(self) -> str:
        """
        title: Return string representation of the WithItem.
        returns:
          type: str
        """
        if self.instance_name:
            return f"{self.context_expr} as {self.instance_name}"
        return str(self.context_expr)

    def _prepare_struct(
        self, key: str, value: DataTypesStruct, simplified: bool = False
    ) -> dict[str, DataTypesStruct]:
        """
        title: Prepare structural representation.
        parameters:
          key:
            type: str
          value:
            type: DataTypesStruct
          simplified:
            type: bool
        returns:
          type: dict[str, DataTypesStruct]
        """
        return {key: value} if simplified else {"WithItem": {key: value}}

    def get_struct(
        self, simplified: bool = False
    ) -> dict[str, DataTypesStruct]:
        """
        title: Get structural representation of the WithItem.
        parameters:
          simplified:
            type: bool
        returns:
          type: dict[str, DataTypesStruct]
        """
        key = (
            "CONTEXT"
            if not self.instance_name
            else f"CONTEXT[{self.context_expr!s}]"
        )
        value = cast(DataTypesStruct, self.context_expr.get_struct(simplified))
        return self._prepare_struct(key, value, simplified)


class WithStmt(StatementType):
    """
    title: AST class for the `with` statement (context manager).
    attributes:
      items:
        type: list[WithItem]
      body:
        type: Block
      kind:
        type: ASTKind
    """

    items: list[WithItem]
    body: Block
    kind: ASTKind

    def __init__(
        self,
        items: list[WithItem],
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize WithStmt instance.
        parameters:
          items:
            type: list[WithItem]
          body:
            type: Block
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.items = items
        self.body = body
        self.kind = ASTKind.WithStmtKind

    def __str__(self) -> str:
        """
        title: Return string representation of the WithStmt.
        returns:
          type: str
        """
        items_str = ", ".join(str(item) for item in self.items)
        return f"WithStmt[{items_str}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Get structural representation of the WithStmt.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        items_structs: list[dict[str, DataTypesStruct]] = [
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
