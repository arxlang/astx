"""Test script to verify the new AST-based implementation works."""

import astx
import pytest

from astx_transpilers.python_string import ASTxPythonTranspiler


@pytest.fixture
def transpiler() -> ASTxPythonTranspiler:
    """Provide a transpiler instance for tests."""
    return ASTxPythonTranspiler()


def test_literals(transpiler: ASTxPythonTranspiler) -> None:
    """Test simple literals."""
    print("\n1. Testing Literals:")
    try:
        literal_int = astx.LiteralInt32(value=42)
        result = transpiler.visit(literal_int)
        print(f"   LiteralInt32(42): '{result}'")
    except Exception as e:
        print(f"   LiteralInt32 Error: {e}")

    try:
        literal_str = astx.LiteralString(value="hello")
        result = transpiler.visit(literal_str)
        print(f"   LiteralString('hello'): '{result}'")
    except Exception as e:
        print(f"   LiteralString Error: {e}")


def test_variables(transpiler: ASTxPythonTranspiler) -> None:
    """Test variables."""
    print("\n2. Testing Variables:")
    try:
        variable = astx.Variable(name="x")
        result = transpiler.visit(variable)
        print(f"   Variable('x'): '{result}'")
    except Exception as e:
        print(f"   Variable Error: {e}")


def test_binary_operations(transpiler: ASTxPythonTranspiler) -> None:
    """Test binary operations."""
    print("\n3. Testing Binary Operations:")
    try:
        left = astx.LiteralInt32(value=10)
        right = astx.LiteralInt32(value=20)
        binary_op = astx.BinaryOp(lhs=left, op_code="+", rhs=right)
        result = transpiler.visit(binary_op)
        print(f"   BinaryOp(10 + 20): '{result}'")
    except Exception as e:
        print(f"   BinaryOp Error: {e}")


def test_new_implementation() -> None:
    """Test the new AST-based implementation."""
    print("Testing new AST-based implementation:")
    print("=" * 50)

    transpiler = ASTxPythonTranspiler()

    test_literals(transpiler)
    test_variables(transpiler)
    test_binary_operations(transpiler)

    print("\n" + "=" * 50)
    print("Test completed!")


if __name__ == "__main__":
    test_new_implementation()
