"""ASTx to Python string transpiler (New Implementation)."""

import ast
import sys

from typing import Union

import astx

from astx.tools.typing import typechecked

from astx_transpilers.python_to_ast import ASTxPythonASTTranspiler


@typechecked
class ASTxPythonTranspiler:
    """
    Transpiler that converts ASTx nodes to Python source code strings.

    This transpiler uses the AST-based approach by first converting ASTx to
    Python AST and then using ast.unparse() to generate the string
    representation.
    """

    def __init__(self) -> None:
        self.indent_level = 0
        self.indent_str = "    "
        self._ast_transpiler = ASTxPythonASTTranspiler()

    def visit(self, node: Union[astx.AST, astx.ASTNodes]) -> str:  # noqa: D102
        try:
            python_ast = self._ast_transpiler.visit(node)
            if sys.version_info >= (3, 9):
                code = ast.unparse(python_ast)
            else:
                try:
                    import astunparse
                    code = astunparse.unparse(python_ast).strip()
                except ImportError:
                    raise ImportError(
                        "For Python < 3.9, please install 'astunparse' package"
                    )
            if self.indent_level > 0:
                lines = code.split("\n")
                indented_lines = [
                    (
                        self.indent_str * self.indent_level + line
                        if line.strip()
                        else line
                    )
                    for line in lines
                ]
                code = "\n".join(indented_lines)

            return code

        except Exception as e:
            return f"# Error converting {type(node).__name__!s}: {e!s}"

    def set_indent(self, level: int, indent_str: str = "    ") -> None:  # noqa: D102
        self.indent_level = level
        self.indent_str = indent_str

    def _generate_block(self, block: astx.ASTNodes) -> str:
        self.indent_level += 1
        result = self.visit(block)
        self.indent_level -= 1
        return result
        if not result.strip():
            return self.indent_str * (self.indent_level + 1) + "pass"
        return result
