"""ASTx to Python AST transpiler."""

import ast
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from plum import dispatch

import astx
from astx.tools.typing import typechecked


@typechecked
class ASTxPythonASTTranspiler:
    """
    Transpiler that converts ASTx nodes to Python's AST nodes.

    This transpiler allows direct conversion from ASTx to Python's native AST
    representation, enabling seamless integration with Python's compile(),
    exec(), and other AST-based tools.

    Notes
    -----
    Please keep the visit method in alphabet order according to the node type.
    The visit method for astx.AST should be the first one.
    """

    def __init__(self) -> None:
        self.symbol_table: Dict[str, Any] = {}
        self.current_scope: List[Dict[str, Any]] = [{}]

    def _enter_scope(self) -> None:
        """Enter a new scope for variable tracking."""
        self.current_scope.append({})

    def _exit_scope(self) -> None:
        """Exit the current scope."""
        if len(self.current_scope) > 1:
            self.current_scope.pop()

    def _add_to_current_scope(self, name: str, node_type: Any) -> None:
        """Add a variable to the current scope."""
        self.current_scope[-1][name] = node_type

    def _lookup_variable(self, name: str) -> Optional[Any]:
        """Look up a variable in all scopes, from innermost to outermost."""
        for scope in reversed(self.current_scope):
            if name in scope:
                return scope[name]
        return None

    def _create_module(self, body: List[ast.AST]) -> ast.Module:
        """Create a Python AST Module node containing the given body statements."""
        return ast.Module(body=body, type_ignores=[])

    @dispatch.abstract
    def visit(self, expr: astx.AST) -> ast.AST:
        """Translate an ASTx node to Python AST."""
        raise Exception(f"Not implemented yet for AST node: {expr}")

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AliasExpr) -> ast.alias:
        """Handle AliasExpr nodes."""
        return ast.alias(name=node.name, asname=node.asname)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Argument) -> ast.arg:
        """Handle Argument nodes."""
        # Transform the ASTx type to a Python AST annotation
        type_annotation = self.visit(node.type_) if node.type_ else None
        return ast.arg(arg=node.name, annotation=type_annotation)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Arguments) -> List[ast.arg]:
        """Handle Arguments nodes."""
        return [self.visit(arg) for arg in node.nodes]

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AssignmentExpr) -> ast.Assign:
        """Handle AssignmentExpr nodes."""
        targets = [self.visit(target) for target in node.targets]
        value = self.visit(node.value)
        return ast.Assign(targets=targets, value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BinaryOp) -> ast.BinOp:
        """Handle BinaryOp nodes."""
        # Map ASTx operators to Python AST operators
        op_map = {
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
        
        if node.op_code not in op_map:
            raise ValueError(f"Unsupported binary operator: {node.op_code}")
        
        return ast.BinOp(
            left=self.visit(node.lhs),
            op=op_map[node.op_code],
            right=self.visit(node.rhs)
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Block) -> List[ast.AST]:
        """Handle Block nodes."""
        result = []
        for child_node in node.nodes:
            child_ast = self.visit(child_node)
            # Some nodes may return lists (e.g., for statements that expand to multiple Python statements)
            if isinstance(child_ast, list):
                result.extend(child_ast)
            else:
                result.append(child_ast)
        return result

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CaseStmt) -> ast.match_case:
        """Handle CaseStmt nodes."""
        # Convert condition to pattern
        pattern = (
            self.visit(node.condition) 
            if node.condition is not None 
            else ast.MatchAs(name="_")  # Wildcard pattern
        )
        
        # Convert body
        body = self.visit(node.body)
        if not isinstance(body, list):
            body = [body]
            
        return ast.match_case(pattern=pattern, guard=None, body=body)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CatchHandlerStmt) -> ast.ExceptHandler:
        """Handle CatchHandlerStmt nodes."""
        # Handle exception types
        if node.types:
            # If multiple types, create a tuple of them
            if len(node.types) > 1:
                type_ast = ast.Tuple(
                    elts=[self.visit(t) for t in node.types],
                    ctx=ast.Load()
                )
            else:
                type_ast = self.visit(node.types[0])
        else:
            type_ast = None
            
        # Handle exception name
        name = self.visit(node.name).id if node.name else None
        
        # Handle body
        body = self.visit(node.body)
        if not isinstance(body, list):
            body = [body]
            
        return ast.ExceptHandler(type=type_ast, name=name, body=body)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ClassDefStmt) -> ast.ClassDef:
        """Handle ClassDefStmt nodes."""
        # Enter a new scope for the class
        self._enter_scope()
        
        bases = []
        keywords = []
        
        # Add ABC base class if abstract
        if node.is_abstract:
            bases.append(ast.Name(id="ABC", ctx=ast.Load()))
            
        # Convert body
        body_nodes = self.visit(node.body)
        if not isinstance(body_nodes, list):
            body_nodes = [body_nodes]
            
        # Exit the class scope
        self._exit_scope()
        
        return ast.ClassDef(
            name=node.name,
            bases=bases,
            keywords=keywords,
            body=body_nodes,
            decorator_list=[]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.EnumDeclStmt) -> ast.ClassDef:
        """Handle EnumDeclStmt nodes."""
        # Create class with Enum as base
        bases = [ast.Name(id="Enum", ctx=ast.Load())]
        
        # Convert attributes to assignments
        body = []
        for attr in node.attributes:
            body.append(self.visit(attr))
            
        return ast.ClassDef(
            name=node.name,
            bases=bases,
            keywords=[],
            body=body,
            decorator_list=[]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ExceptionHandlerStmt) -> ast.Try:
        """Handle ExceptionHandlerStmt nodes."""
        # Convert body
        body = self.visit(node.body)
        if not isinstance(body, list):
            body = [body]
            
        # Convert handlers
        handlers = [self.visit(handler) for handler in node.handlers]
        
        # Convert finally handler if present
        finalbody = []
        if node.finally_handler:
            finalbody = self.visit(node.finally_handler.body)
            if not isinstance(finalbody, list):
                finalbody = [finalbody]
                
        # No else block in the AST representation provided
        orelse = []
        
        return ast.Try(
            body=body,
            handlers=handlers,
            orelse=orelse,
            finalbody=finalbody
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FinallyHandlerStmt) -> List[ast.AST]:
        """Handle FinallyHandlerStmt nodes."""
        body = self.visit(node.body)
        if not isinstance(body, list):
            body = [body]
        return body

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ForRangeLoopExpr) -> ast.ListComp:
        """Handle ForRangeLoopExpr nodes."""
        if len(node.body) > 1:
            raise ValueError(
                "ForRangeLoopExpr in Python just accept 1 node in the body attribute."
            )
            
        # Create the target
        target = ast.Name(id=node.variable.name, ctx=ast.Store())
        
        # Create the range call
        range_call = ast.Call(
            func=ast.Name(id="range", ctx=ast.Load()),
            args=[
                self.visit(node.start),
                self.visit(node.end),
                self.visit(node.step)
            ],
            keywords=[]
        )
        
        # Create the generator
        generator = ast.comprehension(
            target=target,
            iter=range_call,
            ifs=[],
            is_async=0
        )
        
        # Visit the body expression
        elt = self.visit(node.body.nodes[0])
        
        return ast.ListComp(elt=elt, generators=[generator])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Function) -> ast.FunctionDef:
        """Handle Function nodes."""
        # Enter a new scope for the function
        self._enter_scope()
        
        # Process arguments
        args_ast = self.visit(node.prototype.args)
        
        # Create arguments node
        arguments = ast.arguments(
            posonlyargs=[],
            args=args_ast,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None
        )
        
        # Process return type annotation
        returns = self.visit(node.prototype.return_type) if node.prototype.return_type else None
        
        # Process body
        body_ast = self.visit(node.body)
        if not isinstance(body_ast, list):
            body_ast = [body_ast]
        
        # If body is empty, add a pass statement
        if not body_ast:
            body_ast = [ast.Pass()]
            
        # Exit the function scope
        self._exit_scope()
        
        return ast.FunctionDef(
            name=node.name,
            args=arguments,
            body=body_ast,
            decorator_list=[],
            returns=returns
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionCall) -> ast.Call:
        """Handle FunctionCall nodes."""
        # Convert function name to Name node
        func = ast.Name(id=node.fn.name, ctx=ast.Load())
        
        # Convert arguments
        args = [self.visit(arg) for arg in node.args]
        
        return ast.Call(
            func=func,
            args=args,
            keywords=[]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionReturn) -> ast.Return:
        """Handle FunctionReturn nodes."""
        value = self.visit(node.value) if node.value else None
        return ast.Return(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Identifier) -> ast.Name:
        """Handle Identifier nodes."""
        return ast.Name(id=node.value, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfExpr) -> ast.IfExp:
        """Handle IfExpr nodes."""
        if node.else_ is not None and len(node.else_) > 1:
            raise ValueError(
                "IfExpr in Python just accept 1 node in the else attribute."
            )

        if len(node.then) > 1:
            raise ValueError(
                "IfExpr in Python just accept 1 node in the then attribute."
            )

        test = self.visit(node.condition)
        body = self.visit(node.then.nodes[0])
        orelse = self.visit(node.else_.nodes[0]) if node.else_ else ast.Constant(value=None)
        
        return ast.IfExp(test=test, body=body, orelse=orelse)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfStmt) -> ast.If:
        """Handle IfStmt nodes."""
        test = self.visit(node.condition)
        
        # Process then body
        then_body = self.visit(node.then)
        if not isinstance(then_body, list):
            then_body = [then_body]
        
        # Process else body if present
        else_body = []
        if node.else_ is not None:
            else_body = self.visit(node.else_)
            if not isinstance(else_body, list):
                else_body = [else_body]
                
        return ast.If(
            test=test,
            body=then_body,
            orelse=else_body
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromStmt) -> ast.ImportFrom:
        """Handle ImportFromStmt nodes."""
        names = [self.visit(name) for name in node.names]
        return ast.ImportFrom(
            module=node.module,
            names=names,
            level=node.level
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportStmt) -> ast.Import:
        """Handle ImportStmt nodes."""
        names = [self.visit(name) for name in node.names]
        return ast.Import(names=names)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LambdaExpr) -> ast.Lambda:
        """Handle LambdaExpr nodes."""
        # Create arguments
        params = [ast.arg(arg=param.name, annotation=None) for param in node.params]
        arguments = ast.arguments(
            posonlyargs=[],
            args=params,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None
        )
        
        # Visit body
        body = self.visit(node.body)
        
        return ast.Lambda(args=arguments, body=body)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralBoolean) -> ast.Constant:
        """Handle LiteralBoolean nodes."""
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Union[astx.LiteralComplex32, astx.LiteralComplex64, astx.LiteralComplex]) -> ast.Call:
        """Handle LiteralComplex nodes."""
        real, imag = node.value
        
        # Create a call to complex()
        return ast.Call(
            func=ast.Name(id="complex", ctx=ast.Load()),
            args=[
                ast.Constant(value=real),
                ast.Constant(value=imag)
            ],
            keywords=[]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Union[astx.LiteralFloat16, astx.LiteralFloat32, astx.LiteralFloat64]) -> ast.Constant:
        """Handle LiteralFloat nodes."""
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt32) -> ast.Constant:
        """Handle LiteralInt32 nodes."""
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Union[astx.LiteralString, astx.LiteralUTF8String]) -> ast.Constant:
        """Handle LiteralString nodes."""
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralUTF8Char) -> ast.Constant:
        """Handle LiteralUTF8Char nodes."""
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Union[astx.StructDeclStmt, astx.StructDefStmt]) -> ast.ClassDef:
        """Handle StructDeclStmt and StructDefStmt nodes."""
        # Create a class with dataclass decorator
        decorator_list = [
            ast.Name(id="dataclass", ctx=ast.Load())
        ]
        
        # Process attributes
        body = []
        for attr in node.attributes:
            body.append(self.visit(attr))
            if not body:
                body = [ast.Pass()]
                
        return ast.ClassDef(
            name=node.name,
            bases=[],
            keywords=[],
            body=body,
            decorator_list=decorator_list
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SubscriptExpr) -> ast.Subscript:
        """Handle SubscriptExpr nodes."""
        # Create value
        value = ast.Name(id=node.value.name, ctx=ast.Load())
        
        # Handle slice
        if isinstance(node.lower, astx.LiteralNone) and isinstance(node.upper, astx.LiteralNone):
            # Simple index
            slice_node = ast.Index(value=self.visit(node.index))
        else:
            # Slice
            lower = None if isinstance(node.lower, astx.LiteralNone) else self.visit(node.lower)
            upper = None if isinstance(node.upper, astx.LiteralNone) else self.visit(node.upper)
            step = None if isinstance(node.step, astx.LiteralNone) else self.visit(node.step)
            
            slice_node = ast.Slice(lower=lower, upper=upper, step=step)
            
        return ast.Subscript(
            value=value,
            slice=slice_node,
            ctx=ast.Load()
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SwitchStmt) -> ast.Match:
        """Handle SwitchStmt nodes."""
        subject = self.visit(node.value)
        
        # Process cases
        cases = []
        for case_node in node.cases.nodes:
            cases.append(self.visit(case_node))
            
        return ast.Match(
            subject=subject,
            cases=cases
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Union[astx.Complex32, astx.Complex64]) -> ast.Name:
        """Handle Complex type nodes."""
        return ast.Name(id="complex", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Union[astx.Float16, astx.Float32, astx.Float64]) -> ast.Name:
        """Handle Float type nodes."""
        return ast.Name(id="float", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Int32) -> ast.Name:
        """Handle Int32 type nodes."""
        return ast.Name(id="int", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.TypeCastExpr) -> ast.Call:
        """Handle TypeCastExpr nodes."""
        target_type = self.visit(node.target_type)
        expr = ast.Name(id=node.expr.name, ctx=ast.Load())
        
        return ast.Call(
            func=ast.Name(id="cast", ctx=ast.Load()),
            args=[target_type, expr],
            keywords=[]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ThrowStmt) -> ast.Raise:
        """Handle ThrowStmt nodes."""
        exc = self.visit(node.exception) if node.exception else None
        return ast.Raise(exc=exc, cause=None)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UnaryOp) -> ast.UnaryOp:
        """Handle UnaryOp nodes."""
        # Map operators
        op_map = {
            "+": ast.UAdd(),
            "-": ast.USub(),
            "~": ast.Invert(),
            "not": ast.Not()
        }
        
        if node.op_code not in op_map:
            raise ValueError(f"Unsupported unary operator: {node.op_code}")
            
        operand = self.visit(node.operand)
        return ast.UnaryOp(op=op_map[node.op_code], operand=operand)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Union[astx.UTF8Char, astx.UTF8String]) -> ast.Name:
        """Handle UTF8Char and UTF8String type nodes."""
        return ast.Name(id="str", ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Variable) -> ast.Name:
        """Handle Variable nodes."""
        return ast.Name(id=node.name, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableAssignment) -> ast.Assign:
        """Handle VariableAssignment nodes."""
        target = ast.Name(id=node.name, ctx=ast.Store())
        value = self.visit(node.value)
        
        return ast.Assign(targets=[target], value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableDeclaration) -> ast.AnnAssign:
        """Handle VariableDeclaration nodes."""
        target = ast.Name(id=node.name, ctx=ast.Store())
        annotation = ast.Name(id=node.value.type_.__class__.__name__, ctx=ast.Load())
        value = self.visit(node.value)
        
        # Add to the current scope
        self._add_to_current_scope(node.name, node.value.type_.__class__.__name__)
        
        return ast.AnnAssign(
            target=target,
            annotation=annotation,
            value=value,
            simple=1
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WalrusOp) -> ast.NamedExpr:
        """Handle Walrus operator."""
        target = self.visit(node.lhs)
        # Ensure target has Store context
        if isinstance(target, ast.Name):
            target.ctx = ast.Store()
            
        value = self.visit(node.rhs)
        return ast.NamedExpr(target=target, value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileExpr) -> ast.ListComp:
        """Handle WhileExpr nodes."""
        if len(node.body) > 1:
            raise ValueError(
                "WhileExpr in Python just accept 1 node in the body attribute."
            )
            
        # Create a list comprehension with iter(lambda: condition, False)
        condition = self.visit(node.condition)
        
        # Create lambda
        lambda_args = ast.arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None
        )
        lambda_body = condition
        lambda_node = ast.Lambda(args=lambda_args, body=lambda_body)
        
        # Create iter call
        iter_call = ast.Call(
            func=ast.Name(id="iter", ctx=ast.Load()),
            args=[
                lambda_node,
                ast.Constant(value=False)
            ],
            keywords=[]
        )
        
        # Create the generator
        generator = ast.comprehension(
            target=ast.Name(id="_", ctx=ast.Store()),
            iter=iter_call,
            ifs=[],
            is_async=0
        )
        
        # Visit the body expression
        elt = self.visit(node.body.nodes[0])
        
        return ast.ListComp(elt=elt, generators=[generator])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileStmt) -> ast.While:
        """Handle WhileStmt nodes."""
        test = self.visit(node.condition)
        
        # Process body
        body = self.visit(node.body)
        if not isinstance(body, list):
            body = [body]
            
        return ast.While(
            test=test,
            body=body,
            orelse=[]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldExpr) -> ast.Yield:
        """Handle YieldExpr nodes."""
        value = self.visit(node.value) if node.value else None
        return ast.Yield(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Union[astx.Date, astx.Time, astx.Timestamp, astx.DateTime]) -> ast.Name:
        """Handle Date/Time type nodes."""
        type_map = {
            astx.Date: "date",
            astx.Time: "time",
            astx.Timestamp: "datetime",
            astx.DateTime: "datetime"
        }
        return ast.Name(id=type_map[type(node)], ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDate) -> ast.Call:
        """Handle LiteralDate nodes."""
        # datetime.strptime(...).date()
        strptime_call = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="datetime", ctx=ast.Load()),
                attr="strptime",
                ctx=ast.Load()
            ),
            args=[
                ast.Constant(value=node.value),
                ast.Constant(value="%Y-%m-%d")
            ],
            keywords=[]
        )
        
        return ast.Call(
            func=ast.Attribute(
                value=strptime_call,
                attr="date",
                ctx=ast.Load()
            ),
            args=[],
            keywords=[]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTime) -> ast.Call:
        """Handle LiteralTime nodes."""
        # datetime.strptime(...).time()
        strptime_call = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="datetime", ctx=ast.Load()),
                attr="strptime",
                ctx=ast.Load()
            ),
            args=[
                ast.Constant(value=node.value),
                ast.Constant(value="%H:%M:%S")
            ],
            keywords=[]
        )
        
        return ast.Call(
            func=ast.Attribute(
                value=strptime_call,
                attr="time",
                ctx=ast.Load()
            ),
            args=[],
            keywords=[]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Union[astx.LiteralTimestamp, astx.LiteralDateTime]) -> ast.Call:
        """Handle LiteralTimestamp and LiteralDateTime nodes."""
        format_map = {
            astx.LiteralTimestamp: "%Y-%m-%d %H:%M:%S",
            astx.LiteralDateTime: "%Y-%m-%dT%H:%M:%S"
        }
        
        # datetime.strptime(...)
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="datetime", ctx=ast.Load()),
                attr="strptime",
                ctx=ast.Load()
            ),
            args=[
                ast.Constant(value=node.value),
                ast.Constant(value=format_map[type(node)])
            ],
            keywords=[]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ParenthesizedExpr) -> ast.AST:
        """Handle ParenthesizedExpr nodes."""
        # In Python AST, parentheses don't have their own node type
        # Just return the inner expression
        return self.visit(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AndOp) -> ast.BoolOp:
        """Handle AndOp nodes."""
        values = [self.visit(node.lhs), self.visit(node.rhs)]
        return ast.BoolOp(op=ast.And(), values=values)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.OrOp) -> ast.BoolOp:
        """Handle OrOp nodes."""
        values = [self.visit(node.lhs), self.visit(node.rhs)]
    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NandOp) -> ast.BoolOp:
        """Handle NandOp nodes."""
        values = [self.visit(node.lhs), self.visit(node.rhs)]
        return ast.UnaryOp(op=ast.Not(), operand=ast.BoolOp(op=ast.And(), values=values))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NorOp) -> ast.BoolOp:
        """Handle NorOp nodes."""
        values = [self.visit(node.lhs), self.visit(node.rhs)]
        return ast.UnaryOp(op=ast.Not(), operand=ast.BoolOp(op=ast.Or(), values=values))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.XnorOp) -> ast.BoolOp:
        """Handle XnorOp nodes."""
        values = [self.visit(node.lhs), self.visit(node.rhs)]
        return ast.UnaryOp(op=ast.Not(), operand=ast.BinOp(left=values[0], op=ast.BitXor(), right=values[1]))

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.MatchStmt) -> ast.Match:
        """Handle MatchStmt nodes."""
        subject = self.visit(node.value)
        cases = [self.visit(case) for case in node.cases.nodes]
        return ast.Match(subject=subject, cases=cases)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WithStmt) -> ast.With:
        """Handle WithStmt nodes."""
        items = [ast.withitem(context_expr=self.visit(item.context_expr), optional_vars=self.visit(item.optional_vars) if item.optional_vars else None) for item in node.items]
        body = self.visit(node.body)
        if not isinstance(body, list):
            body = [body]
        return ast.With(items=items, body=body)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BreakStmt) -> ast.Break:
        """Handle BreakStmt nodes."""
        return ast.Break()

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ContinueStmt) -> ast.Continue:
        """Handle ContinueStmt nodes."""
        return ast.Continue()
    
# if __name__ == "__main__":
#     import astx

#     transpiler = ASTxPythonASTTranspiler()
#     test_nodes = [
#         astx.NandOp(lhs=astx.Identifier(value='a'), rhs=astx.Identifier(value='b')),
#         astx.MatchStmt(value=astx.Identifier(value='x'), cases=astx.Block(nodes=[])),
#         astx.BreakStmt(),
#         astx.ContinueStmt()
#     ]

#     for node in test_nodes:
#         py_ast = transpiler.visit(node)
#         print(ast.dump(py_ast, indent=4))