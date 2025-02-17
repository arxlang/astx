"""Tests for exceptions classes."""

from astx.base import Identifier
from astx.exceptions import ThrowStmt
from astx.viz import visualize


def test_throw_stmt() -> None:
    """Test `ThrowStmt` class."""
    # specify the exception to be thrown
    exc = Identifier("exception_message")

    # create the throw statement
    throw_stmt = ThrowStmt(exception=exc)

    assert str(throw_stmt)
    assert throw_stmt.get_struct()
    assert throw_stmt.get_struct(simplified=True)
    visualize(throw_stmt.get_struct())
