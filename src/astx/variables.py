"""Module for Variables."""
from __future__ import annotations

from public import public

from astx.base import (
    ASTKind,
    ExprType,
    ReprStruct,
    SourceLocation,
    StatementType,
    Undefined,
)
from astx.blocks import Block
from astx.modifiers import MutabilityKind, ScopeKind, VisibilityKind
from astx.operators import DataTypeOps

UNDEFINED = Undefined()


@public
class VarDeclaration(StatementType):
    """AST class for variable declaration."""

    mutability: MutabilityKind
    visibility: VisibilityKind
    scope: ScopeKind
    name: str
    type_: ExprType
    value: Expr

    def __init__(
        self,
        name: str,
        type_: ExprType,
        mutability: MutabilityKind = MutabilityKind.constant,
        visibility: VisibilityKind = VisibilityKind.public,
        scope: ScopeKind = ScopeKind.local,
        value: Expr = UNDEFINED,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the VarExprAST instance."""
        self.loc = loc
        self.mutability = mutability
        self.scope = scope
        self.visibility = visibility
        self.name = name
        self.type_ = type_
        self.value = value
        self.kind = ASTKind.VarDeclKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        return f"VarDeclaration[{self.name}, {type_}] = {self.value}"

    def get_struct(self) -> ReprStruct:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        struct_key = f"VarDeclaration[{self.name}, {type_}] = {self.value}"
        return {struct_key: self.name}


@public
class VarAssignment(StatementType):
    """AST class for variable declaration."""

    name: str
    value: Expr

    def __init__(
        self,
        name: str,
        value: Expr,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the VarExprAST instance."""
        self.loc = loc
        self.name = name
        self.value = value
        self.kind = ASTKind.VarAssignmentKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"VarAssignment[{self.name}] = {self.value}"

    def get_struct(self) -> ReprStruct:
        """Return a string that represents the object."""
        struct_key = f"VarAssignment[{self.name}] = {self.value}"
        return {struct_key: self.value}


@public
class Variable(DataTypeOps):
    """AST class for the variable usage."""

    name: str

    def __init__(
        self,
        name: str,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the Variable instance."""
        super().__init__(loc)
        self.name = name

    def __str__(self) -> str:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        return f"Variable[{self.name}]"

    def get_struct(self) -> ReprStruct:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        return {f"Variable[{self.name}]": self.name}
