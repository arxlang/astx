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
        if node.op_code not in OP_MAP:
            raise ValueError(f"Unsupported binary operator: {node.op_code}")

        return ast.BinOp(
            left=self.visit(node.lhs),
            op=OP_MAP[node.op_code],
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

    @dispatch
    def visit(self, node: astx.EllipsisLiteral) -> ast.Constant:
        """Handle Ellipsis (`...`) in type hints and NumPy slices."""
        return ast.Constant(value=Ellipsis)


    @dispatch
    def visit(self, node: astx.WalrusOp) -> ast.NamedExpr:
        """Handle Named Expressions (`x := y`)."""
        return ast.NamedExpr(target=self.visit(node.lhs), value=self.visit(node.rhs))


    @dispatch
    def visit(self, node: astx.FStringExpr) -> ast.JoinedStr:
        """Handle Python F-Strings (`f"Hello {x}"`)."""
        values = [self.visit(part) for part in node.parts]  # Convert f-string parts
        return ast.JoinedStr(values=values)


    @dispatch
    def visit(self, node: astx.ListUnpacking) -> ast.Starred:
        """Handle List Unpacking (`*args`, `*items`)."""
        return ast.Starred(value=self.visit(node.value), ctx=ast.Load())


    @dispatch
    def visit(self, node: astx.DictMergeOp) -> ast.BinOp:
        """Handle Dictionary Merging (`dict1 |= dict2`)."""
        return ast.BinOp(
            left=self.visit(node.lhs),
            op=ast.BitOr(),  # `|` operator for dict merging
            right=self.visit(node.rhs)
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
    @dispatch
    def visit(self, node: astx.ForElseStmt) -> ast.For:
        """Handle For-Else blocks (`for x in items: ... else: ...`)."""
        return ast.For(
            target=self.visit(node.target),
            iter=self.visit(node.iterable),
            body=[self.visit(stmt) for stmt in node.body],
            orelse=[self.visit(stmt) for stmt in node.orelse]
        )


    @dispatch
    def visit(self, node: astx.WhileElseStmt) -> ast.While:
        """Handle While-Else blocks (`while condition: ... else: ...`)."""
        return ast.While(
            test=self.visit(node.condition),
            body=[self.visit(stmt) for stmt in node.body],
            orelse=[self.visit(stmt) for stmt in node.orelse]
        )


    @dispatch
    def visit(self, node: astx.TryElseStmt) -> ast.Try:
        """Handle Try-Else statements (`try: ... else: ...`)."""
        return ast.Try(
            body=[self.visit(stmt) for stmt in node.body],
            handlers=[self.visit(handler) for handler in node.handlers],
            orelse=[self.visit(stmt) for stmt in node.orelse],
            finalbody=[]
        )


    @dispatch
    def visit(self, node: astx.NestedTryStmt) -> ast.Try:
        """Handle Nested Try-Except (`try: try: ... except: ... except: ...`)."""
        inner_try = ast.Try(
            body=[self.visit(stmt) for stmt in node.inner_body],
            handlers=[self.visit(handler) for handler in node.inner_handlers],
            orelse=[self.visit(stmt) for stmt in node.inner_orelse],
            finalbody=[self.visit(stmt) for stmt in node.inner_finalbody]
        )

        return ast.Try(
            body=[inner_try],
            handlers=[self.visit(handler) for handler in node.outer_handlers],
            orelse=[self.visit(stmt) for stmt in node.outer_orelse],
            finalbody=[self.visit(stmt) for stmt in node.outer_finalbody]
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

    @dispatch
    def visit(self, node: astx.NestedWithStmt) -> ast.With:
        """Handle Nested Context Managers (`with open(), open():`)."""
        return ast.With(
            items=[ast.withitem(context_expr=self.visit(expr)) for expr in node.contexts],
            body=[self.visit(stmt) for stmt in node.body]
        )


    @dispatch
    def visit(self, node: astx.DynamicRaiseStmt) -> ast.Raise:
        """Handle Dynamic Exception Raising (`raise Exception(f"Error: {x}")`)."""
        return ast.Raise(
            exc=ast.Call(
                func=ast.Name(id=node.exception_type, ctx=ast.Load()),
                args=[self.visit(node.message)],
                keywords=[]
            ),
            cause=None
        )


    @dispatch
    def visit(self, node: astx.DeleteStmt) -> ast.Delete:
        """Handle `del` Statements (`del x`)."""
        return ast.Delete(targets=[self.visit(target) for target in node.targets])


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

    @dispatch
    def visit(self, node: astx.FunctionWithDecorators) -> ast.FunctionDef:
        """Handle Function Decorators (`@staticmethod`, `@property`)."""
        return ast.FunctionDef(
            name=node.name,
            args=self.visit(node.args),
            body=[self.visit(stmt) for stmt in node.body],
            decorator_list=[self.visit(decorator) for decorator in node.decorators],
        )


    @dispatch
    def visit(self, node: astx.ClassWithDecorators) -> ast.ClassDef:
        """Handle Class Decorators (`@dataclass`)."""
        return ast.ClassDef(
            name=node.name,
            bases=[self.visit(base) for base in node.bases],
            keywords=[],
            body=[self.visit(stmt) for stmt in node.body],
            decorator_list=[self.visit(decorator) for decorator in node.decorators],
        )

    @dispatch
    def visit(self, node: astx.LambdaWithDefaults) -> ast.Lambda:
        """Handle Lambda Functions with Default Arguments (`lambda x=10: x+1`)."""
        return ast.Lambda(
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg=param.name, annotation=None) for param in node.params],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[self.visit(param.default) if param.default else ast.Constant(value=None) for param in node.params] 
            ),
            body=self.visit(node.body)
        )
    @dispatch
    def visit(self, node: astx.ClassWithMetaclass) -> ast.ClassDef:
        """Handle Metaclasses (`class C(metaclass=Meta)`)."""
        return ast.ClassDef(
            name=node.name,
            bases=[self.visit(base) for base in node.bases],
            keywords=[
                ast.keyword(arg="metaclass", value=ast.Name(id=node.metaclass, ctx=ast.Load()))
            ],
            body=[self.visit(stmt) for stmt in node.body],
            decorator_list=[self.visit(decorator) for decorator in node.decorators]
        )


    @dispatch
    def visit(self, node: astx.OverloadedOperator) -> ast.FunctionDef:
        """Handle Overloaded Operators (`__add__`, `__sub__`, `__mul__`)."""
        return ast.FunctionDef(
            name=node.operator,
            args=self.visit(node.args),
            body=[self.visit(stmt) for stmt in node.body],
            decorator_list=[]
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
    @dispatch
    def visit(self, node: astx.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        """Handle Async Function Definitions (`async def`)."""
        return ast.AsyncFunctionDef(
            name=node.name,
            args=self.visit(node.args),
            body=[self.visit(stmt) for stmt in node.body],
            decorator_list=[self.visit(decorator) for decorator in node.decorators],
            returns=self.visit(node.return_type) if node.return_type else None
        )


    @dispatch
    def visit(self, node: astx.AwaitExpr) -> ast.Await:
        """Handle Await Expressions (`await x()`)."""
        return ast.Await(value=self.visit(node.value))


    @dispatch
    def visit(self, node: astx.AsyncForStmt) -> ast.AsyncFor:
        """Handle Async For Loops (`async for`)."""
        return ast.AsyncFor(
            target=self.visit(node.target),
            iter=self.visit(node.iterable),
            body=[self.visit(stmt) for stmt in node.body],
            orelse=[self.visit(stmt) for stmt in node.orelse]
        )


    @dispatch
    def visit(self, node: astx.AsyncWithStmt) -> ast.AsyncWith:
        """Handle Async With Statements (`async with`)."""
        return ast.AsyncWith(
            items=[ast.withitem(context_expr=self.visit(expr), optional_vars=self.visit(var) if var else None) for expr, var in node.items],
            body=[self.visit(stmt) for stmt in node.body]
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

    @dispatch
    def find_unused_variables(self, node: astx.Module) -> set:
        """Detect declared but never used variables."""
        declared = set()
        used = set()

        class VariableTracker(ast.NodeVisitor):
            def visit_Assign(self, node):
                if isinstance(node.targets[0], ast.Name):
                    declared.add(node.targets[0].id)

            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    used.add(node.id)

        VariableTracker().visit(node)
        return declared - used


    @dispatch
    def visit(self, node: astx.InfiniteLoopCheck) -> ast.While:
        """Detect Infinite Loops (`while True:` with no `break`)."""
        has_break = any(isinstance(stmt, ast.Break) for stmt in node.body)
        if not has_break:
            raise ValueError("Infinite loop detected: `while True:` without `break`.")

        return ast.While(
            test=ast.Constant(value=True),
            body=[self.visit(stmt) for stmt in node.body],
            orelse=[]
        )


    @dispatch
    def visit(self, node: astx.UndefinedVarCheck) -> ast.Name:
        """Ensure variables are defined before use."""
        if node.id not in self.symbol_table:
            raise NameError(f"Undefined variable: {node.id}")

        return ast.Name(id=node.id, ctx=ast.Load())


    @dispatch
    def visit(self, node: astx.TypeInference) -> ast.AnnAssign:
        """Infer types based on assignments (`x: int = 10`)."""
        inferred_type = self._infer_type(node.value)
        return ast.AnnAssign(
            target=ast.Name(id=node.name, ctx=ast.Store()),
            annotation=ast.Name(id=inferred_type, ctx=ast.Load()),
            value=self.visit(node.value),
            simple=1
        )


    def _infer_type(self, value):
        """Helper method to infer type from value."""
        if isinstance(value, ast.Constant):
            if isinstance(value.value, int):
                return "int"
            if isinstance(value.value, float):
                return "float"
            if isinstance(value.value, str):
                return "str"
            if isinstance(value.value, bool):
                return "bool"
        return "Any"
    @dispatch
    def visit(self, node: astx.SetOperation) -> ast.AugAssign:
        """Handle Set Operations (`&=, |=, -=, ^=`)."""
        op_map = {
            "&=": ast.BitAnd(),
            "|=": ast.BitOr(),
            "-=": ast.Sub(),
            "^=": ast.BitXor()
        }

        if node.operator not in op_map:
            raise ValueError(f"Unsupported set operation: {node.operator}")

        return ast.AugAssign(
            target=self.visit(node.target),
            op=op_map[node.operator],
            value=self.visit(node.value)
        )


    @dispatch
    def visit(self, node: astx.DynamicExec) -> ast.Expr:
        """Handle Dynamic Code Execution (`exec(code)`)."""
        return ast.Expr(
            value=ast.Call(
                func=ast.Name(id="exec", ctx=ast.Load()),
                args=[self.visit(node.code)],
                keywords=[]
            )
        )


    @dispatch
    def visit(self, node: astx.DynamicEval) -> ast.Expr:
        """Handle Dynamic Evaluation (`eval(code)`)."""
        return ast.Expr(
            value=ast.Call(
                func=ast.Name(id="eval", ctx=ast.Load()),
                args=[self.visit(node.code)],
                keywords=[]
            )
        )


    @dispatch
    def visit(self, node: astx.SetTrace) -> ast.Expr:
        """Handle Python Debugging (`sys.settrace(trace_func)`)."""
        return ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="sys", ctx=ast.Load()),
                    attr="settrace",
                    ctx=ast.Load()
                ),
                args=[self.visit(node.trace_func)],
                keywords=[]
            )
        )
    @dispatch
    def visit(self, node: astx.PartialFunction) -> ast.Call:
        """Handle Function Partial Application (`functools.partial`)."""
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="functools", ctx=ast.Load()),
                attr="partial",
                ctx=ast.Load()
            ),
            args=[self.visit(node.func)] + [self.visit(arg) for arg in node.args],
            keywords=[]
        )


    @dispatch
    def visit(self, node: astx.HigherOrderFunction) -> ast.Call:
        """Handle Higher-Order Functions (`map`, `filter`, `reduce`)."""
        if node.func_name not in {"map", "filter", "reduce"}:
            raise ValueError(f"Unsupported higher-order function: {node.func_name}")

        return ast.Call(
            func=ast.Name(id=node.func_name, ctx=ast.Load()),
            args=[self.visit(node.lambda_func), self.visit(node.iterable)],
            keywords=[]
        )


    @dispatch
    def visit(self, node: astx.PatternMatchStmt) -> ast.Match:
        """Handle Pattern Matching (`match x:`)."""
        return ast.Match(
            subject=self.visit(node.subject),
            cases=[self.visit(case) for case in node.cases]
        )


    @dispatch
    def visit(self, node: astx.MatchCaseStmt) -> ast.match_case:
        """Handle `case` in Pattern Matching (`case 1, case _: ...`)."""
        return ast.match_case(
            pattern=self.visit(node.pattern),
            guard=self.visit(node.guard) if node.guard else None,
            body=[self.visit(stmt) for stmt in node.body]
        )
    @dispatch
    def visit(self, node: astx.GarbageCollection) -> ast.Expr:
        """Handle Garbage Collection Control (`gc.collect()`)."""
        return ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="gc", ctx=ast.Load()), attr="collect", ctx=ast.Load()
                ),
                args=[],
                keywords=[]
            )
        )


    @dispatch
    def visit(self, node: astx.HeapStackAnalysis) -> ast.Expr:
        """Handle Heap & Stack Analysis (`sys._getframe()`)."""
        return ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="sys", ctx=ast.Load()), attr="_getframe", ctx=ast.Load()
                ),
                args=[ast.Constant(value=node.depth) if node.depth is not None else ast.Constant(value=0)],
                keywords=[]
            )
        )


    @dispatch
    def visit(self, node: astx.SymbolTableManagement) -> ast.Expr:
        """Handle Symbol Table Management (`symtable.symtable()`)."""
        return ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="symtable", ctx=ast.Load()), attr="symtable", ctx=ast.Load()
                ),
                args=[self.visit(node.source_code), ast.Constant(value=node.type)],
                keywords=[]
            )
        )


    @dispatch
    def visit(self, node: astx.DynamicVariableResolution) -> ast.Expr:
        """Handle Dynamic Variable Resolution (`globals()`, `locals()`)."""
        if node.scope == "globals":
            func_name = "globals"
        elif node.scope == "locals":
            func_name = "locals"
        else:
            raise ValueError(f"Unsupported dynamic scope resolution: {node.scope}")

        return ast.Expr(
            value=ast.Call(
                func=ast.Name(id=func_name, ctx=ast.Load()),
                args=[],
                keywords=[]
            )
        )
    @dispatch
    def visit(self, node: astx.BytecodeExec) -> ast.Expr:
        """Handle Bytecode Execution (`exec(bytecode)`)."""
        return ast.Expr(
            value=ast.Call(
                func=ast.Name(id="exec", ctx=ast.Load()),
                args=[self.visit(node.bytecode)],
                keywords=[]
            )
        )


    @dispatch
    def visit(self, node: astx.RawBytes) -> ast.Bytes:
        """Handle Raw Byte Objects (`b'hello'`)."""
        return ast.Bytes(s=node.value)


    @dispatch
    def visit(self, node: astx.DynamicMetaclass) -> ast.Call:
        """Handle Dynamic Metaclasses (`type("NewClass", (Base,), {})`)."""
        return ast.Call(
            func=ast.Name(id="type", ctx=ast.Load()),
            args=[
                ast.Constant(value=node.name),
                ast.Tuple(elts=[self.visit(base) for base in node.bases], ctx=ast.Load()),
                ast.Dict(keys=[ast.Constant(k) for k in node.attrs.keys()], values=[self.visit(v) for v in node.attrs.values()])
            ],
            keywords=[]
        )


    @dispatch
    def visit(self, node: astx.PointerArithmetic) -> ast.Call:
        """Handle Pointer Arithmetic using C FFI (`ctypes` or `cffi`)."""
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="ctypes", ctx=ast.Load()),
                attr=node.operation,
                ctx=ast.Load()
            ),
            args=[self.visit(node.pointer), self.visit(node.offset)],
            keywords=[]
        )
    @dispatch
    def visit(self, node: astx.HigherOrderFunction) -> ast.FunctionDef:
        """Handle Higher-Order Functions (functions that take/return functions)."""
        return ast.FunctionDef(
            name=node.name,
            args=self.visit(node.args),
            body=[self.visit(stmt) for stmt in node.body],
            decorator_list=[self.visit(decorator) for decorator in node.decorators],
            returns=self.visit(node.return_type) if node.return_type else None
        )


    @dispatch
    def visit(self, node: astx.CurryingFunction) -> ast.Call:
        """Handle Function Currying (`functools.partial`)."""
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="functools", ctx=ast.Load()),
                attr="partial",
                ctx=ast.Load()
            ),
            args=[self.visit(node.func)] + [self.visit(arg) for arg in node.args],
            keywords=[]
        )


    @dispatch
    def visit(self, node: astx.MemoizedFunction) -> ast.FunctionDef:
        """Handle Function Memoization (`@lru_cache`)."""
        return ast.FunctionDef(
            name=node.name,
            args=self.visit(node.args),
            body=[self.visit(stmt) for stmt in node.body],
            decorator_list=[
                ast.Call(
                    func=ast.Name(id="lru_cache", ctx=ast.Load()), args=[], keywords=[]
                )
            ],
            returns=self.visit(node.return_type) if node.return_type else None
        )
    @dispatch
    def visit(self, node: astx.LazyEvaluation) -> ast.Call:
        """Handle Lazy Evaluation Pipelines (`lazy_eval(lambda: expr)`)."""
        return ast.Call(
            func=ast.Name(id="lazy_eval", ctx=ast.Load()),
            args=[self.visit(node.expr)],
            keywords=[]
        )


    @dispatch
    def visit(self, node: astx.NumPyVectorization) -> ast.Call:
        """Handle Automatic NumPy Vectorization (`np.vectorize(function)`)."""
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="np", ctx=ast.Load()), attr="vectorize", ctx=ast.Load()
            ),
            args=[self.visit(node.func)],
            keywords=[]
        )


    @dispatch
    def visit(self, node: astx.ParallelExecution) -> ast.AsyncFor:
        """Handle Parallel Execution of Expressions (`async for` in multiprocessing)."""
        return ast.AsyncFor(
            target=self.visit(node.target),
            iter=self.visit(node.iterable),
            body=[self.visit(stmt) for stmt in node.body],
            orelse=[]
        )
    @dispatch
    def visit(self, node: astx.AICodeGeneration) -> ast.Expr:
        """Handle AI-Based Code Generation (`exec(ast.unparse())`)."""
        generated_code = call_openai_gpt(node.prompt)
        return ast.Expr(
            value=ast.Call(
                func=ast.Name(id="exec", ctx=ast.Load()),
                args=[ast.Call(
                    func=ast.Name(id="ast.unparse", ctx=ast.Load()),
                    args=[ast.parse(generated_code)],
                    keywords=[]
                )],
                keywords=[]
            )
        )


    @dispatch
    def visit(self, node: astx.AutonomousRefactoring) -> ast.Module:
        """Handle Autonomous Code Refactoring (`Rewrite inefficient code dynamically`)."""
        optimized_code = ai_refactor_tool(ast.unparse(node.code))
        return ast.parse(optimized_code)


    @dispatch
    def visit(self, node: astx.BugPrediction) -> ast.Expr:
        """Handle AI Bug Prediction (`Use AI to detect potential errors`)."""
        detected_issues = lint_code_with_gpt(ast.unparse(node.code))
        return ast.Expr(
            value=ast.Call(
                func=ast.Name(id="print", ctx=ast.Load()),
                args=[ast.Constant(value=detected_issues)],
                keywords=[]
            )
        )
    @dispatch
    def visit(self, node: astx.AIAssistedDocstring) -> ast.FunctionDef:
        """Handle AI-Assisted Code Documentation (Generate docstrings with AI)."""
        ai_docstring = generate_docstring_with_ai(ast.unparse(node.func_body))
        return ast.FunctionDef(
            name=node.name,
            args=self.visit(node.args),
            body=[ast.Expr(value=ast.Constant(value=ai_docstring))] + [self.visit(stmt) for stmt in node.body],
            decorator_list=[],
            returns=self.visit(node.return_type) if node.return_type else None
        )


    @dispatch
    def visit(self, node: astx.AIBugFixing) -> ast.Module:
        """Handle AI-Based Bug Fixing (GPT-4 automatically fixes detected bugs)."""
        fixed_code = fix_bugs_with_gpt(ast.unparse(node.code))
        return ast.parse(fixed_code)


    @dispatch
    def visit(self, node: astx.ASTOptimization) -> ast.Module:
        """Handle AST-Based Optimization (Remove redundant operations dynamically)."""
        optimized_ast = optimize_ast_tree(node.ast_tree)
        return optimized_ast
