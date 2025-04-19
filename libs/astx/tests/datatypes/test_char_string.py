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

NUM_VALUES_SIMPLE = 2
NUM_VALUES_MIXED = 3


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


def test_formatted_value_simple() -> None:
    """Test simple FormattedValue instantiation."""
    var_x = astx.Variable("x")
    fmt_val = astx.FormattedValue(value=var_x)

    assert isinstance(fmt_val, astx.FormattedValue)
    assert fmt_val.value == var_x
    assert fmt_val.conversion is None
    assert fmt_val.format_spec is None
    assert str(fmt_val) == "FormattedValue(x)"

    struct = fmt_val.get_struct()
    assert isinstance(struct, dict)
    assert "FormattedValue" in struct
    outer_val = cast(Dict[str, Any], struct["FormattedValue"])
    struct_content = outer_val.get("content")
    assert isinstance(struct_content, dict)
    assert "value" in struct_content
    assert "conversion" not in struct_content
    assert "format_spec" not in struct_content

    struct_simple = fmt_val.get_struct(simplified=True)
    assert isinstance(struct_simple, dict)
    assert "FormattedValue" in struct_simple
    struct_simple_val = cast(Dict[str, Any], struct_simple["FormattedValue"])
    assert "value" in struct_simple_val
    assert "conversion" not in struct_simple_val
    assert "format_spec" not in struct_simple_val


def test_formatted_value_with_conversion() -> None:
    """Test FormattedValue with conversion."""
    var_y = astx.Variable("y")
    fmt_val = astx.FormattedValue(value=var_y, conversion=ord("r"))

    assert fmt_val.conversion == ord("r")
    assert str(fmt_val) == "FormattedValue(y!r)"

    struct = fmt_val.get_struct()
    assert isinstance(struct, dict)
    outer_val = cast(Dict[str, Any], struct["FormattedValue"])
    struct_content = outer_val.get("content")
    assert isinstance(struct_content, dict)
    assert struct_content.get("conversion") == "r"

    struct_simple = fmt_val.get_struct(simplified=True)
    assert isinstance(struct_simple, dict)
    struct_simple_val = cast(Dict[str, Any], struct_simple["FormattedValue"])
    assert struct_simple_val.get("conversion") == "r"


def test_formatted_value_with_format_spec() -> None:
    """Test FormattedValue with format specifier."""
    var_z = astx.Variable("z")
    format_spec_node = astx.LiteralString(".2f")
    fmt_val = astx.FormattedValue(value=var_z, format_spec=format_spec_node)

    assert fmt_val.format_spec is format_spec_node
    assert str(fmt_val) == "FormattedValue(z:.2f)"

    struct = fmt_val.get_struct()
    assert isinstance(struct, dict)
    outer_val = cast(Dict[str, Any], struct["FormattedValue"])
    struct_content = outer_val.get("content")
    assert isinstance(struct_content, dict)
    format_spec_struct = struct_content.get("format_spec")
    assert isinstance(format_spec_struct, dict)
    assert "LiteralString: .2f" in format_spec_struct

    struct_simple = fmt_val.get_struct(simplified=True)
    assert isinstance(struct_simple, dict)
    struct_simple_val = cast(Dict[str, Any], struct_simple["FormattedValue"])
    format_spec_struct_simple = struct_simple_val.get("format_spec")
    assert isinstance(format_spec_struct_simple, dict)
    assert "LiteralString: .2f" in format_spec_struct_simple


def test_formatted_value_with_conversion_and_format_spec() -> None:
    """Test FormattedValue with conversion and format specifier."""
    var_a = astx.Variable("a")
    format_spec_node = astx.LiteralString(" >10")
    fmt_val = astx.FormattedValue(
        value=var_a, conversion=ord("s"), format_spec=format_spec_node
    )

    assert fmt_val.conversion == ord("s")
    assert fmt_val.format_spec is format_spec_node
    assert str(fmt_val) == "FormattedValue(a!s: >10)"

    struct = fmt_val.get_struct()
    assert isinstance(struct, dict)
    outer_val = cast(Dict[str, Any], struct["FormattedValue"])
    struct_content = outer_val.get("content")
    assert isinstance(struct_content, dict)
    assert struct_content.get("conversion") == "s"
    format_spec_struct = struct_content.get("format_spec")
    assert isinstance(format_spec_struct, dict)
    assert "LiteralString:  >10" in format_spec_struct

    struct_simple = fmt_val.get_struct(simplified=True)
    assert isinstance(struct_simple, dict)
    struct_simple_val = cast(Dict[str, Any], struct_simple["FormattedValue"])
    assert struct_simple_val.get("conversion") == "s"
    format_spec_struct_simple = struct_simple_val.get("format_spec")
    assert isinstance(format_spec_struct_simple, dict)
    assert "LiteralString:  >10" in format_spec_struct_simple


def test_joined_str_creation_simple() -> None:
    """Test JoinedStr with only LiteralString."""
    lit1 = astx.LiteralString("hello ")
    lit2 = astx.LiteralString("world")
    joined = astx.JoinedStr(values=[lit1, lit2])

    assert isinstance(joined, astx.JoinedStr)
    assert joined.values == [lit1, lit2]
    assert (
        str(joined)
        == "JoinedStr([LiteralString(hello ), LiteralString(world)])"
    )

    struct = joined.get_struct()
    assert isinstance(struct, dict)
    assert "JoinedStr" in struct
    outer_val = cast(Dict[str, Any], struct["JoinedStr"])
    struct_content = outer_val.get("content")
    assert isinstance(struct_content, dict)
    assert "values" in struct_content
    assert isinstance(struct_content["values"], list)
    assert len(struct_content["values"]) == NUM_VALUES_SIMPLE
    assert isinstance(struct_content["values"][0], dict)
    assert "LiteralString: hello " in struct_content["values"][0]
    assert isinstance(struct_content["values"][1], dict)
    assert "LiteralString: world" in struct_content["values"][1]


def test_joined_str_creation_mixed() -> None:
    """Test JoinedStr with LiteralString and FormattedValue."""
    lit1 = astx.LiteralString("Value is ")
    var_x = astx.Variable("x")
    fmt_val = astx.FormattedValue(value=var_x, conversion=ord("r"))
    lit2 = astx.LiteralString(".")
    joined = astx.JoinedStr(values=[lit1, fmt_val, lit2])

    assert isinstance(joined, astx.JoinedStr)
    assert joined.values == [lit1, fmt_val, lit2]
    expected_str = (
        "JoinedStr([LiteralString(Value is ), "
        "FormattedValue(x!r), LiteralString(.)])"
    )
    assert str(joined) == expected_str

    struct = joined.get_struct()
    assert isinstance(struct, dict)
    assert "JoinedStr" in struct
    outer_val = cast(Dict[str, Any], struct["JoinedStr"])
    struct_content = outer_val.get("content")
    assert isinstance(struct_content, dict)
    assert "values" in struct_content
    assert len(struct_content["values"]) == NUM_VALUES_MIXED
    assert "LiteralString: Value is " in struct_content["values"][0]
    assert "FormattedValue" in struct_content["values"][1]
    assert "LiteralString: ." in struct_content["values"][2]
