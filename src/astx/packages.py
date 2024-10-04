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
    StatementType,
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

    # def get_struct(self, simplified: bool = False) -> ReprStruct: """Return
    # the AST structure of the alias.""" key = "Alias" value = { "name":
    # self.name, "asname": self.asname, } return self._prepare_struct(key,
    # value, simplified) # Argument 2 to "_prepare_struct" of "AST" has
    # incompatible type "Dict[str, Optional[str]]"; expected "Union[str,
    # ReprStruct]"  [arg-type]

    # def get_struct(self, simplified: bool = False) -> ReprStruct:
    #     """Return the AST structure of the alias."""
    #     key = "Alias"
    #
    #     value_1 = {"name": self.name}
    #     value_2 = {"asname": self.asname}
    #
    #     value: ReprStruct = {
    #         **value_1,
    #         **value_2,
    #     }
    #
    # return self._prepare_struct(key, value, simplified) 199: error:
    # Unpacked dict entry 1 has incompatible type "Dict[str, Optional[str]]";
    # expected "SupportsKeysAndGetItem[str, Union[int, str, float, Dict[str,
    # DataTypesStruct], List[DataTypesStruct]]]"  [dict-item]

    #     def get_struct(self, simplified: bool = False) -> ReprStruct:
    #         """Return the AST structure of the alias."""
    #         key = "Alias"
    #
    #         value_1 = {"name": self.name}
    #         value_2 = {"asname": self.asname}
    #
    #         if self.asname:
    #             value: ReprStruct = {
    #                 **value_1,
    #                 **value_2,
    #             }
    #         else:
    #             value: ReprStruct = value_1
    #         return self._prepare_struct(key, value, simplified)
    #
    #
    # # 215: error: Unpacked dict entry 1 has incompatible type "Dict[str,
    # Optional[str]]"; expected "SupportsKeysAndGetItem[str, Union[int, str,
    # float, Dict[str, DataTypesStruct], List[DataTypesStruct]]]" # 218:
    # error: Name "value" already defined on line 213

    #     def get_struct(self, simplified: bool = False) -> ReprStruct:
    #         """Return the AST structure of the alias."""
    #         key = "Alias"
    #
    #         value_1 = {"name": self.name}
    #
    #         if self.asname:
    #             value: ReprStruct = {
    #                 **value_1,
    #                 **{"asname": self.asname},
    #             }
    #             return self._prepare_struct(key, value, simplified)
    #         else:
    #             value: ReprStruct = value_1
    #         return self._prepare_struct(key, value, simplified)
    #
    # # 238: error: Name "value" already defined on line 232

    #     def get_struct(self, simplified: bool = False) -> ReprStruct:
    #         """Return the AST structure of the alias."""
    #         key = "Alias"
    #
    #         value_1 = {"name": self.name}
    #
    #         if self.asname:
    #             value_1.update({"asname": self.asname})
    #
    # value: ReprStruct = value_1 return self._prepare_struct(key, value,
    # simplified) 252: error: Incompatible types in assignment (expression
    # has type "Dict[str, str]", variable has type "ReprStruct")  [assignment]

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the alias."""
        key = "Alias"

        name_dict = {"name": self.name}

        if self.asname:
            value_names: ReprStruct = {
                **name_dict,
                **{"asname": self.asname},
            }
            return self._prepare_struct(key, value_names, simplified)

        value_name: ReprStruct = {**name_dict}
        return self._prepare_struct(key, value_name, simplified)


@public
class ImportStmt(StatementType):
    """Represents an import statement."""

    names: list[AliasExpr]

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
class ImportFromStmt(StatementType):  # ISSUES HERE!
    """Represents an import-from statement."""

    module: Optional[str]
    names: list[AliasExpr]  #
    level: int

    def __init__(
        self,
        # names: Optional[list[AliasExpr]] = None,  #
        names: list[AliasExpr],  #
        module: Optional[
            str
        ] = "",  # None, # put empty string here to avoid different data types
        level: int = 0,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.module = module
        # self.names = names or []  # does this work?
        self.names = names
        self.level = level
        self.kind = ASTKind.ImportFromStmtKind

    def __str__(self) -> str:
        """Return a string representation of the import-from statement."""
        level_dots = "." * self.level
        module_str = (
            f"{level_dots}{self.module}" if self.module else level_dots
        )
        # if self.names:
        #     names_str = ", ".join(str(name) for name in self.names)
        # else:
        #     names_str = "*"
        names_str = ", ".join(str(name) for name in self.names)
        return f"from {module_str} import {names_str}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the import-from statement."""
        key = "ImportFrom"

        level_dict = {"level": self.level}
        # if self.names:
        #     names_values = cast(
        #         ReprStruct,
        #         [name.get_struct(simplified) for name in self.names],
        #     )
        #     names_dict = {"names": names_values}
        # else:
        #     names_dict = {"names": "*"}
        # src/astx/packages.py:337: error: Dict entry 0 has incompatible type
        # "str": "str"; expected "str": "Union[List[DataTypesStruct],
        # DictDataTypesStruct]"  [dict-item]

        names_values = cast(
            ReprStruct,
            [name.get_struct(simplified) for name in self.names],
        )
        names_dict = {"names": names_values}

        if self.module:
            module_dict = {"module": self.module}
            value_module: ReprStruct = {
                **module_dict,
                **level_dict,
                **names_dict,
            }
            return self._prepare_struct(key, value_module, simplified)

        value: ReprStruct = {
            **level_dict,
            **names_dict,
        }
        return self._prepare_struct(key, value, simplified)

        # def get_struct(self, simplified: bool = False) -> ReprStruct:
        #     """Return the AST structure of the import-from statement."""
        #     key = "ImportFrom"
        #     value = {
        #         "module": self.module,
        #         "level": self.level,
        #         "names": [
        #             name.get_struct(simplified) for name in self.names
        #         ],
        #     }
        #     return self._prepare_struct(key, value, simplified)

    # 344: error: Argument 2 to "_prepare_struct" of "AST" has incompatible
    # type "Dict[str, Union[List[Union[List[DataTypesStruct],
    # DictDataTypesStruct]], int, str, None]]"; expected
    # "Union[str, ReprStruct]
    #
    # def get_struct(self, simplified: bool = False) -> ReprStruct:
    #     """Return the AST structure of the import-from statement."""
    #     key = "ImportFrom"
    #
    #     level_dict = {"level": self.level}
    #     names_values = [
    #         name.get_struct(simplified) for name in self.names
    #     ]
    #     names_dict = {"names": names_values}
    #
    #     if self.module:
    #         module_dict = {"module": self.module}
    #         value_module: ReprStruct = {
    #             **module_dict,
    #             **level_dict,
    #             **names_dict,
    #         }
    #         return self._prepare_struct(key, value_module, simplified)
    #
    #     value: ReprStruct = {
    #         **level_dict,
    #         **names_dict,
    #     }
    #     return self._prepare_struct(key, value, simplified)

    # src/astx/packages.py:383: error: Unpacked dict entry 2 has incompatible
    # type "Dict[str, List[Union[List[DataTypesStruct],
    # DictDataTypesStruct]]]"; expected "SupportsKeysAndGetItem[str,
    # Union[int, str, float, Dict[str, DataTypesStruct],
    # List[DataTypesStruct]]]"  [dict-item] src/astx/packages.py:389: error:
    # Unpacked dict entry 1 has incompatible type "Dict[str, List[Union[List[
    # DataTypesStruct], DictDataTypesStruct]]]"; expected
    # "SupportsKeysAndGetItem[str, Union[int, str, float, Dict[str,
    # DataTypesStruct], List[DataTypesStruct]]]"  [dict-item]


#     def get_struct(self, simplified: bool = False) -> ReprStruct:
#         """Return the AST structure of the import-from statement."""
#         key = "ImportFrom"
#
#         module_dict: Dict[str, Union[str, None]] = {"module": self.module}
#         level_dict = {"level": self.level}
#         names_values = cast(
#             ReprStruct, [name.get_struct(simplified) for name in self.names]
#         )
#         names_dict = {"names": names_values}
#
#         value_module: ReprStruct = {
#             **module_dict,
#             **level_dict,
#             **names_dict,
#         }
#         return self._prepare_struct(key, value_module, simplified)
#
# 407: error: Unpacked dict entry 0 has incompatible type "Dict[str,
# Optional[str]]"; expected "SupportsKeysAndGetItem[str, Union[int, str,
# float, Dict[str, DataTypesStruct], List[DataTypesStruct]]]"
