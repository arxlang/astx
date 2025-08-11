"""Test to see if the usage demo in README.md still works."""

import textwrap


def usage_demo() -> str:
    """Execute an exact copy of the code shown in README.md."""
    import astx
    args = astx.Arguments(
        astx.Argument(name="x", type_=astx.Int32()),
        astx.Argument(name="y", type_=astx.Int32()),
    )
    fn_body = astx.Block()
    fn_body.append(
        astx.FunctionReturn(
            value=astx.BinaryOp(
                op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("y")
            )
        )
    )
    add_function = astx.FunctionDef(
        prototype=astx.FunctionPrototype(
            name="add", args=args, return_type=astx.Int32()
        ),
        body=fn_body,
    )

    from astx_transpilers.python_string_new import ASTxPythonTranspiler

    # Transpile the AST to Python
    transpiler = ASTxPythonTranspiler()
    python_code = transpiler.visit(add_function)

    return str(python_code)


def test_readme_usage() -> None:
    """Test usage demo as shown in README.md."""
    expected = """\
                def add(x: int, y: int) -> int:
                    return (x + y)
                """

    assert usage_demo() == textwrap.dedent(expected).strip()
