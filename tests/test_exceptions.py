"""Tests for exceptions classes."""

from astx.exceptions import ThrowStmt
from astx.viz import visualize


def test_throw_stmt() -> None:
    """Test `ThrowStmt` class."""
    # Create a class declaration
    throw_stmt = ThrowStmt()

    assert str(throw_stmt)
    assert throw_stmt.get_struct()
    assert throw_stmt.get_struct(simplified=True)
    visualize(throw_stmt.get_struct())
