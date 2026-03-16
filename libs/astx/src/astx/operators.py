"""
title: ASTx classes for the operators.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Literal, Optional, cast

from public import public
from typing_extensions import TypeAlias

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
from astx.data import Variable
from astx.tools.typing import typechecked

if TYPE_CHECKING:
    from astx.data import Identifier


@public
@typechecked
class WalrusOp(DataType):
    """
    title: AST class for the Walrus (assignment expression) operator.
    attributes:
      lhs:
        type: Variable
      rhs:
        type: DataType
      kind:
        type: ASTKind
    """

    lhs: Variable
    rhs: DataType
    kind: ASTKind

    def __init__(
        self,
        lhs: Variable,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """
        title: Initialize the WalrusOp instance.
        parameters:
          lhs:
            type: Variable
          rhs:
            type: DataType
          loc:
            type: SourceLocation
        """
        super().__init__(loc=loc)
        self.lhs = lhs
        self.rhs = rhs
        self.kind = ASTKind.WalrusOpKind

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"WalrusOp[:=]({self.lhs} := {self.rhs})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure that represents the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = "WALRUS[:=]"
        lhs = {"lhs": self.lhs.get_struct(simplified)}
        rhs = {"rhs": self.rhs.get_struct(simplified)}

        content: ReprStruct = {**lhs, **rhs}
        return self._prepare_struct(key, content, simplified)


@public
@typechecked
class AssignmentExpr(Expr):
    """
    title: AST class for assignment expressions.
    attributes:
      kind:
        type: ASTKind
      targets:
        type: ASTNodes[Expr]
      value:
        type: Expr
    """

    kind: ASTKind

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
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"AssignmentExpr[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
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
    """
    title: AST class for variable declaration.
    attributes:
      loc:
        type: SourceLocation
      kind:
        type: ASTKind
      name:
        type: str
      value:
        type: Expr
    """

    loc: SourceLocation
    kind: ASTKind

    name: str
    value: Expr

    def __init__(
        self,
        name: str,
        value: Expr,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the VarExprAST instance.
        parameters:
          name:
            type: str
          value:
            type: Expr
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.loc = loc
        self.name = name
        self.value = value
        self.kind = ASTKind.VariableAssignmentKind

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"VariableAssignment[{self.name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = str(self)
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


OpCodeAugAssign: TypeAlias = Literal[
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
]


@public
@typechecked
class AugAssign(DataType):
    """
    title: AST class for augmented assignment.
    attributes:
      kind:
        type: ASTKind
      target:
        type: Identifier
      op_code:
        type: OpCodeAugAssign
      value:
        type: DataType
    """

    kind: ASTKind

    target: Identifier
    op_code: OpCodeAugAssign
    value: DataType

    def __init__(
        self,
        target: Identifier,
        op_code: OpCodeAugAssign,
        value: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        super().__init__(loc=loc)
        self.target = target
        self.op_code = op_code
        self.value = value
        self.kind = ASTKind.AugmentedAssignKind

    def __str__(self) -> str:
        """
        title: Return a string that represents the augmented assignment object.
        returns:
          type: str
        """
        return f"AugAssign[{self.op_code}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = str(self)
        value: ReprStruct = {
            "target": self.target.get_struct(simplified),
            "value": self.value.get_struct(simplified),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class CompareOp(DataType):
    """
    title: AST class for comparison operators acting as properties.
    attributes:
      ops:
        type: list[Literal[==, !=, <, >, <=, >=]]
      comparators:
        type: list[DataType]
      left:
        type: DataType
      kind:
        type: ASTKind
    """

    ops: list[Literal["==", "!=", "<", ">", "<=", ">="]]
    comparators: list[DataType]
    left: DataType
    kind: ASTKind

    def __init__(
        self,
        left: DataType,
        ops: Iterable[Literal["==", "!=", "<", ">", "<=", ">="]],
        comparators: Iterable[DataType],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """
        title: Initialize the CompareOp instance.
        parameters:
          left:
            type: DataType
          ops:
            type: Iterable[Literal[==, !=, <, >, <=, >=]]
          comparators:
            type: Iterable[DataType]
          loc:
            type: SourceLocation
        """
        super().__init__(loc=loc)
        self.ops = list(ops)
        self.comparators = list(comparators)
        if len(self.ops) != len(self.comparators):
            raise ValueError(
                "Number of operators must equal number of comparators."
            )
        for op in self.ops:
            if op not in ["==", "!=", "<", ">", "<=", ">="]:
                raise ValueError(f"Invalid comparison operator: {op}")
        self.left = left
        self.kind = ASTKind.CompareOpKind

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        ops_str = ", ".join(self.ops)
        return f"Compare[{ops_str}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure that represents the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        ops_str = ", ".join(self.ops)
        key = f"COMPARE[{ops_str}]"
        content: ReprStruct = {
            "left": self.left.get_struct(simplified),
            "comparators": [
                comp.get_struct(simplified) for comp in self.comparators
            ],
        }
        return self._prepare_struct(key, content, simplified)


@public
@typechecked
class Starred(Expr):
    """
    title: AST class for starred expressions (*expr).
    attributes:
      kind:
        type: ASTKind
      value:
        type: Expr
    """

    kind: ASTKind

    value: Expr

    def __init__(
        self,
        value: Expr,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.kind = ASTKind.StarredKind

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"Starred[*]({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure that represents the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = "STARRED[*]"
        content: ReprStruct = {"value": self.value.get_struct(simplified)}
        return self._prepare_struct(key, content, simplified)
