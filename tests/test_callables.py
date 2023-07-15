from arxast.blocks import Block
from arxast.callables import Call, Function, FunctionPrototype, Return
from arxast.datatypes import Variable, Int32
from arxast.modifiers import ScopeKind, VisibilityKind


def test_function_creation_with_no_modifiers():
    var_a = Variable("a", type_=Int32)
    var_b = Variable("b", type_=Int32)
    proto = FunctionPrototype(
        name="add",
        args=[var_a, var_b],
        return_type=Int32,
    )
    fn_block = Block()
    fn = Function(prototype=proto, body=fn_block)


def test_function_creation_with_modifiers():
    var_a = Variable("a", type_=Int32)
    var_b = Variable("b", type_=Int32)
    proto = FunctionPrototype(
        name="add",
        args=[var_a, var_b],
        return_type=Int32,
        visibility=VisibilityKind.public,
        scope=ScopeKind.global_,
    )
    fn_block = Block()
    fn = Function(prototype=proto, body=fn_block)
