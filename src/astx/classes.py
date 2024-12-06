"""Module for classes definitions/declarations."""

from __future__ import annotations

from typing import Iterable, List, Optional, cast

from public import public
from typeguard import typechecked

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

    # just for consistency, shouldn't the default values for the methods
    # be the default values for the instance? Specifically for bases and
    # decorators,[] vs None
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
        abstract = ", abstract" if self.is_abstract else ""
        vis = self.visibility.name.lower()
        key = f"CLASS-DECL[{self.name}{abstract}, {vis}]"

        bases_dict: ReprStruct = {}
        decors_dict: ReprStruct = {}
        metaclass_dict: ReprStruct = {}
        # if self.bases is not XX:# none does not work,
        # [] does not work. len(self.bases)>=1 works
        if len(self.bases) != 0:  # default is empty list
            bases_dict = {
                "bases": [b.get_struct(simplified) for b in self.bases]
            }

        if len(self.decorators) != 0:  # default is empty list
            decors_dict = {
                "decorators": [
                    d.get_struct(simplified) for d in self.decorators
                ]
            }

        if self.metaclass:  # default is None
            metaclass_dict = {
                "metaclass": self.metaclass.get_struct(simplified)
            }

        value: ReprStruct = {
            **cast(DictDataTypesStruct, bases_dict),
            **cast(DictDataTypesStruct, decors_dict),
            **cast(DictDataTypesStruct, metaclass_dict),
        }

        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ClassDefStmt(ClassDeclStmt):
    """AST class for class definition, including attributes and methods."""

    attributes: Iterable[VariableDeclaration]
    methods: Iterable[Function]
    body: Block

    # what does it mean to have body up here but not down?
    def __init__(  # shouldn't there be body here?
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

    # how can there be a body in the ast w/o a body in the init?
    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        # can I put the same way as above here, just to keep it consistent?
        key = f"CLASS-DEF[{self.name}]"
        value = {}
        value["attributes"] = [
            attr.get_struct(simplified) for attr in self.attributes
        ]
        value["methods"] = [
            method.get_struct(simplified) for method in self.methods
        ]
        value["body"] = [self.body.get_struct(simplified=True)]

        return self._prepare_struct(key, value, simplified)
