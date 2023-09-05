"""Module for Variables."""
from typing import List, Tuple

from public import public

from astx.base import (
    ASTKind,
    DataType,
    Expr,
    ExprType,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.blocks import Block
from astx.operators import DataTypeOps


@public
class VarDecl(StatementType):
    """AST class for variable declaration."""

    var_names: List[Tuple[str, Expr]]
    type_name: str
    body: Block

    def __init__(
        self,
        var_names: List[Tuple[str, Expr]],
        type_name: str,
        body: Block,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the VarExprAST instance."""
        self.loc = loc
        self.var_names = var_names
        self.type_name = type_name
        self.body = body
        self.kind = ASTKind.VarKind


@public
class Variable(DataTypeOps):
    """AST class for the variable usage."""

    type_: ExprType
    value: DataType

    def __init__(
        self,
        name: str,
        type_: ExprType,
        value: DataType,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the Variable instance."""
        super().__init__(loc)
        self.name = name
        self.type_ = type_
        self.kind = ASTKind.VariableKind
        self.value: DataType = value

    def __str__(self) -> str:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        return f"Variable[{type_}]({self.value})"

    def get_struct(self) -> ReprStruct:
        """Return a string that represents the object."""
        type_ = self.type_.__name__
        return {f"Variable[{self.name}: {type_}]": self.value.get_struct()}
