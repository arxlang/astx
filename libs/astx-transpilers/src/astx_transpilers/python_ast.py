# libs/astx-transpilers/src/astx_transpilers/python_ast.py
"""Transpiler from ASTx to Python AST."""

import ast
import sys

# Conditional import for pattern matching types
if sys.version_info >= (3, 10):
    # Use real types if available
    from ast import (
        Match as ast_Match,
        match_case as ast_match_case,
        pattern as ast_pattern,
    )
else:
    # Use Any as placeholder for type hints on older versions
    from typing import Any

    ast_pattern = Any
    ast_match_case = Any
    ast_Match = Any


from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from plum import dispatch

import astx
import astx.operators
from astx.datatypes import DataType, Void  # Corrected import path
from astx.literals import Literal, LiteralNone
from astx.tools.typing import typechecked
from astx.variables import InlineVariableDeclaration

# Import the STRING transpiler specifically if needed for comparison methods
from astx_transpilers.python_string import ASTxPythonTranspiler


# Define match_case and Match types for Python versions < 3.10
if sys.version_info < (3, 10):
    if not hasattr(ast, "match_case"):

        class MatchCase:
            """Stub for match_case in Python < 3.10."""

            def __init__(
                self, pattern: Any, guard: Optional[Any], body: List[Any]
            ) -> None:
                self.pattern = pattern
                self.guard = guard
                self.body = body

        # Assign stub only if it doesn't exist
        ast.match_case = MatchCase  # type: ignore[misc, assignment]

    if not hasattr(ast, "Match"):

        class Match(ast.stmt):
            """Stub for Match in Python < 3.10."""

            def __init__(self, subject: Any, cases: List[Any]) -> None:
                self.subject = subject
                self.cases = cases

        # Assign stub only if it doesn't exist
        ast.Match = Match  # type: ignore[misc, assignment]


