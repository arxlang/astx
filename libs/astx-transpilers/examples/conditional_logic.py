# libs/astx-transpilers/examples/conditional_logic.py
"""
Example: If statement using the ASTx to Python AST transpiler.

This example demonstrates conditional logic:
1. Create an ASTx if statement with then/else branches
2. Convert it to Python AST
3. Execute the code to see the correct branch taken
"""

import ast
from typing import Any, Dict  # Added for type hints

import astx

from astx_transpilers.python_ast import ASTxPythonASTTranspiler


def main() -> None:  # Added return type hint
    """Run the conditional logic example."""
    print("=" * 50)
    print("EXAMPLE: IF STATEMENT")
    print("=" * 50)

    # Create a simple if statement:
    # x = 42
    # if x > 10:
    #     result = "Greater than 10"
    # else:
    #     result = "Less than or equal to 10"

    # Step 1: Create variable assignment
    x_assign = astx.VariableAssignment("x", astx.LiteralInt32(42))

    # Step 2: Create if condition
    condition = astx.BinaryOp(
        lhs=astx.Variable("x"), op_code=">", rhs=astx.LiteralInt32(10)
    )

    # Step 3: Create then block
    then_block = astx.Block(name="then_block")
    then_block.append(
        astx.VariableAssignment(
            "result", astx.LiteralString("Greater than 10")
        )
    )

    # Step 4: Create else block
    else_block = astx.Block(name="else_block")
    else_block.append(
        astx.VariableAssignment(
            "result", astx.LiteralString("Less than or equal to 10")
        )
    )

    # Step 5: Create if statement
    if_stmt = astx.IfStmt(
        condition=condition, then=then_block, else_=else_block
    )

    # Step 6: Create program block
    program = astx.Block(name="program")
    program.append(x_assign)
    program.append(if_stmt)

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
        print("x = 42")
        print("if (x > 10):")  # AST often adds parentheses
        print("    result = 'Greater than 10'")
        print("else:")
        print("    result = 'Less than or equal to 10'")

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

        print(f"x = {result_dict.get('x')}")
        print(f"result = {result_dict.get('result')}")

        # Verify
        expected = (
            "Greater than 10" if 42 > 10 else "Less than or equal to 10"
        )  # Keep comparison for logic clarity
        if result_dict.get("result") == expected:
            print("✅ If statement execution successful!")
        else:
            print("❌ If statement execution failed")
    except Exception as e:
        print(f"Error during execution: {e}")

        # Manual verification
        x = 42
        result = "Greater than 10" if x > 10 else "Less than or equal to 10"
        print("\nManual verification:")
        print(f"x = {x}")
        print(f"result = {result}")
        print("(This is the expected output of the transpiled code)")


if __name__ == "__main__":
    main()
