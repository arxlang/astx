"""Module for subscripts definitions/declarations."""

from typing import Optional, cast

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    DictDataTypesStruct,
    Expr,
    ReprStruct,
    SourceLocation,
)
from astx.tools.typing import typechecked


@public
@typechecked
class SubscriptExpr(Expr):
    """AST class for subscript expressions."""

    value: Expr
    index: Optional[Expr]
    lower: Optional[Expr]
    upper: Optional[Expr]
    step: Optional[Expr]

    def __init__(
        self,
        value: Expr,
        index: Optional[Expr] = None,
        lower: Optional[Expr] = None,
        upper: Optional[Expr] = None,
        step: Optional[Expr] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        Initialize the SubscriptExpr instance.

        Parameters
        ----------
        value: Expr
            The expression representing the object being indexed (e.g.,
        an array or list).
        index (optional): Expr
            The index of the variable.
        lower (optional): Expr
            The lower bound of the slice (inclusive).
        upper (optional): Expr
            The upper bound of the slice (exclusive).
        step (optional): Expr
            The step size for the slice.
        loc:
            The source location of the expression.
        parent (optional): ASTNodes
            The parent AST node.
        """
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.index = index
        self.lower = lower
        self.upper = upper
        self.step = step
        self.kind = ASTKind.SubscriptExprKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        lower_str = str(self.lower) if self.lower else str(self.index)
        upper_str = ":" + str(self.upper) if self.upper else ""
        step_str = ":" + str(self.step) if self.step else ""
        return f"SubscriptExpr({self.value}[{lower_str}{upper_str}{step_str}])"

    def _get_struct_wrapper(self, simplified: bool) -> DictDataTypesStruct:
        """Return the AST structure of the object."""
        value_dict: ReprStruct = {"indexed": self.value.get_struct(simplified)}

        lower_key = "lower" if self.lower else "index"
        lower_value = (
            self.lower.get_struct(simplified)
            if self.lower
            else self.index.get_struct(simplified)
        )
        lower_dict: ReprStruct = {lower_key: lower_value}

        upper_dict: ReprStruct = {}
        if self.upper:
            upper_dict = {"upper": self.upper.get_struct(simplified)}

        step_dict: ReprStruct = {}
        if self.step:
            step_dict = {"step": self.step.get_struct(simplified)}

        value: DictDataTypesStruct = {
            **cast(DictDataTypesStruct, value_dict),
            **cast(DictDataTypesStruct, lower_dict),
            **cast(DictDataTypesStruct, upper_dict),
            **cast(DictDataTypesStruct, step_dict),
        }
        return value

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "SubscriptExpr"

        value = self._get_struct_wrapper(simplified)

        return self._prepare_struct(key, value, simplified)
