"""Tests visualization methods."""

from astx.blocks import Block
from astx.data import Variable, VariableDeclaration
from astx.literals.numeric import LiteralInt32
from astx.types.numeric import Int32
from astx.types.operators import BinaryOp
from astx.viz import visualize_ascii


def test_viz_image() -> None:
    """Test image visualization method."""
    var_a = Variable("a")
    var_b = Variable("b")

    bin_1 = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)

    lit_a = LiteralInt32(value=1)
    lit_b = LiteralInt32(value=2)

    bin_2 = BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)

    bin_1._repr_png_()
    bin_2._repr_png_()


def test_viz_ascii() -> None:
    """Test ascii representation."""
    block = Block()
    decl_a = VariableDeclaration("a", type_=Int32(), value=LiteralInt32(1))
    decl_b = VariableDeclaration("b", type_=Int32(), value=LiteralInt32(2))
    var_a = Variable("a")
    var_b = Variable("b")
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)
    block.append(decl_a)
    block.append(decl_b)
    block.append(sum_op)

    visualize_ascii(block.get_struct())
