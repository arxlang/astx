"""Tests for complex number data types."""

from __future__ import annotations

from astx.datatypes import Int32, TypeCastExpr
from astx.variables import Variable
from astx.viz import visualize


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

    visualize(cast_expr.get_struct())
