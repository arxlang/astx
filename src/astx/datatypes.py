"""ASTx Data Types module."""
from __future__ import annotations

from typing import Any

from public import public

from astx.base import (
    ASTKind,
    DataType,
    ExprType,
    ReprStruct,
    SourceLocation,
)

# Operators


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

    def __truediv__(self, other: DataType) -> BinaryOp:
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
class UnaryOp(DataTypeOps):
    """AST class for the unary operator."""

    def __init__(
        self,
        op_code: str,
        operand: DataType,
        loc: SourceLocation = SourceLocation(0, 0),
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

    def get_struct(self) -> ReprStruct:
        """Return the AST structure of the object."""
        return {f"UNARY[{self.op_code}]": self.operand.get_struct()}


@public
class BinaryOp(DataTypeOps):
    """AST class for the binary operator."""

    type_: ExprType

    def __init__(
        self,
        op_code: str,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the BinaryOp instance."""
        super().__init__()

        self.loc = loc
        self.op_code = op_code
        self.lhs = lhs
        self.rhs = rhs
        self.kind = ASTKind.BinaryOpKind

        if not (
            issubclass(lhs.type_, Number) and issubclass(lhs.type_, Number)
        ):
            raise Exception(
                "For now, binary operators are just allowed for numbers."
                f"LHS: {lhs.type_}, RHS: {rhs.type_}"
            )

        if lhs.type_ == rhs.type_:
            self.type_ = lhs.type_
        else:
            # inference
            self.type_ = max([lhs.type_, rhs.type_], key=lambda v: v.nbytes)

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"BinaryOp[{self.op_code}]({self.lhs},{self.rhs})"

    def get_struct(self) -> ReprStruct:
        """Return the AST structure that represents the object."""
        return {
            f"BINARY[{self.op_code}]": {
                "lhs": self.lhs.get_struct(),
                "rhs": self.rhs.get_struct(),
            }
        }


# Data Types


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

    def __str__(self) -> str:
        """Return a string that represents the object."""
        klass = self.__class__.__name__
        return f"{klass}({self.value})"

    def get_struct(self) -> ReprStruct:
        """Return the AST representation for the object."""
        return {f"Literal[{self.type_}]": self.value}


@public
class LiteralInt8(Literal):
    """LiteralInt8 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = SourceLocation(0, 0)
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
        self, value: int, loc: SourceLocation = SourceLocation(0, 0)
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
        self, value: int, loc: SourceLocation = SourceLocation(0, 0)
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
        self, value: int, loc: SourceLocation = SourceLocation(0, 0)
    ) -> None:
        """Initialize LiteralInt64."""
        super().__init__(loc)
        self.value = value
        self.type_ = Int64
        self.loc = loc
