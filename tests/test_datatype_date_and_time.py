import pytest

from astx import Date, Time, Variable
from astx.operators import BinaryOp, UnaryOp

VAR_A = Variable("a")

# Sample Date and Time values for testing
DATE_SAMPLE = "2024-10-26"
TIME_SAMPLE = "13:45:00"


def test_variable() -> None:
    """Test variable Date and Time."""
    var_date = Variable("date")
    var_time = Variable("time")

    # Testing binary operations with variables
    BinaryOp(op_code="+", lhs=var_date, rhs=var_time)


def test_date_literal() -> None:
    """Test Date literals."""
    date_a = Date(value=DATE_SAMPLE, format="yyyy-mm-dd")
    date_b = Date(value="2024-10-27", format="yyyy-mm-dd")
    BinaryOp(op_code="+", lhs=date_a, rhs=date_b)


def test_time_literal() -> None:
    """Test Time literals."""
    time_a = Time(value=TIME_SAMPLE, format="HH:mm:ss")
    time_b = Time(value="14:00:00", format="HH:mm:ss")
    BinaryOp(op_code="+", lhs=time_a, rhs=time_b)


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda: VAR_A + Date(value=DATE_SAMPLE, format="yyyy-mm-dd"), "+"),
        (lambda: VAR_A == Date(value=DATE_SAMPLE, format="yyyy-mm-dd"), "=="),
        (lambda: VAR_A != Date(value=DATE_SAMPLE, format="yyyy-mm-dd"), "!="),
    ],
)
def test_bin_ops_date(fn_bin_op, op_code):
    """Test binary operations on Date."""
    bin_op = fn_bin_op()
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_bin_op,op_code",
    [
        (lambda: VAR_A + Time(value=TIME_SAMPLE, format="HH:mm:ss"), "+"),
        (lambda: VAR_A == Time(value=TIME_SAMPLE, format="HH:mm:ss"), "=="),
        (lambda: VAR_A != Time(value=TIME_SAMPLE, format="HH:mm:ss"), "!="),
    ],
)
def test_bin_ops_time(fn_bin_op, op_code):
    """Test binary operations on Time."""
    bin_op = fn_bin_op()
    assert bin_op.op_code == op_code
    assert str(bin_op) != ""
    assert repr(bin_op) != ""
    assert bin_op.get_struct() != {}
    assert bin_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda: +Date(value=DATE_SAMPLE, format="yyyy-mm-dd"), "+"),
    ],
)
def test_unary_ops_date(fn_unary_op, op_code):
    """Test unary operations on Date."""
    unary_op = fn_unary_op()
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}


@pytest.mark.parametrize(
    "fn_unary_op,op_code",
    [
        (lambda: +Time(value=TIME_SAMPLE, format="HH:mm:ss"), "+"),
    ],
)
def test_unary_ops_time(fn_unary_op, op_code):
    """Test unary operations on Time."""
    unary_op = fn_unary_op()
    assert unary_op.op_code == op_code
    assert str(unary_op) != ""
    assert repr(unary_op) != ""
    assert unary_op.get_struct() != {}
    assert unary_op.get_struct(simplified=True) != {}
