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
    decl_a = astx.VariableDeclaration("a", type_=astx.Int32, parent=block)
    assert block.nodes[0] == decl_a


def test_ast_to_json() -> None:
    """Test AST object to json."""
    block = astx.Block()
    astx.VariableDeclaration("a", type_=astx.Int32, parent=block)
    assert block.to_json(simplified=True) != ""
    # assert block.to_json(simplified=False) != ""


def test_ast_to_yaml() -> None:
    """Test AST object to yaml."""
    block = astx.Block()
    astx.VariableDeclaration("a", type_=astx.Int32, parent=block)
    assert block.to_yaml(simplified=True) != ""
    # assert block.to_json(simplified=False) != ""


def test_ast_nodes() -> None:
    """Test ASTNodes class."""
    block = astx.Block()
    astx.VariableDeclaration("a", type_=astx.Int32, parent=block)

    for item in block:
        assert item is not None

    assert len(block) == 1
    count = 0

    for idx, item in enumerate(block):
        assert block[idx] == item
        count += 1

    assert count == 1


def test_data_type() -> None:
    """Test DataType class."""
    dt = astx.DataType()
    assert str(dt) != ""
    assert repr(dt) != ""
    assert dt.get_struct() != {}
    assert dt.get_struct(simplified=True) != {}
