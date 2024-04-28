"""Module for Variables."""

from __future__ import annotations

from typing import Optional, cast

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
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
        type_ = self.type_.__name__
        return f"VariableDeclaration[{self.name}, {type_}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a string that represents the object."""
        key = str(self)
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


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
        type_ = self.type_.__name__
        return f"InlineVariableDeclaration[{self.name}, {type_}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a string that represents the object."""
        key = str(self)
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
class VariableAssignment(StatementType):
    """AST class for variable declaration."""

    name: str
    value: Expr

    def __init__(
        self,
        name: str,
        value: Expr,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the VarExprAST instance."""
        super().__init__(loc=loc, parent=parent)
        self.loc = loc
        self.name = name
        self.value = value
        self.kind = ASTKind.VariableAssignmentKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"VariableAssignment[{self.name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a string that represents the object."""
        key = str(self)
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
class Variable(DataTypeOps):
    """AST class for the variable usage."""

    name: str

    def __init__(
        self,
        name: str,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the Variable instance."""
        super().__init__(loc=loc, parent=parent)
        self.name = name

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"Variable[{self.name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a string that represents the object."""
        key = f"Variable[{self.name}]"
        value = self.name
        return self._prepare_struct(key, value, simplified)


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
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the VarExprAST instance."""
        super().__init__(name=name, loc=loc, parent=parent)
        self.mutability = mutability
        self.type_ = type_
        self.default = default
        self.kind = ASTKind.ArgumentKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        return f"Argument[{self.name}, {type_}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a string that represents the object."""
        key = f"Argument[{self.name}, {self.type_}] = {self.default}"
        value = cast(ReprStruct, self.default)
        return self._prepare_struct(key, value, simplified)


@public
class Arguments(ASTNodes):
    """AST class for argument definition."""

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"Arguments({len(self.nodes)})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a string that represents the object."""
        args_nodes = []

        for node in self.nodes:
            args_nodes.append(node.get_struct(simplified))

        key = str(self)
        value = cast(ReprStruct, args_nodes)
        return self._prepare_struct(key, value, simplified)
