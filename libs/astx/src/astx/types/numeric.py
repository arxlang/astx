"""ASTx Data Types module."""

from __future__ import annotations

from public import public

from astx.tools.typing import typechecked
from astx.types.base import AnyType


@public
@typechecked
class Number(AnyType):
    """Number data type expression."""


@public
@typechecked
class Integer(AnyType):
    """Integer number data type expression."""


@public
@typechecked
class UnsignedInteger(Integer):
    """Unsigned integer number data type expression."""


@public
@typechecked
class SignedInteger(Integer):
    """Signed integer number data type expression."""


@public
@typechecked
class Int8(SignedInteger):
    """Int8 data type expression."""

    nbytes: int = 1


@public
@typechecked
class Int16(SignedInteger):
    """Int16 data type expression."""

    nbytes: int = 2


@public
@typechecked
class Int32(SignedInteger):
    """Int32 data type expression."""

    nbytes: int = 4


@public
@typechecked
class Int64(SignedInteger):
    """Int64 data type expression."""

    nbytes: int = 8


@public
@typechecked
class Int128(SignedInteger):
    """Int128 data type expression."""

    nbytes: int = 16


@public
@typechecked
class UInt8(UnsignedInteger):
    """UInt8 data type expression."""

    nbytes: int = 1


@public
@typechecked
class UInt16(UnsignedInteger):
    """UInt16 data type expression."""

    nbytes: int = 2


@public
@typechecked
class UInt32(UnsignedInteger):
    """UInt32 data type expression."""

    nbytes: int = 4


@public
@typechecked
class UInt64(UnsignedInteger):
    """UInt64 data type expression."""

    nbytes: int = 8


@public
@typechecked
class UInt128(UnsignedInteger):
    """UInt128 data type expression."""

    nbytes: int = 16


@public
@typechecked
class Floating(Number):
    """AST for the literal float number."""


@public
@typechecked
class Float16(Floating):
    """Float16 data type expression."""


@public
@typechecked
class Float32(Floating):
    """Float32 data type expression."""


@public
@typechecked
class Float64(Floating):
    """Float64 data type expression."""


@public
@typechecked
class Complex(Number):
    """Base class for complex numbers."""


@public
@typechecked
class Complex32(Complex):
    """Complex32 data type class."""

    nbytes: int = 8


@public
@typechecked
class Complex64(Complex):
    """Complex64 data type class."""

    nbytes: int = 16
