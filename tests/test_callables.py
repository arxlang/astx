"""Test callable ASTx objects."""

import pytest

from astx.blocks import Block
from astx.callables import (
    Argument,
    Arguments,
    Function,
    FunctionCall,
    FunctionPrototype,
    FunctionReturn,
)
from astx.datatypes import Int32, LiteralInt32
from astx.modifiers import ScopeKind, VisibilityKind
from astx.viz import visualize


def test_function_creation_with_no_modifiers() -> None:
    """Test function creation with no modifiers."""
    var_a = Argument("a", type_=Int32, default=LiteralInt32(1))
    var_b = Argument("b", type_=Int32, default=LiteralInt32(1))

    proto = FunctionPrototype(
        name="add",
        args=Arguments(var_a, var_b),
        return_type=Int32,
    )

    with pytest.raises(Exception):
        proto.get_struct()

    fn_block = Block()
    fn = Function(prototype=proto, body=fn_block)

    assert str(fn)
    assert fn.get_struct()
    assert fn.get_struct(simplified=True)

    visualize(fn.get_struct())


def test_function_creation_with_modifiers() -> None:
    """Test function creation with modifiers."""
    var_a = Argument("a", type_=Int32, default=LiteralInt32(1))
    var_b = Argument("b", type_=Int32, default=LiteralInt32(1))
    proto = FunctionPrototype(
        name="add",
        args=Arguments(var_a, var_b),
        return_type=Int32,
        visibility=VisibilityKind.public,
        scope=ScopeKind.global_,
    )
    fn_block = Block()
    fn = Function(prototype=proto, body=fn_block)

    assert str(fn)
    assert fn.get_struct()
    assert fn.get_struct(simplified=True)

    visualize(fn.get_struct())


def test_function_call() -> None:
    """Test the FunctionCall class."""
    var_a = Argument("a", type_=Int32, default=LiteralInt32(1))
    var_b = Argument("b", type_=Int32, default=LiteralInt32(1))
    proto = FunctionPrototype(
        name="add",
        args=Arguments(var_a, var_b),
        return_type=Int32,
        visibility=VisibilityKind.public,
        scope=ScopeKind.global_,
    )
    fn_block = Block()
    fn = Function(prototype=proto, body=fn_block)

    lit_int32_1 = LiteralInt32(1)

    fn_call = FunctionCall(fn=fn, args=(lit_int32_1,))

    assert hash(fn_call) == hash(fn(args=(lit_int32_1,)))
    assert fn_call.get_struct()
    assert fn_call.get_struct(simplified=True)


def test_function_return() -> None:
    """Test the FunctionReturn class."""
    fn_return = FunctionReturn(LiteralInt32(0))

    assert str(fn_return)
    assert fn_return.get_struct()
    assert fn_return.get_struct(simplified=True)
