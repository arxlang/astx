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
from astx.literals import LiteralNone
from astx.tools.typing import typechecked


@public
@typechecked
class SubscriptExpr(Expr):
    """AST class for subscript expressions."""

    value: Expr
    index: Expr
    lower: Expr
    upper: Expr
    step: Expr

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
        loc: SourceLocation
            The source location of the expression.
        parent (optional): ASTNodes
            The parent AST node.
        """
        super().__init__(loc=loc, parent=parent)
        self.value: Expr = value if value is not None else LiteralNone()
        self.index: Expr = index if index is not None else LiteralNone()
        self.lower: Expr = lower if lower is not None else LiteralNone()
        self.upper: Expr = upper if upper is not None else LiteralNone()
        self.step: Expr = step if step is not None else LiteralNone()
        self.kind = ASTKind.SubscriptExprKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        lower_str = (
            str(self.lower)
            if not isinstance(self.lower, LiteralNone)
            else str(self.index)
        )

        upper_str = (
            ":" + str(self.upper)
            if not isinstance(self.upper, LiteralNone)
            else ""
        )
        step_str = (
            ":" + str(self.step)
            if not isinstance(self.step, LiteralNone)
            else ""
        )
        return f"SubscriptExpr({self.value}[{lower_str}{upper_str}{step_str}])"

    def _get_struct_wrapper(self, simplified: bool) -> DictDataTypesStruct:
        """Return the AST structure of the object."""
        value_dict: ReprStruct = {"indexed": self.value.get_struct(simplified)}

        lower_key = "index" if isinstance(self.lower, LiteralNone) else "lower"
        lower_value = (
            self.index.get_struct(simplified)
            if isinstance(self.lower, LiteralNone)
            else self.lower.get_struct(simplified)
        )
        lower_dict: ReprStruct = {lower_key: lower_value}

        upper_dict: ReprStruct = {}
        if not isinstance(self.upper, LiteralNone):
            upper_dict = {"upper": self.upper.get_struct(simplified)}

        step_dict: ReprStruct = {}
        if not isinstance(self.step, LiteralNone):
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
