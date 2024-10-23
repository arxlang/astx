"""ASTx Data Types module."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from public import public
from typeguard import typechecked

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
        return BinaryOp("+", self, other)  # type: ignore[no-any-return]

    def __eq__(self, other: DataType) -> BinaryOp:  # type: ignore
        """Overload the magic `eq` method."""
        return BinaryOp("==", self, other)  # type: ignore[no-any-return]

    def __floordiv__(self, other: DataType) -> BinaryOp:
        """Overload the magic `floordiv` method."""
        return BinaryOp("//", self, other)  # type: ignore[no-any-return]

    def __ge__(self, other: DataType) -> BinaryOp:
        """Overload the magic `ge` method."""
        return BinaryOp(">=", self, other)  # type: ignore[no-any-return]

    def __gt__(self, other: DataType) -> BinaryOp:
        """Overload the magic `gt` method."""
        return BinaryOp(">", self, other)  # type: ignore[no-any-return]

    def __le__(self, other: DataType) -> BinaryOp:
        """Overload the magic `le` method."""
        return BinaryOp("<=", self, other)  # type: ignore[no-any-return]

    def __lt__(self, other: DataType) -> BinaryOp:
        """Overload the magic `lt` method."""
        return BinaryOp("<", self, other)  # type: ignore[no-any-return]

    def __mod__(self, other: DataType) -> BinaryOp:
        """Overload the magic `mod` method."""
        return BinaryOp("%", self, other)  # type: ignore[no-any-return]

    def __mul__(self, other: DataType) -> BinaryOp:
        """Overload the magic `mul` method."""
        return BinaryOp("*", self, other)  # type: ignore[no-any-return]

    def __ne__(self, other: DataType) -> BinaryOp:  # type: ignore
        """Overload the magic `ne` method."""
        return BinaryOp("!=", self, other)  # type: ignore[no-any-return]

    def __neg__(self) -> UnaryOp:
        """Overload the magic `neg` method."""
        return UnaryOp("-", self)  # type: ignore[no-any-return]

    def __pos__(self) -> UnaryOp:
        """Overload the magic `pos` method."""
        return UnaryOp("+", self)  # type: ignore[no-any-return]

    def __pow__(self, other: DataType) -> BinaryOp:
        """Overload the magic `pow` method."""
        return BinaryOp("^", self, other)  # type: ignore[no-any-return]

    def __sub__(self, other: DataType) -> BinaryOp:
        """Overload the magic `sub` method."""
        return BinaryOp("-", self, other)  # type: ignore[no-any-return]

    def __truediv__(self, other: DataType) -> BinaryOp:
        """Overload the magic `truediv` method."""
        return BinaryOp("/", self, other)  # type: ignore[no-any-return]


@public
class UnaryOp(DataTypeOps):
    """AST class for the unary operator."""

    @typechecked
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

    @typechecked
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
class UnsignedInteger(Integer):
    """Unsigned integer number data type expression."""


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
class Int128(SignedInteger):
    """Int128 data type expression."""

    nbytes: int = 16


@public
class UInt8(UnsignedInteger):
    """UInt8 data type expression."""

    nbytes: int = 1


@public
class UInt16(UnsignedInteger):
    """UInt8 data type expression."""

    nbytes: int = 2


@public
class UInt32(UnsignedInteger):
    """UInt8 data type expression."""

    nbytes: int = 4


@public
class UInt64(UnsignedInteger):
    """UInt8 data type expression."""

    nbytes: int = 8


@public
class UInt128(UnsignedInteger):
    """UInt8 data type expression."""

    nbytes: int = 16


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

    @typechecked
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

    @typechecked
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

    @typechecked
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

    @typechecked
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

    @typechecked
    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInt64."""
        super().__init__(loc)
        self.value = value
        self.type_ = Int64
        self.loc = loc


@public
class LiteralInt128(Literal):
    """LiteralInt128 data type class."""

    value: int

    @typechecked
    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInt128."""
        super().__init__(loc)
        self.value = value
        self.type_ = Int128
        self.loc = loc


@public
class LiteralUInt8(Literal):
    """LiteralUInt8 data type class."""

    value: int

    @typechecked
    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralUInt8."""
        super().__init__(loc)
        self.value = value
        self.type_ = UInt8
        self.loc = loc


@public
class LiteralUInt16(Literal):
    """LiteralUInt16 data type class."""

    value: int

    @typechecked
    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralUInt16."""
        super().__init__(loc)
        self.value = value
        self.type_ = UInt16
        self.loc = loc


@public
class LiteralUInt32(Literal):
    """LiteralUInt32 data type class."""

    value: int

    @typechecked
    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralUInt32."""
        super().__init__(loc)
        self.value = value
        self.type_ = UInt32
        self.loc = loc


