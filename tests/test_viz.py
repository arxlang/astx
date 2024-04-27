"""Tests visualization methods."""

from astx.datatypes import LiteralInt32
from astx.operators import BinaryOp
from astx.variables import Variable


def test_viz_graphviz() -> None:
    """Test graphviz visualization method."""
    var_a = Variable("a")
    var_b = Variable("b")

    bin_1 = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)

    lit_a = LiteralInt32(value=1)
    lit_b = LiteralInt32(value=2)

    bin_2 = BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)

    bin_1._repr_png_()
    bin_2._repr_png_()
