"""Tests for classes in types.py."""

from __future__ import annotations

from astx.types.casting import TypeCastExpr
from astx.types.numeric import Int32
from astx.variables import Variable
from astx.viz import visualize_image


def test_typecastexpr() -> None:
    """Test TypeCastExpr."""
    # Expression to cast
    expr = Variable(name="x")

    # Target type for casting
    target_type = Int32()

    # Create the TypeCastExpr
    cast_expr = TypeCastExpr(expr=expr, target_type=target_type)

    assert str(cast_expr)
    assert cast_expr.get_struct()
    assert cast_expr.get_struct(simplified=True)

    visualize_image(cast_expr.get_struct())
