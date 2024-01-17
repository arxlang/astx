"""Module for testing different kind of ASTx blocks."""
from astx.blocks import Block, Module
from astx.datatypes import Int32, LiteralInt32
from astx.operators import BinaryOp
from astx.variables import VarDeclaration, Variable


def test_block() -> None:
    """Test ASTx block."""
    block = Block()

    decl_a = VarDeclaration("a", type_=Int32, value=LiteralInt32(1))
    decl_b = VarDeclaration("b", type_=Int32, value=LiteralInt32(2))

    var_a = Variable("a")
    var_b = Variable("b")
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)

    block.append(decl_a)
    block.append(decl_b)

    block.append(sum_op)


def test_module() -> None:
    """Test ASTx module."""
    module = Module()

    decl_a = VarDeclaration("a", type_=Int32, value=LiteralInt32(1))
    decl_b = VarDeclaration("b", type_=Int32, value=LiteralInt32(2))

    var_a = Variable("a")
    var_b = Variable("b")
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)

    module.append(decl_a)
    module.append(decl_b)
    module.append(sum_op)
