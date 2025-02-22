"""Tests for context manager related AST nodes."""

import pytest

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    Expr,
    Identifier,
    ReprStruct,
)
from astx.context_manager import WithItem, WithStmt
from astx.keys import Block  # Assuming this is the correct import


# Mock class for Expr
class MockExpr(Expr):
    """A mock expression class for testing."""

    def __init__(self) -> None:
        super().__init__(loc=NO_SOURCE_LOCATION)
        self.type_ = "int"

    def __str__(self) -> str:
        """Return a string representation of the expression."""
        return "42"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a structural representation of the expression."""
        return {"value": 42}


# Fixtures
@pytest.fixture
def context_expr() -> Expr:
    """Fixture providing a basic Expr instance."""
    return MockExpr()


@pytest.fixture
def var_name() -> Identifier:
    """Fixture providing a basic Identifier instance."""
    return Identifier("x")


@pytest.fixture
def empty_block() -> Block:
    """Fixture providing an empty Block instance."""
    return Block(name="empty_block")


class TestWithItem:
    """Test suite for WithItem class."""

    def test_init_basic(
        self, context_expr: Expr, var_name: Identifier
    ) -> None:
        """Test basic initialization of WithItem."""
        item = WithItem(context_expr, var_name)
        assert item.context_expr == context_expr
        assert item.instance_name == var_name

    def test_str_basic(self, context_expr: Expr, var_name: Identifier) -> None:
        """Test string representation."""
        item = WithItem(context_expr, var_name)
        assert str(item) == f"{context_expr} as {var_name}"

    def test_get_struct_basic(
        self, context_expr: Expr, var_name: Identifier
    ) -> None:
        """Test basic structure representation."""
        item = WithItem(context_expr, var_name)
        struct = item.get_struct()
        assert f"CONTEXT[{context_expr}]" in struct
        assert struct[f"CONTEXT[{context_expr}]"] == f"AS {var_name}"


class TestWithStmt:
    """Test suite for WithStmt class."""

    def test_init_basic(
        self, context_expr: Expr, var_name: Identifier, empty_block: Block
    ) -> None:
        """Test basic initialization of WithStmt."""
        item = WithItem(context_expr, var_name)
        stmt = WithStmt([item], empty_block)
        assert stmt.items == [item]
        assert stmt.body == empty_block
        assert stmt.kind == ASTKind.WithStmtKind

    def test_str_basic(
        self, context_expr: Expr, var_name: Identifier, empty_block: Block
    ) -> None:
        """Test string representation."""
        item = WithItem(context_expr, var_name)
        stmt = WithStmt([item], empty_block)
        assert str(stmt) == f"WithStmt[{context_expr} as {var_name}]"

    def test_get_struct_basic(
        self, context_expr: Expr, var_name: Identifier, empty_block: Block
    ) -> None:
        """Test basic structure representation."""
        item = WithItem(context_expr, var_name)
        stmt = WithStmt([item], empty_block)
        struct = stmt.get_struct()

        assert isinstance(struct, dict)
        assert "WITH-STMT" in struct
        with_stmt_content = struct["WITH-STMT"]
        assert isinstance(with_stmt_content, dict)
        assert "items" in with_stmt_content
        assert "body" in with_stmt_content
