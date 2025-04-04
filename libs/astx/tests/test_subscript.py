"""Tests for subscripts."""

from astx.base import ASTKind
from astx.literals import LiteralInt32, LiteralInteger, LiteralString
from astx.subscript import Ellipsis, SubscriptExpr
from astx.variables import Variable
from astx.viz import visualize


def test_subscriptexpr_upper_lower() -> None:
    """Test `SubscriptExpr` class - slice of an array."""
    # Variable
    a_var = Variable(name="a")

    # SubscriptExpr
    subscr_expr = SubscriptExpr(
        value=a_var,
        lower=LiteralInt32(0),
        upper=LiteralInt32(10),
        step=LiteralInt32(2),
    )

    assert str(subscr_expr)
    assert subscr_expr.get_struct()
    assert subscr_expr.get_struct(simplified=True)
    visualize(subscr_expr.get_struct())


def test_subscriptexpr_index() -> None:
    """Test `SubscriptExpr` class - index of an array."""
    # Variable
    a_var = Variable(name="a")

    # SubscriptExpr
    subscr_expr = SubscriptExpr(
        value=a_var,
        index=LiteralInt32(0),
    )

    assert str(subscr_expr)
    assert subscr_expr.get_struct()
    assert subscr_expr.get_struct(simplified=True)
    visualize(subscr_expr.get_struct())

def test_ellipsis_init():
    """Test initialization of Ellipsis."""
    ellipsis = Ellipsis()
    assert ellipsis.kind == ASTKind.EllipsisKind
    assert str(ellipsis) == "..."


def test_ellipsis_str():
    """Test string representation of Ellipsis."""
    ellipsis = Ellipsis()
    assert str(ellipsis) == "..."


def test_ellipsis_get_struct():
    """Test get_struct method of Ellipsis."""
    ellipsis = Ellipsis()
    struct = ellipsis.get_struct()
    assert "Ellipsis" in struct


def test_ellipsis_in_subscript():
    """Test Ellipsis used in a subscript context."""
    arr = LiteralString("arr")
    start = LiteralInteger(1)

    slice_expr = SubscriptExpr(
        value=arr,
        lower=start,
        upper=Ellipsis(),
    )
    
    assert isinstance(slice_expr.upper, Ellipsis)
    assert str(slice_expr.upper) == "..."