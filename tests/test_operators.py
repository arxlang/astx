"""Tests for operators."""

import astx

from astx.literals.numeric import LiteralInt32
from astx.operators import AssignmentExpr, VariableAssignment
from astx.variables import Variable
from astx.viz import visualize


def test_assignment_expr() -> None:
    """Test `AssignmentExpr` class."""
    var_a = Variable(name="a")
    var_b = Variable(name="b")

    assign_expr = AssignmentExpr(targets=[var_a, var_b], value=LiteralInt32(1))

    assert str(assign_expr)
    assert assign_expr.get_struct()
    assert assign_expr.get_struct(simplified=True)
    visualize(assign_expr.get_struct())


def test_variable_assign() -> None:
    """Test function creation with modifiers."""
    assign_a = VariableAssignment("a", value=LiteralInt32(1))

    assert str(assign_a)
    assert assign_a.get_struct()
    assert assign_a.get_struct(simplified=True)

    visualize(assign_a.get_struct())


def test_and_op() -> None:
    """Test AndOp."""
    lhs = astx.LiteralBoolean(True)
    rhs = astx.LiteralBoolean(False)
    op = astx.AndOp(lhs=lhs, rhs=rhs)

    assert str(op) == "(True AND False)"
    assert op.get_struct() == {
        "BooleanBinaryOp[AND]": {
            "lhs": lhs.get_struct(),
            "rhs": rhs.get_struct(),
        }
    }


def test_or_op() -> None:
    """Test OrOp."""
    lhs = astx.LiteralBoolean(True)
    rhs = astx.LiteralBoolean(False)
    op = astx.OrOp(lhs=lhs, rhs=rhs)

    assert str(op) == "(True OR False)"
    assert op.get_struct() == {
        "BooleanBinaryOp[OR]": {
            "lhs": lhs.get_struct(),
            "rhs": rhs.get_struct(),
        }
    }


def test_xor_op() -> None:
    """Test XorOp."""
    lhs = astx.LiteralBoolean(True)
    rhs = astx.LiteralBoolean(False)
    op = astx.XorOp(lhs=lhs, rhs=rhs)

    assert str(op) == "(True XOR False)"
    assert op.get_struct() == {
        "BooleanBinaryOp[XOR]": {
            "lhs": lhs.get_struct(),
            "rhs": rhs.get_struct(),
        }
    }


def test_nand_op() -> None:
    """Test NandOp."""
    lhs = astx.LiteralBoolean(True)
    rhs = astx.LiteralBoolean(False)
    op = astx.NandOp(lhs=lhs, rhs=rhs)

    assert str(op) == "(True NAND False)"
    assert op.get_struct() == {
        "BooleanBinaryOp[NAND]": {
            "lhs": lhs.get_struct(),
            "rhs": rhs.get_struct(),
        }
    }


def test_nor_op() -> None:
    """Test NorOp."""
    lhs = astx.LiteralBoolean(True)
    rhs = astx.LiteralBoolean(False)
    op = astx.NorOp(lhs=lhs, rhs=rhs)

    assert str(op) == "(True NOR False)"
    assert op.get_struct() == {
        "BooleanBinaryOp[NOR]": {
            "lhs": lhs.get_struct(),
            "rhs": rhs.get_struct(),
        }
    }


def test_xnor_op() -> None:
    """Test XnorOp."""
    lhs = astx.LiteralBoolean(True)
    rhs = astx.LiteralBoolean(False)
    op = astx.XnorOp(lhs=lhs, rhs=rhs)

    assert str(op) == "(True XNOR False)"
    assert op.get_struct() == {
        "BooleanBinaryOp[XNOR]": {
            "lhs": lhs.get_struct(),
            "rhs": rhs.get_struct(),
        }
    }
