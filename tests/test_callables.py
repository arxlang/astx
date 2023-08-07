from astx.blocks import Block
from astx.callables import Function, FunctionPrototype
from astx.datatypes import Variable, Int32, Int32Literal
from astx.modifiers import ScopeKind, VisibilityKind


def test_function_creation_with_no_modifiers():
    var_a = Variable("a", type_=Int32, value=Int32Literal(1))
    var_b = Variable("b", type_=Int32, value=Int32Literal(1))
    proto = FunctionPrototype(
        name="add",
        args=[var_a, var_b],
        return_type=Int32,
    )
    fn_block = Block()
    Function(prototype=proto, body=fn_block)


def test_function_creation_with_modifiers():
    var_a = Variable("a", type_=Int32, value=Int32Literal(1))
    var_b = Variable("b", type_=Int32, value=Int32Literal(1))
    proto = FunctionPrototype(
        name="add",
        args=[var_a, var_b],
        return_type=Int32,
        visibility=VisibilityKind.public,
        scope=ScopeKind.global_,
    )
    fn_block = Block()
    Function(prototype=proto, body=fn_block)
