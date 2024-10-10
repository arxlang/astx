"""Test Python Transpiler."""

import astx

from astx.transpilers import python as astx2py


def test_function() -> None:
    """Test astx.Function."""
    # Function parameters
    args = astx.Arguments(
        astx.Argument(name="x", type_=astx.Int32),
        astx.Argument(name="y", type_=astx.Int32),
    )

    # Function body
    body = astx.Block()
    body.append(
        astx.VariableAssignment(
            name="result",
            value=astx.BinaryOp(
                op_code="+",
                lhs=astx.Variable(name="x"),
                rhs=astx.Variable(name="y"),
                loc=astx.SourceLocation(line=2, col=8),
            ),
            loc=astx.SourceLocation(line=2, col=4),
        )
    )
    body.append(
        astx.FunctionReturn(
            value=astx.Variable(name="result"),
            loc=astx.SourceLocation(line=3, col=4),
        )
    )

    # Function definition
    add_function = astx.Function(
        prototype=astx.FunctionPrototype(
            name="add",
            args=args,
            return_type=astx.Int32,
        ),
        body=body,
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(add_function)
    expected_code = "\n".join(
        [
            "def add(x: int, y: int) -> int:",
            "    result = (x + y)",
            "    return result",
        ]
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_int32() -> None:
    """Test astx.LiteralInt32."""
    # Create a LiteralInt32 node
    literal_int32_node = astx.LiteralInt32(value=42)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_int32_node)
    expected_code = "42"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float16() -> None:
    """Test astx.LiteralFloat16."""
    # Create a LiteralFloat16 node
    literal_float16_node = astx.LiteralFloat16(value=3.14)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_float16_node)
    expected_code = "3.14"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float32() -> None:
    """Test astx.LiteralFloat32."""
    # Create a LiteralFloat32 node
    literal_float32_node = astx.LiteralFloat32(value=2.718)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_float32_node)
    expected_code = "2.718"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float64() -> None:
    """Test astx.LiteralFloat64."""
    # Create a LiteralFloat64 node
    literal_float64_node = astx.LiteralFloat64(value=1.414)

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_float64_node)
    expected_code = "1.414"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_complex() -> None:
    """Test astx.LiteralComplex."""
    # Create a LiteralComplex node
    literal_complex64_node = astx.LiteralComplex(value=complex(3, 4))

    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()

    # Generate Python code
    generated_code = generator.visit(literal_complex64_node)
    expected_code = "(3, 4)"

    assert generated_code == expected_code, "generated_code != expected_code"
