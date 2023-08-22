"""Module for testing different kind of ASTx blocks."""
from astx.blocks import Block, Module
from astx.datatypes import Int32, Int32Literal
from astx.operators import BinaryOp
from astx.variables import Variable


def test_block() -> None:
    """Test ASTx block."""
    block = Block()
    var_a = Variable("a", Int32, Int32Literal(1))
    var_b = Variable("b", Int32, Int32Literal(2))
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)
    block.append(sum_op)


def test_module() -> None:
    """Test ASTx module."""
    module = Module()
    var_a = Variable("a", Int32, Int32Literal(1))
    var_b = Variable("b", Int32, Int32Literal(2))
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)
    module.append(sum_op)
