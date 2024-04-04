"""Test callable ASTx objects."""

from astx.blocks import Block
from astx.callables import Function, FunctionPrototype
from astx.datatypes import Int32, LiteralInt32
from astx.modifiers import ScopeKind, VisibilityKind
from astx.variables import Argument


def test_function_creation_with_no_modifiers() -> None:
    """Test function creation with no modifiers."""
    var_a = Argument("a", type_=Int32, default=LiteralInt32(1))
    var_b = Argument("b", type_=Int32, default=LiteralInt32(1))

    proto = FunctionPrototype(
        name="add",
        args=(var_a, var_b),
        return_type=Int32,
    )
    fn_block = Block()
    Function(prototype=proto, body=fn_block)


def test_function_creation_with_modifiers() -> None:
    """Test function creation with modifiers."""
    var_a = Argument("a", type_=Int32, default=LiteralInt32(1))
    var_b = Argument("b", type_=Int32, default=LiteralInt32(1))
    proto = FunctionPrototype(
        name="add",
        args=(var_a, var_b),
        return_type=Int32,
        visibility=VisibilityKind.public,
        scope=ScopeKind.global_,
    )
    fn_block = Block()
    Function(prototype=proto, body=fn_block)
