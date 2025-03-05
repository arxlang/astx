"""ASTx classes for the operators."""

from __future__ import annotations

import operator

from typing import Iterable, Literal, Optional, cast

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    DataType,
    DictDataTypesStruct,
    Expr,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.literals.numeric import LiteralInt32
from astx.tools.typing import typechecked
from astx.variables import Variable


@public
@typechecked
class WalrusOp(DataType):
    """AST class for the Walrus (assignment expression) operator."""

    def __init__(
        self,
        lhs: Variable,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the WalrusOp instance."""
        super().__init__(loc=loc)
        self.lhs = lhs
        self.rhs = rhs
        self.kind = ASTKind.WalrusOpKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"WalrusOp[:=]({self.lhs} := {self.rhs})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure that represents the object."""
        key = "WALRUS[:=]"
        lhs = {"lhs": self.lhs.get_struct(simplified)}
        rhs = {"rhs": self.rhs.get_struct(simplified)}

        content: ReprStruct = {**lhs, **rhs}
        return self._prepare_struct(key, content, simplified)


@public
@typechecked
class AssignmentExpr(Expr):
    """AST class for assignment expressions."""

    targets: ASTNodes[Expr]
    value: Expr

    def __init__(
        self,
        targets: Iterable[Expr] | ASTNodes[Expr],
        value: Expr,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)

        if isinstance(targets, ASTNodes):
            self.targets = targets
        else:
            self.targets = ASTNodes()
            for target in targets:
                self.targets.append(target)

        self.value = value
        self.kind = ASTKind.AssignmentExprKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"AssignmentExpr[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "ASSIGNMENT-EXPR"
        targets_dict = {"targets": self.targets.get_struct(simplified)}
        value_dict = {"value": self.value.get_struct(simplified)}

        value = {
            **cast(DictDataTypesStruct, targets_dict),
            **cast(DictDataTypesStruct, value_dict),
        }

        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class VariableAssignment(StatementType):
    """AST class for variable declaration."""

    name: str
    value: Expr

    def __init__(
        self,
        name: str,
        value: Expr,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the VarExprAST instance."""
        super().__init__(loc=loc, parent=parent)
        self.loc = loc
        self.name = name
        self.value = value
        self.kind = ASTKind.VariableAssignmentKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"VariableAssignment[{self.name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = str(self)
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class AugAssign(DataType):
    """AST class for augmented assignment (+= , -= , |=, *= , /= , //= , eg)."""

    OPERATORS = {
        "+=": operator.iadd,
        "-=": operator.isub,
        "*=": operator.imul,
        "/=": operator.itruediv,
        "//=": operator.ifloordiv,
        "%=": operator.imod,
        "**=": operator.ipow,
        "&=": operator.iand,
        "|=": operator.ior,
        "^=": operator.ixor,
        "<<=": operator.ilshift,
        ">>=": operator.irshift,
    }

    def __init__(
        self,
        target: str,
        op_code: Literal[
            "+=",
            "-=",
            "*=",
            "/=",
            "//=",
            "%=",
            "**=",
            "&=",
            "|=",
            "^=",
            "<<=",
            ">>=",
        ],
        value: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        if aug_op not in self.OPERATORS:
            raise ValueError(f"Unsupported operator: {aug_op}")
        super().__init__(loc=loc)
        self.target = target
        self.aug_op = aug_op
        self.value = value
        self.kind = ASTKind.AugmentedAssignKind

    def __str__(self):
        """Return a string that represents the augmented assignment object."""
        value_str = (
            str(self.value)
            if not isinstance(self.value, LiteralInt32)
            else str(self.value.value)
        )
        return f"AugAssign[ {self.aug_op} ]({self.target} {self.aug_op} {value_str})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = str(self)
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)
