"""ASTx to Python AST transpiler."""

import ast
from typing import List

import astx
from astx.tools.typing import typechecked
from plum import dispatch


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
        from astx_transpilers.python_string import ASTxPythonTranspiler
        
        # Convert to string first
        python_string = ASTxPythonTranspiler().visit(node)
        
        # Parse the string to get an AST
        module = ast.parse(python_string)
        
        # Return the first node in the module
        if isinstance(module.body[0], ast.Expr):
            return module.body[0].value
        return module.body[0]
    
    def _convert_block(self, block: astx.ASTNodes) -> List[ast.stmt]:
        """Convert a block of statements to Python AST nodes."""
        result = []
        for node in block.nodes:
            converted = self.visit(node)
            if isinstance(converted, list):
                result.extend(converted)
            else:
                result.append(converted)
        return result

    @dispatch.abstract
    def visit(self, expr: astx.AST) -> ast.AST:
        """Translate an ASTx node to a Python AST node."""
        raise Exception(f"Not implemented yet ({expr}).")

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AliasExpr) -> ast.alias:
        """Handle AliasExpr nodes."""
        return ast.alias(name=node.name, asname=node.asname)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AndOp) -> ast.BoolOp:
        """Handle AndOp nodes."""
        return ast.BoolOp(
            op=ast.And(),
            values=[self.visit(node.lhs), self.visit(node.rhs)]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AssignmentExpr) -> ast.Assign:
        """Handle AssignmentExpr nodes."""
        targets = [ast.Name(id=target.name, ctx=ast.Store()) 
                  for target in node.targets]
        value = self.visit(node.value)
        return ast.Assign(targets=targets, value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ASTNodes) -> List[ast.AST]:
        """Handle ASTNodes nodes."""
        return [self.visit(n) for n in node.nodes]
    
    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AugAssign) -> ast.AugAssign:
        """Handle AugAssign nodes."""
        op_map = {
            '+=': ast.Add(),
            '-=': ast.Sub(),
            '*=': ast.Mult(),
            '/=': ast.Div(),
            '//=': ast.FloorDiv(),
            '%=': ast.Mod(),
            '**=': ast.Pow(),
            '<<=': ast.LShift(),
            '>>=': ast.RShift(),
            '|=': ast.BitOr(),
            '&=': ast.BitAnd(),
            '^=': ast.BitXor(),
        }
        
        target = self.visit(node.target)
        if isinstance(target, ast.Name):
            target.ctx = ast.Store()
            
        value = self.visit(node.value)
        return ast.AugAssign(
            target=target,
            op=op_map.get(node.op_code, ast.Add()),
            value=value
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AwaitExpr) -> ast.Await:
        """Handle AwaitExpr nodes."""
        value = self.visit(node.value)
        return ast.Await(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BinaryOp) -> ast.BinOp:
        """Handle BinaryOp nodes."""
        op_map = {
            '+': ast.Add(),
            '-': ast.Sub(),
            '*': ast.Mult(),
            '/': ast.Div(),
            '//': ast.FloorDiv(),
            '%': ast.Mod(),
            '**': ast.Pow(),
            '<<': ast.LShift(),
            '>>': ast.RShift(),
            '|': ast.BitOr(),
            '&': ast.BitAnd(),
            '^': ast.BitXor(),
        }
        
        if node.op_code not in op_map:
            return self._convert_using_unparse(node)
            
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return ast.BinOp(left=lhs, op=op_map[node.op_code], right=rhs)

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
        bases = []
        keywords = []
        
        if node.is_abstract:
            bases.append(ast.Name(id="ABC", ctx=ast.Load()))
            
        body = self._convert_block(node.body)
        
        return ast.ClassDef(
            name=node.name,
            bases=bases,
            keywords=keywords,
            body=body,
            decorator_list=[]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.CompareOp) -> ast.Compare:
        """Handle CompareOp nodes."""
        op_map = {
            '==': ast.Eq(),
            '!=': ast.NotEq(),
            '<': ast.Lt(),
            '<=': ast.LtE(),
            '>': ast.Gt(),
            '>=': ast.GtE(),
            'in': ast.In(),
            'not in': ast.NotIn(),
            'is': ast.Is(),
            'is not': ast.IsNot(),
        }
        
        ops = [op_map.get(op, ast.Eq()) for op in node.ops]
        comparators = [
            self.visit(comparator) for comparator in node.comparators
        ]
        
        return ast.Compare(
            left=self.visit(node.left),
            ops=ops,
            comparators=comparators
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ContinueStmt) -> ast.Continue:
        """Handle ContinueStmt nodes."""
        return ast.Continue()

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionCall) -> ast.Call:
        """Handle FunctionCall nodes."""
        func = ast.Name(id=node.fn.name, ctx=ast.Load())
        args = [self.visit(arg) for arg in node.args]
        keywords = []
        return ast.Call(func=func, args=args, keywords=keywords)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionDef) -> ast.FunctionDef:
        """Handle FunctionDef nodes."""
        # Process arguments
        arguments = ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg=arg.name, annotation=None)
                for arg in node.prototype.args.nodes
            ],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None
        )
        
        # Process return type annotation if present
        returns = None
        if node.prototype.return_type:
            returns = self.visit(node.prototype.return_type)
            
        # Process function body
        body = self._convert_block(node.body)
        if not body:
            body = [ast.Pass()]
            
        return ast.FunctionDef(
            name=node.name,
            args=arguments,
            body=body,
            decorator_list=[],
            returns=returns,
            type_comment=None
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionAsyncDef) -> ast.AsyncFunctionDef:
        """Handle FunctionAsyncDef nodes."""
        # Process arguments
        arguments = ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg=arg.name, annotation=None)
                for arg in node.prototype.args.nodes
            ],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None
        )
        
        # Process return type annotation if present
        returns = None
        if node.prototype.return_type:
            returns = self.visit(node.prototype.return_type)
            
        # Process function body
        body = self._convert_block(node.body)
        if not body:
            body = [ast.Pass()]
            
        return ast.AsyncFunctionDef(
            name=node.name,
            args=arguments,
            body=body,
            decorator_list=[],
            returns=returns,
            type_comment=None
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionReturn) -> ast.Return:
        """Handle FunctionReturn nodes."""
        value = self.visit(node.value) if node.value else None
        return ast.Return(value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfExpr) -> ast.IfExp:
        """Handle IfExpr nodes."""
        if node.then and len(node.then) == 1:
            then_value = self.visit(node.then[0])
        else:
            then_value = self._convert_using_unparse(node.then)
            
        if node.else_ and len(node.else_) == 1:
            else_value = self.visit(node.else_[0])
        else:
            else_value = self._convert_using_unparse(node.else_)
            
        return ast.IfExp(
            test=self.visit(node.condition),
            body=then_value,
            orelse=else_value
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfStmt) -> ast.If:
        """Handle IfStmt nodes."""
        then_body = self._convert_block(node.then)
        else_body = self._convert_block(node.else_) if node.else_ else []
        
        return ast.If(
            test=self.visit(node.condition),
            body=then_body,
            orelse=else_body
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportStmt) -> ast.Import:
        """Handle ImportStmt nodes."""
        names = [self.visit(name) for name in node.names]
        return ast.Import(names=names)

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
    def visit(self, node: astx.LiteralBoolean) -> ast.Constant:
        """Handle LiteralBoolean nodes."""
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt32) -> ast.Constant:
        """Handle LiteralInt32 nodes."""
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat32) -> ast.Constant:
        """Handle LiteralFloat32 nodes."""
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralString) -> ast.Constant:
        """Handle LiteralString nodes."""
        return ast.Constant(value=node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralList) -> ast.List:
        """Handle LiteralList nodes."""
        elements = [self.visit(element) for element in node.elements]
        return ast.List(elts=elements, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTuple) -> ast.Tuple:
        """Handle LiteralTuple nodes."""
        elements = [self.visit(element) for element in node.elements]
        return ast.Tuple(elts=elements, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDict) -> ast.Dict:
        """Handle LiteralDict nodes."""
        keys = [self.visit(key) for key in node.elements.keys()]
        values = [self.visit(value) for value in node.elements.values()]
        return ast.Dict(keys=keys, values=values)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralSet) -> ast.Set:
        """Handle LiteralSet nodes."""
        elements = [self.visit(element) for element in node.elements]
        return ast.Set(elts=elements)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.OrOp) -> ast.BoolOp:
        """Handle OrOp nodes."""
        return ast.BoolOp(
            op=ast.Or(),
            values=[self.visit(node.lhs), self.visit(node.rhs)]
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SubscriptExpr) -> ast.Subscript:
        """Handle SubscriptExpr nodes."""
        value = self.visit(node.value)
        
        # Handle simple indexing
        if not isinstance(node.index, astx.LiteralNone):
            index = self.visit(node.index)
            return ast.Subscript(value=value, slice=index, ctx=ast.Load())
        
        # Handle slicing
        lower = (self.visit(node.lower) 
                if not isinstance(node.lower, astx.LiteralNone) 
                else None)
        upper = (self.visit(node.upper) 
                if not isinstance(node.upper, astx.LiteralNone) 
                else None)
        step = (self.visit(node.step)
                if not isinstance(node.step, astx.LiteralNone)
                else None)
        
        slice_obj = ast.Slice(lower=lower, upper=upper, step=step)
        return ast.Subscript(value=value, slice=slice_obj, ctx=ast.Load())

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UnaryOp) -> ast.UnaryOp:
        """Handle UnaryOp nodes."""
        op_map = {
            '-': ast.USub(),
            '+': ast.UAdd(),
            '~': ast.Invert(),
            'not': ast.Not(),
        }
        
        if node.op_code not in op_map:
            return self._convert_using_unparse(node)
            
        operand = self.visit(node.operand)
        return ast.UnaryOp(op=op_map[node.op_code], operand=operand)

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
    def visit(self, node: astx.WalrusOp) -> ast.NamedExpr:
        """Handle WalrusOp nodes."""
        target = self.visit(node.lhs)
        if isinstance(target, ast.Name):
            target.ctx = ast.Store()
        value = self.visit(node.rhs)
        return ast.NamedExpr(target=target, value=value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileStmt) -> ast.While:
        """Handle WhileStmt nodes."""
        test = self.visit(node.condition)
        body = self._convert_block(node.body)
        
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
    def visit(self, node: astx.YieldStmt) -> ast.Expr:
        """Handle YieldStmt nodes."""
        value = self.visit(node.value) if node.value else None
        yield_expr = ast.Yield(value=value)
        return ast.Expr(value=yield_expr)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldFromExpr) -> ast.YieldFrom:
        """Handle YieldFromExpr nodes."""
        value = self.visit(node.value)
        return ast.YieldFrom(value=value)

    # For nodes that aren't directly implemented, use the unparse approach
    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AST) -> ast.AST:
        """Handle any other AST nodes by using unparse."""
        return self._convert_using_unparse(node)