"""Tests for operators."""

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
