"""Module for Variables."""

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
    StatementType,
    Undefined,
)
from astx.modifiers import MutabilityKind, ScopeKind, VisibilityKind
from astx.tools.typing import typechecked
from astx.types import AnyType
from astx.types.operators import DataTypeOps

UNDEFINED = Undefined()


@public
@typechecked
class VariableDeclaration(StatementType):
    """AST class for variable declaration."""

    mutability: MutabilityKind
    visibility: VisibilityKind
    scope: ScopeKind
    name: str
    type_: DataType
    value: Expr

    def __init__(
        self,
        name: str,
        type_: DataType,
        mutability: MutabilityKind = MutabilityKind.constant,
        visibility: VisibilityKind = VisibilityKind.public,
        scope: ScopeKind = ScopeKind.local,
        value: Expr = UNDEFINED,
        parent: Optional[ASTNodes] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the VarExprAST instance."""
        super().__init__(loc=loc, parent=parent)
        self.mutability = mutability
        self.scope = scope
        self.visibility = visibility
        self.name = name
        self.type_ = type_
        self.value = value
        self.kind = ASTKind.VarDeclKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        type_ = self.type_.__class__.__name__
        return f"VariableDeclaration[{self.name}, {type_}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = str(self)
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class InlineVariableDeclaration(Expr):
    """
    AST class for inline variable declaration expression.

    Can be used in expressions like for loops.
    """

    mutability: MutabilityKind
    name: str
    type_: DataType
    value: Expr

    def __init__(
        self,
        name: str,
        type_: DataType,
        mutability: MutabilityKind = MutabilityKind.constant,
        visibility: VisibilityKind = VisibilityKind.public,
        scope: ScopeKind = ScopeKind.local,
        value: Expr = UNDEFINED,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the VarExprAST instance."""
        super().__init__(loc=loc, parent=parent)
        self.mutability = mutability
        self.scope = scope
        self.visibility = visibility
        self.name = name
        self.type_ = type_
        self.value = value
        self.kind = ASTKind.VarDeclKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        type_ = self.type_.__class__.__name__
        return f"InlineVariableDeclaration[{self.name}, {type_}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = str(self)
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class Variable(DataTypeOps):
    """AST class for the variable usage."""

    name: str
    type_: DataType = AnyType()

    def __init__(
        self,
        name: str,
        type_: DataType = AnyType(),
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the Variable instance."""
        super().__init__(loc=loc, parent=parent)
        self.name = name
        self.type_ = type_

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"Variable[{self.name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = f"Variable[{self.name}]"
        value = self.name
        return self._prepare_struct(key, value, simplified)
