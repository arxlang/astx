"""
title: Module for Variables.
"""

from __future__ import annotations

from typing import Iterable, Optional

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
    """
    title: AST class for variable declaration.
    attributes:
      kind:
        type: ASTKind
      mutability:
        type: MutabilityKind
      visibility:
        type: VisibilityKind
      scope:
        type: ScopeKind
      name:
        type: str
      type_:
        type: DataType
      value:
        type: Expr
    """

    kind: ASTKind

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
        """
        title: Initialize the VarExprAST instance.
        parameters:
          name:
            type: str
          type_:
            type: DataType
          mutability:
            type: MutabilityKind
          visibility:
            type: VisibilityKind
          scope:
            type: ScopeKind
          value:
            type: Expr
          parent:
            type: Optional[ASTNodes]
          loc:
            type: SourceLocation
        """
        super().__init__(loc=loc, parent=parent)
        self.mutability = mutability
        self.scope = scope
        self.visibility = visibility
        self.name = name
        self.type_ = type_
        self.value = value
        self.kind = ASTKind.VarDeclKind

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        type_ = self.type_.__class__.__name__
        return f"VariableDeclaration[{self.name}, {type_}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = str(self)
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class InlineVariableDeclaration(Expr):
    """
    title: AST class for inline variable declaration expression.
    summary: |-

      Can be used in expressions like for loops.
    attributes:
      scope:
        type: ScopeKind
      visibility:
        type: VisibilityKind
      kind:
        type: ASTKind
      mutability:
        type: MutabilityKind
      name:
        type: str
      type_:
        type: DataType
      value:
        type: Expr
    """

    scope: ScopeKind
    visibility: VisibilityKind
    kind: ASTKind

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
        """
        title: Initialize the VarExprAST instance.
        parameters:
          name:
            type: str
          type_:
            type: DataType
          mutability:
            type: MutabilityKind
          visibility:
            type: VisibilityKind
          scope:
            type: ScopeKind
          value:
            type: Expr
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.mutability = mutability
        self.scope = scope
        self.visibility = visibility
        self.name = name
        self.type_ = type_
        self.value = value
        self.kind = ASTKind.VarDeclKind

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        type_ = self.type_.__class__.__name__
        return f"InlineVariableDeclaration[{self.name}, {type_}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = str(self)
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class Identifier(DataTypeOps):
    """
    title: AST class for identifiers.
    attributes:
      name:
        type: str
      type_:
        type: DataType
    """

    name: str
    type_: DataType = AnyType()

    def __init__(
        self,
        name: str,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the Identifier instance.
        parameters:
          name:
            type: str
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.name = name
        # note: necessary for data operations
        self.type_ = AnyType()

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"{self.__class__.__name__}[{self.name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return a structure that represents the Identifier object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"{self.__class__.__name__.upper()}[{self.name}]"
        return self._prepare_struct(key, self.name, simplified)


@public
@typechecked
class Variable(Identifier):
    """
    title: AST class for the variable usage.
    attributes:
      name:
        type: str
      type_:
        type: DataType
    """

    type_: DataType

    def __init__(
        self,
        name: str,
        type_: DataType = AnyType(),
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the Variable instance.
        parameters:
          name:
            type: str
          type_:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(name=name, loc=loc, parent=parent)
        self.type_ = type_


class DeleteStmt(StatementType):
    """
    title: AST class for 'del' statements.
    attributes:
      kind:
        type: ASTKind
      value:
        type: Iterable[Identifier]
    """

    kind: ASTKind

    value: Iterable[Identifier]

    def __init__(
        self,
        value: Iterable[Identifier],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the DeleteStmt instance.
        parameters:
          value:
            type: Iterable[Identifier]
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.kind = ASTKind.DeleteStmtKind

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        value_str = ", ".join(str(value) for value in self.value)
        return f"DeleteStmt[{value_str}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = "DELETE"

        value: ReprStruct = {
            f"target_{i}": val.get_struct(simplified)
            for i, val in enumerate(self.value)
        }

        return self._prepare_struct(key, value, simplified)
