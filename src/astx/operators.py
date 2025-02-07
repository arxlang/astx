"""ASTx classes for the operators."""

from __future__ import annotations

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    DataType,
    ReprStruct,
    SourceLocation,
)
from astx.tools.typing import typechecked
from astx.variables import Variable


@public
@typechecked
class WalrusOp(DataType):
    """AST class for the Walrus (assignment expression) operator."""

    def __init__(
        self,
        lhs: Variable,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the WalrusOp instance."""
        super().__init__(loc=loc)
        self.lhs = lhs
        self.rhs = rhs
        self.kind = ASTKind.WalrusOpKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"WalrusOp[:=]({self.lhs} := {self.rhs})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure that represents the object."""
        key = "WALRUS[:=]"
        lhs = {"lhs": self.lhs.get_struct(simplified)}
        rhs = {"rhs": self.rhs.get_struct(simplified)}

        content: ReprStruct = {**lhs, **rhs}
        return self._prepare_struct(key, content, simplified)
