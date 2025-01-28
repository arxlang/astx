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

    var_: Expr
    index: Expr
    upper: Optional[Expr]
    step: Optional[Expr]

    def __init__(
        self,
        var_: Expr,
        index: Expr,
        upper: Optional[Expr] = None,
        step: Optional[Expr] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        Initialize the SubscriptExpr instance.

        Parameters
        ----------
        - value: The expression representing the object being indexed (e.g.,
        an array or list).
        - index: The index of the variable. In case of a slice, the lower bound
        of the slice (inclusive).
        - upper (optional): The upper bound, in case of a slice (exclusive).
        - step (optional): The step size, in case of a slice.
        - loc: The source location of the expression.
        - parent: The parent AST node.
        """
        super().__init__(loc=loc, parent=parent)
        self.var = var_
        self.index = index
        self.upper = upper
        self.step = step
        self.kind = ASTKind.SubscriptExprKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        index_str = str(self.index)
        upper_str = ":" + str(self.upper) if self.upper else ""
        step_str = ":" + str(self.step) if self.step else ""
        return f"SubscriptExpr({self.var}[{index_str}{upper_str}{step_str}])"

    def _get_struct_wrapper(self, simplified: bool) -> DictDataTypesStruct:
        """Return the AST structure of the object."""
        var_dict: ReprStruct = {"indexed": self.var.get_struct(simplified)}
        index_key = "lower" if self.upper else "index"
        index_dict: ReprStruct = {
            index_key: self.index.get_struct(simplified)
        }

        upper_dict: ReprStruct = {}
        step_dict: ReprStruct = {}

        if self.upper:
            upper_dict = {"upper": self.upper.get_struct(simplified)}

        if self.step:
            step_dict = {"step": self.step.get_struct(simplified)}

        value: DictDataTypesStruct = {
            **cast(DictDataTypesStruct, var_dict),
            **cast(DictDataTypesStruct, index_dict),
            **cast(DictDataTypesStruct, upper_dict),
            **cast(DictDataTypesStruct, step_dict),
        }
        return value

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "SubscriptExpr"

        value = self._get_struct_wrapper(simplified)

        return self._prepare_struct(key, value, simplified)
