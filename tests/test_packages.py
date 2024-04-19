"""Module for testing different kind of ASTx blocks."""

from astx.datatypes import Int32, LiteralInt32
from astx.operators import BinaryOp
from astx.packages import Module
from astx.variables import Variable, VariableDeclaration


def test_module() -> None:
    """Test ASTx module."""
    module = Module()

    decl_a = VariableDeclaration("a", type_=Int32, value=LiteralInt32(1))
    decl_b = VariableDeclaration("b", type_=Int32, value=LiteralInt32(2))

    var_a = Variable("a")
    var_b = Variable("b")
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)

    module.append(decl_a)
    module.append(decl_b)
    module.append(sum_op)


def test_packages() -> None:
    """Test ASTx module."""
    module = Module()

    decl_a = VariableDeclaration("a", type_=Int32, value=LiteralInt32(1))
    decl_b = VariableDeclaration("b", type_=Int32, value=LiteralInt32(2))

    var_a = Variable("a")
    var_b = Variable("b")
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)

    module.append(decl_a)
    module.append(decl_b)
    module.append(sum_op)


def test_program() -> None:
    """Test ASTx module."""
    module = Module()

    decl_a = VariableDeclaration("a", type_=Int32, value=LiteralInt32(1))
    decl_b = VariableDeclaration("b", type_=Int32, value=LiteralInt32(2))

    var_a = Variable("a")
    var_b = Variable("b")
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)

    module.append(decl_a)
    module.append(decl_b)
    module.append(sum_op)


def test_target() -> None:
    """Test ASTx module."""
    module = Module()

    decl_a = VariableDeclaration("a", type_=Int32, value=LiteralInt32(1))
    decl_b = VariableDeclaration("b", type_=Int32, value=LiteralInt32(2))

    var_a = Variable("a")
    var_b = Variable("b")
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)

    module.append(decl_a)
    module.append(decl_b)
    module.append(sum_op)
