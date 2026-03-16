"""
title: AST comprehension classes and functions.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import (
    Iterable,
    Optional,
)

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    Expr,
    ReprStruct,
    SourceLocation,
)
from astx.tools.typing import typechecked


@public
@typechecked
class ComprehensionClause(Expr):
    """
    title: AST node for generic comprehensions.
    attributes:
      kind:
        type: ASTKind
      target:
        type: Expr
      iterable:
        type: Expr
      conditions:
        type: ASTNodes[Expr]
      is_async:
        type: bool
    """

    kind: ASTKind

    target: Expr
    iterable: Expr
    conditions: ASTNodes[Expr]
    is_async: bool

    def __init__(
        self,
        target: Expr,
        iterable: Expr,
        conditions: Optional[Iterable[Expr] | ASTNodes[Expr]] = None,
        is_async: bool = False,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.target = target
        self.iterable = iterable
        self.is_async = is_async
        self.kind = ASTKind.ComprehensionKind

        if isinstance(conditions, ASTNodes):
            self.conditions = conditions
        elif isinstance(conditions, Iterable):
            self.conditions = ASTNodes()
            for condition in conditions:
                self.conditions.append(condition)
        else:
            self.conditions = ASTNodes[Expr]()

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        return f"COMPREHENSION[is_async={self.is_async}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        conditions = (
            {"conditions": self.conditions.get_struct(simplified)}
            if self.conditions.nodes
            else {}
        )

        value: ReprStruct = {
            "target": self.target.get_struct(simplified),
            "iterable": self.iterable.get_struct(simplified),
            **conditions,
        }

        key = f"{self}" if not simplified else f"{self}#{id(self)}"
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class Comprehension(Expr):
    """
    title: AST Comprehension class.
    attributes:
      generators:
        type: ASTNodes[ComprehensionClause]
    """

    generators: ASTNodes[ComprehensionClause]

    def __init__(
        self,
        generators: (
            Iterable[ComprehensionClause] | ASTNodes[ComprehensionClause]
        ),
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)

        if isinstance(generators, ASTNodes):
            self.generators = generators
        elif isinstance(generators, Iterable):
            self.generators = ASTNodes[ComprehensionClause]()
            for generator in generators:
                self.generators.append(generator)

    @abstractmethod
    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        value: ReprStruct = {
            "generators": self.generators.get_struct(simplified),
        }
        key = f"{self}" if not simplified else f"{self}#{id(self)}"
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ListComprehension(Comprehension):
    """
    title: ListComprehension class.
    attributes:
      generators:
        type: ASTNodes[ComprehensionClause]
      element:
        type: Expr
    """

    element: Expr

    def __init__(
        self,
        element: Expr,
        generators: ASTNodes[ComprehensionClause]
        | Iterable[ComprehensionClause] = [],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the GeneratorExpr instance.
        parameters:
          element:
            type: Expr
          generators:
            type: ASTNodes[ComprehensionClause] | Iterable[ComprehensionClause]
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(generators=generators, loc=loc, parent=parent)
        self.element = element

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"{self}"
        key += f"#{id(self)}" if simplified else ""

        generators = (
            {"generators": self.generators.get_struct(simplified)}
            if self.generators.nodes
            else {}
        )

        value: ReprStruct = {
            "element": self.element.get_struct(simplified),
            **generators,
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class SetComprehension(Comprehension):
    """
    title: AST node representing set comprehension expressions.
    attributes:
      generators:
        type: ASTNodes[ComprehensionClause]
      kind:
        type: ASTKind
      element:
        type: Expr
    """

    kind: ASTKind

    element: Expr

    def __init__(
        self,
        element: Expr,
        generators: ASTNodes[ComprehensionClause]
        | Iterable[ComprehensionClause] = [],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the SetComprehension instance.
        parameters:
          element:
            type: Expr
          generators:
            type: ASTNodes[ComprehensionClause] | Iterable[ComprehensionClause]
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(generators=generators, loc=loc, parent=parent)
        self.element = element
        self.kind = ASTKind.SetComprehensionKind

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        return "SET-COMPREHENSION"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        generators = (
            {"generators": self.generators.get_struct(simplified)}
            if self.generators.nodes
            else {}
        )

        value: ReprStruct = {
            "element": self.element.get_struct(simplified),
            **generators,
        }
        key = f"{self}#{id(self)}" if simplified else f"{self}"
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class GeneratorExpr(Comprehension):
    """
    title: AST class for generator expressions.
    attributes:
      generators:
        type: ASTNodes[ComprehensionClause]
      kind:
        type: ASTKind
      element:
        type: Expr
    """

    kind: ASTKind

    element: Expr

    def __init__(
        self,
        element: Expr,
        generators: Iterable[ComprehensionClause]
        | ASTNodes[ComprehensionClause],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the GeneratorExpr instance.
        parameters:
          element:
            type: Expr
          generators:
            type: Iterable[ComprehensionClause] | ASTNodes[ComprehensionClause]
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(generators=generators, loc=loc, parent=parent)
        self.element = element
        self.kind = ASTKind.GeneratorExprKind

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"GENERATOR-EXPR#{id(self)}" if simplified else "GENERATOR-EXPR"
        value: ReprStruct = {
            "element": self.element.get_struct(simplified),
            "generators": self.generators.get_struct(simplified),
        }
        return self._prepare_struct(key, value, simplified)
