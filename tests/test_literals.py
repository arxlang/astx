"""Tests for i32 data type."""

from astx.datatypes import LiteralInt32


def test_literal_int32() -> None:
    """Test variable i32."""
    lit_1_a = LiteralInt32(value=1)
    lit_1_b = LiteralInt32(value=1)
    lit_2_a = LiteralInt32(value=2)

    assert lit_1_a.ref != lit_1_b.ref != lit_2_a.ref
