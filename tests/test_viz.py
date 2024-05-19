"""Tests visualization methods."""

from astx.blocks import Block
from astx.datatypes import Int32, LiteralInt32
from astx.operators import BinaryOp
from astx.variables import Variable, VariableDeclaration
from astx.viz import graph_to_ascii, traverse_ast_ascii


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


def test_viz_ascii() -> None:
    """Test ascii representation."""
    block = Block()
    decl_a = VariableDeclaration("a", type_=Int32, value=LiteralInt32(1))
    decl_b = VariableDeclaration("b", type_=Int32, value=LiteralInt32(2))
    var_a = Variable("a")
    var_b = Variable("b")
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)
    block.append(decl_a)
    block.append(decl_b)
    block.append(sum_op)

    graph = traverse_ast_ascii(block.get_struct(simplified=True))
    graph_to_ascii(graph)
