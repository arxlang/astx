"""
title: Tests for context manager related AST nodes.
"""

import pytest

from astx import Identifier, LiteralInt32
from astx.base import (
    ASTKind,
    Expr,
)
from astx.blocks import Block
from astx.context_manager import WithItem, WithStmt


# Fixtures
@pytest.fixture
def context_expr() -> Expr:
    """
    title: Fixture providing a basic Expr instance.
    returns:
      type: Expr
    """
    return LiteralInt32(42)


@pytest.fixture
def var_name() -> Identifier:
    """
    title: Fixture providing a basic Identifier instance.
    returns:
      type: Identifier
    """
    return Identifier("x")


@pytest.fixture
def empty_block() -> Block:
    """
    title: Fixture providing an empty Block instance.
    returns:
      type: Block
    """
    return Block(name="empty_block")


class TestWithItem:
    """
    title: Test suite for WithItem class.
    """

    def test_init_basic(
        self, context_expr: Expr, var_name: Identifier
    ) -> None:
        """
        title: Test basic initialization of WithItem.
        parameters:
          context_expr:
            type: Expr
          var_name:
            type: Identifier
        """
        item = WithItem(context_expr, var_name)
        assert item.context_expr == context_expr
        assert item.instance_name is not None
        assert item.instance_name == var_name

    def test_str_basic(self, context_expr: Expr, var_name: Identifier) -> None:
        """
        title: Test string representation.
        parameters:
          context_expr:
            type: Expr
          var_name:
            type: Identifier
        """
        item = WithItem(context_expr, var_name)
        # Type assertion since we know var_name is not None in this test
        assert var_name is not None  # This helps the type checker
        assert str(item) == f"{context_expr} as {var_name}"

    def test_get_struct_basic(
        self, context_expr: Expr, var_name: Identifier
    ) -> None:
        """
        title: Test basic structure representation.
        parameters:
          context_expr:
            type: Expr
          var_name:
            type: Identifier
        """
        item = WithItem(context_expr, var_name)
        struct = item.get_struct()
        expected_key = f"CONTEXT[{context_expr}]"

        # Type checking for nested dictionary structure
        assert isinstance(struct, dict)
        assert "WithItem" in struct
        assert isinstance(struct["WithItem"], dict)

        # Check if the expected key exists in the nested structure
        with_item_content = struct["WithItem"]
        assert any(k == expected_key for k in with_item_content.keys())


class TestWithStmt:
    """
    title: Test suite for WithStmt class.
    """

    def test_init_basic(
        self, context_expr: Expr, var_name: Identifier, empty_block: Block
    ) -> None:
        """
        title: Test basic initialization of WithStmt.
        parameters:
          context_expr:
            type: Expr
          var_name:
            type: Identifier
          empty_block:
            type: Block
        """
        item = WithItem(context_expr, var_name)
        stmt = WithStmt([item], empty_block)
        assert stmt.items == [item]
        assert stmt.body == empty_block
        assert stmt.kind == ASTKind.WithStmtKind

    def test_str_basic(
        self, context_expr: Expr, var_name: Identifier, empty_block: Block
    ) -> None:
        """
        title: Test string representation.
        parameters:
          context_expr:
            type: Expr
          var_name:
            type: Identifier
          empty_block:
            type: Block
        """
        item = WithItem(context_expr, var_name)
        stmt = WithStmt([item], empty_block)
        expected = f"WithStmt[{context_expr} as {var_name}]"
        assert str(stmt) == expected

    def test_get_struct_basic(
        self, context_expr: Expr, var_name: Identifier, empty_block: Block
    ) -> None:
        """
        title: Test basic structure representation.
        parameters:
          context_expr:
            type: Expr
          var_name:
            type: Identifier
          empty_block:
            type: Block
        """
        item = WithItem(context_expr, var_name)
        stmt = WithStmt([item], empty_block)
        struct = stmt.get_struct()

        assert isinstance(struct, dict)
        assert "WITH-STMT" in struct
        with_stmt_content = struct["WITH-STMT"]
        assert isinstance(with_stmt_content, dict)
        assert "items" in with_stmt_content
        assert "body" in with_stmt_content
