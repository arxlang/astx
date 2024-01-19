"""Module for Variables."""
from __future__ import annotations

from typing import cast

from public import public

from astx.base import (
    ASTKind,
    Expr,
    ExprType,
    ReprStruct,
    SourceLocation,
    StatementType,
    Undefined,
)
from astx.modifiers import MutabilityKind, ScopeKind, VisibilityKind
from astx.operators import DataTypeOps

UNDEFINED = Undefined()


@public
class VariableDeclaration(StatementType):
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
        return f"VariableDeclaration[{self.name}, {type_}] = {self.value}"

    def get_struct(self) -> ReprStruct:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        struct_key = (
            f"VariableDeclaration[{self.name}, {type_}] = {self.value}"
        )
        return cast(ReprStruct, {struct_key: self.value})


@public
class InlineVariableDeclaration(Expr):
    """
    AST class for inline variable declaration expression.

    Can be used in expressions like for loops.
    """

    mutability: MutabilityKind
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
        return f"VariableDeclaration[{self.name}, {type_}] = {self.value}"

    def get_struct(self) -> ReprStruct:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        struct_key = (
            f"VariableDeclaration[{self.name}, {type_}] = {self.value}"
        )
        return cast(ReprStruct, {struct_key: self.value})


@public
class VariableAssignment(StatementType):
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
        self.kind = ASTKind.VariableAssignmentKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"VariableAssignment[{self.name}] = {self.value}"

    def get_struct(self) -> ReprStruct:
        """Return a string that represents the object."""
        struct_key = f"VariableAssignment[{self.name}] = {self.value}"
        return cast(ReprStruct, {struct_key: self.value})


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
        return f"Variable[{self.name}]"

    def get_struct(self) -> ReprStruct:
        """Return a string that represents the object."""
        return cast(ReprStruct, {f"Variable[{self.name}]": self})


@public
class Argument(Variable):
    """AST class for argument definition."""

    mutability: MutabilityKind
    name: str
    type_: ExprType
    default: Expr

    def __init__(
        self,
        name: str,
        type_: ExprType,
        mutability: MutabilityKind = MutabilityKind.constant,
        default: Expr = UNDEFINED,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the VarExprAST instance."""
        self.loc = loc
        self.mutability = mutability
        self.name = name
        self.type_ = type_
        self.default = default
        self.kind = ASTKind.ArgumentKind

    def get_struct(self) -> ReprStruct:
        """Return a string that represents the object."""
        struct_key = f"Argument[{self.name}, {self.type_}] = {self.default}"
        return cast(ReprStruct, {struct_key: self.default})
