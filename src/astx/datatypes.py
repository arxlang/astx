from __future__ import annotations

from astx.base import DataType, ASTKind, SourceLocation, ExprType
from astx.operators import BinaryOp


class DataTypeOps(DataType):
    def __add__(self, other: DataType) -> BinaryOp:
        return BinaryOp("+", self, other)

    def __sub__(self, other: DataType) -> BinaryOp:
        return BinaryOp("-", self, other)

    def __div__(self, other: DataType) -> BinaryOp:
        return BinaryOp("/", self, other)

    def __mul__(self, other: DataType) -> BinaryOp:
        return BinaryOp("*", self, other)

    def __pow__(self, other: DataType) -> BinaryOp:
        return BinaryOp("^", self, other)

    def __mod__(self, other: DataType) -> BinaryOp:
        return BinaryOp("%", self, other)


class Number(DataTypeOps):
    """Number data type expression."""


class Integer(Number):
    """Integer number data type expression."""


class SignedInteger(Integer):
    """Signed integer number data type expression."""


class Int8(SignedInteger):
    """Int8 data type expression."""

    nbytes: int = 1


class Int16(SignedInteger):
    """Int16 data type expression."""

    nbytes: int = 2


class Int32(SignedInteger):
    """Int32 data type expression."""

    nbytes: int = 4


class Int64(SignedInteger):
    """Int64 data type expression."""

    nbytes: int = 8


class Floating(Number):
    """AST for the literal float number."""


class Float16(Floating):
    """Float16 data type expression."""


class Float32(Floating):
    """Float32 data type expression."""


class Float64(Floating):
    """Float64 data type expression."""


class Boolean(DataType):
    """Boolean data type expression."""


class Literal(DataTypeOps):
    """Literal Data type."""

    type_: ExprType
    loc: SourceLocation


class Int32Literal(Literal):
    value: int

    def __init__(
        self, value: int, loc: SourceLocation = SourceLocation(0, 0)
    ) -> None:
        super().__init__(loc)
        self.value = value
        self.type_ = Int32
        self.loc = loc


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
