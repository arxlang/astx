"""Constant objects."""

from __future__ import annotations

from astx.types.base import NoneType
from astx.types.boolean import Boolean
from astx.types.numeric import (
    Complex,
    Complex32,
    Complex64,
    Float16,
    Float32,
    Float64,
    Floating,
    Int8,
    Int16,
    Int32,
    Int64,
    Int128,
    Integer,
    Number,
    SignedInteger,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    UInt128,
    UnsignedInteger,
)
from astx.types.string import (
    String,
    UTF8Char,
    UTF8String,
)
from astx.types.temporal import (
    Date,
    DateTime,
    Temporal,
    Time,
    Timestamp,
)

t_none = NoneType()
t_boolean = Boolean()
t_number = Number()
t_integer = Integer()
t_unsigned_integer = UnsignedInteger()
t_signed_integer = SignedInteger()
t_int8 = Int8()
t_int16 = Int16()
t_int32 = Int32()
t_int64 = Int64()
t_int128 = Int128()
t_uint8 = UInt8()
t_uint16 = UInt16()
t_uint32 = UInt32()
t_uint64 = UInt64()
t_uint128 = UInt128()
t_floating = Floating()
t_float16 = Float16()
t_float32 = Float32()
t_float64 = Float64()
t_complex = Complex()
t_complex32 = Complex32()
t_complex64 = Complex64()
t_string = String()
t_utf8_string = UTF8String()
t_utf8_char = UTF8Char()
t_temporal = Temporal()
t_date = Date()
t_time = Time()
t_timestamp = Timestamp()
t_datetime = DateTime()

__all__ = [
    "t_boolean",
    "t_complex",
    "t_complex32",
    "t_complex64",
    "t_date",
    "t_datetime",
    "t_float16",
    "t_float32",
    "t_float64",
    "t_floating",
    "t_int8",
    "t_int16",
    "t_int32",
    "t_int64",
    "t_int128",
    "t_integer",
    "t_none",
    "t_number",
    "t_signed_integer",
    "t_string",
    "t_temporal",
    "t_time",
    "t_timestamp",
    "t_uint8",
    "t_uint16",
    "t_uint32",
    "t_uint64",
    "t_uint128",
    "t_unsigned_integer",
    "t_utf8_char",
    "t_utf8_string",
]
