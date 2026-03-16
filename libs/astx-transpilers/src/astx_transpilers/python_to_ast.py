"""
title: ASTx to Python AST transpiler.
"""

import ast
import sys

from typing import Any, Optional

import astx

from astx.tools.typing import typechecked
from plum import dispatch

# Python 3.10+ compatibility for match statements
if sys.version_info >= (3, 10):
    match_case = ast.match_case
    Match = ast.Match
else:
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
    title: Transpiler that converts ASTx nodes to Python AST nodes.
    summary: |-

      Notes
      -----
      Please keep the visit method in alphabet order according to the node
      type.
      The visit method for astx.AST should be the first one.
    attributes:
      indent_level:
        type: int
    """

    indent_level: int

    def __init__(self) -> None:
        """
        title: Initialize the transpiler.
        """
        self.indent_level = 0

    def _convert_using_unparse(self, node: astx.AST) -> ast.AST:
        """
        title: Convert an ASTx node to a Python AST node using fallback.
        parameters:
          node:
            type: astx.AST
        returns:
          type: ast.AST
        """
        try:
            # Simple fallback without circular import
            if hasattr(node, "value"):
                return ast.Constant(value=str(node.value))
            elif hasattr(node, "name"):
                return ast.Name(id=str(node.name), ctx=ast.Load())
            else:
                return ast.Constant(value=f"<{type(node).__name__}>")
        except Exception:
            return ast.Constant(value=f"<{type(node).__name__}>")

    def _convert_block(
        self, block: Optional[astx.ASTNodes | astx.Block]
    ) -> list[ast.stmt]:
        """
        title: Convert a block of statements to Python AST nodes.
        parameters:
          block:
            type: Optional[astx.ASTNodes | astx.Block]
        returns:
          type: list[ast.stmt]
        """
        if not block:
            return [ast.Pass()]

        if not hasattr(block, "nodes"):
            return [ast.Pass()]

        result = []
        for astx_node in block.nodes:
            try:
                converted = self.visit(astx_node)
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
        """
        title: Translate an ASTx node to a Python AST node.
        parameters:
          expr:
            type: astx.AST
        returns:
          type: ast.AST
        """
        raise Exception(f"Not implemented yet ({expr}).")

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AliasExpr) -> ast.alias:
        """
        title: Handle AliasExpr nodes.
        parameters:
          node:
            type: astx.AliasExpr
        returns:
          type: ast.alias
        """
        if not hasattr(node, "name"):
            return ast.alias(name="", asname=None)
        return ast.alias(
            name=node.name,
            asname=node.asname if hasattr(node, "asname") else None,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AndOp) -> ast.BoolOp:
        """
        title: Handle AndOp nodes.
        parameters:
          node:
            type: astx.AndOp
        returns:
          type: ast.BoolOp
        """
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        return ast.BoolOp(
            op=ast.And(), values=[self.visit(node.lhs), self.visit(node.rhs)]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Argument) -> ast.arg:
        """
        title: Handle Argument nodes.
        parameters:
          node:
            type: astx.Argument
        returns:
          type: ast.arg
        """
        if not hasattr(node, "name"):
            return self._convert_using_unparse(node)
        annotation = None
        if hasattr(node, "type_") and node.type_:
            annotation = self.visit(node.type_)
        return ast.arg(arg=node.name, annotation=annotation)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Arguments) -> ast.arguments:
        """
        title: Handle Arguments nodes.
        parameters:
          node:
            type: astx.Arguments
        returns:
          type: ast.arguments
        """
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
        """
        title: Handle AssignmentExpr nodes.
        parameters:
          node:
            type: astx.AssignmentExpr
        returns:
          type: ast.Assign
        """
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
    def visit(self, node: astx.ASTNodes) -> list[ast.AST]:
        """
        title: Handle ASTNodes nodes.
        parameters:
          node:
            type: astx.ASTNodes
        returns:
          type: list[ast.AST]
        """
        if not hasattr(node, "nodes"):
            return [self._convert_using_unparse(node)]
        return [self.visit(n) for n in node.nodes]

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AsyncForRangeLoopExpr) -> ast.ListComp:
        """
        title: Handle AsyncForRangeLoopExpr nodes.
        parameters:
          node:
            type: astx.AsyncForRangeLoopExpr
        returns:
          type: ast.ListComp
        """
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
        """
        title: Handle AugAssign nodes.
        parameters:
          node:
            type: astx.AugAssign
        returns:
          type: ast.AugAssign
        """
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
        """
        title: Handle AwaitExpr nodes.
        parameters:
          node:
            type: astx.AwaitExpr
        returns:
          type: ast.Await
        """
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        value = self.visit(node.value)
        return ast.Await(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BinaryOp) -> ast.BinOp | ast.Call:
        """
        title: Handle BinaryOp nodes.
        parameters:
          node:
            type: astx.BinaryOp
        returns:
          type: ast.BinOp | ast.Call
        """
        if (
            not hasattr(node, "lhs")
            or not hasattr(node, "rhs")
            or not hasattr(node, "op_code")
        ):
            return self._convert_using_unparse(node)

        if node.op_code not in BINARY_OP_MAP:
            lhs = self.visit(node.lhs)
            rhs = self.visit(node.rhs)
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
        binop = ast.BinOp(left=lhs, op=BINARY_OP_MAP[node.op_code], right=rhs)
        return binop

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Block) -> list[ast.stmt]:
        """
        title: Handle Block nodes.
        parameters:
          node:
            type: astx.Block
        returns:
          type: list[ast.stmt]
        """
        return self._convert_block(node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BreakStmt) -> ast.Break:
        """
        title: Handle BreakStmt nodes.
        parameters:
          node:
            type: astx.BreakStmt
        returns:
          type: ast.Break
        """
        return ast.Break()

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CaseStmt) -> Any:
        """
        title: Handle CaseStmt nodes - Python 3.10+ only.
        parameters:
          node:
            type: astx.CaseStmt
        returns:
          type: Any
        """
        if sys.version_info < (3, 10):
            raise NotImplementedError(
                "CaseStmt requires Python 3.10 or higher"
            )

        if not hasattr(node, "condition"):
            return self._convert_using_unparse(node)

        pattern = (
            ast.MatchAs(name=None, pattern=None)
            if node.condition is None
            else self.visit(node.condition)
        )
        body = (
            self._convert_block(node.body)
            if hasattr(node, "body")
            else [ast.Pass()]
        )

        return ast.match_case(pattern=pattern, guard=None, body=body)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CatchHandlerStmt) -> ast.ExceptHandler:
        """
        title: Handle CatchHandlerStmt nodes.
        parameters:
          node:
            type: astx.CatchHandlerStmt
        returns:
          type: ast.ExceptHandler
        """
        type_ = None
        if hasattr(node, "types") and node.types:
            type_ = self.visit(node.types[0])
        name = None
        if hasattr(node, "name") and node.name:
            if hasattr(node.name, "name"):
                name = node.name.name
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
        """
        title: Handle ClassDefStmt nodes.
        parameters:
          node:
            type: astx.ClassDefStmt
        returns:
          type: ast.ClassDef
        """
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
        """
        title: Handle CompareOp nodes.
        parameters:
          node:
            type: astx.CompareOp
        returns:
          type: ast.Compare
        """
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
        """
        title: Handle ComprehensionClause nodes.
        parameters:
          node:
            type: astx.ComprehensionClause
        returns:
          type: ast.comprehension
        """
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
    def visit(self, node: astx.ContinueStmt) -> ast.Continue:
        """
        title: Handle ContinueStmt nodes.
        parameters:
          node:
            type: astx.ContinueStmt
        returns:
          type: ast.Continue
        """
        return ast.Continue()

    @dispatch  # type: ignore[no-redef]
    def visit(
        self, node: astx.Int8 | astx.Int16 | astx.Int32 | astx.Int64
    ) -> ast.Name:
        """
        title: Handle all integer type nodes.
        parameters:
          node:
            type: astx.Int8 | astx.Int16 | astx.Int32 | astx.Int64
        returns:
          type: ast.Name
        """
        return ast.Name(id="int", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(
        self,
        node: astx.UInt8
        | astx.UInt16
        | astx.UInt32
        | astx.UInt64
        | astx.UInt128,
    ) -> ast.Name:
        """
        title: Handle all unsigned integer type nodes.
        parameters:
          node:
            type: >-
              astx.UInt8 | astx.UInt16 | astx.UInt32 | astx.UInt64 |
              astx.UInt128
        returns:
          type: ast.Name
        """
        return ast.Name(id="int", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(
        self, node: astx.Float16 | astx.Float32 | astx.Float64
    ) -> ast.Name:
        """
        title: Handle all float type nodes.
        parameters:
          node:
            type: astx.Float16 | astx.Float32 | astx.Float64
        returns:
          type: ast.Name
        """
        return ast.Name(id="float", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Complex32 | astx.Complex64) -> ast.Name:
        """
        title: Handle all complex type nodes.
        parameters:
          node:
            type: astx.Complex32 | astx.Complex64
        returns:
          type: ast.Name
        """
        return ast.Name(id="complex", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UTF8Char | astx.UTF8String) -> ast.Name:
        """
        title: Handle UTF8 string type nodes.
        parameters:
          node:
            type: astx.UTF8Char | astx.UTF8String
        returns:
          type: ast.Name
        """
        return ast.Name(id="str", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(
        self, node: astx.Date | astx.DateTime | astx.Time | astx.Timestamp
    ) -> ast.Name:
        """
        title: Handle all datetime type nodes.
        parameters:
          node:
            type: astx.Date | astx.DateTime | astx.Time | astx.Timestamp
        returns:
          type: ast.Name
        """
        type_mapping = {
            "Date": "date",
            "DateTime": "datetime",
            "Time": "time",
            "Timestamp": "timestamp",
        }
        type_name = type_mapping.get(type(node).__name__, "datetime")
        return ast.Name(id=type_name, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DataType) -> ast.Name:
        """
        title: Handle DataType nodes.
        parameters:
          node:
            type: astx.DataType
        returns:
          type: ast.Name
        """
        if hasattr(node, "id") and node.id:
            type_id = node.id
        else:
            type_id = "object"
        return ast.Name(id=type_id, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DeleteStmt) -> ast.Delete:
        """
        title: Handle DeleteStmt nodes.
        parameters:
          node:
            type: astx.DeleteStmt
        returns:
          type: ast.Delete
        """
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        targets = [self.visit(target) for target in node.value]
        return ast.Delete(targets=targets)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DoWhileExpr) -> ast.ListComp:
        """
        title: Handle DoWhileExpr nodes.
        parameters:
          node:
            type: astx.DoWhileExpr
        returns:
          type: ast.ListComp
        """
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
        """
        title: Handle DoWhileStmt nodes.
        parameters:
          node:
            type: astx.DoWhileStmt
        returns:
          type: ast.While
        """
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
        """
        title: Handle Ellipsis nodes.
        parameters:
          node:
            type: astx.Ellipsis
        returns:
          type: ast.Constant
        """
        return ast.Constant(value=...)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.EnumDeclStmt) -> ast.ClassDef:
        """
        title: Handle EnumDeclStmt nodes.
        parameters:
          node:
            type: astx.EnumDeclStmt
        returns:
          type: ast.ClassDef
        """
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
        """
        title: Handle ExceptionHandlerStmt nodes.
        parameters:
          node:
            type: astx.ExceptionHandlerStmt
        returns:
          type: ast.Try
        """
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
        """
        title: Handle FinallyHandlerStmt nodes.
        parameters:
          node:
            type: astx.FinallyHandlerStmt
        returns:
          type: ast.Try
        """
        if not hasattr(node, "body"):
            return self._convert_using_unparse(node)

        finalbody = self._convert_block(node.body)

        return ast.Try(
            body=[ast.Pass()], handlers=[], orelse=[], finalbody=finalbody
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ForCountLoopStmt) -> ast.For:
        """
        title: Handle ForCountLoopStmt nodes.
        parameters:
          node:
            type: astx.ForCountLoopStmt
        returns:
          type: ast.For
        """
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
        """
        title: Handle ForRangeLoopExpr nodes.
        parameters:
          node:
            type: astx.ForRangeLoopExpr
        returns:
          type: ast.ListComp
        """
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
        """
        title: Handle ForRangeLoopStmt nodes.
        parameters:
          node:
            type: astx.ForRangeLoopStmt
        returns:
          type: ast.For
        """
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
        """
        title: Handle FunctionAsyncDef nodes.
        parameters:
          node:
            type: astx.FunctionAsyncDef
        returns:
          type: ast.AsyncFunctionDef
        """
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
        """
        title: Handle FunctionCall nodes.
        parameters:
          node:
            type: astx.FunctionCall
        returns:
          type: ast.Call
        """
        if not hasattr(node, "fn"):
            return ast.Call(
                func=ast.Name(id="unknown_function", ctx=ast.Load()),
                args=[],
                keywords=[],
            )

        if hasattr(node.fn, "prototype") and hasattr(
            node.fn.prototype, "name"
        ):
            func = ast.Name(id=node.fn.prototype.name, ctx=ast.Load())
        elif hasattr(node.fn, "name"):
            func = ast.Name(id=node.fn.name, ctx=ast.Load())
        elif isinstance(node.fn, str):
            func = ast.Name(id=node.fn, ctx=ast.Load())
        else:
            try:
                visited_fn = self.visit(node.fn)
                if isinstance(visited_fn, (ast.Name, ast.Attribute)):
                    func = visited_fn
                else:
                    func = ast.Name(id="unknown_function", ctx=ast.Load())
            except Exception:
                func = ast.Name(id="unknown_function", ctx=ast.Load())

        args = []
        if hasattr(node, "args") and node.args:
            args = [self.visit(arg) for arg in node.args]

        return ast.Call(func=func, args=args, keywords=[])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionDef) -> ast.FunctionDef:
        """
        title: Handle FunctionDef nodes.
        parameters:
          node:
            type: astx.FunctionDef
        returns:
          type: ast.FunctionDef
        """
        if not hasattr(node, "prototype"):
            return self._convert_using_unparse(node)

        args = self.visit(node.prototype.args)
        returns = (
            self.visit(node.prototype.return_type)
            if hasattr(node.prototype, "return_type")
            and node.prototype.return_type
            else None
        )
        body = self._convert_block(node.body)

        func_def = ast.FunctionDef(
            name=node.prototype.name,
            args=args,
            body=body,
            decorator_list=[],
            returns=returns,
        )

        # Ensure all required attributes are set
        func_def.lineno = 1
        func_def.col_offset = 0
        func_def.end_lineno = 1
        func_def.end_col_offset = 0

        # Set attributes on args as well
        if hasattr(args, "args"):
            for i, arg in enumerate(args.args):
                arg.lineno = 1
                arg.col_offset = 0
                arg.end_lineno = 1
                arg.end_col_offset = 0

        return func_def

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionPrototype) -> ast.FunctionDef:
        """
        title: Handle FunctionPrototype nodes.
        parameters:
          node:
            type: astx.FunctionPrototype
        returns:
          type: ast.FunctionDef
        """
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
        """
        title: Handle FunctionReturn nodes.
        parameters:
          node:
            type: astx.FunctionReturn
        returns:
          type: ast.Return
        """
        value = None
        if hasattr(node, "value") and node.value:
            value = self.visit(node.value)
        return ast.Return(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.GeneratorExpr) -> ast.GeneratorExp:
        """
        title: Handle GeneratorExpr nodes.
        parameters:
          node:
            type: astx.GeneratorExpr
        returns:
          type: ast.GeneratorExp
        """
        if not hasattr(node, "element") or not hasattr(node, "generators"):
            return self._convert_using_unparse(node)
        element = self.visit(node.element)
        generators = [self.visit(gen) for gen in node.generators]
        return ast.GeneratorExp(elt=element, generators=generators)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Identifier) -> ast.Name:
        """
        title: Handle Identifier nodes.
        parameters:
          node:
            type: astx.Identifier
        returns:
          type: ast.Name
        """
        # Get the identifier name from the node
        if hasattr(node, "name"):
            identifier_name = node.name
        elif hasattr(node, "id"):
            identifier_name = node.id
        elif hasattr(node, "value"):
            identifier_name = str(node.value)
        else:
            for attr_name in ["_name", "identifier", "token"]:
                if hasattr(node, attr_name):
                    identifier_name = getattr(node, attr_name)
                    break
            else:
                identifier_name = "unknown_identifier"

        return ast.Name(id=str(identifier_name), ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfExpr) -> ast.IfExp:
        """
        title: Handle IfExpr nodes.
        parameters:
          node:
            type: astx.IfExpr
        returns:
          type: ast.IfExp
        """
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
        """
        title: Handle IfStmt nodes.
        parameters:
          node:
            type: astx.IfStmt
        returns:
          type: ast.If
        """
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
        """
        title: Handle ImportExpr nodes.
        parameters:
          node:
            type: astx.ImportExpr
        returns:
          type: ast.Assign
        """
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
        """
        title: Handle ImportFromExpr nodes.
        parameters:
          node:
            type: astx.ImportFromExpr
        returns:
          type: ast.Assign
        """
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
        """
        title: Handle ImportFromStmt nodes.
        parameters:
          node:
            type: astx.ImportFromStmt
        returns:
          type: ast.ImportFrom
        """
        if not hasattr(node, "names") or not hasattr(node, "module"):
            return self._convert_using_unparse(node)
        names = [self.visit(name) for name in node.names]
        level = node.level if hasattr(node, "level") else 0
        return ast.ImportFrom(module=node.module, names=names, level=level)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportStmt) -> ast.Import:
        """
        title: Handle ImportStmt nodes.
        parameters:
          node:
            type: astx.ImportStmt
        returns:
          type: ast.Import
        """
        if not hasattr(node, "names"):
            return ast.Import(names=[ast.alias(name="", asname=None)])
        names = [self.visit(name) for name in node.names]
        return ast.Import(names=names)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.InlineVariableDeclaration) -> ast.AnnAssign:
        """
        title: Handle InlineVariableDeclaration nodes.
        parameters:
          node:
            type: astx.InlineVariableDeclaration
        returns:
          type: ast.AnnAssign
        """
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
    def visit(self, node: astx.LambdaExpr) -> ast.Lambda:
        """
        title: Handle LambdaExpr nodes.
        parameters:
          node:
            type: astx.LambdaExpr
        returns:
          type: ast.Lambda
        """
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
        """
        title: Handle ListComprehension nodes.
        parameters:
          node:
            type: astx.ListComprehension
        returns:
          type: ast.ListComp
        """
        if not hasattr(node, "element") or not hasattr(node, "generators"):
            return self._convert_using_unparse(node)
        element = self.visit(node.element)
        generators = [self.visit(gen) for gen in node.generators]
        return ast.ListComp(elt=element, generators=generators)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralBoolean) -> ast.Constant:
        """
        title: Handle LiteralBoolean nodes.
        parameters:
          node:
            type: astx.LiteralBoolean
        returns:
          type: ast.Constant
        """
        if not hasattr(node, "value"):
            return ast.Constant(value=False)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(
        self,
        node: astx.LiteralInt8
        | astx.LiteralInt16
        | astx.LiteralInt32
        | astx.LiteralInt64
        | astx.LiteralInt128,
    ) -> ast.Constant:
        """
        title: Handle all integer literal nodes.
        parameters:
          node:
            type: >-
              astx.LiteralInt8 | astx.LiteralInt16 | astx.LiteralInt32 |
              astx.LiteralInt64 | astx.LiteralInt128
        returns:
          type: ast.Constant
        """
        if not hasattr(node, "value"):
            return ast.Constant(value=0)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(
        self,
        node: astx.LiteralUInt8
        | astx.LiteralUInt16
        | astx.LiteralUInt32
        | astx.LiteralUInt64
        | astx.LiteralUInt128,
    ) -> ast.Constant:
        """
        title: Handle all unsigned integer literal nodes.
        parameters:
          node:
            type: >-
              astx.LiteralUInt8 | astx.LiteralUInt16 | astx.LiteralUInt32 |
              astx.LiteralUInt64 | astx.LiteralUInt128
        returns:
          type: ast.Constant
        """
        if not hasattr(node, "value"):
            return ast.Constant(value=0)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(
        self,
        node: astx.LiteralFloat16 | astx.LiteralFloat32 | astx.LiteralFloat64,
    ) -> ast.Constant:
        """
        title: Handle all float literal nodes.
        parameters:
          node:
            type: >-
              astx.LiteralFloat16 | astx.LiteralFloat32 | astx.LiteralFloat64
        returns:
          type: ast.Constant
        """
        if not hasattr(node, "value"):
            return ast.Constant(value=0.0)
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(
        self, node: astx.LiteralComplex32 | astx.LiteralComplex64
    ) -> ast.Call:
        """
        title: Handle all complex literal nodes.
        parameters:
          node:
            type: astx.LiteralComplex32 | astx.LiteralComplex64
        returns:
          type: ast.Call
        """
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
    def visit(
        self, node: astx.LiteralUTF8Char | astx.LiteralUTF8String
    ) -> ast.Constant:
        """
        title: Handle UTF8 string literal nodes.
        parameters:
          node:
            type: astx.LiteralUTF8Char | astx.LiteralUTF8String
        returns:
          type: ast.Constant
        """
        if not hasattr(node, "value"):
            return ast.Constant(value="")
        return ast.Constant(value=str(node.value))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDate) -> ast.Call:
        """
        title: Handle LiteralDate nodes.
        parameters:
          node:
            type: astx.LiteralDate
        returns:
          type: ast.Call
        """
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
    def visit(self, node: astx.LiteralDateTime) -> ast.Name:
        """
        title: Handle LiteralDateTime nodes.
        parameters:
          node:
            type: astx.LiteralDateTime
        returns:
          type: ast.Name
        """
        return ast.Name(id="datetime", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTime) -> ast.Name:
        """
        title: Handle LiteralTime nodes.
        parameters:
          node:
            type: astx.LiteralTime
        returns:
          type: ast.Name
        """
        return ast.Name(id="time", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTimestamp) -> ast.Name:
        """
        title: Handle LiteralTimestamp nodes.
        parameters:
          node:
            type: astx.LiteralTimestamp
        returns:
          type: ast.Name
        """
        return ast.Name(id="timestamp", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex) -> ast.Name:
        """
        title: Handle LiteralComplex nodes.
        parameters:
          node:
            type: astx.LiteralComplex
        returns:
          type: ast.Name
        """
        return ast.Name(id="complex", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDict) -> ast.Dict:
        """
        title: Handle LiteralDict nodes.
        parameters:
          node:
            type: astx.LiteralDict
        returns:
          type: ast.Dict
        """
        if not hasattr(node, "elements"):
            return ast.Dict(keys=[], values=[])
        keys = [self.visit(key) for key in node.elements.keys()]
        values = [self.visit(value) for value in node.elements.values()]
        return ast.Dict(keys=keys, values=values)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralList) -> ast.List:
        """
        title: Handle LiteralList nodes.
        parameters:
          node:
            type: astx.LiteralList
        returns:
          type: ast.List
        """
        if not hasattr(node, "elements"):
            return ast.List(elts=[], ctx=ast.Load())
        elements = [self.visit(element) for element in node.elements]
        return ast.List(elts=elements, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralNone) -> ast.Constant:
        """
        title: Handle LiteralNone nodes.
        parameters:
          node:
            type: astx.LiteralNone
        returns:
          type: ast.Constant
        """
        return ast.Constant(value=None)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralSet) -> ast.Set:
        """
        title: Handle LiteralSet nodes.
        parameters:
          node:
            type: astx.LiteralSet
        returns:
          type: ast.Set
        """
        if not hasattr(node, "elements"):
            return ast.Set(elts=[])
        elements = [self.visit(element) for element in node.elements]
        return ast.Set(elts=elements)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralString) -> ast.Constant:
        """
        title: Handle LiteralString nodes.
        parameters:
          node:
            type: astx.LiteralString
        returns:
          type: ast.Constant
        """
        if not hasattr(node, "value"):
            return ast.Constant(value="")
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTuple) -> ast.Tuple:
        """
        title: Handle LiteralTuple nodes.
        parameters:
          node:
            type: astx.LiteralTuple
        returns:
          type: ast.Tuple
        """
        if not hasattr(node, "elements"):
            return ast.Tuple(elts=[], ctx=ast.Load())
        elements = [self.visit(element) for element in node.elements]
        return ast.Tuple(elts=elements, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Module) -> ast.Module:
        """
        title: Handle Module nodes.
        parameters:
          node:
            type: astx.Module
        returns:
          type: ast.Module
        """
        if not hasattr(node, "body"):
            return ast.Module(body=[ast.Pass()], type_ignores=[])

        body = self._convert_block(node.body)
        return ast.Module(body=body, type_ignores=[])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NandOp) -> ast.UnaryOp:
        """
        title: Handle NandOp nodes.
        parameters:
          node:
            type: astx.NandOp
        returns:
          type: ast.UnaryOp
        """
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)

        and_op = ast.BoolOp(op=ast.And(), values=[lhs, rhs])
        return ast.UnaryOp(op=ast.Not(), operand=and_op)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NorOp) -> ast.UnaryOp:
        """
        title: Handle NorOp nodes.
        parameters:
          node:
            type: astx.NorOp
        returns:
          type: ast.UnaryOp
        """
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)

        or_op = ast.BoolOp(op=ast.Or(), values=[lhs, rhs])
        return ast.UnaryOp(op=ast.Not(), operand=or_op)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NotOp) -> ast.UnaryOp:
        """
        title: Handle NotOp nodes.
        parameters:
          node:
            type: astx.NotOp
        returns:
          type: ast.UnaryOp
        """
        if not hasattr(node, "operand"):
            return self._convert_using_unparse(node)

        operand = self.visit(node.operand)
        return ast.UnaryOp(op=ast.Not(), operand=operand)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.OrOp) -> ast.BoolOp:
        """
        title: Handle OrOp nodes.
        parameters:
          node:
            type: astx.OrOp
        returns:
          type: ast.BoolOp
        """
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        return ast.BoolOp(
            op=ast.Or(), values=[self.visit(node.lhs), self.visit(node.rhs)]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ParenthesizedExpr) -> ast.AST:
        """
        title: Handle ParenthesizedExpr nodes.
        parameters:
          node:
            type: astx.ParenthesizedExpr
        returns:
          type: ast.AST
        """
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        return self.visit(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SetComprehension) -> ast.SetComp:
        """
        title: Handle SetComprehension nodes.
        parameters:
          node:
            type: astx.SetComprehension
        returns:
          type: ast.SetComp
        """
        if not hasattr(node, "element") or not hasattr(node, "generators"):
            return self._convert_using_unparse(node)
        element = self.visit(node.element)
        generators = [self.visit(gen) for gen in node.generators]
        return ast.SetComp(elt=element, generators=generators)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Starred) -> ast.Starred:
        """
        title: Handle Starred nodes.
        parameters:
          node:
            type: astx.Starred
        returns:
          type: ast.Starred
        """
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)

        value = self.visit(node.value)
        return ast.Starred(value=value, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.StructDeclStmt) -> ast.ClassDef:
        """
        title: Handle StructDeclStmt nodes.
        parameters:
          node:
            type: astx.StructDeclStmt
        returns:
          type: ast.ClassDef
        """
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
        """
        title: Handle StructDefStmt nodes.
        parameters:
          node:
            type: astx.StructDefStmt
        returns:
          type: ast.ClassDef
        """
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
        """
        title: Handle SwitchStmt nodes - Python 3.10+ only.
        parameters:
          node:
            type: astx.SwitchStmt
        returns:
          type: Any
        """
        if sys.version_info < (3, 10):
            raise NotImplementedError(
                "SwitchStmt requires Python 3.10 or higher"
            )

        if not hasattr(node, "value") or not hasattr(node, "cases"):
            return self._convert_using_unparse(node)

        subject = self.visit(node.value)
        cases = (
            [self.visit(case) for case in node.cases.nodes]
            if hasattr(node.cases, "nodes")
            else []
        )

        return ast.Match(subject=subject, cases=cases)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SubscriptExpr) -> ast.Subscript:
        """
        title: Handle SubscriptExpr nodes.
        parameters:
          node:
            type: astx.SubscriptExpr
        returns:
          type: ast.Subscript
        """
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
    def visit(self, node: astx.ThrowStmt) -> ast.Raise:
        """
        title: Handle ThrowStmt nodes.
        parameters:
          node:
            type: astx.ThrowStmt
        returns:
          type: ast.Raise
        """
        exc = None
        if hasattr(node, "exception") and node.exception:
            try:
                if hasattr(node.exception, "fn"):
                    if hasattr(node.exception.fn, "prototype") and hasattr(
                        node.exception.fn.prototype, "name"
                    ):
                        func_name = node.exception.fn.prototype.name
                        args = []
                        if (
                            hasattr(node.exception, "args")
                            and node.exception.args
                        ):
                            args = [
                                self.visit(arg) for arg in node.exception.args
                            ]
                        exc = ast.Call(
                            func=ast.Name(id=func_name, ctx=ast.Load()),
                            args=args,
                            keywords=[],
                        )
                    elif hasattr(node.exception.fn, "name"):
                        func_name = node.exception.fn.name
                        args = []
                        if (
                            hasattr(node.exception, "args")
                            and node.exception.args
                        ):
                            args = [
                                self.visit(arg) for arg in node.exception.args
                            ]
                        exc = ast.Call(
                            func=ast.Name(id=func_name, ctx=ast.Load()),
                            args=args,
                            keywords=[],
                        )
                    else:
                        exc_node = self.visit(node.exception)
                        if isinstance(exc_node, ast.Call):
                            exc = exc_node
                        elif isinstance(exc_node, ast.Name):
                            exc = ast.Call(func=exc_node, args=[], keywords=[])
                        else:
                            exc = ast.Call(
                                func=ast.Name(id="Exception", ctx=ast.Load()),
                                args=[ast.Constant(value="Unknown exception")],
                                keywords=[],
                            )
                else:
                    exc_node = self.visit(node.exception)
                    if isinstance(exc_node, ast.Call):
                        exc = exc_node
                    elif isinstance(exc_node, ast.Name):
                        exc = ast.Call(func=exc_node, args=[], keywords=[])
                    else:
                        exc = ast.Call(
                            func=ast.Name(id="Exception", ctx=ast.Load()),
                            args=[ast.Constant(value="Unknown exception")],
                            keywords=[],
                        )
            except Exception:
                exc = ast.Call(
                    func=ast.Name(id="Exception", ctx=ast.Load()),
                    args=[ast.Constant(value="Unknown exception")],
                    keywords=[],
                )
        else:
            exc = None

        return ast.Raise(exc=exc, cause=None)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.TypeCastExpr) -> ast.Call:
        """
        title: Handle TypeCastExpr nodes.
        parameters:
          node:
            type: astx.TypeCastExpr
        returns:
          type: ast.Call
        """
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
        """
        title: Handle UnaryOp nodes.
        parameters:
          node:
            type: astx.UnaryOp
        returns:
          type: ast.UnaryOp
        """
        if not hasattr(node, "op_code") or not hasattr(node, "operand"):
            return self._convert_using_unparse(node)
        if node.op_code not in UNARY_OP_MAP:
            return self._convert_using_unparse(node)
        operand = self.visit(node.operand)
        return ast.UnaryOp(op=UNARY_OP_MAP[node.op_code], operand=operand)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Variable) -> ast.Name:
        """
        title: Handle Variable nodes.
        parameters:
          node:
            type: astx.Variable
        returns:
          type: ast.Name
        """
        if not hasattr(node, "name"):
            return ast.Name(id="undefined", ctx=ast.Load())
        return ast.Name(id=node.name, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableAssignment) -> ast.Assign:
        """
        title: Handle VariableAssignment nodes.
        parameters:
          node:
            type: astx.VariableAssignment
        returns:
          type: ast.Assign
        """
        if not hasattr(node, "name") or not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        target = ast.Name(id=node.name, ctx=ast.Store())
        value = self.visit(node.value)
        return ast.Assign(targets=[target], value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableDeclaration) -> ast.AnnAssign:
        """
        title: Handle VariableDeclaration nodes.
        parameters:
          node:
            type: astx.VariableDeclaration
        returns:
          type: ast.AnnAssign
        """
        if not hasattr(node, "name"):
            return self._convert_using_unparse(node)

        target = ast.Name(id=node.name, ctx=ast.Store())
        annotation = None
        if hasattr(node, "type_") and node.type_:
            annotation = self.visit(node.type_)
        elif hasattr(node, "type") and node.type:
            annotation = self.visit(node.type)
        else:
            annotation = ast.Name(id="object", ctx=ast.Load())

        if not isinstance(
            annotation, (ast.Name, ast.Attribute, ast.Subscript)
        ):
            annotation = ast.Name(id="object", ctx=ast.Load())

        value = None
        if hasattr(node, "value") and node.value is not None:
            value = self.visit(node.value)

        return ast.AnnAssign(
            target=target,
            annotation=annotation,
            value=value,
            simple=1,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WalrusOp) -> ast.NamedExpr:
        """
        title: Handle WalrusOp nodes.
        parameters:
          node:
            type: astx.WalrusOp
        returns:
          type: ast.NamedExpr
        """
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        target = self.visit(node.lhs)
        if isinstance(target, ast.Name):
            target.ctx = ast.Store()
        value = self.visit(node.rhs)
        return ast.NamedExpr(target=target, value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileExpr) -> ast.ListComp:
        """
        title: Handle WhileExpr nodes.
        parameters:
          node:
            type: astx.WhileExpr
        returns:
          type: ast.ListComp
        """
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
        """
        title: Handle WhileStmt nodes.
        parameters:
          node:
            type: astx.WhileStmt
        returns:
          type: ast.While
        """
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
        """
        title: Handle XnorOp nodes.
        parameters:
          node:
            type: astx.XnorOp
        returns:
          type: ast.UnaryOp
        """
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        xor_op = ast.BinOp(left=lhs, op=ast.BitXor(), right=rhs)
        return ast.UnaryOp(op=ast.Not(), operand=xor_op)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.XorOp) -> ast.BinOp:
        """
        title: Handle XorOp nodes.
        parameters:
          node:
            type: astx.XorOp
        returns:
          type: ast.BinOp
        """
        if not hasattr(node, "lhs") or not hasattr(node, "rhs"):
            return self._convert_using_unparse(node)
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return ast.BinOp(left=lhs, op=ast.BitXor(), right=rhs)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldExpr) -> ast.Yield:
        """
        title: Handle YieldExpr nodes.
        parameters:
          node:
            type: astx.YieldExpr
        returns:
          type: ast.Yield
        """
        value = None
        if hasattr(node, "value") and node.value:
            value = self.visit(node.value)
        return ast.Yield(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldFromExpr) -> ast.YieldFrom:
        """
        title: Handle YieldFromExpr nodes.
        parameters:
          node:
            type: astx.YieldFromExpr
        returns:
          type: ast.YieldFrom
        """
        if not hasattr(node, "value"):
            return self._convert_using_unparse(node)
        value = self.visit(node.value)
        return ast.YieldFrom(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldStmt) -> ast.Expr:
        """
        title: Handle YieldStmt nodes.
        parameters:
          node:
            type: astx.YieldStmt
        returns:
          type: ast.Expr
        """
        value = None
        if hasattr(node, "value") and node.value:
            value = self.visit(node.value)
        yield_expr = ast.Yield(value=value)
        return ast.Expr(value=yield_expr)
