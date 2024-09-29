"""Define ASTx for more broader scope."""

from __future__ import annotations

import copy

from typing import Optional, cast

from public import public

from astx.base import (
    AST,
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    Expr,
    SourceLocation,
)
from astx.blocks import Block
from astx.types import ReprStruct


@public
class Target(Expr):
    """Define the Architecture target for the program."""

    datalayout: str
    triple: str

    def __init__(self, datalayout: str, triple: str) -> None:
        """Initialize the AST instance."""
        super().__init__()
        self.datalayout = datalayout
        self.triple = triple

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "TARGET"
        value = f"{self.datalayout}, {self.triple}"
        return self._prepare_struct(key, value, simplified)


@public
class Module(Block):
    """AST main expression class."""

    name: str

    def __init__(
        self,
        name: str = "main",
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the AST instance."""
        super().__init__(name=name, loc=loc)
        self.kind = ASTKind.ModuleKind

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return f"Module[{self.name}]"

    @property
    def block(self) -> list[AST]:
        """Define an alias for self.nodes."""
        return self.nodes

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        block_node = []

        for node in self.nodes:
            block_node.append(node.get_struct(simplified))

        key = f"MODULE[{self.name}]"
        value = cast(ReprStruct, block_node)

        return self._prepare_struct(key, value, simplified)


@public
class Package(ASTNodes):
    """AST class for Package."""

    name: str
    modules: list[Module]
    packages: list[Package]

    def __init__(
        self,
        name: str = "main",
        modules: list[Module] = [],
        packages: list[Package] = [],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the AST instance."""
        super().__init__(loc=loc)
        self.name = name
        self.modules = copy.deepcopy(modules)
        self.packages = copy.deepcopy(packages)

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return f"PACKAGE[{self.name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        packages = []
        modules = []

        for package in self.packages:
            packages.append(package.get_struct(simplified))

        for module in self.modules:
            modules.append(module.get_struct(simplified))

        key = str(self)
        value = cast(
            ReprStruct,
            {
                "modules": modules,
                "packages": packages,
            },
        )

        return self._prepare_struct(key, value, simplified)


@public
class Program(Package):
    """AST class for Program."""

    target: Target

    def __init__(
        self,
        name: str = "main",
        target: Target = Target("", ""),
        modules: list[Module] = [],
        packages: list[Package] = [],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the AST instance."""
        super().__init__(
            name=name, modules=modules, packages=packages, loc=loc
        )
        self.target = copy.deepcopy(target)

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return f"PROGRAM[{self.name}]"


@public
class AliasExpr(Expr):
    """Represents an alias in an import statement."""

    name: str
    asname: Optional[str]

    def __init__(
        self,
        name: str,
        asname: Optional[str] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.name = name
        self.asname = asname
        self.kind = ASTKind.AliasExprKind

    def __str__(self) -> str:
        """Return a string representation of the alias."""
        if self.asname:
            return f"{self.name} as {self.asname}"
        else:
            return self.name

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the alias."""
        key = "Alias"
        value = {
            "name": self.name,
            "asname": self.asname,
        }
        return self._prepare_struct(key, value, simplified)  # type: ignore[arg-type]


# error: Argument 2 to "_prepare_struct" of "AST" has incompatible type
# "Dict[str, List[str]]"; expected "Union[str, ReprStruct]"  [arg-type]

# src/astx/packages.py:186: error: Argument 2 to "_prepare_struct" of
# "AST" has incompatible type "Dict[str, Optional[str]]"; expected
# "Union[str, ReprStruct]"  [arg-type]
