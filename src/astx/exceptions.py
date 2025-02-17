"""Module for Exceptions."""

from typing import Optional

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    Expr,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.tools.typing import typechecked


@public
@typechecked
class ThrowStmt(StatementType):
    """AST class for throw statements."""

    exception: Optional[Expr]

    def __init__(
        self,
        exception: Optional[Expr] = None,
        parent: Optional[ASTNodes] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the instance."""
        super().__init__(loc=loc, parent=parent)
        self.exception = exception
        self.kind = ASTKind.ThrowStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        throw_str = f"ThrowStmt[{self.exception.value}]" if self.exception else "ThrowStmt"
        return throw_str

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = str(self)
        value = self.exception.get_struct(simplified) if self.exception else ""
        return self._prepare_struct(key, value, simplified)
