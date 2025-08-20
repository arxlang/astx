"""Tests for subscripts."""

from typing import cast

from astx.base import ASTKind, DictDataTypesStruct
from astx.data import Variable
from astx.literals import LiteralInt32
from astx.subscript import Ellipsis, SubscriptExpr
from astx.viz import visualize_image


def test_subscriptexpr_upper_lower() -> None:
    """Test `SubscriptExpr` class - slice of an array."""
    # Variable
    a_var = Variable(name="a")

    # SubscriptExpr
    subscr_expr = SubscriptExpr(
        value=a_var,
        lower=LiteralInt32(0),
        upper=LiteralInt32(10),
        step=LiteralInt32(2),
    )

    assert str(subscr_expr)
    assert subscr_expr.get_struct()
    assert subscr_expr.get_struct(simplified=True)
    visualize_image(subscr_expr.get_struct())


def test_subscriptexpr_index() -> None:
    """Test `SubscriptExpr` class - index of an array."""
    # Variable
    a_var = Variable(name="a")

    # SubscriptExpr
    subscr_expr = SubscriptExpr(
        value=a_var,
        index=LiteralInt32(0),
    )

    assert str(subscr_expr)
    assert subscr_expr.get_struct()
    assert subscr_expr.get_struct(simplified=True)
    visualize_image(subscr_expr.get_struct())


def test_ellipsis_basic_properties() -> None:
    """Test basic properties of the Ellipsis class."""
    ellip = Ellipsis()
    assert ellip.kind == ASTKind.EllipsisKind
    assert str(ellip) == "Ellipsis"
    struct = ellip.get_struct()
    struct_dict = cast(DictDataTypesStruct, struct)
    assert "Ellipsis" in struct_dict


def test_ellipsis_in_various_slice_positions() -> None:
    """Test Ellipsis used in different positions in subscript expressions."""
    arr = Variable(name="array")
    # Case 1:upper bound
    slice_upper = SubscriptExpr(
        value=arr,
        lower=LiteralInt32(1),
        upper=Ellipsis(),
    )
    assert isinstance(slice_upper.upper, Ellipsis)
    assert "Ellipsis" in str(slice_upper)  # Changed from "..." to "Ellipsis"
    # Case 2:lower bound
    slice_lower = SubscriptExpr(
        value=arr,
        lower=Ellipsis(),
        upper=LiteralInt32(10),
    )
    assert isinstance(slice_lower.lower, Ellipsis)
    # Case 3:ellipse as an step
    slice_step = SubscriptExpr(
        value=arr,
        lower=LiteralInt32(1),
        upper=LiteralInt32(10),
        step=Ellipsis(),
    )
    assert isinstance(slice_step.step, Ellipsis)


def test_ellipsis_as_standalone_index() -> None:
    """Test using Ellipsis as a standalone index - array[...]."""
    arr = Variable(name="data")
    subscr = SubscriptExpr(
        value=arr,
        index=Ellipsis(),
    )

    assert isinstance(subscr.index, Ellipsis)
    struct = subscr.get_struct()
    struct_dict = cast(DictDataTypesStruct, struct)
    assert "SubscriptExpr" in struct_dict
    subscr_dict = cast(DictDataTypesStruct, struct_dict["SubscriptExpr"])
    content_dict = cast(DictDataTypesStruct, subscr_dict["content"])
    assert "indexed" in content_dict
    assert "index" in content_dict


def test_ellipsis_nested_expressions() -> None:
    """Test Ellipsis in more complex nested expressions."""
    inner_arr = Variable(name="vector")
    inner_subscr = SubscriptExpr(
        value=inner_arr,
        index=Ellipsis(),
    )
    assert "Ellipsis" in str(inner_subscr)
    assert isinstance(inner_subscr.index, Ellipsis)