@typechecked
class ASTxPythonASTTranspiler:
    """
    Transpile ASTx nodes to Python AST nodes.

    Enables integration with Python-based tools, static analysis, compilers.
    """

    def __init__(self) -> None:
        self.scope_stack: List[Dict[str, bool]] = []
        self.current_scope: Dict[str, bool] = {}

    def _enter_scope(self) -> None:
        """Enter a new scope level."""
        self.scope_stack.append(self.current_scope)
        self.current_scope = {}

    def _exit_scope(self) -> None:
        """Exit the current scope level."""
        if self.scope_stack:
            self.current_scope = self.scope_stack.pop()
        else:
            self.current_scope = {}

    @dispatch.abstract
    def visit(self, expr: astx.AST) -> ast.AST:
        """Translate an ASTx expression to Python AST."""
        raise NotImplementedError(
            f"AST visit not implemented for type {type(expr).__name__}"
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AliasExpr) -> ast.alias:
        """Convert AliasExpr."""
        return ast.alias(name=node.name, asname=node.asname)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Argument) -> ast.arg:
        """Convert Argument."""
        type_annotation_node: Optional[ast.AST] = (
            self.visit(node.type_) if node.type_ else None
        )
        type_annotation: Optional[ast.expr] = None
        if type_annotation_node is not None:
            if isinstance(type_annotation_node, ast.expr):
                type_annotation = type_annotation_node
            elif isinstance(node.type_, Void):
                type_annotation = ast.Constant(value=None)
            else:
                raise TypeError(
                    "Argument annotation must be an expression, got "
                    f"{type(type_annotation_node)}"
                )
        return ast.arg(arg=node.name, annotation=type_annotation)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Arguments) -> List[ast.arg]:
        """Convert Arguments."""
        return [self.visit(arg) for arg in node.nodes]

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AssignmentExpr) -> ast.Assign:
        """Convert AssignmentExpr."""
        targets_nodes = [self.visit(target) for target in node.targets]
        targets: List[ast.expr] = []
        for target_node in targets_nodes:
            if not isinstance(target_node, ast.expr):
                raise TypeError(
                    "Assignment target must be expr, got "
                    f"{type(target_node)}"
                )
            if isinstance(target_node, (ast.Name, ast.Attribute, ast.Subscript)):
                target_node.ctx = ast.Store()
            targets.append(target_node)
        value_node = self.visit(node.value)
        if not isinstance(value_node, ast.expr):
            raise TypeError(
                f"Assignment value must be expr, got {type(value_node)}"
            )
        return ast.Assign(targets=targets, value=value_node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AsyncForRangeLoopExpr) -> ast.AsyncFor:
        """Convert AsyncForRangeLoopExpr."""
        if len(node.body) > 1:
            raise ValueError(
                "AsyncForRangeLoopExpr body must have 0 or 1 node."
            )
        start_node = (
            self.visit(node.start)
            if hasattr(node, "start") and node.start is not None
            else ast.Constant(value=0)
        )
        end_node = self.visit(node.end)
        step_node = (
            self.visit(node.step)
            if hasattr(node, "step") and node.step is not None
            else ast.Constant(value=1)
        )
        if (
            not isinstance(start_node, ast.expr)
            or not isinstance(end_node, ast.expr)
            or not isinstance(step_node, ast.expr)
        ):
            raise TypeError("Range arguments must be expressions")
        range_call = ast.Call(
            func=ast.Name(id="range", ctx=ast.Load()),
            args=[start_node, end_node, step_node],
            keywords=[],
        )
        if not isinstance(node.variable, InlineVariableDeclaration):
            raise TypeError(
                "AsyncForRangeLoopExpr variable must be "
                "InlineVariableDeclaration"
            )
        target = ast.Name(id=node.variable.name, ctx=ast.Store())
        body: List[ast.stmt] = []
        if node.body:
            body_result = self.visit(node.body[0])
            if isinstance(body_result, list):
                body.extend(
                    stmt for stmt in body_result if isinstance(stmt, ast.stmt)
                )
            elif isinstance(body_result, ast.stmt):
                body = [body_result]
            elif isinstance(body_result, ast.expr):
                body = [ast.Expr(value=body_result)]
            else:
                raise TypeError(f"Unexpected body type: {type(body_result)}")
        return ast.AsyncFor(
            target=target,
            iter=range_call,
            body=body or [ast.Pass()],
            orelse=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AwaitExpr) -> ast.Await:
        """Convert AwaitExpr."""
        value_node = self.visit(node.value) if node.value else None
        value: Optional[ast.expr] = cast(
            Optional[ast.expr], value_node
        ) if isinstance(value_node, ast.expr) or value_node is None else None
        if value_node is not None and value is None:
            raise TypeError("Await value must be an expression")
        return ast.Await(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BinaryOp) -> ast.AST:
        """Convert BinaryOp."""
        binop_mapping: Dict[str, ast.operator] = {
            "+": ast.Add(), "-": ast.Sub(), "*": ast.Mult(), "/": ast.Div(),
            "//": ast.FloorDiv(), "%": ast.Mod(), "**": ast.Pow(),
            "<<": ast.LShift(), ">>": ast.RShift(), "|": ast.BitOr(),
            "&": ast.BitAnd(), "^": ast.BitXor(), "@": ast.MatMult(),
        }
        compare_mapping: Dict[str, ast.cmpop] = {
            "==": ast.Eq(), "!=": ast.NotEq(), "<": ast.Lt(), "<=": ast.LtE(),
            ">": ast.Gt(), ">=": ast.GtE(), "in": ast.In(),
            "not in": ast.NotIn(), "is": ast.Is(), "is not": ast.IsNot(),
        }
        lhs_node = self.visit(node.lhs)
        rhs_node = self.visit(node.rhs)
        if not isinstance(lhs_node, ast.expr) or not isinstance(
            rhs_node, ast.expr
        ):
            raise TypeError(
                "Operands must be expressions, got "
                f"{type(lhs_node)} and {type(rhs_node)}"
            )
        if node.op_code in compare_mapping:
            return ast.Compare(
                left=lhs_node,
                ops=[compare_mapping[node.op_code]],
                comparators=[rhs_node],
            )
        if node.op_code in binop_mapping:
            return ast.BinOp(
                left=lhs_node, op=binop_mapping[node.op_code], right=rhs_node
            )
        raise ValueError(f"Unsupported binary operator: {node.op_code}")

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Block) -> List[ast.stmt]:
        """Convert Block."""
        self._enter_scope()
        stmts_results: List[
            Union[ast.stmt, List[ast.stmt], ast.expr, None]
        ] = [self.visit(n) for n in node.nodes]
        self._exit_scope()
        result: List[ast.stmt] = []
        for item in stmts_results:
            if isinstance(item, list):
                result.extend(
                    stmt for stmt in item if isinstance(stmt, ast.stmt)
                )
            elif isinstance(item, ast.stmt):
                result.append(item)
            elif isinstance(item, ast.expr):
                result.append(ast.Expr(value=item))
        return result

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CaseStmt) -> "ast_match_case":
        """Convert CaseStmt."""
        pattern: "ast_pattern"
        if node.condition is not None:
            pattern_result = self.visit(node.condition)
            if sys.version_info >= (3, 10) and isinstance(
                pattern_result, ast_pattern
            ):
                pattern = pattern_result
            elif isinstance(pattern_result, ast.expr):
                pattern = pattern_result  # type: ignore[assignment]
            else:
                raise TypeError(
                    f"Cannot use {type(pattern_result)} as match pattern"
                )
        else:  # Default case
            if sys.version_info >= (3, 10):
                pattern = ast.MatchAs(name=None)
            else:
                pattern = ast.Name(id="_", ctx=ast.Load())
        body_result = self.visit(node.body)
        if not isinstance(body_result, list):
            raise TypeError(
                "CaseStmt body visit must return List[stmt], got "
                f"{type(body_result)}"
            )
        body: List[ast.stmt] = body_result
        match_case_constructor = getattr(
            ast, "match_case", MatchCase if "MatchCase" in globals() else None
        )
        if match_case_constructor is None:
            raise RuntimeError("match_case not available")
        return match_case_constructor(pattern=pattern, guard=None, body=body)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ClassDefStmt) -> ast.ClassDef:
        """Convert ClassDefStmt."""
        bases_nodes = (
            [self.visit(b) for b in node.bases]
            if hasattr(node, "bases") and node.bases
            else []
        )
        bases: List[ast.expr] = [
            b for b in bases_nodes if isinstance(b, ast.expr)
        ]
        if node.is_abstract and not any(
            isinstance(b, ast.Name) and b.id == "ABC" for b in bases
        ):
            bases.append(ast.Name(id="ABC", ctx=ast.Load()))
        decorator_nodes = (
            [self.visit(d) for d in node.decorators]
            if hasattr(node, "decorators") and node.decorators
            else []
        )
        decorator_list: List[ast.expr] = [
            d for d in decorator_nodes if isinstance(d, ast.expr)
        ]
        self._enter_scope()
        body_result = self.visit(node.body)
        self._exit_scope()
        if not isinstance(body_result, list):
            raise TypeError(
                "Class body visit must return List[stmt], got "
                f"{type(body_result)}"
            )
        body: List[ast.stmt] = body_result
        return ast.ClassDef(
            name=node.name,
            bases=bases,
            keywords=[],
            body=body or [ast.Pass()],
            decorator_list=decorator_list,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CompareOp) -> ast.Compare:
        """Convert CompareOp."""
        op_mapping: Dict[str, ast.cmpop] = {
            "==": ast.Eq(), "!=": ast.NotEq(), "<": ast.Lt(), "<=": ast.LtE(),
            ">": ast.Gt(), ">=": ast.GtE(), "in": ast.In(),
            "not in": ast.NotIn(), "is": ast.Is(), "is not": ast.IsNot(),
        }
        ops: List[ast.cmpop] = []
        for op in node.ops:
            if op not in op_mapping:
                raise ValueError(f"Unsupported comparison operator: {op}")
            ops.append(op_mapping[op])
        comparators_nodes = [
            self.visit(comparator) for comparator in node.comparators
        ]
        comparators: List[ast.expr] = [
            c for c in comparators_nodes if isinstance(c, ast.expr)
        ]
        if len(comparators) != len(comparators_nodes):
            raise TypeError("Comparators must be expressions")
        left_node = self.visit(node.left)
        if not isinstance(left_node, ast.expr):
            raise TypeError("Left operand must be an expression")
        return ast.Compare(left=left_node, ops=ops, comparators=comparators)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.EnumDeclStmt) -> ast.ClassDef:
        """Convert EnumDeclStmt."""
        bases: List[ast.expr] = [ast.Name(id="Enum", ctx=ast.Load())]
        body: List[ast.stmt] = []
        for attr in node.attributes:
            attr_node = self.visit(attr)
            if isinstance(attr_node, (ast.Assign, ast.AnnAssign)):
                body.append(attr_node)
        return ast.ClassDef(
            name=node.name,
            bases=bases,
            keywords=[],
            body=body or [ast.Pass()],
            decorator_list=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ForRangeLoopExpr) -> ast.ListComp:
        """Convert ForRangeLoopExpr."""
        if len(node.body) != 1:
            raise ValueError("ForRangeLoopExpr body must have one node.")
        start_node = self.visit(node.start)
        end_node = self.visit(node.end)
        step_node = self.visit(node.step)
        if (
            not isinstance(start_node, ast.expr)
            or not isinstance(end_node, ast.expr)
            or not isinstance(step_node, ast.expr)
        ):
            raise TypeError("Range arguments must be expressions")
        range_call = ast.Call(
            func=ast.Name(id="range", ctx=ast.Load()),
            args=[start_node, end_node, step_node],
            keywords=[],
        )
        elt_node = self.visit(node.body[0])
        if not isinstance(elt_node, ast.expr):
            raise TypeError("ForRangeLoopExpr body must be an expression.")
        if not isinstance(node.variable, InlineVariableDeclaration):
            raise TypeError(
                "ForRangeLoopExpr variable must be InlineVariableDeclaration"
            )
        target = ast.Name(id=node.variable.name, ctx=ast.Store())
        return ast.ListComp(
            elt=elt_node,
            generators=[
                ast.comprehension(
                    target=target, iter=range_call, ifs=[], is_async=0
                )
            ],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionAsyncDef) -> ast.AsyncFunctionDef:
        """Convert FunctionAsyncDef."""
        self._enter_scope()
        args_list: List[ast.arg] = (
            self.visit(node.prototype.args) if node.prototype.args else []
        )
        arguments = ast.arguments(
            posonlyargs=[],
            args=args_list,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None,
        )
        return_type_node = (
            self.visit(node.prototype.return_type)
            if node.prototype.return_type
            else None
        )
        returns: Optional[ast.expr] = cast(
            Optional[ast.expr], return_type_node
        ) if isinstance(return_type_node, ast.expr) or return_type_node is None else None
        body_result = self.visit(node.body)
        if not isinstance(body_result, list):
            raise TypeError("Function body visit must return List[stmt]")
        body: List[ast.stmt] = body_result
        self._exit_scope()
        return ast.AsyncFunctionDef(
            name=node.name,
            args=arguments,
            body=body or [ast.Pass()],
            decorator_list=[],
            returns=returns,
            type_comment=None,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionCall) -> ast.Call:
        """Convert FunctionCall."""
        func_node: ast.AST
        if isinstance(node.fn, astx.FunctionDef):
            func_node = ast.Name(id=node.fn.name, ctx=ast.Load())
        else:
            func_node = self.visit(node.fn)
        if not isinstance(func_node, ast.expr):
            raise TypeError(
                "FunctionCall 'fn' must be expr, got " f"{type(func_node)}"
            )
        args_nodes = [self.visit(arg) for arg in node.args]
        args: List[ast.expr] = [
            a for a in args_nodes if isinstance(a, ast.expr)
        ]
        if len(args) != len(args_nodes):
            raise TypeError("FunctionCall arguments must be expressions")
        return ast.Call(func=func_node, args=args, keywords=[])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionDef) -> ast.FunctionDef:
        """Convert FunctionDef."""
        self._enter_scope()
        args_list: List[ast.arg] = (
            self.visit(node.prototype.args) if node.prototype.args else []
        )
        arguments = ast.arguments(
            posonlyargs=[],
            args=args_list,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None,
        )
        return_type_node = (
            self.visit(node.prototype.return_type)
            if node.prototype.return_type
            else None
        )
        returns: Optional[ast.expr] = cast(
            Optional[ast.expr], return_type_node
        ) if isinstance(return_type_node, ast.expr) or return_type_node is None else None
        body_result = self.visit(node.body)
        if not isinstance(body_result, list):
            raise TypeError("Function body visit must return List[stmt]")
        body: List[ast.stmt] = body_result
        self._exit_scope()
        return ast.FunctionDef(
            name=node.name,
            args=arguments,
            body=body or [ast.Pass()],
            decorator_list=[],
            returns=returns,
            type_comment=None,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(
        self, node: astx.FunctionPrototype
    ) -> Tuple[List[ast.arg], Optional[ast.expr]]:
        """Convert FunctionPrototype."""
        args: List[ast.arg] = self.visit(node.args) if node.args else []
        return_type_node = (
            self.visit(node.return_type) if node.return_type else None
        )
        return_type: Optional[ast.expr] = None
        if return_type_node is not None:
            if isinstance(return_type_node, ast.expr):
                return_type = return_type_node
            elif isinstance(node.return_type, Void):
                return_type = ast.Constant(value=None)
        return args, return_type

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionReturn) -> ast.Return:
        """Convert FunctionReturn."""
        value_node = self.visit(node.value) if node.value else None
        value: Optional[ast.expr] = cast(
            Optional[ast.expr], value_node
        ) if isinstance(value_node, ast.expr) or value_node is None else None
        if value_node is not None and value is None:
            raise TypeError("Return value must be an expression")
        return ast.Return(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Identifier) -> ast.Name:
        """Convert Identifier."""
        return ast.Name(id=node.value, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfExpr) -> ast.IfExp:
        """Convert IfExpr."""
        if node.else_ is not None and len(node.else_) > 1:
            raise ValueError("IfExpr else block must have 0 or 1 node.")
        if len(node.then) != 1:
            raise ValueError("IfExpr then block must have exactly 1 node.")
        test_node = self.visit(node.condition)
        then_node = self.visit(node.then[0])
        else_node = (
            self.visit(node.else_[0]) if node.else_ else ast.Constant(value=None)
        )
        if (
            not isinstance(test_node, ast.expr)
            or not isinstance(then_node, ast.expr)
            or not isinstance(else_node, ast.expr)
        ):
            raise TypeError(
                "IfExpr condition, then, and else must be expressions"
            )
        return ast.IfExp(test=test_node, body=then_node, orelse=else_node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfStmt) -> ast.If:
        """Convert IfStmt."""
        test_node = self.visit(node.condition)
        if not isinstance(test_node, ast.expr):
            raise TypeError("If condition must be an expression")
        self._enter_scope()
        then_body_result = self.visit(node.then)
        self._exit_scope()
        if not isinstance(then_body_result, list):
            raise TypeError("If 'then' body visit must return List[stmt]")
        then_body: List[ast.stmt] = then_body_result
        else_body: List[ast.stmt] = []
        if node.else_ is not None:
            self._enter_scope()
            else_body_result = self.visit(node.else_)
            self._exit_scope()
            if not isinstance(else_body_result, list):
                raise TypeError("If 'else' body visit must return List[stmt]")
            else_body = else_body_result
        return ast.If(
            test=test_node,
            body=then_body or [ast.Pass()],
            orelse=else_body or [],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromExpr) -> ast.Expr:
        """Convert ImportFromExpr."""
        names: List[ast.alias] = [self.visit(name) for name in node.names]
        level_dots = "." * node.level
        module_str = f"{level_dots}{node.module}" if node.module else level_dots
        import_calls: List[ast.expr] = []
        for name in names:
            if isinstance(name, ast.alias):
                name_str = name.name
                fromlist = [ast.Constant(value=name_str)]
                import_call = ast.Call(
                    func=ast.Name(id="getattr", ctx=ast.Load()),
                    args=[
                        ast.Call(
                            func=ast.Name(id="__import__", ctx=ast.Load()),
                            args=[
                                ast.Constant(value=module_str),
                                ast.Dict(keys=[], values=[]),
                                ast.Dict(keys=[], values=[]),
                                ast.List(elts=fromlist, ctx=ast.Load()),
                                ast.Constant(value=node.level),
                            ],
                            keywords=[],
                        ),
                        ast.Constant(value=name_str),
                    ],
                    keywords=[],
                )
                import_calls.append(import_call)
        value: ast.expr = (
            import_calls[0]
            if len(import_calls) == 1
            else ast.Tuple(elts=import_calls, ctx=ast.Load())
        )
        return ast.Expr(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromStmt) -> ast.ImportFrom:
        """Convert ImportFromStmt."""
        names: List[ast.alias] = [self.visit(name) for name in node.names]
        return ast.ImportFrom(
            module=node.module, names=names, level=node.level
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportExpr) -> ast.Expr:
        """Convert ImportExpr."""
        names: List[ast.alias] = [self.visit(name) for name in node.names]
        import_calls: List[ast.expr] = []
        for name in names:
            if isinstance(name, ast.alias):
                module_name_to_import = name.name
                import_call = ast.Call(
                    func=ast.Name(id="__import__", ctx=ast.Load()),
                    args=[ast.Constant(value=module_name_to_import)],
                    keywords=[],
                )
                import_calls.append(import_call)
        value: ast.expr = (
            import_calls[0]
            if len(import_calls) == 1
            else ast.Tuple(elts=import_calls, ctx=ast.Load())
        )
        return ast.Expr(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportStmt) -> ast.Import:
        """Convert ImportStmt."""
        names: List[ast.alias] = [self.visit(name) for name in node.names]
        return ast.Import(names=names)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LambdaExpr) -> ast.Lambda:
        """Convert LambdaExpr."""
        params_list: List[ast.arg] = self.visit(node.params) if node.params else []
        arguments = ast.arguments(
            posonlyargs=[],
            args=params_list,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None,
        )
        body_node = self.visit(node.body)
        if not isinstance(body_node, ast.expr):
            raise TypeError("Lambda body must be an expression")
        return ast.Lambda(args=arguments, body=body_node)

    # --- Literal Visit Methods ---
    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralBoolean) -> ast.Constant:
        """Convert LiteralBoolean."""
        return ast.Constant(value=bool(node.value))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex) -> ast.Constant:
        """Convert LiteralComplex."""
        return ast.Constant(value=complex(node.value[0], node.value[1]))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex32) -> ast.Constant:
        """Convert LiteralComplex32."""
        return ast.Constant(value=complex(node.value[0], node.value[1]))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex64) -> ast.Constant:
        """Convert LiteralComplex64."""
        return ast.Constant(value=complex(node.value[0], node.value[1]))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat16) -> ast.Constant:
        """Convert LiteralFloat16."""
        return ast.Constant(value=float(node.value))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat32) -> ast.Constant:
        """Convert LiteralFloat32."""
        return ast.Constant(value=float(node.value))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat64) -> ast.Constant:
        """Convert LiteralFloat64."""
        return ast.Constant(value=float(node.value))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt32) -> ast.Constant:
        """Convert LiteralInt32."""
        return ast.Constant(value=int(node.value))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralString) -> ast.Constant:
        """Convert LiteralString."""
        return ast.Constant(value=str(node.value))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralUTF8String) -> ast.Constant:
        """Convert LiteralUTF8String."""
        return ast.Constant(value=str(node.value))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralUTF8Char) -> ast.Constant:
        """Convert LiteralUTF8Char."""
        return ast.Constant(value=str(node.value))

    # --- End Literal Visit Methods ---

    @dispatch  # type: ignore[no-redef]
    def visit(
        self, node: Union[astx.StructDeclStmt, astx.StructDefStmt]
    ) -> ast.ClassDef:
        """Convert StructDeclStmt/StructDefStmt."""
        decorator_list: List[ast.expr] = [
            ast.Name(id="dataclass", ctx=ast.Load())
        ]
        body: List[ast.stmt] = []
        for attr in node.attributes:
            attr_node = self.visit(attr)
            if isinstance(attr_node, (ast.AnnAssign, ast.Assign)):
                body.append(attr_node)
        return ast.ClassDef(
            name=node.name,
            bases=[],
            keywords=[],
            body=body or [ast.Pass()],
            decorator_list=decorator_list,
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SubscriptExpr) -> ast.Subscript:
        """Convert SubscriptExpr."""
        value_node = self.visit(node.value)
        if not isinstance(value_node, ast.expr):
            raise TypeError("Subscript value must be an expression")
        slice_obj: Union[ast.Slice, ast.expr]
        if (
            hasattr(node, "lower")
            or hasattr(node, "upper")
            or hasattr(node, "step")
        ):
            lower_node = (
                self.visit(node.lower)
                if hasattr(node, "lower") and not isinstance(node.lower, LiteralNone)
                else None
            )
            upper_node = (
                self.visit(node.upper)
                if hasattr(node, "upper") and not isinstance(node.upper, LiteralNone)
                else None
            )
            step_node = (
                self.visit(node.step)
                if hasattr(node, "step") and not isinstance(node.step, LiteralNone)
                else None
            )
            lower = cast(
                Optional[ast.expr], lower_node
            ) if isinstance(lower_node, ast.expr) or lower_node is None else None
            upper = cast(
                Optional[ast.expr], upper_node
            ) if isinstance(upper_node, ast.expr) or upper_node is None else None
            step = cast(
                Optional[ast.expr], step_node
            ) if isinstance(step_node, ast.expr) or step_node is None else None
            if (
                (lower_node is not None and lower is None)
                or (upper_node is not None and upper is None)
                or (step_node is not None and step is None)
            ):
                raise TypeError("Slice components must be expressions or None")
            slice_obj = ast.Slice(lower=lower, upper=upper, step=step)
        elif hasattr(node, "index"):
            index_node = self.visit(node.index)
            if not isinstance(index_node, ast.expr):
                raise TypeError("Subscript index must be an expression")
            slice_obj = index_node
        else:
            raise ValueError(
                "SubscriptExpr must have index or slice attributes"
            )
        return ast.Subscript(
            value=value_node, slice=slice_obj, ctx=ast.Load()
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SwitchStmt) -> "ast_Match":
        """Convert SwitchStmt."""
        subject_node = self.visit(node.value)
        if not isinstance(subject_node, ast.expr):
            raise TypeError("Switch subject must be an expression")
        cases: List["ast_match_case"] = [
            self.visit(case) for case in node.cases
        ]
        match_constructor = getattr(
            ast, "Match", Match if "Match" in globals() else None
        )
        if match_constructor is None:
            raise RuntimeError("Match not available")
        return match_constructor(subject=subject_node, cases=cases)

    # --- Type Visit Methods ---
    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Complex32) -> ast.Name:
        """Convert Complex32 type."""
        return ast.Name(id="complex", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Complex64) -> ast.Name:
        """Convert Complex64 type."""
        return ast.Name(id="complex", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Float16) -> ast.Name:
        """Convert Float16 type."""
        return ast.Name(id="float", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Float32) -> ast.Name:
        """Convert Float32 type."""
        return ast.Name(id="float", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Float64) -> ast.Name:
        """Convert Float64 type."""
        return ast.Name(id="float", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Int32) -> ast.Name:
        """Convert Int32 type."""
        return ast.Name(id="int", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Void) -> ast.Constant:
        """Convert Void type to None constant."""
        return ast.Constant(value=None)

    # --- End Type Visit Methods ---

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.TypeCastExpr) -> ast.Call:
        """Convert TypeCastExpr."""
        target_type_node = self.visit(node.target_type)
        expr_node = self.visit(node.expr)
        if not isinstance(target_type_node, ast.expr) or not isinstance(
            expr_node, ast.expr
        ):
            raise TypeError(
                "TypeCast target type and expression must be expressions"
            )
        return ast.Call(
            func=ast.Name(id="cast", ctx=ast.Load()),
            args=[target_type_node, expr_node],
            keywords=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ThrowStmt) -> ast.Raise:
        """Convert ThrowStmt."""
        exc_node = self.visit(node.exception) if node.exception else None
        exc: Optional[ast.expr] = cast(
            Optional[ast.expr], exc_node
        ) if isinstance(exc_node, ast.expr) or exc_node is None else None
        if exc_node is not None and exc is None:
            raise TypeError("Raise exception must be an expression")
        return ast.Raise(exc=exc, cause=None)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UnaryOp) -> ast.UnaryOp:
        """Convert UnaryOp."""
        op_mapping: Dict[str, ast.unaryop] = {
            "-": ast.USub(), "+": ast.UAdd(), "~": ast.Invert(), "not": ast.Not()
        }
        if node.op_code not in op_mapping:
            raise ValueError(f"Unsupported unary operator: {node.op_code}")
        operand_node = self.visit(node.operand)
        if not isinstance(operand_node, ast.expr):
            raise TypeError("UnaryOp operand must be an expression")
        return ast.UnaryOp(op=op_mapping[node.op_code], operand=operand_node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Variable) -> ast.Name:
        """Convert Variable."""
        self.current_scope[node.name] = True
        return ast.Name(id=node.name, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableAssignment) -> ast.Assign:
        """Convert VariableAssignment."""
        target = ast.Name(id=node.name, ctx=ast.Store())
        value_node = self.visit(node.value)
        if not isinstance(value_node, ast.expr):
            raise TypeError("Assignment value must be an expression")
        self.current_scope[node.name] = True
        return ast.Assign(targets=[target], value=value_node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableDeclaration) -> ast.AnnAssign:
        """Convert VariableDeclaration."""
        target = ast.Name(id=node.name, ctx=ast.Store())
        annotation_node = self.visit(node.type_)
        if not isinstance(annotation_node, ast.expr):
            if isinstance(node.type_, Void):
                annotation = ast.Constant(value=None)
            else:
                annotation = ast.Name(id="Any", ctx=ast.Load())  # Fallback
        else:
            annotation = annotation_node
        value_node = self.visit(node.value) if node.value else None
        value: Optional[ast.expr] = cast(
            Optional[ast.expr], value_node
        ) if isinstance(value_node, ast.expr) or value_node is None else None
        if value_node is not None and value is None:
            raise TypeError("VariableDeclaration value must be an expression")
        self.current_scope[node.name] = True
        return ast.AnnAssign(
            target=target, annotation=annotation, value=value, simple=1
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WalrusOp) -> ast.NamedExpr:
        """Convert WalrusOp."""
        lhs_node = self.visit(node.lhs)
        if not isinstance(lhs_node, ast.Name):
            raise TypeError(
                "LHS of Walrus must be Variable, got " f"{type(node.lhs)}"
            )
        target = ast.Name(id=lhs_node.id, ctx=ast.Store())
        value_node = self.visit(node.rhs)
        if not isinstance(value_node, ast.expr):
            raise TypeError("RHS of Walrus must be an expression")
        if isinstance(node.lhs, astx.Variable):
            self.current_scope[node.lhs.name] = True
        return ast.NamedExpr(target=target, value=value_node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AugAssign) -> ast.AugAssign:
        """Convert AugAssign."""
        op_mapping: Dict[str, ast.operator] = {
            "+=": ast.Add(), "-=": ast.Sub(), "*=": ast.Mult(), "/=": ast.Div(),
            "//=": ast.FloorDiv(), "%=": ast.Mod(), "**=": ast.Pow(),
            "<<=": ast.LShift(), ">>=": ast.RShift(), "|=": ast.BitOr(),
            "&=": ast.BitAnd(), "^=": ast.BitXor(), "@=": ast.MatMult(),
        }
        if node.op_code not in op_mapping:
            raise ValueError(
                "Unsupported augmented assignment operator: " f"{node.op_code}"
            )
        target_node = self.visit(node.target)
        if not isinstance(target_node, (ast.Name, ast.Attribute, ast.Subscript)):
            raise TypeError(
                "Invalid target for augmented assignment: "
                f"{type(target_node)}"
            )
        target_node.ctx = ast.Store()
        value_node = self.visit(node.value)
        if not isinstance(value_node, ast.expr):
            raise TypeError("AugAssign value must be an expression")
        return ast.AugAssign(
            target=target_node, op=op_mapping[node.op_code], value=value_node
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileExpr) -> ast.ListComp:
        """Convert WhileExpr."""
        if len(node.body) != 1:
            raise ValueError("WhileExpr body must have exactly one node.")
        condition_node = self.visit(node.condition)
        body_node = self.visit(node.body[0])
        if not isinstance(condition_node, ast.expr) or not isinstance(
            body_node, ast.expr
        ):
            raise TypeError(
                "WhileExpr condition and body must be expressions"
            )
        lambda_expr = ast.Lambda(
            args=ast.arguments(
                posonlyargs=[],
                args=[],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
                vararg=None,
                kwarg=None,
            ),
            body=condition_node,
        )
        iter_call = ast.Call(
            func=ast.Name(id="iter", ctx=ast.Load()),
            args=[lambda_expr, ast.Constant(value=False)],
            keywords=[],
        )
        return ast.ListComp(
            elt=body_node,
            generators=[
                ast.comprehension(
                    target=ast.Name(id="_", ctx=ast.Store()),
                    iter=iter_call,
                    ifs=[],
                    is_async=0,
                )
            ],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileStmt) -> ast.While:
        """Convert WhileStmt."""
        condition_node = self.visit(node.condition)
        if not isinstance(condition_node, ast.expr):
            raise TypeError("While condition must be an expression")
        self._enter_scope()
        body_result = self.visit(node.body)
        self._exit_scope()
        if not isinstance(body_result, list):
            raise TypeError("While body visit must return List[stmt]")
        body: List[ast.stmt] = body_result
        return ast.While(
            test=condition_node, body=body or [ast.Pass()], orelse=[]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldExpr) -> ast.Yield:
        """Convert YieldExpr."""
        value_node = self.visit(node.value) if node.value else None
        value: Optional[ast.expr] = cast(
            Optional[ast.expr], value_node
        ) if isinstance(value_node, ast.expr) or value_node is None else None
        if value_node is not None and value is None:
            raise TypeError("Yield value must be an expression")
        return ast.Yield(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldFromExpr) -> ast.YieldFrom:
        """Convert YieldFromExpr."""
        value_node = self.visit(node.value)
        if not isinstance(value_node, ast.expr):
            raise TypeError("YieldFrom value must be an expression")
        return ast.YieldFrom(value=value_node)

    # --- Date/Time Type/Literal Visit Methods ---
    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Date) -> ast.Name:
        """Convert Date type."""
        return ast.Name(id="date", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Time) -> ast.Name:
        """Convert Time type."""
        return ast.Name(id="time", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Timestamp) -> ast.Name:
        """Convert Timestamp type."""
        return ast.Name(id="datetime", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DateTime) -> ast.Name:
        """Convert DateTime type."""
        return ast.Name(id="datetime", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDate) -> ast.Call:
        """Convert LiteralDate."""
        strptime_call = ast.Call(
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
        )
        return ast.Call(
            func=ast.Attribute(
                value=strptime_call, attr="date", ctx=ast.Load()
            ),
            args=[],
            keywords=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTime) -> ast.Call:
        """Convert LiteralTime."""
        strptime_call = ast.Call(
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
        )
        return ast.Call(
            func=ast.Attribute(
                value=strptime_call, attr="time", ctx=ast.Load()
            ),
            args=[],
            keywords=[],
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTimestamp) -> ast.Call:
        """Convert LiteralTimestamp."""
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
    def visit(self, node: astx.LiteralDateTime) -> ast.Call:
        """Convert LiteralDateTime."""
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

    # --- End Date/Time Visit Methods ---

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ParenthesizedExpr) -> ast.AST:
        """Convert ParenthesizedExpr."""
        return self.visit(node.value)

    # --- Boolean Op Visit Methods ---
    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AndOp) -> ast.BoolOp:
        """Convert AndOp."""
        lhs = cast(ast.expr, self.visit(node.lhs))
        rhs = cast(ast.expr, self.visit(node.rhs))
        return ast.BoolOp(op=ast.And(), values=[lhs, rhs])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.OrOp) -> ast.BoolOp:
        """Convert OrOp."""
        lhs = cast(ast.expr, self.visit(node.lhs))
        rhs = cast(ast.expr, self.visit(node.rhs))
        return ast.BoolOp(op=ast.Or(), values=[lhs, rhs])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.XorOp) -> ast.BinOp:
        """Convert XorOp."""
        lhs = cast(ast.expr, self.visit(node.lhs))
        rhs = cast(ast.expr, self.visit(node.rhs))
        return ast.BinOp(left=lhs, op=ast.BitXor(), right=rhs)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NandOp) -> ast.UnaryOp:
        """Convert NandOp."""
        lhs = cast(ast.expr, self.visit(node.lhs))
        rhs = cast(ast.expr, self.visit(node.rhs))
        return ast.UnaryOp(
            op=ast.Not(), operand=ast.BoolOp(op=ast.And(), values=[lhs, rhs])
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NorOp) -> ast.UnaryOp:
        """Convert NorOp."""
        lhs = cast(ast.expr, self.visit(node.lhs))
        rhs = cast(ast.expr, self.visit(node.rhs))
        return ast.UnaryOp(
            op=ast.Not(), operand=ast.BoolOp(op=ast.Or(), values=[lhs, rhs])
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.XnorOp) -> ast.UnaryOp:
        """Convert XnorOp."""
        lhs = cast(ast.expr, self.visit(node.lhs))
        rhs = cast(ast.expr, self.visit(node.rhs))
        return ast.UnaryOp(
            op=ast.Not(),
            operand=ast.BinOp(left=lhs, op=ast.BitXor(), right=rhs),
        )

    # --- End Boolean Op Visit Methods ---

    # --- Collection Literal Visit Methods ---
    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralList) -> ast.List:
        """Convert LiteralList."""
        elements: List[ast.expr] = [
            cast(ast.expr, self.visit(element)) for element in node.elements
        ]
        return ast.List(elts=elements, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTuple) -> ast.Tuple:
        """Convert LiteralTuple."""
        elements: List[ast.expr] = [
            cast(ast.expr, self.visit(element)) for element in node.elements
        ]
        return ast.Tuple(elts=elements, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralSet) -> ast.Set:
        """Convert LiteralSet."""
        elements_nodes = [self.visit(element) for element in node.elements]
        elements: List[ast.expr] = [
            e for e in elements_nodes if isinstance(e, ast.expr)
        ]
        if len(elements) != len(elements_nodes):
            raise TypeError("Set elements must be expressions")
        return ast.Set(elts=elements)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDict) -> ast.Dict:
        """Convert LiteralDict."""
        keys_nodes = [self.visit(key) for key in node.elements.keys()]
        values_nodes = [self.visit(value) for value in node.elements.values()]
        keys: List[Optional[ast.expr]] = [
            cast(Optional[ast.expr], k)
            if isinstance(k, ast.expr) or k is None
            else None
            for k in keys_nodes
        ]
        values: List[ast.expr] = [
            v for v in values_nodes if isinstance(v, ast.expr)
        ]
        if len(keys) != len(keys_nodes) or len(values) != len(values_nodes):
            raise TypeError("Dict keys and values must be expressions")
        valid_keys: List[ast.expr] = [k for k in keys if k is not None]
        if len(valid_keys) != len(values):
            if None in keys:
                raise NotImplementedError("Dict unpacking not supported")
            else:
                raise ValueError("Mismatch between keys and values")
        return ast.Dict(keys=valid_keys, values=values)

    # --- End Collection Literal Visit Methods ---

    # --- Helper Methods ---
    def convert(self, astx_node: astx.AST) -> ast.Module:
        """Convert ASTx node to Python AST Module."""
        result = self.visit(astx_node)
        body: List[ast.stmt] = []
        if isinstance(result, list):  # Usually from Block
            body.extend(stmt for stmt in result if isinstance(stmt, ast.stmt))
        elif isinstance(result, ast.stmt):
            body = [result]
        elif isinstance(result, ast.expr):
            body = [ast.Expr(value=result)]
        elif isinstance(result, ast.Module):
            body = result.body  # Already a Module
        else:
            raise TypeError(
                f"Unexpected result type from visit: {type(result)}"
            )
        return ast.Module(body=body, type_ignores=[])

    def convert_and_compile(
        self, astx_node: astx.AST, filename: str = "<astx>"
    ) -> Any:
        """Convert ASTx node to Python AST Module and compile it."""
        python_module: ast.Module = self.convert(astx_node)
        ast.fix_missing_locations(python_module)
        return compile(python_module, filename, "exec")

    def execute(
        self,
        astx_node: astx.AST,
        globals_dict: Optional[Dict[str, Any]] = None,
        locals_dict: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Convert, compile and execute an ASTx node."""
        code_obj = self.convert_and_compile(astx_node)
        exec_globals: Dict[str, Any] = (
            {} if globals_dict is None else globals_dict.copy()
        )
        exec_locals: Dict[str, Any] = (
            {} if locals_dict is None else locals_dict.copy()
        )

        # Add necessary built-ins/imports if not present
        required_builtins = {
            "cast": getattr(__import__("typing"), "cast", None),
            "Any": getattr(__import__("typing"), "Any", None),
            "Enum": getattr(__import__("enum"), "Enum", None),
            "dataclass": getattr(__import__("dataclasses"), "dataclass", None),
            "ABC": getattr(__import__("abc"), "ABC", None),
            "datetime": __import__("datetime"),
            "date": getattr(__import__("datetime"), "date", None),
            "time": getattr(__import__("datetime"), "time", None),
        }
        for name, obj in required_builtins.items():
            if obj is not None and name not in exec_globals:
                exec_globals[name] = obj
        if "ast" not in exec_globals:
            exec_globals["ast"] = ast

        exec(code_obj, exec_globals, exec_locals)
        # Update globals with functions defined in locals for recursion
        for key, value in exec_locals.items():
            if callable(value) and key not in exec_globals:
                exec_globals[key] = value
        return exec_locals

    def to_python_string(self, astx_node: astx.AST) -> str:
        """Convert ASTx directly to Python source code."""
        string_transpiler = ASTxPythonTranspiler()
        result = string_transpiler.visit(astx_node)
        # Ensure the result is a string
        if not isinstance(result, str):
            raise TypeError(
                "Expected str from string transpiler, got " f"{type(result)}"
            )
        return result

    def ast_to_string(self, python_ast: ast.AST) -> str:
        """Convert a Python AST node to a Python source code string."""
        if not isinstance(python_ast, (ast.Module, ast.stmt, ast.expr)):
            raise TypeError(f"Cannot unparse node of type {type(python_ast)}")
        if hasattr(ast, "unparse"):
            return ast.unparse(python_ast)
        else:
            try:
                import astunparse
                return astunparse.unparse(python_ast)
            except ImportError:
                raise ImportError(
                    "Python < 3.9 requires 'astunparse'. "
                    "Install with 'pip install astunparse'"
                )

    def astx_to_ast_to_string(self, astx_node: astx.AST) -> str:
        """Convert an ASTx node to Python source code via Python AST."""
        python_ast_module = self.convert(astx_node)
        return self.ast_to_string(python_ast_module)

    def compare_transpilation_methods(
        self, astx_node: astx.AST
    ) -> Tuple[str, str, bool]:
        """Compare direct string transpilation with AST-based transpilation."""
        direct_string = self.to_python_string(astx_node)
        ast_based_string = self.astx_to_ast_to_string(astx_node)
        direct_normalized = " ".join(direct_string.split())
        ast_normalized = " ".join(ast_based_string.split())
        return (
            direct_string,
            ast_based_string,
            direct_normalized == ast_normalized,
        )
