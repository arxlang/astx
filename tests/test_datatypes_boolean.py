"""Tests for Boolean data type."""

from astx.datatypes import Boolean, LiteralBoolean
from astx.variables import VariableDeclaration


def test_variable_boolean() -> None:
    """Test variable boolean."""
    decl_a = VariableDeclaration(
        name="a", type_=Boolean, value=LiteralBoolean(value=True)
    )
    assert decl_a.type_ == Boolean.__mro__[0]  # astx.datatypes.Boolean
    assert decl_a.get_struct()


def test_literal_boolean() -> None:
    """Test literal boolean."""
    lit_a = LiteralBoolean(value=True)
    assert type(lit_a) == LiteralBoolean
    assert lit_a.get_struct()
