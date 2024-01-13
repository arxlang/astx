"""Module for Variables."""
from __future__ import annotations

from public import public

from astx.base import (
    ASTKind,
    DataType,
    ExprType,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.blocks import Block
from astx.modifiers import MutabilityKind, ScopeKind, VisibilityKind
from astx.operators import DataTypeOps


@public
class VarDecl(StatementType):
    """AST class for variable declaration."""

    mutability: MutabilityKind
    visibility: VisibilityKind
    scope: ScopeKind
    var_names: tuple[str, ...]
    type_name: ExprType
    body: Block

    def __init__(
        self,
        mutability: MutabilityKind,
        visibility: VisibilityKind,
        scope: ScopeKind,
        var_names: tuple[str, ...],
        type_name: ExprType,
        body: Block,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the VarExprAST instance."""
        self.loc = loc
        self.mutability = mutability
        self.scope = scope
        self.visibility = visibility
        self.var_names = var_names
        self.type_name = type_name
        self.body = body
        self.kind = ASTKind.VarKind


@public
class Variable(DataTypeOps):
    """AST class for the variable usage."""

    type_: ExprType
    value: DataType

    def __init__(
        self,
        name: str,
        type_: ExprType,
        value: DataType,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the Variable instance."""
        super().__init__(loc)
        self.name = name
        self.type_ = type_
        self.kind = ASTKind.VariableKind
        self.value: DataType = value

    def __str__(self) -> str:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        return f"Variable[{type_}]({self.value})"

    def get_struct(self) -> ReprStruct:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        return {f"Variable[{self.name}: {type_}]": self.value.get_struct()}
