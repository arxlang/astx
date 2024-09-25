import pytest
from astx.datatypes import LiteralBoolean
from astx.datatypes import And, Or, Xor, Not

def test_literal_boolean() -> None:
    """Test LiteralBoolean creation."""
    true_lit = LiteralBoolean(True)
    false_lit = LiteralBoolean(False)
    
    assert str(true_lit) == "LiteralBoolean(True)"
    assert str(false_lit) == "LiteralBoolean(False)"

def test_boolean_operators() -> None:
    """Test boolean operators."""
    true_lit = LiteralBoolean(True)
    false_lit = LiteralBoolean(False)

    # Test And
    and_op = And(true_lit, false_lit)
    assert str(and_op) == "LiteralBoolean(True) and LiteralBoolean(False)"

    # Test Or
    or_op = Or(true_lit, false_lit)
    assert str(or_op) == "LiteralBoolean(True) or LiteralBoolean(False)"

    # Test Xor
    xor_op = Xor(true_lit, false_lit)
    assert str(xor_op) == "LiteralBoolean(True) xor LiteralBoolean(False)"

    # Test Not
    not_op = Not(true_lit)
    assert str(not_op) == "not LiteralBoolean(True)"
