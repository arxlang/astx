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
class VarDecl(StatementType):
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
        return f"VarDecl[{self.name}, {type_}] = {self.value}"

    def get_struct(self) -> ReprStruct:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        struct_key = f"VarDecl[{self.name}, {type_}] = {self.value}"
        return {struct_key: self.name}


class VarsDecl(StatementType):
    """AST class for variable declaration."""

    mutability: MutabilityKind
    visibility: VisibilityKind
    scope: ScopeKind
    names: tuple[str, ...]
    type_: ExprType
    values: Expr | tuple[Expr]

    def __init__(
        self,
        names: tuple[str, ...],
        type_: ExprType,
        mutability: MutabilityKind = MutabilityKind.constant,
        visibility: VisibilityKind = VisibilityKind.public,
        scope: ScopeKind = ScopeKind.local,
        values: Expr | tuple[Expr] = UNDEFINED,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the VarExprAST instance."""
        self.loc = loc
        self.mutability = mutability
        self.scope = scope
        self.visibility = visibility
        self.names = names
        self.type_ = type_
        self.values = value
        self.kind = ASTKind.VarsDeclKind


@public
class VarAssignment(StatementType):
    """AST class for variable declaration."""

    name: str
    body: Block

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
        self.kind = ASTKind.VarAssignKind


@public
class VarsAssignment(StatementType):
    """AST class for variable declaration."""

    names: tuple[str, ...]
    values: Expr | tuple[Expr]

    def __init__(
        self,
        names: tuple[str, ...],
        values: Expr | tuple[Expr],
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the VarExprAST instance."""
        self.loc = loc
        self.names = names
        self.value = value
        self.kind = ASTKind.VarsAssignKind


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
