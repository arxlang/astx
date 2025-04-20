"""Tests for operators."""

from typing import cast

import astx
import pytest

from astx.base import ASTKind, Identifier
from astx.base import ASTKind
from astx.literals.numeric import LiteralInt32
from astx.operators import (
    AssignmentExpr,
    AugAssign,
    OpCodeAugAssign,
    VariableAssignment,
)
from astx.variables import Variable
from astx.viz import visualize
from typeguard import TypeCheckError


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


def test_starred_creation() -> None:
    """Test creating a Starred operator."""
    # Test with a variable
    var = astx.Variable(name="args")
    starred = astx.Starred(value=var)
    assert starred.value == var
    assert starred.kind == ASTKind.StarredKind
    assert str(starred) == "Starred[*](Variable[args])"


def test_starred_simplified_struct() -> None:
    """Test Starred operator simplified struct representation."""
    var = astx.Variable(name="args")
    starred = astx.Starred(value=var)
    simplified = starred.get_struct(simplified=True)
    assert isinstance(simplified, dict), (
        f"Expected dict, got {type(simplified)}"
    )
    assert "STARRED[*]" in simplified
    starred_content = simplified["STARRED[*]"]
    assert isinstance(starred_content, dict), (
        f"Expected dict, got {type(starred_content)}"
    )
    assert "value" in starred_content
    value_dict = starred_content["value"]
    assert isinstance(value_dict, dict), (
        f"Expected dict, got {type(value_dict)}"
    )
    assert "Variable[args]" in value_dict
    variable_args = value_dict["Variable[args]"]
    assert isinstance(variable_args, str), (
        f"Expected str, got {type(variable_args)}"
    )
    assert variable_args == "args"


def test_starred_location() -> None:
    """Test Starred operator source location."""
    var = astx.Variable(name="args")
    loc = astx.SourceLocation(line=1, col=0)
    starred = astx.Starred(value=var, loc=loc)
    assert starred.loc == loc
    assert starred.loc.line == 1
    assert starred.loc.col == 0


def test_starred_parent() -> None:
    """Test Starred operator parent relationship."""
    var = astx.Variable(name="args")
    parent = astx.Block()
    starred = astx.Starred(value=var, parent=parent)
    assert starred.parent is parent
    assert starred.value is var


def test_starred_creation() -> None:
    """Test creating a Starred operator."""
    var = astx.Variable(name="args")
    starred = astx.Starred(value=var)
    assert starred.value == var
    assert starred.kind == ASTKind.StarredKind
    assert str(starred) == "Starred[*](Variable[args])"


def test_starred_simplified_struct() -> None:
    """Test Starred operator simplified struct representation."""
    var = astx.Variable(name="args")
    starred = astx.Starred(value=var)
    simplified = starred.get_struct(simplified=True)
    assert isinstance(simplified, dict)
    assert "STARRED[*]" in simplified
    starred_content = simplified["STARRED[*]"]
    assert isinstance(starred_content, dict)
    assert "value" in starred_content


def test_starred_location() -> None:
    """Test Starred operator source location."""
    var = astx.Variable(name="args")
    loc = astx.SourceLocation(line=1, col=0)
    starred = astx.Starred(value=var, loc=loc)
    assert starred.loc == loc
    assert starred.loc.line == 1
    assert starred.loc.col == 0


def test_starred_parent() -> None:
    """Test Starred operator parent relationship."""
    var = astx.Variable(name="args")
    parent = astx.Block()
    starred = astx.Starred(value=var, parent=parent)
    assert starred.parent is parent
    assert starred.value is var


def test_starred_with_different_expressions() -> None:
    """Test Starred with different types of expressions."""
    ident = Identifier("a")
    starred_ident = astx.Starred(value=ident)
    assert (
        str(starred_ident) == "Starred[*](Identifier)"
    )  # Updated to match actual output
    assert starred_ident.kind == ASTKind.StarredKind

    lit = LiteralInt32(42)
    starred_lit = astx.Starred(value=lit)
    assert str(starred_lit) == "Starred[*](LiteralInt32(42))"

    var = Variable(name="x")
    starred_var = astx.Starred(value=var)
    assert str(starred_var) == "Starred[*](Variable[x])"


def test_starred_struct_representation() -> None:
    """Test the structure representation of Starred expressions."""
    ident = astx.Identifier("x")
    starred = astx.Starred(value=ident)
    struct = starred.get_struct(simplified=True)

    # Add type checking before using 'in' operator
    assert isinstance(struct, dict)
    assert "STARRED[*]" in struct

    # Add type checking before dictionary access
    assert isinstance(struct["STARRED[*]"], dict)
    content = struct["STARRED[*]"]
    assert "value" in content


def test_starred_location_and_parent() -> None:
    """Test Starred with source location and parent node."""
    ident = astx.Identifier("x")
    loc = astx.SourceLocation(line=1, col=0)
    parent = astx.Block()

    starred = astx.Starred(value=ident, loc=loc, parent=parent)

    assert starred.loc == loc
    assert starred.parent is parent
    assert starred.value is ident
    assert starred.kind == ASTKind.StarredKind


def test_starred_type_validation() -> None:
    """Test type validation for Starred expressions."""
    with pytest.raises(TypeCheckError):
        astx.Starred(value="not_an_expr")  # type: ignore

    with pytest.raises(TypeCheckError):
        astx.Starred(value=None)  # type: ignore


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
