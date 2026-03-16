"""
title: Tests for Date, Time, Timestamp, and DateTime data types.
"""

from __future__ import annotations

from typing import Callable

import astx
import pytest

from astx.data import Variable
from astx.literals.temporal import (
    LiteralDate,
    LiteralDateTime,
    LiteralTime,
    LiteralTimestamp,
)
from astx.types.operators import BinaryOp, UnaryOp

VAR_A = Variable("a")

DATE_LITERAL_CLASSES = [
    LiteralDate,
    LiteralTime,
    LiteralTimestamp,
    LiteralDateTime,
]


def test_variable_date() -> None:
    """
    title: Test variable declaration with date types.
    """
    var_date = Variable("date_var")
    var_time = Variable("time_var")
    BinaryOp(op_code="+", lhs=var_date, rhs=var_time)


@pytest.mark.parametrize("literal_class", DATE_LITERAL_CLASSES)
def test_literal_initialization(literal_class: type[astx.Literal]) -> None:
    """
    title: Test date and time literals.
    parameters:
      literal_class:
        type: type[astx.Literal]
    """
    literal_instance = literal_class("2023-10-31")
    assert str(literal_instance) != ""
    assert repr(literal_instance) != ""
    assert literal_instance.get_struct() != {}
    assert literal_instance.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda literal_class: VAR_A + literal_class("2023-10-31"), "+"),
        (lambda literal_class: VAR_A == literal_class("2023-10-31"), "=="),
        (lambda literal_class: VAR_A != literal_class("2023-10-31"), "!="),
        (lambda literal_class: VAR_A > literal_class("2023-10-31"), ">"),
        (lambda literal_class: VAR_A >= literal_class("2023-10-31"), ">="),
        (lambda literal_class: VAR_A < literal_class("2023-10-31"), "<"),
        (lambda literal_class: VAR_A <= literal_class("2023-10-31"), "<="),
    ],
)
@pytest.mark.parametrize("literal_class", DATE_LITERAL_CLASSES)
def test_binary_operations(
    literal_class: type[astx.Literal],
    fn_bin_op: Callable[[type[astx.Literal]], BinaryOp],
    op_code: str,
) -> None:
    """
    title: Test binary operations on date and time literals.
    parameters:
      literal_class:
        type: type[astx.Literal]
      fn_bin_op:
        type: Callable[[type[astx.Literal]], BinaryOp]
      op_code:
        type: str
    """
    bin_op = fn_bin_op(literal_class)
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda literal_class: +literal_class("2023-10-31"), "+"),
        (lambda literal_class: -literal_class("2023-10-31"), "-"),
    ],
)
@pytest.mark.parametrize("literal_class", DATE_LITERAL_CLASSES)
def test_unary_operations(
    literal_class: type[astx.Literal],
    fn_unary_op: Callable[[type[astx.Literal]], UnaryOp],
    op_code: str,
) -> None:
    """
    title: Test unary operations on date and time literals.
    parameters:
      literal_class:
        type: type[astx.Literal]
      fn_unary_op:
        type: Callable[[type[astx.Literal]], UnaryOp]
      op_code:
        type: str
    """
    unary_op = fn_unary_op(literal_class)
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}


def test_literal_date_format() -> None:
    """
    title: Test LiteralDate format.
    """
    literal_date = LiteralDate("2023-10-31")
    assert literal_date.value == "2023-10-31"
    assert isinstance(literal_date, LiteralDate)


def test_literal_time_format() -> None:
    """
    title: Test LiteralTime format.
    """
    literal_time = LiteralTime("12:00:00")
    assert literal_time.value == "12:00:00"
    assert isinstance(literal_time, LiteralTime)


def test_literal_timestamp_format() -> None:
    """
    title: Test LiteralTimestamp format.
    """
    literal_timestamp = LiteralTimestamp("2023-10-31 12:00:00")
    assert literal_timestamp.value == "2023-10-31 12:00:00"
    assert isinstance(literal_timestamp, LiteralTimestamp)


def test_literal_datetime_format() -> None:
    """
    title: Test LiteralDateTime format.
    """
    literal_datetime = LiteralDateTime("2023-10-31 12:00:00.123456")
    assert literal_datetime.value == "2023-10-31 12:00:00.123456"
    assert isinstance(literal_datetime, LiteralDateTime)
