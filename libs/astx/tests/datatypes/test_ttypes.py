"""Test type objects."""

import pytest

from astx.base import DataType
from astx.data import Variable
from astx.types.ttypes import (
    t_boolean,
    t_complex,
    t_complex32,
    t_complex64,
    t_date,
    t_datetime,
    t_float16,
    t_float32,
    t_float64,
    t_floating,
    t_int8,
    t_int16,
    t_int32,
    t_int64,
    t_int128,
    t_integer,
    t_none,
    t_number,
    t_signed_integer,
    t_string,
    t_temporal,
    t_time,
    t_timestamp,
    t_uint8,
    t_uint16,
    t_uint32,
    t_uint64,
    t_uint128,
    t_unsigned_integer,
    t_utf8_char,
    t_utf8_string,
)

ttypes = [
    t_boolean,
    t_complex,
    t_complex32,
    t_complex64,
    t_date,
    t_datetime,
    t_float16,
    t_float32,
    t_float64,
    t_floating,
    t_int8,
    t_int16,
    t_int32,
    t_int64,
    t_int128,
    t_integer,
    t_none,
    t_number,
    t_signed_integer,
    t_string,
    t_temporal,
    t_time,
    t_timestamp,
    t_uint8,
    t_uint16,
    t_uint32,
    t_uint64,
    t_uint128,
    t_unsigned_integer,
    t_utf8_char,
    t_utf8_string,
]


@pytest.mark.parametrize("ttype", ttypes)
def test_ttypes(ttype: DataType) -> None:
    """Test ttypes."""
    Variable("a", type_=ttype)
