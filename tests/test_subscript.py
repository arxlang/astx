"""Tests for subscripts."""

from astx.literals import LiteralInt32
from astx.subscript import SubscriptExpr
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
