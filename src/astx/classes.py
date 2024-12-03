"""Module for classes definitions/declarations."""

from __future__ import annotations

from typing import Iterable, List, Optional

from public import public
from typeguard import typechecked

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    Expr,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.blocks import Block
from astx.callables import Function
from astx.modifiers import VisibilityKind
from astx.variables import VariableDeclaration


@public
@typechecked
class ClassDeclStmt(StatementType):
    """AST class for class declaration."""

    name: str
    bases: List[Expr]
    decorators: List[Expr]
    visibility: VisibilityKind
    is_abstract: bool
    metaclass: Optional[Expr]

    def __init__(
        self,
        name: str,
        bases: Optional[List[Expr]] = None,
        decorators: Optional[List[Expr]] = None,
        visibility: VisibilityKind = VisibilityKind.public,
        is_abstract: bool = False,
        metaclass: Optional[Expr] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize ClassDeclStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.name = name
        self.bases = bases or []
        self.decorators = decorators or []
        self.visibility = visibility
        self.is_abstract = is_abstract
        self.metaclass = metaclass
        self.kind = ASTKind.ClassDeclStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        modifiers = []
        if self.visibility != VisibilityKind.public:
            modifiers.append(self.visibility.name.lower())
        if self.is_abstract:
            modifiers.append("abstract")
        modifiers_str = " ".join(modifiers)
        bases_str = (
            ", ".join(str(base) for base in self.bases) if self.bases else ""
        )
        decorators_str = "".join(
            f"@{decorator}\n" for decorator in self.decorators
        )
        metaclass_str = (
            f" metaclass={self.metaclass}" if self.metaclass else ""
        )
        class_str = f"class {self.name}"
        if bases_str:
            class_str += f"({bases_str})"
        class_str += f"{metaclass_str}"
        return f"{decorators_str}{modifiers_str} {class_str}".strip()

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = f"ClassDeclaration[{self.name}]"
        value = {
            "visibility": self.visibility.name.lower(),
            "is_abstract": self.is_abstract,
            "bases": [base.get_struct(simplified) for base in self.bases],
            "decorators": [
                decorator.get_struct(simplified)
                for decorator in self.decorators
            ],
            "metaclass": self.metaclass.get_struct(simplified)
            if self.metaclass
            else None,
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ClassDefStmt(ClassDeclStmt):
    """AST class for class definition, including attributes and methods."""

    attributes: Iterable[VariableDeclaration]
    methods: Iterable[Function]
    body: Block

    def __init__(
        self,
        name: str,
        bases: Optional[List[Expr]] = None,
        decorators: Optional[List[Expr]] = None,
        visibility: VisibilityKind = VisibilityKind.public,
        is_abstract: bool = False,
        metaclass: Optional[Expr] = None,
        attributes: Iterable[VariableDeclaration] = [],
        methods: Iterable[Function] = [],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize ClassDefStmt instance."""
        super().__init__(
            name=name,
            bases=bases,
            decorators=decorators,
            visibility=visibility,
            is_abstract=is_abstract,
            metaclass=metaclass,
            loc=loc,
            parent=parent,
        )
        self.attributes = attributes if attributes is not None else []
        self.methods = methods if methods is not None else []
        # Construct body as a block containing attributes and methods
        self.body = Block(name=f"{name}_body")
        for attr in self.attributes:
            self.body.append(attr)
        for method in self.methods:
            self.body.append(method)
        self.kind = ASTKind.ClassDefStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        class_decl_str = super().__str__()
        if not self.body.nodes:
            body_str = "    pass"
        else:
            body_str = "\n    ".join(str(stmt) for stmt in self.body.nodes)
        return f"{class_decl_str}:\n    {body_str}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        # value = super().get_struct(simplified)
        key = f"ClassDefinition[{self.name}]"
        value = {}
        value["attributes"] = [
            attr.get_struct(simplified) for attr in self.attributes
        ]
        value["methods"] = [
            method.get_struct(simplified) for method in self.methods
        ]
        value["body"] = [self.body.get_struct(simplified=True)]

        return self._prepare_struct(key, value, simplified)
