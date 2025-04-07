"""AST comprehension classes and functions."""

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
    """AST node for generic comprehensions."""

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
        """Return a string representation of the object."""
        return f"COMPREHENSION[is_async={self.is_async}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
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
    """AST Comprehension class."""

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
        """Return the AST structure of the object."""
        value: ReprStruct = {
            "generators": self.generators.get_struct(simplified),
        }
        key = f"{self}" if not simplified else f"{self}#{id(self)}"
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ListComprehension(Comprehension):
    """ListComprehension class."""

    element: Expr

    def __init__(
        self,
        element: Expr,
        generators: ASTNodes[ComprehensionClause]
        | Iterable[ComprehensionClause] = [],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the GeneratorExpr instance."""
        super().__init__(generators=generators, loc=loc, parent=parent)
        self.element = element

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
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
    """AST node representing set comprehension expressions."""

    element: Expr

    def __init__(
        self,
        element: Expr,
        generators: ASTNodes[ComprehensionClause]
        | Iterable[ComprehensionClause] = [],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the SetComprehension instance."""
        super().__init__(generators=generators, loc=loc, parent=parent)
        self.element = element
        self.kind = ASTKind.SetComprehensionKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return "SET-COMPREHENSION"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
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
    """AST class for generator expressions."""

    element: Expr

    def __init__(
        self,
        element: Expr,
        generators: Iterable[ComprehensionClause]
        | ASTNodes[ComprehensionClause],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the GeneratorExpr instance."""
        super().__init__(generators=generators, loc=loc, parent=parent)
        self.element = element
        self.kind = ASTKind.GeneratorExprKind

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = f"GENERATOR-EXPR#{id(self)}" if simplified else "GENERATOR-EXPR"
        value: ReprStruct = {
            "element": self.element.get_struct(simplified),
            "generators": self.generators.get_struct(simplified),
        }
        return self._prepare_struct(key, value, simplified)
