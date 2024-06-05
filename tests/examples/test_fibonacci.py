"""Test fibonnaci with astx."""

from __future__ import annotations

import astx


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
