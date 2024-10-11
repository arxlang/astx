"""Define ASTx for more broader scope."""

from __future__ import annotations

import copy

from typing import Optional, cast

from public import public
from typeguard import typechecked

from astx.base import (
    AST,
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    Expr,
    SourceLocation,
    StatementType,
)
from astx.blocks import Block
from astx.types import ReprStruct


@public
class Target(Expr):
    """Define the Architecture target for the program."""

    datalayout: str
    triple: str

    @typechecked
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

    @typechecked
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

    @typechecked
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

    @typechecked
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

    @typechecked
    def __init__(
        self,
        name: str,
        asname: str = "",
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

        name_dict = {"name": self.name}
        asname_dict = {"asname": self.asname} if self.asname else {}
        value: ReprStruct = {
            **name_dict,
            **asname_dict,
        }
        return self._prepare_struct(key, value, simplified)


@public
class ImportStmt(StatementType):
    """Represents an import statement."""

    names: list[AliasExpr]

    @typechecked
    def __init__(
        self,
        names: list[AliasExpr],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.names = names
        self.kind = ASTKind.ImportStmtKind

    def __str__(self) -> str:
        """Return a string representation of the import statement."""
        names_str = ", ".join(str(name) for name in self.names)
        return f"import {names_str}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the import statement."""
        key = "Import"
        value = cast(
            ReprStruct, [name.get_struct(simplified) for name in self.names]
        )
        return self._prepare_struct(key, value, simplified)


@public
class ImportFromStmt(StatementType):
    """Represents an import-from statement."""

    module: Optional[str]
    names: list[AliasExpr]
    level: int

    @typechecked
    def __init__(
        self,
        names: list[AliasExpr],
        module: str = "",
        level: int = 0,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.module = module
        self.names = names
        self.level = level
        self.kind = ASTKind.ImportFromStmtKind

    def __str__(self) -> str:
        """Return a string representation of the import-from statement."""
        level_dots = "." * self.level
        module_str = (
            f"{level_dots}{self.module}" if self.module else level_dots
        )
        names_str = ", ".join(str(name) for name in self.names)
        return f"from {module_str} import {names_str}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the import-from statement."""
        key = "ImportFrom"

        module_dict = {"module": self.module} if self.module else {}
        level_dict = {"level": self.level}
        names_values = cast(
            ReprStruct,
            [name.get_struct(simplified) for name in self.names],
        )
        names_dict = {"names": names_values}

        value: ReprStruct = {
            **module_dict,
            **level_dict,
            **names_dict,
        }

        return self._prepare_struct(key, value, simplified)


@public
class ImportExpr(Expr):
    """Represents an import operation as an expression."""

    name: str
    asname: str

    # maybe put @typechecked here?
    def __init__(
        self,
        name: str,
        asname: str = "",
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.name = name
        self.asname = asname
        self.kind = ASTKind.ImportExprKind
        # You can set the type_ attribute if needed
        # self.type_ = ModuleType or similar

    def __str__(self) -> str:
        """Return a string representation of the import expression."""
        if self.asname:
            return f"import {self.name} as {self.asname}"
        else:
            return f"import {self.name}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the import expression."""
        key = "ImportExpr"
        value: ReprStruct = {
            "name": self.name,
            "asname": self.asname,
        }
        return self._prepare_struct(key, value, simplified)


@public
class ImportFromExpr(Expr):
    """Represents a 'from ... import ...' operation as an expression."""

    module: str
    names: list[str]
    asnames: dict[str, str]  # Mapping from name to alias
    level: int  # Number of leading dots for relative imports

    def __init__(
        self,
        names: list[str],
        module: str = "",
        asnames: dict[str, str] = {},
        level: int = 0,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.names = names
        self.module = module
        self.asnames = asnames
        self.level = level
        self.kind = ASTKind.ImportFromExprKind
        # You can set the type_ attribute if needed

    def __str__(self) -> str:
        """Return a string representation of the import-from expression."""
        level_dots = "." * self.level
        module_str = (
            f"{level_dots}{self.module}" if self.module else level_dots
        )
        imports = []
        for name in self.names:
            asname = self.asnames.get(name)
            if asname:
                imports.append(f"{name} as {asname}")
            else:
                imports.append(name)
        names_str = ", ".join(imports)
        return f"from {module_str} import {names_str}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the import-from expression."""
        key = "ImportFromExpr"

        module_dict = {"module": self.module} if self.module else {}
        level_dict = {"level": self.level}
        names_values = cast(
            ReprStruct,
            [
                {"name": name, "alias": self.asnames.get(name)}
                for name in self.names
            ],
        )
        names_dict = {"names": names_values}

        value: ReprStruct = {
            **module_dict,
            **level_dict,
            **names_dict,
        }
        return self._prepare_struct(key, value, simplified)
