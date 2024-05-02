"""Test callable ASTx objects."""

import astx

from astx.viz import visualize


def test_variable() -> None:
    """Test function creation with modifiers."""
    var_a = astx.Variable("a")

    assert str(var_a)
    assert var_a.get_struct()
    assert var_a.get_struct(simplified=True)

    visualize(var_a.get_struct())


def test_variable_decl() -> None:
    """Test function creation with modifiers."""
    decl_a = astx.VariableDeclaration(
        "a", type_=astx.Int32, value=astx.LiteralInt32(1)
    )

    assert str(decl_a)
    assert decl_a.get_struct()
    assert decl_a.get_struct(simplified=True)

    visualize(decl_a.get_struct())


def test_inline_variable_decl() -> None:
    """Test function creation with modifiers."""
    decl_a = astx.InlineVariableDeclaration(
        "a", type_=astx.Int32, value=astx.LiteralInt32(1)
    )

    assert str(decl_a)
    assert decl_a.get_struct()
    assert decl_a.get_struct(simplified=True)

    visualize(decl_a.get_struct())


def test_variable_assign() -> None:
    """Test function creation with modifiers."""
    assign_a = astx.VariableAssignment("a", value=astx.LiteralInt32(1))

    assert str(assign_a)
    assert assign_a.get_struct()
    assert assign_a.get_struct(simplified=True)

    visualize(assign_a.get_struct())


def test_argument() -> None:
    """Test function creation with modifiers."""
    arg_a = astx.Argument("a", type_=astx.Int32, default=astx.LiteralInt32(1))

    assert str(arg_a)
    assert arg_a.get_struct()
    assert arg_a.get_struct(simplified=True)

    visualize(arg_a.get_struct())


def test_arguments() -> None:
    """Test function creation with modifiers."""
    arg_a = astx.Argument("a", type_=astx.Int32, default=astx.LiteralInt32(1))
    arg_b = astx.Argument("b", type_=astx.Int32, default=astx.LiteralInt32(2))
    arg_c = astx.Argument("c", type_=astx.Int32, default=astx.LiteralInt32(3))

    args = astx.Arguments(arg_a, arg_b)
    args.append(arg_c)

    assert str(args)
    assert args.get_struct()
    assert args.get_struct(simplified=True)

    visualize(args.get_struct())
