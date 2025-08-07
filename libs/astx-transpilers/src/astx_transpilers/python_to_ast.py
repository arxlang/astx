"""ASTx to Python AST transpiler."""

import ast
import sys

from typing import Any, List, Optional, Union

import astx

from astx.tools.typing import typechecked
from plum import dispatch

# Python 3.10+ compatibility for match statements
if sys.version_info >= (3, 10):
    match_case = ast.match_case
    Match = ast.Match
else:
    # Fallback for older Python versions
    match_case = Any
    Match = Any

# Operator mappings
BINARY_OP_MAP = {
    "+": ast.Add(),
    "-": ast.Sub(),
    "*": ast.Mult(),
    "/": ast.Div(),
    "//": ast.FloorDiv(),
    "%": ast.Mod(),
    "**": ast.Pow(),
    "<<": ast.LShift(),
    ">>": ast.RShift(),
    "|": ast.BitOr(),
    "&": ast.BitAnd(),
    "^": ast.BitXor(),
}

AUGASSIGN_OP_MAP = {
    "+=": ast.Add(),
    "-=": ast.Sub(),
    "*=": ast.Mult(),
    "/=": ast.Div(),
    "//=": ast.FloorDiv(),
    "%=": ast.Mod(),
    "**=": ast.Pow(),
    "<<=": ast.LShift(),
    ">>=": ast.RShift(),
    "|=": ast.BitOr(),
    "&=": ast.BitAnd(),
    "^=": ast.BitXor(),
}

COMPARE_OP_MAP = {
    "==": ast.Eq(),
    "!=": ast.NotEq(),
    "<": ast.Lt(),
    "<=": ast.LtE(),
    ">": ast.Gt(),
    ">=": ast.GtE(),
    "in": ast.In(),
    "not in": ast.NotIn(),
    "is": ast.Is(),
    "is not": ast.IsNot(),
}

UNARY_OP_MAP = {
    "-": ast.USub(),
    "+": ast.UAdd(),
    "~": ast.Invert(),
    "not": ast.Not(),
}


