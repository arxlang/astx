"""Tests for operators."""

from typing import cast

import astx
import pytest

from astx.literals.numeric import LiteralInt32
from astx.operators import (
    AssignmentExpr,
    AugAssign,
    OpCodeAugAssign,
    VariableAssignment,
)
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

    assert str(op)
    assert op.get_struct()
    assert op.get_struct(simplified=True)
    assert op.get_struct() == (lhs & rhs).get_struct()
    visualize(op.get_struct())


def test_or_op() -> None:
    """Test OrOp."""
    lhs = astx.LiteralBoolean(True)
    rhs = astx.LiteralBoolean(False)
    op = astx.OrOp(lhs=lhs, rhs=rhs)

    assert str(op)
    assert op.get_struct()
    assert op.get_struct(simplified=True)
    assert op.get_struct() == (lhs | rhs).get_struct()
    visualize(op.get_struct())


def test_xor_op() -> None:
    """Test XorOp."""
    lhs = astx.LiteralBoolean(True)
    rhs = astx.LiteralBoolean(False)
    op = astx.XorOp(lhs=lhs, rhs=rhs)

    assert str(op)
    assert op.get_struct()
    assert op.get_struct(simplified=True)
    assert op.get_struct() == (lhs ^ rhs).get_struct()
    visualize(op.get_struct())


def test_nand_op() -> None:
    """Test NandOp."""
    lhs = astx.LiteralBoolean(True)
    rhs = astx.LiteralBoolean(False)
    op = astx.NandOp(lhs=lhs, rhs=rhs)

    assert str(op)
    assert op.get_struct()
    assert op.get_struct(simplified=True)
    visualize(op.get_struct())


def test_nor_op() -> None:
    """Test NorOp."""
    lhs = astx.LiteralBoolean(True)
    rhs = astx.LiteralBoolean(False)
    op = astx.NorOp(lhs=lhs, rhs=rhs)

    assert str(op)
    assert op.get_struct()
    assert op.get_struct(simplified=True)
    visualize(op.get_struct())


def test_xnor_op() -> None:
    """Test XnorOp."""
    lhs = astx.LiteralBoolean(True)
    rhs = astx.LiteralBoolean(False)
    op = astx.XnorOp(lhs=lhs, rhs=rhs)

    assert str(op)
    assert op.get_struct()
    assert op.get_struct(simplified=True)
    visualize(op.get_struct())


def test_not_op() -> None:
    """Test NotOp."""
    operand = astx.LiteralBoolean(True)
    op = astx.NotOp(operand=operand)

    assert str(op)
    assert op.get_struct()
    assert op.get_struct(simplified=True)
    visualize(op.get_struct())


@pytest.mark.parametrize(
    "operator, value",
    [
        (cast(OpCodeAugAssign, "+="), 10),
        (cast(OpCodeAugAssign, "-="), 5),
        (cast(OpCodeAugAssign, "*="), 3),
        (cast(OpCodeAugAssign, "/="), 2),
        (cast(OpCodeAugAssign, "//="), 2),
        (cast(OpCodeAugAssign, "%="), 4),
        (cast(OpCodeAugAssign, "**="), 2),
        (cast(OpCodeAugAssign, "&="), 6),
        (cast(OpCodeAugAssign, "|="), 3),
        (cast(OpCodeAugAssign, "^="), 1),
        (cast(OpCodeAugAssign, "<<="), 1),
        (cast(OpCodeAugAssign, ">>="), 2),
    ],
)
def test_aug_assign_operations(operator: OpCodeAugAssign, value: int) -> None:
    """Test all augmented assignment operators using parametrize."""
    var_x = astx.Identifier(value="x")
    literal_value = LiteralInt32(value)
    aug_assign = AugAssign(var_x, operator, literal_value)

    assert str(aug_assign) == f"AugAssign[{operator}]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)
