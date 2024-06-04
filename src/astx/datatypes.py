"""ASTx Data Types module."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    DataType,
    ExprType,
    SourceLocation,
)
from astx.types import ReprStruct


@public
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
            issubclass(lhs.type_, (Number, BinaryOp, DataType))
            and issubclass(rhs.type_, (Number, BinaryOp, DataType))
        ):
            raise Exception(
                "For now, binary operators are just allowed for numbers."
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


# Data Types


@public
class AnyExpr(DataTypeOps):
    """Generic data type expression."""


@public
class Number(DataTypeOps):
    """Number data type expression."""


@public
class Integer(Number):
    """Integer number data type expression."""


@public
class SignedInteger(Integer):
    """Signed integer number data type expression."""


@public
class Int8(SignedInteger):
    """Int8 data type expression."""

    nbytes: int = 1


@public
class Int16(SignedInteger):
    """Int16 data type expression."""

    nbytes: int = 2


@public
class Int32(SignedInteger):
    """Int32 data type expression."""

    nbytes: int = 4


@public
class Int64(SignedInteger):
    """Int64 data type expression."""

    nbytes: int = 8


@public
class Floating(Number):
    """AST for the literal float number."""


@public
class Float16(Floating):
    """Float16 data type expression."""


@public
class Float32(Floating):
    """Float32 data type expression."""


@public
class Float64(Floating):
    """Float64 data type expression."""


@public
class Boolean(DataType):
    """Boolean data type expression."""


@public
class Literal(DataTypeOps):
    """Literal Data type."""

    type_: ExprType
    loc: SourceLocation
    value: Any

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*args, **kwargs)
        self.ref = uuid4().hex

    def __str__(self) -> str:
        """Return a string that represents the object."""
        klass = self.__class__.__name__
        return f"{klass}({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST representation for the object."""
        key = f"Literal[{self.type_}]: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
class LiteralInt8(Literal):
    """LiteralInt8 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInt8."""
        super().__init__(loc)
        self.value = value
        self.type_ = Int8
        self.loc = loc


@public
class LiteralInt16(Literal):
    """LiteralInt16 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInt16."""
        super().__init__(loc)
        self.value = value
        self.type_ = Int16
        self.loc = loc


@public
class LiteralInt32(Literal):
    """LiteralInt32 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInt32."""
        super().__init__(loc)
        self.value = value
        self.type_ = Int32
        self.loc = loc


@public
class LiteralInt64(Literal):
    """LiteralInt64 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInt64."""
        super().__init__(loc)
        self.value = value
        self.type_ = Int64
        self.loc = loc


@public
class LiteralBoolean(Literal):
    """LiteralBoolean data type class."""

    value: bool

    def __init__(
        self, value: bool, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralBoolean."""
        super().__init__(loc)
        self.value = value
        self.type_ = Boolean
        self.loc = loc
