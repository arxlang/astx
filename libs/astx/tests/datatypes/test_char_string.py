"""Tests for UTF-8 character and string data types."""

from __future__ import annotations

from typing import Callable, Type

import astx
import pytest

from astx.types.operators import BinaryOp, UnaryOp
from astx.variables import Variable
from astx.base import Expr

VAR_A = Variable("a")

UTF8_CHAR_LITERAL_CLASSES = [
    astx.LiteralUTF8Char,
]

UTF8_STRING_LITERAL_CLASSES = [
    astx.LiteralUTF8String,
]

FORMATTED_STRING_LITERAL_CLASSES = [
    astx.LiteralFormattedString,
]

def test_variable() -> None:
    """Test variable UTF-8 character and string."""
    var_a = Variable("a")
    var_b = Variable("b")

    BinaryOp(op_code="+", lhs=var_a, rhs=var_b)


@pytest.mark.parametrize("literal_class", UTF8_CHAR_LITERAL_CLASSES)
def test_utf8_char_literal(literal_class: Type[astx.Literal]) -> None:
    """Test UTF-8 character literals."""
    lit_a = literal_class("A")
    lit_b = literal_class("B")
    BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)


@pytest.mark.parametrize("literal_class", UTF8_STRING_LITERAL_CLASSES)
def test_utf8_string_literal(literal_class: Type[astx.Literal]) -> None:
    """Test UTF-8 string literals."""
    lit_a = literal_class("Hello")
    lit_b = literal_class("World")
    BinaryOp(op_code="+", lhs=lit_a, rhs=lit_b)


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda literal_class: VAR_A + literal_class("A"), "+"),
        (lambda literal_class: VAR_A == literal_class("A"), "=="),
        (lambda literal_class: VAR_A != literal_class("A"), "!="),
    ],
)
@pytest.mark.parametrize("literal_class", UTF8_CHAR_LITERAL_CLASSES)
def test_bin_ops_char(
    literal_class: Type[astx.Literal],
    fn_bin_op: Callable[[Type[astx.Literal]], BinaryOp],
    op_code: str,
) -> None:
    """Test binary operations on UTF-8 characters."""
    bin_op = fn_bin_op(literal_class)
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda literal_class: VAR_A + literal_class("Hello"), "+"),
        (lambda literal_class: VAR_A == literal_class("Hello"), "=="),
        (lambda literal_class: VAR_A != literal_class("Hello"), "!="),
    ],
)
@pytest.mark.parametrize("literal_class", UTF8_STRING_LITERAL_CLASSES)
def test_bin_ops_string(
    literal_class: Type[astx.Literal],
    fn_bin_op: Callable[[Type[astx.Literal]], BinaryOp],
    op_code: str,
) -> None:
    """Test binary operations on UTF-8 strings."""
    bin_op = fn_bin_op(literal_class)
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda literal_class: +literal_class("A"), "+"),
    ],
)
@pytest.mark.parametrize("literal_class", UTF8_CHAR_LITERAL_CLASSES)
def test_unary_ops_char(
    literal_class: Type[astx.Literal],
    fn_unary_op: Callable[[Type[astx.Literal]], UnaryOp],
    op_code: str,
) -> None:
    """Test unary operations on UTF-8 characters."""
    unary_op = fn_unary_op(literal_class)
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda literal_class: +literal_class("Hello"), "+"),
    ],
)
@pytest.mark.parametrize("literal_class", UTF8_STRING_LITERAL_CLASSES)
def test_unary_ops_string(
    literal_class: Type[astx.Literal],
    fn_unary_op: Callable[[Type[astx.Literal]], UnaryOp],
    op_code: str,
) -> None:
    """Test unary operations on UTF-8 strings."""
    unary_op = fn_unary_op(literal_class)
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}

def test_formatted_string_literal() -> None:
    """Test formatted string literals."""
    # Simple case with just an expression
    expr = Variable("x")
    formatted = astx.LiteralFormattedString(value=expr)
    assert formatted.value == expr
    assert formatted.format_spec is None
    assert formatted.conversion is None
    
    # With format spec
    formatted_with_spec = astx.LiteralFormattedString(value=expr, format_spec=".2f")
    assert formatted_with_spec.format_spec == ".2f"
    
    # With conversion
    formatted_with_conversion = astx.LiteralFormattedString(value=expr, conversion="s")
    assert formatted_with_conversion.conversion == "s"
    
    # With both format spec and conversion
    formatted_complete = astx.LiteralFormattedString(
        value=expr, format_spec=".2f", conversion="s"
    )
    assert formatted_complete.format_spec == ".2f"
    assert formatted_complete.conversion == "s"


def test_formatted_string_str_repr() -> None:
    """Test string representation of formatted string literals."""
    expr = Variable("x")
    
    # Simple case
    formatted = astx.LiteralFormattedString(value=expr)
    assert str(formatted) == f"LiteralFormattedString({expr})"
    
    # With format spec
    formatted_with_spec = astx.LiteralFormattedString(value=expr, format_spec=".2f")
    assert str(formatted_with_spec) == f"LiteralFormattedString({expr}:.2f)"
    
    # With conversion
    formatted_with_conversion = astx.LiteralFormattedString(value=expr, conversion="s")
    assert str(formatted_with_conversion) == f"LiteralFormattedString({expr}!s)"
    
    # With both
    formatted_complete = astx.LiteralFormattedString(
        value=expr, format_spec=".2f", conversion="s"
    )
    assert str(formatted_complete) == f"LiteralFormattedString({expr}!s:.2f)"


def test_formatted_string_structure() -> None:
    """Test the AST structure of formatted string literals."""
    expr = Variable("x")
    formatted = astx.LiteralFormattedString(
        value=expr, format_spec=".2f", conversion="s"
    )
    
    # Test regular structure
    struct = formatted.get_struct()
    assert "LiteralFormattedString" in struct
    content = struct["LiteralFormattedString"]["content"]
    assert "value" in content
    assert "format_spec" in content
    assert "conversion" in content
    assert content["format_spec"] == ".2f"
    assert content["conversion"] == "s"
    
    # Test simplified structure
    simple_struct = formatted.get_struct(simplified=True)
    assert "LiteralFormattedString" in simple_struct
    simple_content = simple_struct["LiteralFormattedString"]
    assert "value" in simple_content
    assert "format_spec" in simple_content
    assert "conversion" in simple_content


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda literal_class, expr: VAR_A + literal_class(expr), "+"),
        (lambda literal_class, expr: VAR_A == literal_class(expr), "=="),
        (lambda literal_class, expr: VAR_A != literal_class(expr), "!="),
    ],
)
def test_bin_ops_formatted_string(
    fn_bin_op: Callable[[Type[astx.Literal], Expr], BinaryOp],
    op_code: str,
) -> None:
    """Test binary operations on formatted strings."""
    expr = Variable("x")
    bin_op = fn_bin_op(astx.LiteralFormattedString, expr)
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}