"""Module for classes definitions/declarations."""

from __future__ import annotations

import copy

from typing import Iterable, Optional, cast

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    DictDataTypesStruct,
    Expr,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.blocks import Block
from astx.callables import Function
from astx.modifiers import VisibilityKind
from astx.tools.typing import typechecked
from astx.variables import VariableDeclaration


@public
@typechecked
class ClassDeclStmt(StatementType):
    """AST class for class declaration."""

    name: str
    bases: ASTNodes
    decorators: ASTNodes
    visibility: VisibilityKind
    is_abstract: bool
    metaclass: Optional[Expr]
    attributes: ASTNodes
    methods: ASTNodes

    def __init__(
        self,
        name: str,
        bases: Iterable[Expr] | ASTNodes = [],
        decorators: Iterable[Expr] | ASTNodes = [],
        visibility: VisibilityKind = VisibilityKind.public,
        is_abstract: bool = False,
        metaclass: Optional[Expr] = None,
        attributes: Iterable[VariableDeclaration] | ASTNodes = [],
        methods: Iterable[Function] | ASTNodes = [],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize ClassDeclStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.name = name

        if isinstance(bases, ASTNodes):
            self.bases = bases
        else:
            self.bases = ASTNodes()
            for base in bases:
                self.bases.append(base)

        if isinstance(decorators, ASTNodes):
            self.decorators = decorators
        else:
            self.decorators = ASTNodes()
            for decorator in decorators:
                self.decorators.append(decorator)

        self.attributes = ASTNodes()
        for a in attributes:
            self.attributes.append(a)

        self.methods = ASTNodes()
        for m in methods:
            self.methods.append(m)

        self.visibility = visibility
        self.is_abstract = is_abstract
        self.metaclass = metaclass
        self.kind = ASTKind.ClassDeclStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        modifiers = []
        if self.visibility != VisibilityKind.public:
            modifiers.append(self.visibility.name)
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

    def _get_struct_wrapper(self, simplified: bool) -> DictDataTypesStruct:
        bases_dict: ReprStruct = {}
        decors_dict: ReprStruct = {}
        metaclass_dict: ReprStruct = {}
        attrs_dict: ReprStruct = {}
        methods_dict: ReprStruct = {}

        if self.bases:
            bases_dict = {"bases": self.bases.get_struct(simplified)}

        if self.decorators:
            decors_dict = {
                "decorators": self.decorators.get_struct(simplified)
            }

        if self.metaclass:
            metaclass_dict = {
                "metaclass": self.metaclass.get_struct(simplified)
            }

        if self.attributes:
            attrs_dict = {"attributes": self.attributes.get_struct(simplified)}

        if self.methods:
            methods_dict = {"methods": self.methods.get_struct(simplified)}

        value: DictDataTypesStruct = {
            **cast(DictDataTypesStruct, bases_dict),
            **cast(DictDataTypesStruct, decors_dict),
            **cast(DictDataTypesStruct, metaclass_dict),
            **cast(DictDataTypesStruct, attrs_dict),
            **cast(DictDataTypesStruct, methods_dict),
        }
        return value

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        vis = dict(zip(("public", "private", "protected"), ("+", "-", "#")))
        abstract = ", abstract" if self.is_abstract else ""

        key = f"CLASS-DECL[{vis[self.visibility.name]}{self.name}{abstract}]"
        value = self._get_struct_wrapper(simplified)

        return self._prepare_struct(key, value, simplified)


CLASS_BODY_DEFAULT = Block(name="class_body")


@public
@typechecked
class ClassDefStmt(ClassDeclStmt):
    """AST class for class definition, including attributes and methods."""

    body: Block

    def __init__(
        self,
        name: str,
        bases: Iterable[Expr] | ASTNodes = [],
        decorators: Iterable[Expr] | ASTNodes = [],
        body: Block = CLASS_BODY_DEFAULT,
        visibility: VisibilityKind = VisibilityKind.public,
        is_abstract: bool = False,
        metaclass: Optional[Expr] = None,
        attributes: Iterable[VariableDeclaration] | ASTNodes = [],
        methods: Iterable[Function] | ASTNodes = [],
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
            attributes=attributes,
            methods=methods,
            loc=loc,
            parent=parent,
        )

        if body != CLASS_BODY_DEFAULT:
            self.body = body
        else:
            self.body = copy.deepcopy(body)
            self.body.name = f"{name}_body"
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
        vis = dict(zip(("public", "private", "protected"), ("+", "-", "#")))
        abstract = ", abstract" if self.is_abstract else ""

        key = f"CLASS-DEF[{vis[self.visibility.name]}{self.name}{abstract}]"
        value = self._get_struct_wrapper(simplified)

        if self.body != CLASS_BODY_DEFAULT:
            value["body"] = self.body.get_struct(simplified)

        return self._prepare_struct(key, value, simplified)
