"""ASTx Data Types module."""
from __future__ import annotations

from public import public

from astx.base import DataType, ExprType, SourceLocation
from astx.operators import BinaryOp


@public
class DataTypeOps(DataType):
    """Overload some magic functions used for the main operations."""

    def __add__(self, other: DataType) -> BinaryOp:
        """Overload the magic `add` method."""
        return BinaryOp("+", self, other)

    def __sub__(self, other: DataType) -> BinaryOp:
        """Overload the magic `sub` method."""
        return BinaryOp("-", self, other)

    def __div__(self, other: DataType) -> BinaryOp:
        """Overload the magic `div` method."""
        return BinaryOp("/", self, other)

    def __mul__(self, other: DataType) -> BinaryOp:
        """Overload the magic `mul` method."""
        return BinaryOp("*", self, other)

    def __pow__(self, other: DataType) -> BinaryOp:
        """Overload the magic `pow` method."""
        return BinaryOp("^", self, other)

    def __mod__(self, other: DataType) -> BinaryOp:
        """Overload the magic `mod` method."""
        return BinaryOp("%", self, other)


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


@public
class Int32Literal(Literal):
    """Int32Literal data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = SourceLocation(0, 0)
    ) -> None:
        super().__init__(loc)
        self.value = value
        self.type_ = Int32
        self.loc = loc
