"""Test classes from the base module."""

from __future__ import annotations

import astx

from astx.base import is_using_jupyter_notebook


def test_is_using_jupyter_notebook() -> None:
    """Test is_using_jupyter_notebook function."""
    assert not is_using_jupyter_notebook()


def test_source_location() -> None:
    """Test SourceLocation."""
    line = 1
    col = 2

    loc = astx.SourceLocation(line, col)
    assert loc.line == line
    assert loc.col == col


def test_ast_parent() -> None:
    """Test AST parent usage."""
    block = astx.Block()
    decl_a = astx.VariableDeclaration("a", type_=astx.Int32(), parent=block)
    assert block.nodes[0] == decl_a


def test_ast_to_json() -> None:
    """Test AST object to json."""
    block = astx.Block()
    astx.VariableDeclaration("a", type_=astx.Int32(), parent=block)
    assert block.to_json(simplified=True) != ""
    # assert block.to_json(simplified=False) != ""


def test_ast_to_yaml() -> None:
    """Test AST object to yaml."""
    block = astx.Block()
    astx.VariableDeclaration("a", type_=astx.Int32(), parent=block)
    assert block.to_yaml(simplified=True) != ""
    # assert block.to_json(simplified=False) != ""


def test_ast_nodes() -> None:
    """Test ASTNodes class."""
    block = astx.Block()
    astx.VariableDeclaration("a", type_=astx.Int32(), parent=block)

    for item in block:
        assert item is not None

    assert len(block) == 1
    count = 0

    for idx, item in enumerate(block):
        count += 1

    assert count == 1


def test_data_type() -> None:
    """Test DataType class."""
    dt = astx.DataType()
    assert str(dt) != ""
    assert repr(dt) != ""
    assert dt.get_struct() != {}
    assert dt.get_struct(simplified=True) != {}


COLUMN_NUMBER = 10


def test_identifier_creation() -> None:
    """Test basic identifier creation."""
    ident = astx.Identifier("test_var")
    assert ident.value == "test_var"


def test_identifier_with_location() -> None:
    """Test identifier with location."""
    loc = astx.SourceLocation(1, COLUMN_NUMBER)
    ident_with_loc = astx.Identifier("var2", loc=loc)
    assert ident_with_loc.value == "var2"
    assert ident_with_loc.loc.line == 1
    assert ident_with_loc.loc.col == COLUMN_NUMBER


def test_identifier_as_part_of_block() -> None:
    """Test identifier as part of a block."""
    block = astx.Block()
    ident_with_parent = astx.Identifier("var3", parent=block)
    assert block.nodes[0] == ident_with_parent


def test_struct_representation() -> None:
    """Test struct representation."""
    ident = astx.Identifier("test_var")
    struct = ident.get_struct(simplified=True)
    assert struct == {"IDENTIFIER[test_var]": "test_var"}


def test_parenthesized_expr_1() -> None:
    """Test ParenthesizedExpr 1."""
    node = astx.ParenthesizedExpr(
        astx.AndOp(astx.LiteralBoolean(True), astx.LiteralBoolean(False))
    )
    assert node.get_struct(simplified=True)
    assert node.get_struct(simplified=False)


def test_parenthesized_expr_2() -> None:
    """Test ParenthesizedExpr 2."""
    node_1 = astx.ParenthesizedExpr(
        astx.AndOp(
            astx.LiteralBoolean(True),
            astx.LiteralBoolean(False),
        )
    )

    node_2 = astx.OrOp(node_1, node_1)
    assert node_2.get_struct(simplified=True)
    assert node_2.get_struct(simplified=False)


def test_slice_expr() -> None:
    """Test slice expression."""
    # Simple slice with all components
    slice_full = astx.Slice(
        lower=astx.LiteralInt32(1),
        upper=astx.LiteralInt32(10),
        step=astx.LiteralInt32(2),
    )

    assert str(slice_full) == "1:10:2"
    assert slice_full.get_struct(simplified=True)

    # Slice with missing components
    slice_partial = astx.Slice(upper=astx.LiteralInt32(5))

    assert str(slice_partial) == ":5"
    assert slice_partial.get_struct(simplified=True)

    # Empty slice
    slice_empty = astx.Slice()

    assert str(slice_empty) == ":"
    assert slice_empty.get_struct(simplified=True)
