"""Test callable ASTx objects."""

import astx
import pytest

from astx.blocks import Block
from astx.callables import (
    Function,
    FunctionCall,
    FunctionPrototype,
    FunctionReturn,
)
from astx.datatypes import Int32, LiteralInt32
from astx.modifiers import ScopeKind, VisibilityKind
from astx.variables import Argument, Arguments
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


def test_function_call_fibonacci() -> None:
    """Test the FunctionCall class with fibonacci."""
    # Initialize the ASTx module
    module = astx.Module()

    # Define the Fibonacci function prototype
    fib_proto = astx.FunctionPrototype(
        name="fib",
        args=astx.Arguments(astx.Argument("n", astx.Int32)),
        return_type=astx.Int32,
    )

    # Create the function body block
    fib_block = astx.Block()

    # Declare the variables
    decl_a = astx.VariableDeclaration(
        name="a", type_=astx.Int32, value=astx.LiteralInt32(0)
    )
    decl_b = astx.VariableDeclaration(
        name="b", type_=astx.Int32, value=astx.LiteralInt32(1)
    )
    decl_i = astx.VariableDeclaration(
        name="i", type_=astx.Int32, value=astx.LiteralInt32(2)
    )

    # Initialize the block with declarations
    fib_block.append(decl_a)
    fib_block.append(decl_b)
    fib_block.append(decl_i)

    # Create the loop condition
    cond = astx.BinaryOp(
        op_code="<", lhs=astx.Variable(name="i"), rhs=astx.Variable(name="n")
    )

    # Define the loop body
    loop_block = astx.Block()
    assign_sum = astx.VariableAssignment(
        name="sum",
        value=astx.BinaryOp(
            op_code="+",
            lhs=astx.Variable(name="a"),
            rhs=astx.Variable(name="b"),
        ),
    )
    assign_a = astx.VariableAssignment(name="a", value=astx.Variable(name="b"))
    assign_b = astx.VariableAssignment(
        name="b", value=astx.Variable(name="sum")
    )
    inc_i = astx.VariableAssignment(
        name="i",
        value=astx.BinaryOp(
            op_code="+", lhs=astx.Variable(name="i"), rhs=astx.LiteralInt32(1)
        ),
    )

    # Add assignments to the loop body
    loop_block.append(assign_sum)
    loop_block.append(assign_a)
    loop_block.append(assign_b)
    loop_block.append(inc_i)

    # Create the loop statement
    loop = astx.While(condition=cond, body=loop_block)
    fib_block.append(loop)

    # Add return statement
    return_stmt = astx.FunctionReturn(astx.Variable(name="b"))
    fib_block.append(return_stmt)

    # Define the function with its body
    fib_fn = astx.Function(prototype=fib_proto, body=fib_block)

    # Append the Fibonacci function to the module block
    module.block.append(fib_fn)

    assert module.get_struct()
    assert module.get_struct(simplified=True)


def test_function_return() -> None:
    """Test the FunctionReturn class."""
    fn_return = FunctionReturn(LiteralInt32(0))

    assert str(fn_return)
    assert fn_return.get_struct()
    assert fn_return.get_struct(simplified=True)