@public
class LiteralUInt64(Literal):
    """LiteralUInt64 data type class."""

    value: int

    @typechecked
    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralUInt64."""
        super().__init__(loc)
        self.value = value
        self.type_ = UInt64
        self.loc = loc


@public
class LiteralUInt128(Literal):
    """LiteralUInt128 data type class."""

    value: int

    @typechecked
    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralUInt128."""
        super().__init__(loc)
        self.value = value
        self.type_ = UInt128
        self.loc = loc


@public
class LiteralBoolean(Literal):
    """LiteralBoolean data type class."""

    value: bool

    @typechecked
    def __init__(
        self, value: bool, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralBoolean."""
        super().__init__(loc)
        self.value = value
        self.type_ = Boolean
        self.loc = loc


@public
class LiteralFloat16(Literal):
    """LiteralFloat16 data type class."""

    value: float

    @typechecked
    def __init__(
        self, value: float, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralFloat16."""
        super().__init__(loc)
        self.value = value
        self.type_ = Float16
        self.loc = loc


@public
class LiteralFloat32(Literal):
    """LiteralFloat32 data type class."""

    value: float

    @typechecked
    def __init__(
        self, value: float, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralFloat32."""
        super().__init__(loc)
        self.value = value
        self.type_ = Float32
        self.loc = loc


@public
class LiteralFloat64(Literal):
    """LiteralFloat64 data type class."""

    value: float

    @typechecked
    def __init__(
        self, value: float, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralFloat64."""
        super().__init__(loc)
        self.value = value
        self.type_ = Float64
        self.loc = loc


@public
class Complex(Number):
    """Base class for complex numbers."""

    def __init__(self, real: float, imag: float) -> None:
        """Initialize a complex number with real and imaginary parts."""
        self.real = real
        self.imag = imag

    def __str__(self) -> str:
        """Return a string representation of the complex number."""
        return f"{self.real} + {self.imag}j"


@public
class Complex32(Complex):
    """Complex32 data type class."""

    nbytes: int = 8

    def __init__(self, real: float, imag: float) -> None:
        """Initialize a 32-bit complex number."""
        super().__init__(real, imag)


@public
class Complex64(Complex):
    """Complex64 data type class."""

    nbytes: int = 16

    def __init__(self, real: float, imag: float) -> None:
        """Initialize a 64-bit complex number."""
        super().__init__(real, imag)


@public
class LiteralComplex(Literal):
    """Base class for literal complex numbers."""

    value: Complex

    def __init__(
        self, value: Complex, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralComplex with a complex number."""
        super().__init__(loc)
        if isinstance(value, Complex):
            self.value = value
            self.type_ = (
                Complex64 if isinstance(value, Complex64) else Complex32
            )
        else:
            raise TypeError("Value must be an instance of Complex.")
        self.loc = loc

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"LiteralComplex({self.value.real} + {self.value.imag}j)"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST representation for the complex literal."""
        key = f"{self.__class__.__name__}: {self.value}"
        value: ReprStruct = {
            "real": self.value.real,
            "imag": self.value.imag,
        }
        return self._prepare_struct(key, value, simplified)


@public
class LiteralComplex32(LiteralComplex):
    """LiteralComplex32 data type class."""

    def __init__(
        self,
        real: float,
        imag: float,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize LiteralComplex32."""
        super().__init__(Complex32(real, imag), loc)
        self.type_ = Complex32


@public
class LiteralComplex64(LiteralComplex):
    """LiteralComplex64 data type class."""

    def __init__(
        self,
        real: float,
        imag: float,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize LiteralComplex64."""
        super().__init__(Complex64(real, imag), loc)
        self.type_ = Complex64


@public
class UTF8String(DataTypeOps):
    """Class for UTF-8 encoded strings."""

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        if not isinstance(value, str):
            raise TypeError("Expected a valid UTF-8 string.")
        value.encode("utf-8")
        super().__init__()
        self.value = value
        self.loc = loc
        self.kind = ASTKind.UTF8StringDTKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"UTF8String({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the object in a simplified."""
        key = "UTF8String"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
class UTF8Char(DataTypeOps):
    """Class for UTF-8 encoded characters."""

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        if len(value) != 1:
            raise ValueError("Expected a single UTF-8 character.")
        value.encode("utf-8")
        super().__init__()
        self.value = value
        self.loc = loc
        self.kind = ASTKind.UTF8CharDTKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"UTF8Char({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the object in a simplified."""
        key = "UTF8Char"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
class LiteralUTF8String(Literal):
    """Literal class for UTF-8 strings."""

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        super().__init__(loc)
        value.encode("utf-8")
        self.value = value
        self.type_ = UTF8String
        self.loc = loc

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"LiteralUTF8String({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the object in a simplified."""
        key = f"LiteralUTF8String: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
class LiteralUTF8Char(Literal):
    """Literal class for UTF-8 characters."""

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        super().__init__(loc)
        value.encode("utf-8")
        self.value = value
        self.type_ = UTF8Char
        self.loc = loc

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"LiteralUTF8Char({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the object in a simplified."""
        key = f"LiteralUTF8Char: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)
