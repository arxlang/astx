# libs/astx-transpilers/examples/complex_program.py
"""
Example: While loop using the ASTx to Python AST transpiler.

This example demonstrates loops and state tracking:
1. Create an ASTx while loop that sums numbers
2. Convert it to Python AST
3. Execute the code to calculate the sum
"""

import ast
from typing import Any, Dict  # Added for type hints

import astx

from astx_transpilers.python_ast import ASTxPythonASTTranspiler

# Define constants to avoid magic numbers
LOOP_LIMIT = 5


def main() -> None:  # Added return type hint
    """Run the while loop example."""
    print("=" * 50)
    print("EXAMPLE: WHILE LOOP")
    print("=" * 50)

    # Create a simple while loop:
    # i = 0
    # sum_val = 0 # Renamed variable to avoid conflict with built-in sum
    # while i < LOOP_LIMIT:
    #     sum_val = sum_val + i
    #     i = i + 1

    # Step 1: Initialize variables
    i_init = astx.VariableAssignment("i", astx.LiteralInt32(0))
    sum_init = astx.VariableAssignment(
        "sum_val", astx.LiteralInt32(0)
    )  # Use sum_val

    # Step 2: Create while condition
    condition = astx.BinaryOp(
        lhs=astx.Variable("i"),
        op_code="<",
        rhs=astx.LiteralInt32(LOOP_LIMIT),
    )

    # Step 3: Create while body
    body = astx.Block(name="while_body")

    # sum_val = sum_val + i
    sum_update = astx.VariableAssignment(
        "sum_val",  # Use sum_val
        astx.BinaryOp(
            lhs=astx.Variable("sum_val"),  # Use sum_val
            op_code="+",
            rhs=astx.Variable("i"),
        ),
    )
    body.append(sum_update)

    # i = i + 1
    i_update = astx.VariableAssignment(
        "i",
        astx.BinaryOp(
            lhs=astx.Variable("i"), op_code="+", rhs=astx.LiteralInt32(1)
        ),
    )
    body.append(i_update)

    # Step 4: Create while statement
    while_stmt = astx.WhileStmt(condition=condition, body=body)

    # Step 5: Create program block
    program = astx.Block(name="program")
    program.append(i_init)
    program.append(sum_init)
    program.append(while_stmt)

    # Initialize transpiler
    transpiler = ASTxPythonASTTranspiler()

    # Convert to Python AST Module
    python_ast_module = transpiler.convert(program)

    # Show the equivalent Python code using ast_to_string
    print("Equivalent Python code (from AST):")
    try:
        print(transpiler.ast_to_string(python_ast_module))
    except Exception as e:  # Fallback
        print(f"(Unparsing failed: {e})")
        print("i = 0")
        print("sum_val = 0")  # Use sum_val
        print(f"while (i < {LOOP_LIMIT}):")  # AST often adds parentheses
        print("    sum_val = (sum_val + i)")  # Use sum_val
        print("    i = (i + 1)")

    # Execute the code
    print("\nExecuting code using transpiler:")
    try:
        # Provide type hints for dictionaries
        globals_dict: Dict[str, Any] = {}
        locals_dict: Dict[str, Any] = {}
        # Execute expects the original ASTx node
        result_dict = transpiler.execute(
            program, globals_dict=globals_dict, locals_dict=locals_dict
        )

        print(f"Final i = {result_dict.get('i')}")
        print(f"Final sum_val = {result_dict.get('sum_val')}")  # Use sum_val

        # Verify
        expected_i = LOOP_LIMIT
        expected_sum = sum(range(LOOP_LIMIT))  # sum of 0 to 4

        if (
            result_dict.get("i") == expected_i
            and result_dict.get("sum_val") == expected_sum
        ):  # Use sum_val
            print("✅ While loop execution successful!")
        else:
            print("❌ While loop execution incorrect")
            print(f"Expected i = {expected_i}, got {result_dict.get('i')}")
            print(
                f"Expected sum_val = {expected_sum}, "
                f"got {result_dict.get('sum_val')}"
            )  # Use sum_val
    except Exception as e:
        print(f"Error during execution: {e}")

        # Manual verification
        i = 0
        sum_val = 0  # Use sum_val
        while i < LOOP_LIMIT:
            sum_val = sum_val + i  # Use sum_val
            i = i + 1

        print("\nManual verification:")
        print(f"Final i = {i}")
        print(f"Final sum_val = {sum_val}")  # Use sum_val
        print("(This is the expected output of the transpiled code)")


if __name__ == "__main__":
    main()
