"""ASTx Data Types module."""

from __future__ import annotations

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    DataType,
    ExprType,
    ReprStruct,
    SourceLocation,
)
from astx.tools.typing import typechecked
from astx.variables import Variable


@public
@typechecked
class DataTypeOps(DataType):
    """Overload some magic functions used for the main operations."""

    def __hash__(self) -> int:
        """Ensure that the hash method is not None."""
        return super().__hash__()

    def __add__(self, other: DataType) -> BinaryOp:
        """Overload the magic `add` method."""
        return BinaryOp("+", self, other)

    def __eq__(self, other: DataType) -> BinaryOp:  # type: ignore
        """Overload the magic `eq` method."""
        return BinaryOp("==", self, other)

    def __floordiv__(self, other: DataType) -> BinaryOp:
        """Overload the magic `floordiv` method."""
        return BinaryOp("//", self, other)

    def __ge__(self, other: DataType) -> BinaryOp:
        """Overload the magic `ge` method."""
        return BinaryOp(">=", self, other)

    def __gt__(self, other: DataType) -> BinaryOp:
        """Overload the magic `gt` method."""
        return BinaryOp(">", self, other)

    def __le__(self, other: DataType) -> BinaryOp:
        """Overload the magic `le` method."""
        return BinaryOp("<=", self, other)

    def __lt__(self, other: DataType) -> BinaryOp:
        """Overload the magic `lt` method."""
        return BinaryOp("<", self, other)

    def __mod__(self, other: DataType) -> BinaryOp:
        """Overload the magic `mod` method."""
        return BinaryOp("%", self, other)

    def __mul__(self, other: DataType) -> BinaryOp:
        """Overload the magic `mul` method."""
        return BinaryOp("*", self, other)

    def __ne__(self, other: DataType) -> BinaryOp:  # type: ignore
        """Overload the magic `ne` method."""
        return BinaryOp("!=", self, other)

    def __neg__(self) -> UnaryOp:
        """Overload the magic `neg` method."""
        return UnaryOp("-", self)

    def __pos__(self) -> UnaryOp:
        """Overload the magic `pos` method."""
        return UnaryOp("+", self)

    def __pow__(self, other: DataType) -> BinaryOp:
        """Overload the magic `pow` method."""
        return BinaryOp("^", self, other)

    def __sub__(self, other: DataType) -> BinaryOp:
        """Overload the magic `sub` method."""
        return BinaryOp("-", self, other)

    def __truediv__(self, other: DataType) -> BinaryOp:
        """Overload the magic `truediv` method."""
        return BinaryOp("/", self, other)


@public
@typechecked
class UnaryOp(DataTypeOps):
    """AST class for the unary operator."""

    def __init__(
        self,
        op_code: str,
        operand: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the UnaryOp instance."""
        super().__init__()
        self.loc = loc
        self.op_code = op_code
        self.operand = operand
        self.kind = ASTKind.UnaryOpKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"UnaryOp[{self.op_code}]({self.operand})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = f"UNARY[{self.op_code}]"
        value = self.operand.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class BinaryOp(DataTypeOps):
    """AST class for the binary operator."""

    type_: ExprType

    def __init__(
        self,
        op_code: str,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the BinaryOp instance."""
        super().__init__()

        self.loc = loc
        self.op_code = op_code
        self.lhs = lhs
        self.rhs = rhs
        self.kind = ASTKind.BinaryOpKind

        if not (
            isinstance(lhs.type_, DataType) and isinstance(rhs.type_, DataType)
        ):
            raise Exception(
                "For now, binary operators are just allowed for `DataType`."
                f"LHS: {lhs.type_}, RHS: {rhs.type_}"
            )

        if lhs.type_ == rhs.type_:
            self.type_ = lhs.type_
        else:
            # type inference
            self.type_ = max([lhs.type_, rhs.type_], key=lambda v: v.nbytes)

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"BinaryOp[{self.op_code}]({self.lhs},{self.rhs})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure that represents the object."""
        key = f"BINARY[{self.op_code}]"
        lhs = {"lhs": self.lhs.get_struct(simplified)}
        rhs = {"rhs": self.rhs.get_struct(simplified)}

        content: ReprStruct = {**lhs, **rhs}
        return self._prepare_struct(key, content, simplified)


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
