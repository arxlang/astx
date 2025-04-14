"""Tests for UTF-8 character and string data types."""

from __future__ import annotations

from typing import Any, Callable, Dict, Type, cast

import astx
import pytest

from astx.types.operators import BinaryOp, UnaryOp
from astx.variables import Variable

VAR_A = Variable("a")

UTF8_CHAR_LITERAL_CLASSES = [
    astx.LiteralUTF8Char,
]

UTF8_STRING_LITERAL_CLASSES = [
    astx.LiteralUTF8String,
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


# --- Tests for LiteralFormattedString ---


def test_literal_formatted_string_simple() -> None:
    """Test simple LiteralFormattedString instantiation."""
    var_x = astx.Variable("x")
    fmt_val = astx.LiteralFormattedString(value=var_x)

    assert isinstance(fmt_val, astx.LiteralFormattedString)
    assert fmt_val.value == var_x
    assert fmt_val.conversion is None
    assert fmt_val.format_spec is None
    assert str(fmt_val) == "LiteralFormattedString(x)"

    struct = fmt_val.get_struct()
    assert isinstance(struct, dict)
    assert "LiteralFormattedString" in struct
    outer_val = cast(Dict[str, Any], struct["LiteralFormattedString"])
    struct_content = outer_val.get("content")
    assert isinstance(struct_content, dict)
    assert "value" in struct_content
    assert "conversion" not in struct_content
    assert "format_spec" not in struct_content

    struct_simple = fmt_val.get_struct(simplified=True)
    assert isinstance(struct_simple, dict)
    assert "LiteralFormattedString" in struct_simple
    struct_simple_val = cast(
        Dict[str, Any], struct_simple["LiteralFormattedString"]
    )
    assert "value" in struct_simple_val
    assert "conversion" not in struct_simple_val
    assert "format_spec" not in struct_simple_val


def test_literal_formatted_string_with_conversion() -> None:
    """Test LiteralFormattedString with conversion."""
    var_y = astx.Variable("y")
    fmt_val = astx.LiteralFormattedString(value=var_y, conversion=ord("r"))

    assert fmt_val.conversion == ord("r")
    assert str(fmt_val) == "LiteralFormattedString(y!r)"

    struct = fmt_val.get_struct()
    assert isinstance(struct, dict)
    outer_val = cast(Dict[str, Any], struct["LiteralFormattedString"])
    struct_content = outer_val.get("content")
    assert isinstance(struct_content, dict)
    assert struct_content.get("conversion") == "r"

    struct_simple = fmt_val.get_struct(simplified=True)
    assert isinstance(struct_simple, dict)
    struct_simple_val = cast(
        Dict[str, Any], struct_simple["LiteralFormattedString"]
    )
    assert struct_simple_val.get("conversion") == "r"


def test_literal_formatted_string_with_format_spec() -> None:
    """Test LiteralFormattedString with format specifier."""
    var_z = astx.Variable("z")
    format_spec_node = astx.LiteralString(".2f")
    fmt_val = astx.LiteralFormattedString(
        value=var_z, format_spec=format_spec_node
    )

    assert fmt_val.format_spec is format_spec_node
    assert str(fmt_val) == "LiteralFormattedString(z:.2f)"

    struct = fmt_val.get_struct()
    assert isinstance(struct, dict)
    outer_val = cast(Dict[str, Any], struct["LiteralFormattedString"])
    struct_content = outer_val.get("content")
    assert isinstance(struct_content, dict)
    format_spec_struct = struct_content.get("format_spec")
    assert isinstance(format_spec_struct, dict)
    assert "LiteralString: .2f" in format_spec_struct

    struct_simple = fmt_val.get_struct(simplified=True)
    assert isinstance(struct_simple, dict)
    struct_simple_val = cast(
        Dict[str, Any], struct_simple["LiteralFormattedString"]
    )
    format_spec_struct_simple = struct_simple_val.get("format_spec")
    assert isinstance(format_spec_struct_simple, dict)
    assert "LiteralString: .2f" in format_spec_struct_simple


def test_literal_formatted_string_with_conversion_and_format_spec() -> None:
    """Test LiteralFormattedString with conversion and format specifier."""
    var_a = astx.Variable("a")
    format_spec_node = astx.LiteralString(" >10")
    fmt_val = astx.LiteralFormattedString(
        value=var_a, conversion=ord("s"), format_spec=format_spec_node
    )

    assert fmt_val.conversion == ord("s")
    assert fmt_val.format_spec is format_spec_node
    assert str(fmt_val) == "LiteralFormattedString(a!s: >10)"

    struct = fmt_val.get_struct()
    assert isinstance(struct, dict)
    outer_val = cast(Dict[str, Any], struct["LiteralFormattedString"])
    struct_content = outer_val.get("content")
    assert isinstance(struct_content, dict)
    assert struct_content.get("conversion") == "s"
    format_spec_struct = struct_content.get("format_spec")
    assert isinstance(format_spec_struct, dict)
    assert "LiteralString:  >10" in format_spec_struct

    struct_simple = fmt_val.get_struct(simplified=True)
    assert isinstance(struct_simple, dict)
    struct_simple_val = cast(
        Dict[str, Any], struct_simple["LiteralFormattedString"]
    )
    assert struct_simple_val.get("conversion") == "s"
    format_spec_struct_simple = struct_simple_val.get("format_spec")
    assert isinstance(format_spec_struct_simple, dict)
    assert "LiteralString:  >10" in format_spec_struct_simple
