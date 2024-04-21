"""Define ASTx for more broader scope."""

from __future__ import annotations

import copy

from typing import cast

from public import public

from astx.base import AST, ASTKind, Expr, ReprStruct, SourceLocation
from astx.blocks import Block


@public
class Target(Expr):
    """Define the Architecture target for the program."""

    datalayout: str
    triple: str

    def __init__(self, datalayout: str, triple: str) -> None:
        """Initialize the AST instance."""
        self.datalayout = datalayout
        self.triple = triple

    def get_struct(self) -> ReprStruct:
        """Return the AST structure of the object."""
        node = {"TARGET": f"{self.datalayout}, {self.triple}"}
        return cast(ReprStruct, node)


@public
class Module(Block):
    """AST main expression class."""

    name: str

    def __init__(
        self,
        name: str = "main",
        loc: SourceLocation = SourceLocation(0, 0),
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

    def get_struct(self) -> ReprStruct:
        """Return the AST structure of the object."""
        block_node = []

        for node in self.nodes:
            block_node.append(node.get_struct())

        module_node = {f"MODULE[{self.name}]": block_node}

        return cast(ReprStruct, module_node)


@public
class Package(AST):
    """AST class for Package."""

    name: str
    modules: list[Module]
    packages: list[Package]

    def __init__(
        self,
        name: str = "main",
        modules: list[Module] = [],
        packages: list[Package] = [],
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the AST instance."""
        super().__init__(loc=loc)
        self.name = name
        self.modules = copy.deepcopy(modules)
        self.packages = copy.deepcopy(packages)

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return f"PACKAGE[{self.name}]"

    def get_struct(self) -> ReprStruct:
        """Return the AST structure of the object."""
        packages = []
        modules = []

        for package in self.packages:
            packages.append(package.get_struct())

        for module in self.modules:
            modules.append(module.get_struct())

        package_node = {
            str(self): {
                "modules": modules,
                "packages": packages,
            }
        }

        return cast(ReprStruct, package_node)


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
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the AST instance."""
        super().__init__(
            name=name, modules=modules, packages=packages, loc=loc
        )
        self.target = copy.deepcopy(target)

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return f"PROGRAM[{self.name}]"
