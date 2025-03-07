"""Tests for operators."""

from typing import get_args

import astx
import pytest

from astx.literals.numeric import LiteralInt32
from astx.operators import AssignmentExpr, AugAssign, VariableAssignment
from astx.variables import Variable
from astx.viz import visualize
from astx import Identifier


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


def test_valid_aug_assign():
    """Test valid augmented assignment operations."""
    # var_x = "x"
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(5)
    op_code_type = AugAssign.__annotations__["op_code"]
    operators = get_args(op_code_type)
    for op in operators:
        aug_assign = AugAssign(var_x, op, value)
        assert str(aug_assign) == f"AugAssign[{op}]"
        assert aug_assign.get_struct()
        assert aug_assign.get_struct(simplified=True)
        visualize(aug_assign.get_struct())


@pytest.mark.xfail(reason="Testing invalid augmented assignment")
def test_invalid_aug_assign() -> None:
    """Test invalid augmented assignment operator."""
    with pytest.raises(ValueError, match="Unsupported operator: <<<"):
        var_x = Identifier(name="x")
        AugAssign(var_x, "<<<", LiteralInt32(5))


def test_aug_assign_addition():
    """Test += operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(10)
    aug_assign = AugAssign(var_x, "+=", value)

    assert str(aug_assign) == "AugAssign[+=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)


def test_aug_assign_subtraction():
    """Test -= operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(5)
    aug_assign = AugAssign(var_x, "-=", value)

    assert str(aug_assign) == "AugAssign[-=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)


def test_aug_assign_multiplication():
    """Test *= operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(3)
    aug_assign = AugAssign(var_x, "*=", value)

    assert str(aug_assign) == "AugAssign[*=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)


def test_aug_assign_division():
    """Test /= operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(2)
    aug_assign = AugAssign(var_x, "/=", value)

    assert str(aug_assign) == "AugAssign[/=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)


def test_aug_assign_floor_division():
    """Test //= operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(2)
    aug_assign = AugAssign(var_x, "//=", value)

    assert str(aug_assign) == "AugAssign[//=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)


def test_aug_assign_modulo():
    """Test %= operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(4)
    aug_assign = AugAssign(var_x, "%=", value)

    assert str(aug_assign) == "AugAssign[%=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)


def test_aug_assign_power():
    """Test **= operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(2)
    aug_assign = AugAssign(var_x, "**=", value)

    assert str(aug_assign) == "AugAssign[**=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)


def test_aug_assign_bitwise_and():
    """Test &= operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(6)
    aug_assign = AugAssign(var_x, "&=", value)

    assert str(aug_assign) == "AugAssign[&=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)


def test_aug_assign_bitwise_or():
    """Test |= operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(3)
    aug_assign = AugAssign(var_x, "|=", value)

    assert str(aug_assign) == "AugAssign[|=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)


def test_aug_assign_bitwise_xor():
    """Test ^= operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(1)
    aug_assign = AugAssign(var_x, "^=", value)

    assert str(aug_assign) == "AugAssign[^=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)


def test_aug_assign_left_shift():
    """Test <<= operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(1)
    aug_assign = AugAssign(var_x, "<<=", value)

    assert str(aug_assign) == "AugAssign[<<=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)


def test_aug_assign_right_shift():
    """Test >>= operator."""
    var_x = astx.Identifier(value="x")
    value = LiteralInt32(2)
    aug_assign = AugAssign(var_x, ">>=", value)

    assert str(aug_assign) == "AugAssign[>>=]"
    assert aug_assign.get_struct()
    assert aug_assign.get_struct(simplified=True)
