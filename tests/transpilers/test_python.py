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

def test_float32() -> None:
    """Test astx.Float32."""
    # Variable declaration
    float32_var = astx.VariableAssignment(
        name="x",
        value=astx.LiteralFloat32(10.5),
        loc=astx.SourceLocation(line=1, col=0),
    )
    # Binary operation
    binary_op = astx.BinaryOp(
        op_code="+",
        lhs=astx.Variable(name="x"),
        rhs=astx.LiteralFloat32(5.5),
        loc=astx.SourceLocation(line=2, col=4),
    )
    # Function body
    body = astx.Block()
    body.append(float32_var)
    body.append(binary_op)
    # Function definition
    add_float32_function = astx.Function(
        prototype=astx.FunctionPrototype(
            name="add_float32",
            args=astx.Arguments(),
            return_type=astx.Float32,
        ),
        body=body,
        loc=astx.SourceLocation(line=1, col=0),
    )
    # Initialize the generator
    generator = astx2py.ASTxPythonTranspiler()
    # Generate Python code
    generated_code = generator.visit(add_float32_function)
    expected_code = "\n".join(
        [
            "def add_float32() -> float:",
            "    x = 10.5",
            "    return (x + 5.5)",
        ]
    )
    assert generated_code == expected_code, "generated_code != expected_code"
