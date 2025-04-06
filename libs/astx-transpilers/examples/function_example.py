# libs/astx-transpilers/examples/function_example.py
"""
Example: Function definition using the ASTx to Python AST transpiler.

This example demonstrates how to:
1. Create an ASTx function definition
2. Convert it to Python AST
3. Execute the function

The function takes a number and doubles it.
"""

import ast
from typing import Any, Dict  # Added for type hints

import astx

from astx_transpilers.python_ast import ASTxPythonASTTranspiler


# Add type hint for the manually defined function for comparison/demonstration
def double(x: int) -> int:
    """Return double the input number."""
    return x * 2


def main() -> None:  # Added return type hint
    """Run the function definition example."""
    print("=" * 50)
    print("EXAMPLE: FUNCTION DEFINITION")
    print("=" * 50)

    # Create a simple function that doubles a number
    # def double(x):
    #     return x * 2

    # Step 1: Create function prototype with argument
    arg = astx.Argument("x", astx.Int32())
    args_obj = astx.Arguments(arg)  # Pass arg directly to constructor
    prototype = astx.FunctionPrototype(
        name="double", args=args_obj, return_type=astx.Int32()  # Pass object
    )

    # Step 2: Create function body
    body = astx.Block(name="func_body")
    calculation = astx.BinaryOp(
        lhs=astx.Variable("x"), op_code="*", rhs=astx.LiteralInt32(2)
    )
    body.append(astx.FunctionReturn(calculation))

    # Step 3: Create the function definition
    func_def = astx.FunctionDef(prototype, body)

    # Initialize transpiler
    transpiler = ASTxPythonASTTranspiler()

    # Convert to Python AST Module
    python_ast_module = transpiler.convert(func_def)
    print("Python AST Module (unparsed):")
    # Use ast_to_string for better readability if available
    try:
        print(transpiler.ast_to_string(python_ast_module))
    except Exception as e:  # Fallback if unparse fails
        print(f"(Unparsing failed: {e})")
        print(str(ast.dump(python_ast_module, indent=2))[:500] + "...")

    # Generate equivalent code manually for demonstration
    print("\nEquivalent Python code (Manually written):")
    print("def double(x: int) -> int:")
    print("    return x * 2")

    # Execute function using the transpiler's execute method
    print("\nExecuting function using transpiler:")
    try:
        # Provide type hints for the dictionaries used in execute
        globals_dict: Dict[str, Any] = {}
        locals_dict: Dict[str, Any] = {}
        # Execute expects the ASTx node, not the converted Python AST
        result_dict = transpiler.execute(
            func_def, globals_dict=globals_dict, locals_dict=locals_dict
        )

        if "double" in result_dict:
            # The executed function will be in locals_dict
            double_func_executed = result_dict["double"]
            test_values = [0, 5, -3, 10]

            print("Testing function with different inputs:")
            all_correct = True
            for val in test_values:
                # Call the function obtained from execution
                output = double_func_executed(val)
                expected = val * 2
                print(f"double({val}) = {output} (expected: {expected})")
                if output != expected:
                    all_correct = False

            if all_correct:
                print("✅ Function execution successful for all test cases!")
            else:
                print("❌ Function execution incorrect for some test cases")
        else:
            print("Function 'double' not found in execution result")
            print(f"Available variables: {list(result_dict.keys())}")
    except Exception as e:
        print(f"Error during execution: {e}")
        print("\nDemonstrating manually instead:")

        # Use the manually defined 'double' function
        for val in [0, 5, -3, 10]:
            # Call the manually defined function
            print(f"double({val}) = {double(val)}")  # Using the top-level double


if __name__ == "__main__":
    main()
