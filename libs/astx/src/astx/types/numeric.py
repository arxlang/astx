"""
title: ASTx Data Types module.
"""

from __future__ import annotations

from public import public

from astx.tools.typing import typechecked
from astx.types.base import AnyType


@public
@typechecked
class Number(AnyType):
    """
    title: Number data type expression.
    """


@public
@typechecked
class Integer(AnyType):
    """
    title: Integer number data type expression.
    """


@public
@typechecked
class UnsignedInteger(Integer):
    """
    title: Unsigned integer number data type expression.
    """


@public
@typechecked
class SignedInteger(Integer):
    """
    title: Signed integer number data type expression.
    """


@public
@typechecked
class Int8(SignedInteger):
    """
    title: Int8 data type expression.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 1


@public
@typechecked
class Int16(SignedInteger):
    """
    title: Int16 data type expression.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 2


@public
@typechecked
class Int32(SignedInteger):
    """
    title: Int32 data type expression.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 4


@public
@typechecked
class Int64(SignedInteger):
    """
    title: Int64 data type expression.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 8


@public
@typechecked
class Int128(SignedInteger):
    """
    title: Int128 data type expression.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 16


@public
@typechecked
class UInt8(UnsignedInteger):
    """
    title: UInt8 data type expression.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 1


@public
@typechecked
class UInt16(UnsignedInteger):
    """
    title: UInt16 data type expression.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 2


@public
@typechecked
class UInt32(UnsignedInteger):
    """
    title: UInt32 data type expression.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 4


@public
@typechecked
class UInt64(UnsignedInteger):
    """
    title: UInt64 data type expression.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 8


@public
@typechecked
class UInt128(UnsignedInteger):
    """
    title: UInt128 data type expression.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 16


@public
@typechecked
class Floating(Number):
    """
    title: AST for the literal float number.
    """


@public
@typechecked
class Float16(Floating):
    """
    title: Float16 data type expression.
    """


@public
@typechecked
class Float32(Floating):
    """
    title: Float32 data type expression.
    """


@public
@typechecked
class Float64(Floating):
    """
    title: Float64 data type expression.
    """


@public
@typechecked
class Complex(Number):
    """
    title: Base class for complex numbers.
    """


@public
@typechecked
class Complex32(Complex):
    """
    title: Complex32 data type class.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 8


@public
@typechecked
class Complex64(Complex):
    """
    title: Complex64 data type class.
    attributes:
      nbytes:
        type: int
    """

    nbytes: int = 16
