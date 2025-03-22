"""ASTx Python transpiler."""

from typing import Union, cast

from plum import dispatch

import astx
import astx.operators

from astx.tools.typing import typechecked
from astx.tools.transpilers.python_ast import ASTxPythonASTTranspiler


@typechecked
class ASTxPythonTranspiler:
    """
    Transpiler that converts ASTx nodes to Python code.

    Notes
    -----
    Please keep the visit method in alphabet order according to the node type.
    The visit method for astx.AST should be the first one.
    """

    def __init__(self) -> None:
        self.indent_level = 0
        self.indent_str = "    "  # 4 spaces
        self.ast_transpiler = ASTxPythonASTTranspiler()

    def _generate_block(self, block: astx.ASTNodes) -> str:
        """Generate code for a block of statements with proper indentation."""
        self.indent_level += 1
        indent = self.indent_str * self.indent_level
        lines = [indent + self.visit(node) for node in block.nodes]
        result = (
            "\n".join(lines)
            if lines
            else self.indent_str * self.indent_level + "pass"
        )
        self.indent_level -= 1
        return result

    @dispatch.abstract
    def visit(self, expr: astx.AST) -> str:
        """Translate an ASTx expression."""
        raise Exception(f"Not implemented yet ({expr}).")

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AliasExpr) -> str:
        """Handle AliasExpr nodes."""
        if node.asname:
            return f"{node.name} as {node.asname}"
        return f"{node.name}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Argument) -> str:
        """Handle Argument nodes."""
        type_ = self.visit(node.type_)
        return f"{node.name}: {type_}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Arguments) -> str:
        """Handle Argumens nodes."""
        return ", ".join([self.visit(arg) for arg in node.nodes])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AssignmentExpr) -> str:
        """Handle AssignmentExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AsyncForRangeLoopExpr) -> str:
        """Handle AsyncForRangeLoopExpr nodes."""
        if len(node.body) > 1:
            raise ValueError(
                "AsyncForRangeLoopExpr in Python just accept 1 node in the "
                "body attribute."
            )
        start = (
            self.visit(node.start)
            if getattr(node, "start", None) is not None
            else "0"
        )
        end = self.visit(node.end)
        step = (
            self.visit(node.step)
            if getattr(node, "step", None) is not None
            else "1"
        )

        return (
            f"result = [{self.visit(node.body).strip()} async for "
            f"{node.variable.name} in range({start}, {end}, {step})]"
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AwaitExpr) -> str:
        """Handle AwaitExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BinaryOp) -> str:
        """Handle BinaryOp nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Block) -> str:
        """Handle Block nodes."""
        return self._generate_block(node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CaseStmt) -> str:
        """Handle CaseStmt nodes."""
        cond_str = (
            self.visit(node.condition) if node.condition is not None else "_"
        )
        body_str = self.visit(node.body)
        return f"case {cond_str}:\n{body_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CatchHandlerStmt) -> str:
        """Handle CatchHandlerStmt nodes."""
        types_str = (
            f" ({' ,'.join(self.visit(t) for t in node.types)})"
            if node.types
            else ""
        )
        name_str = f" as {self.visit(node.name)}" if node.name else ""
        body_str = self._generate_block(node.body)
        return f"except{types_str}{name_str}:\n{body_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ClassDefStmt) -> str:
        """Handle ClassDefStmt nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.EnumDeclStmt) -> str:
        """Handle EnumDeclStmt nodes."""
        attr_str = "\n    ".join(self.visit(attr) for attr in node.attributes)
        return f"class {node.name}(Enum):\n    {attr_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ExceptionHandlerStmt) -> str:
        """Handle ExceptionHandlerStmt nodes."""
        body_str = self._generate_block(node.body)
        handlers_str = "\n".join(
            self.visit(handler) for handler in node.handlers
        )
        finally_str = (
            f"\n{self.visit(node.finally_handler)}"
            if node.finally_handler
            else ""
        )
        return f"try:\n{body_str}\n{handlers_str}{finally_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FinallyHandlerStmt) -> str:
        """Handle FinallyHandlerStmt nodes."""
        body_str = self._generate_block(node.body)
        return f"finally:\n{body_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ForRangeLoopExpr) -> str:
        """Handle ForRangeLoopExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionAsyncDef) -> str:
        """Handle FunctionAsyncDef nodes."""
        args = self.visit(node.prototype.args)
        returns = (
            f" -> {self.visit(node.prototype.return_type)}"
            if node.prototype.return_type
            else ""
        )
        header = f"async def {node.name}({args}){returns}:"
        body = self.visit(node.body)
        return f"{header}\n{body}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionDef) -> str:
        """Handle FunctionDef nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

        @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionCall) -> str:
        """Handle FunctionCall nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionReturn) -> str:
        """Handle FunctionReturn nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Identifier) -> str:
        """Handle Identifier nodes."""
        return f"{node.value}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfExpr) -> str:
        """Handle IfExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfStmt) -> str:
        """Handle IfStmt nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromStmt) -> str:
        """Handle ImportFromStmt nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportExpr) -> str:
        """Handle ImportExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromExpr) -> str:
        """Handle ImportFromExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)


        @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportStmt) -> str:
        """Handle ImportStmt nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromStmt) -> str:
        """Handle ImportFromStmt nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LambdaExpr) -> str:
        """Handle LambdaExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralBoolean) -> str:
        """Handle LiteralBoolean nodes."""
        return "True" if node.value else "False"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex32) -> str:
        """Handle LiteralComplex32 nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex) -> str:
        """Handle LiteralComplex nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)


        @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex64) -> str:
        """Handle LiteralComplex64 nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat16) -> str:
        """Handle LiteralFloat nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat32) -> str:
        """Handle LiteralFloat nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat64) -> str:
        """Handle LiteralFloat nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt32) -> str:
        """Handle LiteralInt32 nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralString) -> str:
        """Handle LiteralUTF8String nodes."""
        return repr(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralUTF8String) -> str:
        """Handle LiteralUTF8String nodes."""
        return repr(node.value)


        @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralUTF8Char) -> str:
        """Handle LiteralUTF8Char nodes."""
        return repr(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Union[astx.StructDeclStmt, astx.StructDefStmt]) -> str:
        """Handle StructDeclStmt and StructDefStmt nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SubscriptExpr) -> str:
        """Handle SubscriptExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SwitchStmt) -> str:
        """Handle SwitchStmt nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Complex32) -> str:
        """Handle Complex32 nodes."""
        return "Complex"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Complex64) -> str:
        """Handle Complex64 nodes."""
        return "Complex"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Float16) -> str:
        """Handle Float nodes."""
        return "float"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Float32) -> str:
        """Handle Float nodes."""
        return "float"


        @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Float64) -> str:
        """Handle Float nodes."""
        return "float"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Int32) -> str:
        """Handle Int32 nodes."""
        return "int"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.TypeCastExpr) -> str:
        """Handle TypeCastExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ThrowStmt) -> str:
        """Handle ThrowStmt nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UnaryOp) -> str:
        """Handle UnaryOp nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UTF8Char) -> str:
        """Handle UTF8Char nodes."""
        return repr(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UTF8String) -> str:
        """Handle UTF8String nodes."""
        return repr(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Variable) -> str:
        """Handle Variable nodes."""
        return node.name

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableAssignment) -> str:
        """Handle VariableAssignment nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableDeclaration) -> str:
        """Handle VariableDeclaration nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WalrusOp) -> str:
        """Handle Walrus operator."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)


        @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AugAssign) -> str:
        """Handle Augmented assign operator."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileExpr) -> str:
        """Handle WhileExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileStmt) -> str:
        """Handle WhileStmt nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldExpr) -> str:
        """Handle YieldExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldFromExpr) -> str:
        """Handle YieldFromExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Date) -> str:
        """Handle Date nodes."""
        return "date"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Time) -> str:
        """Handle Time nodes."""
        return "time"

        @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Timestamp) -> str:
        """Handle Timestamp nodes."""
        return "timestamp"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DateTime) -> str:
        """Handle DateTime nodes."""
        return "datetime"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDate) -> str:
        """Handle LiteralDate nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTime) -> str:
        """Handle LiteralTime nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTimestamp) -> str:
        """Handle LiteralTimestamp nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDateTime) -> str:
        """Handle LiteralDateTime nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ParenthesizedExpr) -> str:
        """Handle ParenthesizedExpr nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AndOp) -> str:
        """Handle AndOp nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)


        @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.OrOp) -> str:
        """Handle OrOp nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.XorOp) -> str:
        """Handle XorOp nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NandOp) -> str:
        """Handle NandOp nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NorOp) -> str:
        """Handle NorOp nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.XnorOp) -> str:
        """Handle XnorOp nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralList) -> str:
        """Handle LiteralList nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTuple) -> str:
        """Handle LiteralTuple nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralSet) -> str:
        """Handle LiteralSet nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDict) -> str:
        """Handle LiteralDict nodes."""
        python_ast = self.ast_transpiler.visit(node)
        return ast.unparse(python_ast)
