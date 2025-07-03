"""ASTx to Python AST transpiler."""

import ast

from typing import List, Optional, Union

import astx

from astx.tools.typing import typechecked
from plum import dispatch

# Operator mappings - moved outside of methods for efficiency
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

            # Convert to string first
            python_string = ASTxPythonTranspiler().visit(node)

            # Parse the string to get an AST
            module = ast.parse(python_string)

            # Return the first node in the module
            if module.body and isinstance(module.body[0], ast.Expr):
                return module.body[0].value
            elif module.body:
                return module.body[0]
            else:
                # Fallback to a pass statement if no body
                return ast.Pass()
        except Exception as e:
            raise Exception(
                f"Failed to convert node {type(node)} using unparse: {e}"
            )

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
                    # If it's an expression, wrap it in an Expr statement
                    result.append(ast.Expr(value=converted))
                else:
                    # Fallback for unexpected types
                    result.append(ast.Pass())
            except Exception:
                # If conversion fails, skip this node and continue
                continue

        # Return at least one statement to ensure valid Python
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
    def visit(self, node: astx.BinaryOp) -> ast.BinOp:
        """Handle BinaryOp nodes."""
        if (
            not hasattr(node, "lhs")
            or not hasattr(node, "rhs")
            or not hasattr(node, "op_code")
        ):
            return self._convert_using_unparse(node)

        if node.op_code not in BINARY_OP_MAP:
            return self._convert_using_unparse(node)

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
    def visit(self, node: astx.ContinueStmt) -> ast.Continue:
        """Handle ContinueStmt nodes."""
        return ast.Continue()

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionCall) -> ast.Call:
        """Handle FunctionCall nodes."""
        if (
            not hasattr(node, "fn")
            or not hasattr(node.fn, "name")
            or not hasattr(node, "args")
        ):
            return self._convert_using_unparse(node)

        func = ast.Name(id=node.fn.name, ctx=ast.Load())
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

        # Process arguments
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

        # Process return type annotation if present
        returns = None
        if (
            hasattr(node.prototype, "return_type")
            and node.prototype.return_type
        ):
            returns = self.visit(node.prototype.return_type)

        # Process function body
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
    def visit(self, node: astx.FunctionAsyncDef) -> ast.AsyncFunctionDef:
        """Handle FunctionAsyncDef nodes."""
        if (
            not hasattr(node, "name")
            or not hasattr(node, "prototype")
            or not hasattr(node.prototype, "args")
        ):
            return self._convert_using_unparse(node)

        # Process arguments
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

        # Process return type annotation if present
        returns = None
        if (
            hasattr(node.prototype, "return_type")
            and node.prototype.return_type
        ):
            returns = self.visit(node.prototype.return_type)

        # Process function body
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
    def visit(self, node: astx.FunctionReturn) -> ast.Return:
        """Handle FunctionReturn nodes."""
        value = None
        if hasattr(node, "value") and node.value:
            value = self.visit(node.value)
        return ast.Return(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfExpr) -> ast.IfExp:
        """Handle IfExpr nodes."""
        if not hasattr(node, "condition"):
            return self._convert_using_unparse(node)

        # Handle then branch
        then_value = None
        if hasattr(node, "then") and node.then:
            if len(node.then) == 1:
                then_value = self.visit(node.then[0])
            else:
                then_value = self._convert_using_unparse(node.then)
        else:
            then_value = ast.Constant(value=None)

        # Handle else branch
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
    def visit(self, node: astx.ImportStmt) -> ast.Import:
        """Handle ImportStmt nodes."""
        if not hasattr(node, "names"):
            return ast.Import(names=[ast.alias(name="", asname=None)])

        names = [self.visit(name) for name in node.names]
        return ast.Import(names=names)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromStmt) -> ast.ImportFrom:
        """Handle ImportFromStmt nodes."""
        if not hasattr(node, "names") or not hasattr(node, "module"):
            return self._convert_using_unparse(node)

        names = [self.visit(name) for name in node.names]
        level = node.level if hasattr(node, "level") else 0

        return ast.ImportFrom(module=node.module, names=names, level=level)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralBoolean) -> ast.Constant:
        """Handle LiteralBoolean nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value=False)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt32) -> ast.Constant:
        """Handle LiteralInt32 nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value=0)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat32) -> ast.Constant:
        """Handle LiteralFloat32 nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value=0.0)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralString) -> ast.Constant:
        """Handle LiteralString nodes."""
        if not hasattr(node, "value"):
            return ast.Constant(value="")
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralList) -> ast.List:
        """Handle LiteralList nodes."""
        if not hasattr(node, "elements"):
            return ast.List(elts=[], ctx=ast.Load())
        elements = [self.visit(element) for element in node.elements]
        return ast.List(elts=elements, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTuple) -> ast.Tuple:
        """Handle LiteralTuple nodes."""
        if not hasattr(node, "elements"):
            return ast.Tuple(elts=[], ctx=ast.Load())
        elements = [self.visit(element) for element in node.elements]
        return ast.Tuple(elts=elements, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDict) -> ast.Dict:
        """Handle LiteralDict nodes."""
        if not hasattr(node, "elements"):
            return ast.Dict(keys=[], values=[])
        keys = [self.visit(key) for key in node.elements.keys()]
        values = [self.visit(value) for value in node.elements.values()]
        return ast.Dict(keys=keys, values=values)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralSet) -> ast.Set:
        """Handle LiteralSet nodes."""
        if not hasattr(node, "elements"):
            return ast.Set(elts=[])
        elements = [self.visit(element) for element in node.elements]
        return ast.Set(elts=elements)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.OrOp) -> ast.BoolOp:
        """Handle OrOp nodes."""
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        return ast.BoolOp(
            op=ast.Or(), values=[self.visit(node.lhs), self.visit(node.rhs)]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SubscriptExpr) -> ast.Subscript:
        """Handle SubscriptExpr nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)

        value = self.visit(node.value)

        # Handle simple indexing
        if hasattr(node, "index") and not isinstance(
            node.index, astx.LiteralNone
        ):
            index = self.visit(node.index)
            return ast.Subscript(value=value, slice=index, ctx=ast.Load())

        # Handle slicing
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
    def visit(self, node: astx.UnaryOp) -> ast.UnaryOp:
        """Handle UnaryOp nodes."""
        if not hasattr(node, "op_code") or not hasattr(node, "operand"):
            return self._convert_using_unparse(node)

        if node.op_code not in UNARY_OP_MAP:
            return self._convert_using_unparse(node)

        operand = self.visit(node.operand)
        return ast.UnaryOp(op=UNARY_OP_MAP[node.op_code], operand=operand)

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
    def visit(self, node: astx.YieldExpr) -> ast.Yield:
        """Handle YieldExpr nodes."""
        value = None
        if hasattr(node, "value") and node.value:
            value = self.visit(node.value)
        return ast.Yield(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldStmt) -> ast.Expr:
        """Handle YieldStmt nodes."""
        value = None
        if hasattr(node, "value") and node.value:
            value = self.visit(node.value)
        yield_expr = ast.Yield(value=value)
        return ast.Expr(value=yield_expr)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldFromExpr) -> ast.YieldFrom:
        """Handle YieldFromExpr nodes."""
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        value = self.visit(node.value)
        return ast.YieldFrom(value=value)

    # For nodes that aren't directly implemented, use the unparse approach
    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AST) -> ast.AST:
        """Handle any other AST nodes by using unparse."""
        return self._convert_using_unparse(node)