@typechecked
class ASTxPythonASTTranspiler:
    """
    Transpiler that converts ASTx nodes to Python AST nodes.

    Notes
    -----
    Please keep the visit method in alphabet order according to the node type.
    The visit method for astx.AST should be the first one.
    """

    def __init__(self) -> None:
        """Initialize the transpiler."""
        self.indent_level = 0

    def _convert_using_unparse(self, node: astx.AST) -> ast.AST:
        """Convert an ASTx node to a Python AST node using unparse."""
        try:
            from astx_transpilers.python_string import ASTxPythonTranspiler

            python_string = ASTxPythonTranspiler().visit(node)

            module = ast.parse(python_string)

            if module.body and isinstance(module.body[0], ast.Expr):
                return module.body[0].value
            elif module.body:
                return module.body[0]
            else:
                return ast.Pass()

        except Exception:
            if hasattr(node, "value"):
                return ast.Constant(value=str(node.value))
            else:
                return ast.Constant(value=f"<{type(node).__name__}>")

    def _convert_block(
        self, block: Optional[Union[astx.ASTNodes, astx.Block]]
    ) -> List[ast.stmt]:
        """Convert a block of statements to Python AST nodes."""
        if not block:
            return [ast.Pass()]

        if not hasattr(block, "nodes"):
            return [ast.Pass()]

        result = []
        for node in block.nodes:
            try:
                converted = self.visit(node)
                if isinstance(converted, list):
                    result.extend(converted)
                elif isinstance(converted, ast.stmt):
                    result.append(converted)
                elif isinstance(converted, ast.expr):
                    result.append(ast.Expr(value=converted))
                else:
                    result.append(ast.Pass())
            except Exception:
                continue

        return result if result else [ast.Pass()]

    @dispatch.abstract
    def visit(self, expr: astx.AST) -> ast.AST:
        """Translate an ASTx node to a Python AST node."""
        raise Exception(f"Not implemented yet ({expr}).")

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AliasExpr) -> ast.alias:
        """Handle AliasExpr nodes."""
        if not hasattr(node, "name"):
            return ast.alias(name="", asname=None)
        return ast.alias(
            name=node.name,
            asname=node.asname if hasattr(node, "asname") else None,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AndOp) -> ast.BoolOp:
        """Handle AndOp nodes."""
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        return ast.BoolOp(
            op=ast.And(), values=[self.visit(node.lhs), self.visit(node.rhs)]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Argument) -> ast.arg:
        """Handle Argument nodes."""
        if not hasattr(node, "name"):
            return self._convert_using_unparse(node)
        annotation = None
        if hasattr(node, "type_") and node.type_:
            annotation = self.visit(node.type_)
        return ast.arg(arg=node.name, annotation=annotation)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Arguments) -> ast.arguments:
        """Handle Arguments nodes."""
        if not hasattr(node, "nodes"):
            return self._convert_using_unparse(node)
        args = [self.visit(arg) for arg in node.nodes]
        return ast.arguments(
            posonlyargs=[],
            args=args,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AssignmentExpr) -> ast.Assign:
        """Handle AssignmentExpr nodes."""
        if not hasattr(node, "targets") or not node.targets:
            return self._convert_using_unparse(node)

        targets = []
        for target in node.targets:
            if hasattr(target, "name"):
                targets.append(ast.Name(id=target.name, ctx=ast.Store()))
            else:
                return self._convert_using_unparse(node)

        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)

        value = self.visit(node.value)
        return ast.Assign(targets=targets, value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ASTNodes) -> List[ast.AST]:
        """Handle ASTNodes nodes."""
        if not hasattr(node, "nodes"):
            return [self._convert_using_unparse(node)]
        return [self.visit(n) for n in node.nodes]

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AsyncForRangeLoopExpr) -> ast.ListComp:
        """Handle AsyncForRangeLoopExpr nodes."""
        if not hasattr(node, "variable") or not hasattr(node, "body"):
            return self._convert_using_unparse(node)
        target = ast.Name(id=node.variable.name, ctx=ast.Store())
        start = (
            self.visit(node.start)
            if hasattr(node, "start") and node.start
            else ast.Constant(value=0)
        )
        end = self.visit(node.end)
        step = (
            self.visit(node.step)
            if hasattr(node, "step") and node.step
            else ast.Constant(value=1)
        )
        iter_expr = ast.Call(
            func=ast.Name(id="range", ctx=ast.Load()),
            args=[start, end, step],
            keywords=[],
        )
        comp = ast.comprehension(
            target=target, iter=iter_expr, ifs=[], is_async=1
        )
        element = (
            self.visit(node.body.nodes[0])
            if hasattr(node.body, "nodes")
            else ast.Name(id="result", ctx=ast.Load())
        )

        return ast.ListComp(elt=element, generators=[comp])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AugAssign) -> ast.AugAssign:
        """Handle AugAssign nodes."""
        if (
            not hasattr(node, "target")
            or not hasattr(node, "value")
            or not hasattr(node, "op_code")
        ):
            return self._convert_using_unparse(node)

        target = self.visit(node.target)
        if isinstance(target, ast.Name):
            target.ctx = ast.Store()

        value = self.visit(node.value)
        return ast.AugAssign(
            target=target,
            op=AUGASSIGN_OP_MAP.get(node.op_code, ast.Add()),
            value=value,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AwaitExpr) -> ast.Await:
        """Handle AwaitExpr nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        value = self.visit(node.value)
        return ast.Await(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BinaryOp) -> Union[ast.BinOp, ast.Call]:
        """Handle BinaryOp nodes."""
        if (
            not hasattr(node, "lhs")
            or not hasattr(node, "rhs")
            or not hasattr(node, "op_code")
        ):
            return self._convert_using_unparse(node)

        if node.op_code not in BINARY_OP_MAP:
            lhs = self.visit(node.lhs)
            rhs = self.visit(node.rhs)

            # Clean the operator code first
            op_code_clean = (
                node.op_code.replace("@", "at")
                .replace("&", "and")
                .replace("|", "or")
            )
            func_name = f"operator_{op_code_clean}"

            return ast.Call(
                func=ast.Name(id=func_name, ctx=ast.Load()),
                args=[lhs, rhs],
                keywords=[],
            )

        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return ast.BinOp(left=lhs, op=BINARY_OP_MAP[node.op_code], right=rhs)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Block) -> List[ast.stmt]:
        """Handle Block nodes."""
        return self._convert_block(node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BreakStmt) -> ast.Break:
        """Handle BreakStmt nodes."""
        return ast.Break()

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CaseStmt) -> Any:
        """Handle CaseStmt nodes."""
        if not hasattr(node, "condition"):
            return self._convert_using_unparse(node)

        if node.condition is None:
            if sys.version_info >= (3, 10):
                pattern = ast.MatchAs(name=None, pattern=None)
            else:
                return self._convert_using_unparse(node)
        else:
            pattern = self.visit(node.condition)
        body = (
            self._convert_block(node.body)
            if hasattr(node, "body")
            else [ast.Pass()]
        )

        if sys.version_info >= (3, 10):
            return ast.match_case(pattern=pattern, guard=None, body=body)
        else:
            return self._convert_using_unparse(node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CatchHandlerStmt) -> ast.ExceptHandler:
        """Handle CatchHandlerStmt nodes."""
        type_ = None
        if hasattr(node, "types") and node.types:
            type_ = self.visit(node.types[0])
        name = None
        if hasattr(node, "name") and node.name:
            if hasattr(node.name, "value"):
                name = node.name.value
            elif isinstance(node.name, str):
                name = node.name
            else:
                name = str(node.name)
        body = (
            self._convert_block(node.body)
            if hasattr(node, "body")
            else [ast.Pass()]
        )
        return ast.ExceptHandler(type=type_, name=name, body=body)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ClassDefStmt) -> ast.ClassDef:
        """Handle ClassDefStmt nodes."""
        if not hasattr(node, "name"):
            return self._convert_using_unparse(node)

        bases = []
        keywords = []

        if hasattr(node, "is_abstract") and node.is_abstract:
            bases.append(ast.Name(id="ABC", ctx=ast.Load()))

        body = (
            self._convert_block(node.body)
            if hasattr(node, "body")
            else [ast.Pass()]
        )

        return ast.ClassDef(
            name=node.name,
            bases=bases,
            keywords=keywords,
            body=body,
            decorator_list=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CompareOp) -> ast.Compare:
        """Handle CompareOp nodes."""
        if (
            not hasattr(node, "left")
            or not hasattr(node, "ops")
            or not hasattr(node, "comparators")
        ):
            return self._convert_using_unparse(node)

        ops = [COMPARE_OP_MAP.get(op, ast.Eq()) for op in node.ops]
        comparators = [
            self.visit(comparator) for comparator in node.comparators
        ]

        return ast.Compare(
            left=self.visit(node.left), ops=ops, comparators=comparators
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ComprehensionClause) -> ast.comprehension:
        """Handle ComprehensionClause nodes."""
        if not hasattr(node, "target") or not hasattr(node, "iterable"):
            return self._convert_using_unparse(node)
        target = self.visit(node.target)
        iter_ = self.visit(node.iterable)
        ifs = []
        if hasattr(node, "conditions"):
            ifs = [self.visit(cond) for cond in node.conditions]
        is_async = 1 if hasattr(node, "is_async") and node.is_async else 0
        return ast.comprehension(
            target=target,
            iter=iter_,
            ifs=ifs,
            is_async=is_async,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Complex32) -> ast.Name:
        """Handle Complex32 nodes."""
        return ast.Name(id="complex", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Complex64) -> ast.Name:
        """Handle Complex64 nodes."""
        return ast.Name(id="complex", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ContinueStmt) -> ast.Continue:
        """Handle ContinueStmt nodes."""
        return ast.Continue()

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DataType) -> ast.Name:
        """Handle DataType nodes."""
        type_id = getattr(node, "id", "object")
        return ast.Name(id=type_id, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Date) -> ast.Name:
        """Handle Date nodes."""
        return ast.Name(id="date", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DateTime) -> ast.Name:
        """Handle DateTime nodes."""
        return ast.Name(id="datetime", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DeleteStmt) -> ast.Delete:
        """Handle DeleteStmt nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        targets = [self.visit(target) for target in node.value]
        return ast.Delete(targets=targets)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DoWhileExpr) -> ast.ListComp:
        """Handle DoWhileExpr nodes."""
        if not hasattr(node, "body") or not hasattr(node, "condition"):
            return self._convert_using_unparse(node)
        element = (
            self.visit(node.body.nodes[0])
            if hasattr(node.body, "nodes")
            else ast.Name(id="result", ctx=ast.Load())
        )
        condition = self.visit(node.condition)

        comp = ast.comprehension(
            target=ast.Name(id="_", ctx=ast.Store()),
            iter=ast.Call(
                func=ast.Name(id="iter", ctx=ast.Load()),
                args=[
                    ast.Lambda(
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[],
                            vararg=None,
                            kwarg=None,
                        ),
                        body=ast.Constant(value=True),
                    ),
                    ast.Constant(value=False),
                ],
                keywords=[],
            ),
            ifs=[condition],
            is_async=0,
        )

        return ast.ListComp(elt=element, generators=[comp])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DoWhileStmt) -> ast.While:
        """Handle DoWhileStmt nodes."""
        if not hasattr(node, "body") or not hasattr(node, "condition"):
            return self._convert_using_unparse(node)
        body = (
            self._convert_block(node.body)
            if hasattr(node, "body")
            else [ast.Pass()]
        )
        condition = self.visit(node.condition)
        break_if = ast.If(
            test=ast.UnaryOp(op=ast.Not(), operand=condition),
            body=[ast.Break()],
            orelse=[],
        )
        body.append(break_if)

        return ast.While(test=ast.Constant(value=True), body=body, orelse=[])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Ellipsis) -> ast.Constant:
        """Handle Ellipsis nodes."""
        return ast.Constant(value=...)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.EnumDeclStmt) -> ast.ClassDef:
        """Handle EnumDeclStmt nodes."""
        if not hasattr(node, "name") or not hasattr(node, "attributes"):
            return self._convert_using_unparse(node)

        body = []
        for attr in node.attributes:
            if isinstance(attr, astx.VariableDeclaration):
                # Create a simple assignment for enum attributes
                target = ast.Name(id=attr.name, ctx=ast.Store())
                # Use auto() for enum values
                value = ast.Call(
                    func=ast.Name(id="auto", ctx=ast.Load()),
                    args=[],
                    keywords=[],
                )
                assign = ast.Assign(targets=[target], value=value)
                body.append(assign)
            else:
                # For other types, try to visit them directly
                visited = self.visit(attr)
                if isinstance(visited, (ast.stmt, ast.expr)):
                    if isinstance(visited, ast.expr):
                        # Wrap expressions in Expr statement
                        body.append(ast.Expr(value=visited))
                    else:
                        body.append(visited)

        if not body:
            body = [ast.Pass()]

        return ast.ClassDef(
            name=node.name,
            bases=[ast.Name(id="Enum", ctx=ast.Load())],
            keywords=[],
            decorator_list=[],
            body=body,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ExceptionHandlerStmt) -> ast.Try:
        """Handle ExceptionHandlerStmt nodes."""
        if not hasattr(node, "body"):
            return self._convert_using_unparse(node)

        body = self._convert_block(node.body)

        handlers = []
        if hasattr(node, "handlers") and node.handlers:
            handlers = [self.visit(handler) for handler in node.handlers]

        orelse = []
        finalbody = []
        if hasattr(node, "finally_handler") and node.finally_handler:
            finalbody = self._convert_block(node.finally_handler.body)

        return ast.Try(
            body=body, handlers=handlers, orelse=orelse, finalbody=finalbody
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FinallyHandlerStmt) -> ast.Try:
        """Handle FinallyHandlerStmt nodes."""
        if not hasattr(node, "body"):
            return self._convert_using_unparse(node)

        finalbody = self._convert_block(node.body)

        return ast.Try(
            body=[ast.Pass()], handlers=[], orelse=[], finalbody=finalbody
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Float16) -> ast.Name:
        """Handle Float16 nodes."""
        return ast.Name(id="float", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Float32) -> ast.Name:
        """Handle Float32 nodes."""
        return ast.Name(id="float", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Float64) -> ast.Name:
        """Handle Float64 nodes."""
        return ast.Name(id="float", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ForCountLoopStmt) -> ast.For:
        """Handle ForCountLoopStmt nodes."""
        if (
            not hasattr(node, "initializer")
            or not hasattr(node, "condition")
            or not hasattr(node, "update")
        ):
            return self._convert_using_unparse(node)
        target = ast.Name(
            id=node.initializer.name,
            ctx=ast.Store(),
        )
        start = (
            self.visit(node.initializer.value)
            if hasattr(node.initializer, "value")
            else ast.Constant(value=0)
        )
        if (
            hasattr(node.condition, "comparators")
            and node.condition.comparators
        ):
            end = self.visit(node.condition.comparators[0])
        else:
            end = ast.Constant(value=10)
        iter_ = ast.Call(
            func=ast.Name(id="range", ctx=ast.Load()),
            args=[start, end],
            keywords=[],
        )
        body = (
            self._convert_block(node.body)
            if hasattr(node, "body")
            else [ast.Pass()]
        )
        return ast.For(target=target, iter=iter_, body=body, orelse=[])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ForRangeLoopExpr) -> ast.ListComp:
        """Handle ForRangeLoopExpr nodes."""
        if not hasattr(node, "variable") or not hasattr(node, "body"):
            return self._convert_using_unparse(node)
        target = ast.Name(id=node.variable.name, ctx=ast.Store())
        start = (
            self.visit(node.start)
            if hasattr(node, "start") and node.start
            else ast.Constant(value=0)
        )
        end = self.visit(node.end)
        step = (
            self.visit(node.step)
            if hasattr(node, "step") and node.step
            else ast.Constant(value=1)
        )
        iter_expr = ast.Call(
            func=ast.Name(id="range", ctx=ast.Load()),
            args=[start, end, step],
            keywords=[],
        )
        comp = ast.comprehension(
            target=target, iter=iter_expr, ifs=[], is_async=0
        )
        element = (
            self.visit(node.body.nodes[0])
            if hasattr(node.body, "nodes")
            else ast.Name(id="result", ctx=ast.Load())
        )

        return ast.ListComp(elt=element, generators=[comp])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ForRangeLoopStmt) -> ast.For:
        """Handle ForRangeLoopStmt nodes."""
        if not hasattr(node, "variable") or not hasattr(node, "start"):
            return self._convert_using_unparse(node)
        target = ast.Name(id=node.variable.name, ctx=ast.Store())
        start = self.visit(node.start)
        end = self.visit(node.end)
        step = self.visit(node.step) if hasattr(node, "step") else None
        range_args = [start, end]
        if step:
            range_args.append(step)
        iter_ = ast.Call(
            func=ast.Name(id="range", ctx=ast.Load()),
            args=range_args,
            keywords=[],
        )
        body = (
            self._convert_block(node.body)
            if hasattr(node, "body")
            else [ast.Pass()]
        )
        return ast.For(target=target, iter=iter_, body=body, orelse=[])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionAsyncDef) -> ast.AsyncFunctionDef:
        """Handle FunctionAsyncDef nodes."""
        if (
            not hasattr(node, "name")
            or not hasattr(node, "prototype")
            or not hasattr(node.prototype, "args")
        ):
            return self._convert_using_unparse(node)
        args_nodes = []
        if hasattr(node.prototype.args, "nodes"):
            args_nodes = node.prototype.args.nodes
        arguments = ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(
                    arg=arg.name if hasattr(arg, "name") else "arg",
                    annotation=None,
                )
                for arg in args_nodes
            ],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None,
        )
        returns = None
        if (
            hasattr(node.prototype, "return_type")
            and node.prototype.return_type
        ):
            returns = self.visit(node.prototype.return_type)
        body = (
            self._convert_block(node.body)
            if hasattr(node, "body")
            else [ast.Pass()]
        )
        return ast.AsyncFunctionDef(
            name=node.name,
            args=arguments,
            body=body,
            decorator_list=[],
            returns=returns,
            type_comment=None,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionCall) -> ast.Call:
        """Handle FunctionCall nodes."""
        if (
            not hasattr(node, "fn")
            or not hasattr(node.fn, "name")
            or not hasattr(node, "args")
        ):
            return self._convert_using_unparse(node)
        func = ast.Name(id=node.fn, ctx=ast.Load())
        args = [self.visit(arg) for arg in node.args]
        keywords = []
        return ast.Call(func=func, args=args, keywords=keywords)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionDef) -> ast.FunctionDef:
        """Handle FunctionDef nodes."""
        if (
            not hasattr(node, "name")
            or not hasattr(node, "prototype")
            or not hasattr(node.prototype, "args")
        ):
            return self._convert_using_unparse(node)
        args_nodes = []
        if hasattr(node.prototype.args, "nodes"):
            args_nodes = node.prototype.args.nodes
        arguments = ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(
                    arg=arg.name if hasattr(arg, "name") else "arg",
                    annotation=None,
                )
                for arg in args_nodes
            ],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None,
        )
        returns = None
        if (
            hasattr(node.prototype, "return_type")
            and node.prototype.return_type
        ):
            returns = self.visit(node.prototype.return_type)
        body = (
            self._convert_block(node.body)
            if hasattr(node, "body")
            else [ast.Pass()]
        )

        return ast.FunctionDef(
            name=node.name,
            args=arguments,
            body=body,
            decorator_list=[],
            returns=returns,
            type_comment=None,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionPrototype) -> ast.FunctionDef:
        """Handle FunctionPrototype nodes."""
        if not hasattr(node, "name"):
            return self._convert_using_unparse(node)
        args_nodes = []
        if hasattr(node, "args") and hasattr(node.args, "nodes"):
            args_nodes = node.args.nodes
        arguments = ast.arguments(
            posonlyargs=[],
            args=[self.visit(arg) for arg in args_nodes],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None,
        )

        returns = None
        if hasattr(node, "return_type") and node.return_type:
            returns = self.visit(node.return_type)
        return ast.FunctionDef(
            name=node.name,
            args=arguments,
            body=[ast.Pass()],
            decorator_list=[],
            returns=returns,
            type_comment=None,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionReturn) -> ast.Return:
        """Handle FunctionReturn nodes."""
        value = None
        if hasattr(node, "value") and node.value:
            value = self.visit(node.value)
        return ast.Return(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.GeneratorExpr) -> ast.GeneratorExp:
        """Handle GeneratorExpr nodes."""
        if not hasattr(node, "element") or not hasattr(node, "generators"):
            return self._convert_using_unparse(node)
        element = self.visit(node.element)
        generators = [self.visit(gen) for gen in node.generators]
        return ast.GeneratorExp(elt=element, generators=generators)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Identifier) -> ast.Name:
        """Handle Identifier nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        return ast.Name(id=str(node.value), ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfExpr) -> ast.IfExp:
        """Handle IfExpr nodes."""
        if not hasattr(node, "condition"):
            return self._convert_using_unparse(node)
        then_value = None
        if hasattr(node, "then") and node.then:
            if len(node.then) == 1:
                then_value = self.visit(node.then[0])
            else:
                then_value = self._convert_using_unparse(node.then)
        else:
            then_value = ast.Constant(value=None)

        else_value = None
        if hasattr(node, "else_") and node.else_:
            if len(node.else_) == 1:
                else_value = self.visit(node.else_[0])
            else:
                else_value = self._convert_using_unparse(node.else_)
        else:
            else_value = ast.Constant(value=None)
        return ast.IfExp(
            test=self.visit(node.condition), body=then_value, orelse=else_value
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfStmt) -> ast.If:
        """Handle IfStmt nodes."""
        if not hasattr(node, "condition"):
            return self._convert_using_unparse(node)
        then_body = (
            self._convert_block(node.then)
            if hasattr(node, "then")
            else [ast.Pass()]
        )
        else_body = (
            self._convert_block(node.else_)
            if hasattr(node, "else_") and node.else_
            else []
        )
        return ast.If(
            test=self.visit(node.condition), body=then_body, orelse=else_body
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportExpr) -> ast.Assign:
        """Handle ImportExpr nodes."""
        if not hasattr(node, "names"):
            return self._convert_using_unparse(node)
        import_calls = []
        targets = []
        for i, name in enumerate(node.names):
            import_call = ast.Call(
                func=ast.Name(id="__import__", ctx=ast.Load()),
                args=[
                    ast.Constant(
                        value=name.name if hasattr(name, "name") else str(name)
                    )
                ],
                keywords=[],
            )
            import_calls.append(import_call)
            suffix = "" if len(node.names) == 1 else str(i + 1)
            targets.append(ast.Name(id=f"module{suffix}", ctx=ast.Store()))
        if len(import_calls) == 1:
            value = import_calls[0]
            target = targets[0]
        else:
            value = ast.Tuple(elts=import_calls, ctx=ast.Load())
            target = ast.Tuple(elts=targets, ctx=ast.Store())

        return ast.Assign(targets=[target], value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromExpr) -> ast.Assign:
        """Handle ImportFromExpr nodes."""
        if not hasattr(node, "names") or not hasattr(node, "module"):
            return self._convert_using_unparse(node)
        import_calls = []
        targets = []
        level_dots = "." * getattr(node, "level", 0)
        module_name = (
            f"{level_dots}{node.module}" if node.module else level_dots
        )
        for i, name in enumerate(node.names):
            name_str = name.name if hasattr(name, "name") else str(name)
            import_call = ast.Call(
                func=ast.Name(id="getattr", ctx=ast.Load()),
                args=[
                    ast.Call(
                        func=ast.Name(id="__import__", ctx=ast.Load()),
                        args=[
                            ast.Constant(value=module_name),
                        ],
                        keywords=[
                            ast.keyword(
                                arg="fromlist",
                                value=ast.List(
                                    elts=[ast.Constant(value=name_str)],
                                    ctx=ast.Load(),
                                ),
                            )
                        ],
                    ),
                    ast.Constant(value=name_str),
                ],
                keywords=[],
            )
            import_calls.append(import_call)
            suffix = "" if len(node.names) == 1 else str(i + 1)
            targets.append(ast.Name(id=f"name{suffix}", ctx=ast.Store()))
        if len(import_calls) == 1:
            value = import_calls[0]
            target = targets[0]
        else:
            value = ast.Tuple(elts=import_calls, ctx=ast.Load())
            target = ast.Tuple(elts=targets, ctx=ast.Store())
        return ast.Assign(targets=[target], value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromStmt) -> ast.ImportFrom:
        """Handle ImportFromStmt nodes."""
        if not hasattr(node, "names") or not hasattr(node, "module"):
            return self._convert_using_unparse(node)
        names = [self.visit(name) for name in node.names]
        level = node.level if hasattr(node, "level") else 0
        return ast.ImportFrom(module=node.module, names=names, level=level)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportStmt) -> ast.Import:
        """Handle ImportStmt nodes."""
        if not hasattr(node, "names"):
            return ast.Import(names=[ast.alias(name="", asname=None)])
        names = [self.visit(name) for name in node.names]
        return ast.Import(names=names)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.InlineVariableDeclaration) -> ast.AnnAssign:
        """Handle InlineVariableDeclaration nodes."""
        if not hasattr(node, "name") or not hasattr(node, "type_"):
            return self._convert_using_unparse(node)
        target = ast.Name(id=node.name, ctx=ast.Store())
        annotation = self.visit(node.type_)
        value = (
            self.visit(node.value)
            if hasattr(node, "value") and node.value
            else None
        )
        return ast.AnnAssign(
            target=target,
            annotation=annotation,
            value=value,
            simple=1,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Int32) -> ast.Name:
        """Handle Int32 nodes."""
        return ast.Name(id="int", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LambdaExpr) -> ast.Lambda:
        """Handle LambdaExpr nodes."""
        if not hasattr(node, "body"):
            return self._convert_using_unparse(node)
        args = []
        if hasattr(node, "params") and node.params:
            args = [
                ast.arg(arg=param.name, annotation=None)
                for param in node.params
            ]
        arguments = ast.arguments(
            posonlyargs=[],
            args=args,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None,
        )
        body = self.visit(node.body)
        return ast.Lambda(args=arguments, body=body)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ListComprehension) -> ast.ListComp:
        """Handle ListComprehension nodes."""
        if not hasattr(node, "element") or not hasattr(node, "generators"):
            return self._convert_using_unparse(node)
        element = self.visit(node.element)
        generators = [self.visit(gen) for gen in node.generators]
        return ast.ListComp(elt=element, generators=generators)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralBoolean) -> ast.Constant:
        """Handle LiteralBoolean nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value=False)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex) -> ast.Constant:
        """Handle LiteralComplex nodes."""
        if hasattr(node, "value"):
            return ast.Constant(value=node.value)
        elif hasattr(node, "real") and hasattr(node, "imag"):
            return ast.Constant(value=complex(node.real, node.imag))
        else:
            return ast.Constant(value=0j)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex32) -> ast.Call:
        """Handle LiteralComplex32 nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        real = ast.Constant(value=node.value[0])
        imag = ast.Constant(value=node.value[1])
        return ast.Call(
            func=ast.Name(id="complex", ctx=ast.Load()),
            args=[real, imag],
            keywords=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex64) -> ast.Call:
        """Handle LiteralComplex64 nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        real = ast.Constant(value=node.value[0])
        imag = ast.Constant(value=node.value[1])
        return ast.Call(
            func=ast.Name(id="complex", ctx=ast.Load()),
            args=[real, imag],
            keywords=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDate) -> ast.Call:
        """Handle LiteralDate nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        return ast.Call(
            func=ast.Attribute(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="datetime", ctx=ast.Load()),
                        attr="strptime",
                        ctx=ast.Load(),
                    ),
                    args=[
                        ast.Constant(value=node.value),
                        ast.Constant(value="%Y-%m-%d"),
                    ],
                    keywords=[],
                ),
                attr="date",
                ctx=ast.Load(),
            ),
            args=[],
            keywords=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDateTime) -> ast.Call:
        """Handle LiteralDateTime nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="datetime", ctx=ast.Load()),
                attr="strptime",
                ctx=ast.Load(),
            ),
            args=[
                ast.Constant(value=node.value),
                ast.Constant(value="%Y-%m-%dT%H:%M:%S"),
            ],
            keywords=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDict) -> ast.Dict:
        """Handle LiteralDict nodes."""
        if not hasattr(node, "elements"):
            return ast.Dict(keys=[], values=[])
        keys = [self.visit(key) for key in node.elements.keys()]
        values = [self.visit(value) for value in node.elements.values()]
        return ast.Dict(keys=keys, values=values)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat16) -> ast.Constant:
        """Handle LiteralFloat16 nodes."""
        return ast.Constant(value=float(node.value))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat32) -> ast.Constant:
        """Handle LiteralFloat32 nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value=0.0)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat64) -> ast.Constant:
        """Handle LiteralFloat64 nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value=0.0)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt8) -> ast.Constant:
        """Handle LiteralInt8 nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value=0)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt16) -> ast.Constant:
        """Handle LiteralInt16 nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value=0)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt32) -> ast.Constant:
        """Handle LiteralInt32 nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value=0)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt64) -> ast.Constant:
        """Handle LiteralInt64 nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value=0)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralList) -> ast.List:
        """Handle LiteralList nodes."""
        if not hasattr(node, "elements"):
            return ast.List(elts=[], ctx=ast.Load())
        elements = [self.visit(element) for element in node.elements]
        return ast.List(elts=elements, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralNone) -> ast.Constant:
        """Handle LiteralNone nodes."""
        return ast.Constant(value=None)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralSet) -> ast.Set:
        """Handle LiteralSet nodes."""
        if not hasattr(node, "elements"):
            return ast.Set(elts=[])
        elements = [self.visit(element) for element in node.elements]
        return ast.Set(elts=elements)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralString) -> ast.Constant:
        """Handle LiteralString nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value="")
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTime) -> ast.Call:
        """Handle LiteralTime nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        return ast.Call(
            func=ast.Attribute(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="datetime", ctx=ast.Load()),
                        attr="strptime",
                        ctx=ast.Load(),
                    ),
                    args=[
                        ast.Constant(value=node.value),
                        ast.Constant(value="%H:%M:%S"),
                    ],
                    keywords=[],
                ),
                attr="time",
                ctx=ast.Load(),
            ),
            args=[],
            keywords=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTimestamp) -> ast.Call:
        """Handle LiteralTimestamp nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="datetime", ctx=ast.Load()),
                attr="strptime",
                ctx=ast.Load(),
            ),
            args=[
                ast.Constant(value=node.value),
                ast.Constant(value="%Y-%m-%d %H:%M:%S"),
            ],
            keywords=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTuple) -> ast.Tuple:
        """Handle LiteralTuple nodes."""
        if not hasattr(node, "elements"):
            return ast.Tuple(elts=[], ctx=ast.Load())
        elements = [self.visit(element) for element in node.elements]
        return ast.Tuple(elts=elements, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralUTF8Char) -> ast.Constant:
        """Handle LiteralUTF8Char nodes."""
        return ast.Constant(value=str(node.value))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralUTF8String) -> ast.Constant:
        """Handle LiteralUTF8String nodes."""
        return ast.Constant(value=str(node.value))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Module) -> ast.Module:
        """Handle Module nodes."""
        if not hasattr(node, "body"):
            return ast.Module(body=[ast.Pass()], type_ignores=[])

        body = self._convert_block(node.body)
        return ast.Module(body=body, type_ignores=[])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NandOp) -> ast.UnaryOp:
        """Handle NandOp nodes."""
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)

        and_op = ast.BoolOp(op=ast.And(), values=[lhs, rhs])
        return ast.UnaryOp(op=ast.Not(), operand=and_op)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NorOp) -> ast.UnaryOp:
        """Handle NorOp nodes."""
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)

        or_op = ast.BoolOp(op=ast.Or(), values=[lhs, rhs])
        return ast.UnaryOp(op=ast.Not(), operand=or_op)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NotOp) -> ast.UnaryOp:
        """Handle NotOp nodes."""
        if not hasattr(node, "operand"):
            return self._convert_using_unparse(node)

        operand = self.visit(node.operand)
        return ast.UnaryOp(op=ast.Not(), operand=operand)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.OrOp) -> ast.BoolOp:
        """Handle OrOp nodes."""
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        return ast.BoolOp(
            op=ast.Or(), values=[self.visit(node.lhs), self.visit(node.rhs)]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ParenthesizedExpr) -> ast.AST:
        """Handle ParenthesizedExpr nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        return self.visit(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SetComprehension) -> ast.SetComp:
        """Handle SetComprehension nodes."""
        if not hasattr(node, "element") or not hasattr(node, "generators"):
            return self._convert_using_unparse(node)
        element = self.visit(node.element)
        generators = [self.visit(gen) for gen in node.generators]
        return ast.SetComp(elt=element, generators=generators)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Starred) -> ast.Starred:
        """Handle Starred nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)

        value = self.visit(node.value)
        return ast.Starred(value=value, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.StructDeclStmt) -> ast.ClassDef:
        """Handle StructDeclStmt nodes."""
        if not hasattr(node, "name"):
            return self._convert_using_unparse(node)
        decorators = [ast.Name(id="dataclass", ctx=ast.Load())]
        body = []
        if hasattr(node, "attributes") and node.attributes:
            for attr in node.attributes:
                body.append(self.visit(attr))
        else:
            body = [ast.Pass()]
        return ast.ClassDef(
            name=node.name,
            bases=[],
            keywords=[],
            body=body,
            decorator_list=decorators,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.StructDefStmt) -> ast.ClassDef:
        """Handle StructDefStmt nodes."""
        if not hasattr(node, "name"):
            return self._convert_using_unparse(node)
        decorators = [ast.Name(id="dataclass", ctx=ast.Load())]
        body = []
        if hasattr(node, "attributes") and node.attributes:
            for attr in node.attributes:
                body.append(self.visit(attr))
        else:
            body = [ast.Pass()]

        return ast.ClassDef(
            name=node.name,
            bases=[],
            keywords=[],
            body=body,
            decorator_list=decorators,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SwitchStmt) -> Any:
        """Handle SwitchStmt nodes."""
        if not hasattr(node, "value") or not hasattr(node, "cases"):
            return self._convert_using_unparse(node)
        subject = self.visit(node.value)
        cases = []
        if hasattr(node.cases, "nodes"):
            cases = [self.visit(case) for case in node.cases.nodes]
        if sys.version_info >= (3, 10):
            return ast.Match(subject=subject, cases=cases)
        else:
            return self._convert_using_unparse(node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SubscriptExpr) -> ast.Subscript:
        """Handle SubscriptExpr nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        value = self.visit(node.value)
        if hasattr(node, "index") and not isinstance(
            node.index, astx.LiteralNone
        ):
            index = self.visit(node.index)
            return ast.Subscript(value=value, slice=index, ctx=ast.Load())
        lower = None
        upper = None
        step = None
        if hasattr(node, "lower") and not isinstance(
            node.lower, astx.LiteralNone
        ):
            lower = self.visit(node.lower)
        if hasattr(node, "upper") and not isinstance(
            node.upper, astx.LiteralNone
        ):
            upper = self.visit(node.upper)
        if hasattr(node, "step") and not isinstance(
            node.step, astx.LiteralNone
        ):
            step = self.visit(node.step)
        slice_obj = ast.Slice(lower=lower, upper=upper, step=step)
        return ast.Subscript(value=value, slice=slice_obj, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Time) -> ast.Name:
        """Handle Time nodes."""
        return ast.Name(id="time", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Timestamp) -> ast.Name:
        """Handle Timestamp nodes."""
        return ast.Name(id="timestamp", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ThrowStmt) -> ast.Raise:
        """Handle ThrowStmt nodes."""
        exc = None
        if hasattr(node, "exception") and node.exception:
            exc = self.visit(node.exception)
        cause = None
        if hasattr(node, "cause") and node.cause:
            cause = self.visit(node.cause)
        return ast.Raise(exc=exc, cause=cause)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.TypeCastExpr) -> ast.Call:
        """Handle TypeCastExpr nodes."""
        if not hasattr(node, "target_type") or not hasattr(node, "expr"):
            return self._convert_using_unparse(node)
        target_type = self.visit(node.target_type)
        expr = self.visit(node.expr)
        return ast.Call(
            func=ast.Name(id="cast", ctx=ast.Load()),
            args=[target_type, expr],
            keywords=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UnaryOp) -> ast.UnaryOp:
        """Handle UnaryOp nodes."""
        if not hasattr(node, "op_code") or not hasattr(node, "operand"):
            return self._convert_using_unparse(node)
        if node.op_code not in UNARY_OP_MAP:
            return self._convert_using_unparse(node)
        operand = self.visit(node.operand)
        return ast.UnaryOp(op=UNARY_OP_MAP[node.op_code], operand=operand)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UTF8Char) -> ast.Name:
        """Handle UTF8Char nodes."""
        return ast.Name(id="str", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UTF8String) -> ast.Name:
        """Handle UTF8String nodes."""
        return ast.Name(id="str", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Variable) -> ast.Name:
        """Handle Variable nodes."""
        if not hasattr(node, "name"):
            return ast.Name(id="undefined", ctx=ast.Load())
        return ast.Name(id=node.name, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableAssignment) -> ast.Assign:
        """Handle VariableAssignment nodes."""
        if not hasattr(node, "name") or not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        target = ast.Name(id=node.name, ctx=ast.Store())
        value = self.visit(node.value)
        return ast.Assign(targets=[target], value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableDeclaration) -> ast.AnnAssign:
        """Handle VariableDeclaration nodes."""
        if not hasattr(node, "name") or not hasattr(node, "type"):
            return self._convert_using_unparse(node)
        target = ast.Name(id=node.name, ctx=ast.Store())
        annotation = self.visit(node.type)
        value = (
            self.visit(node.value)
            if hasattr(node, "value") and node.value
            else None
        )
        return ast.AnnAssign(
            target=target,
            annotation=annotation,
            value=value,
            simple=1,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WalrusOp) -> ast.NamedExpr:
        """Handle WalrusOp nodes."""
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        target = self.visit(node.lhs)
        if isinstance(target, ast.Name):
            target.ctx = ast.Store()
        value = self.visit(node.rhs)
        return ast.NamedExpr(target=target, value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileExpr) -> ast.ListComp:
        """Handle WhileExpr nodes."""
        if not hasattr(node, "condition") or not hasattr(node, "body"):
            return self._convert_using_unparse(node)
        element = (
            self.visit(node.body.nodes[0])
            if hasattr(node.body, "nodes")
            else ast.Name(id="result", ctx=ast.Load())
        )
        condition = self.visit(node.condition)
        comp = ast.comprehension(
            target=ast.Name(id="_", ctx=ast.Store()),
            iter=ast.Call(
                func=ast.Name(id="iter", ctx=ast.Load()),
                args=[
                    ast.Lambda(
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[],
                            vararg=None,
                            kwarg=None,
                        ),
                        body=condition,
                    ),
                    ast.Constant(value=False),
                ],
                keywords=[],
            ),
            ifs=[],
            is_async=0,
        )

        return ast.ListComp(elt=element, generators=[comp])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileStmt) -> ast.While:
        """Handle WhileStmt nodes."""
        if not hasattr(node, "condition"):
            return self._convert_using_unparse(node)

        test = self.visit(node.condition)
        body = (
            self._convert_block(node.body)
            if hasattr(node, "body")
            else [ast.Pass()]
        )

        return ast.While(test=test, body=body, orelse=[])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.XnorOp) -> ast.UnaryOp:
        """Handle XnorOp nodes."""
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        xor_op = ast.BinOp(left=lhs, op=ast.BitXor(), right=rhs)
        return ast.UnaryOp(op=ast.Not(), operand=xor_op)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.XorOp) -> ast.BinOp:
        """Handle XorOp nodes."""
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return ast.BinOp(left=lhs, op=ast.BitXor(), right=rhs)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldExpr) -> ast.Yield:
        """Handle YieldExpr nodes."""
        value = None
        if hasattr(node, "value") and node.value:
            value = self.visit(node.value)
        return ast.Yield(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldFromExpr) -> ast.YieldFrom:
        """Handle YieldFromExpr nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        value = self.visit(node.value)
        return ast.YieldFrom(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldStmt) -> ast.Expr:
        """Handle YieldStmt nodes."""
        value = None
        if hasattr(node, "value") and node.value:
            value = self.visit(node.value)
        yield_expr = ast.Yield(value=value)
        return ast.Expr(value=yield_expr)
