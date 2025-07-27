"""ASTx Python AST transpiler implementation."""

import ast
import astx
from astx_transpilers.python_to_ast import ASTxPythonASTTranspiler


class TestAdditionalControlFlowNodes:
    """Test additional control flow node types."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = ASTxPythonASTTranspiler()

    def test_subscript_expr_index(self):
        """Test astx.SubscriptExpr with index."""
        value = astx.Variable(name="arr")
        index = astx.LiteralInt32(value=0)
        node = astx.SubscriptExpr(value=value, index=index)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Subscript)
        assert isinstance(result.value, ast.Name)
        assert result.value.id == "arr"

    def test_subscript_expr_slice(self):
        """Test astx.SubscriptExpr with slice."""
        value = astx.Variable(name="arr")
        lower = astx.LiteralInt32(value=1)
        upper = astx.LiteralInt32(value=5)
        node = astx.SubscriptExpr(value=value, lower=lower, upper=upper)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Subscript)
        assert isinstance(result.slice, ast.Slice)

    def test_do_while_expr_simple(self):
        """Test astx.DoWhileExpr with condition and body."""
        condition = astx.LiteralBoolean(value=True)
        body_expr = astx.Variable(name="result")
        body = astx.Block()
        body.append(body_expr)
        node = astx.DoWhileExpr(condition=condition, body=body)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.ListComp)


class TestAdditionalFunctionNodes:
    """Test additional function-related node types."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = ASTxPythonASTTranspiler()
        self.Variable_42 = 42

    def test_function_return_none(self):
        """Test astx.FunctionReturn with None value."""
        value = astx.LiteralNone()
        node = astx.FunctionReturn(value=value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Return)
        assert isinstance(result.value, ast.Constant)
        assert result.value.value is None

    def test_function_return_simple(self):
        """Test astx.FunctionReturn with value."""
        value = astx.LiteralInt32(value=self.Variable_42)
        node = astx.FunctionReturn(value=value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Return)
        assert isinstance(result.value, ast.Constant)
        assert result.value.value == self.Variable_42


class TestAdditionalLiteralNodes:
    """Test additional literal node types."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = ASTxPythonASTTranspiler()
        self.Variable_42 = 42
        self.Variable_1024 = 1024
        self.Variable_3_14 = 3.14
        self.Variable_2_718281828 = 2.718281828
        self.Variable_2 = 2
        self.Variable_1 = 1
        self.Variable_9223372036854775807 = 9223372036854775807

    def test_literal_date_simple(self):
        """Test astx.LiteralDate with date string."""
        node = astx.LiteralDate(value="2023-12-25")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Call)

    def test_literal_datetime_simple(self):
        """Test astx.LiteralDateTime with datetime string."""
        node = astx.LiteralDateTime(value="2023-12-25T10:30:00")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Call)

    def test_literal_dict_simple(self):
        """Test astx.LiteralDict with key-value pairs."""
        elements = {
            astx.LiteralString(value="key1"): astx.LiteralInt32(
                value=self.Variable_1
            ),
            astx.LiteralString(value="key2"): astx.LiteralInt32(
                value=self.Variable_2
            ),
        }
        node = astx.LiteralDict(elements=elements)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Dict)
        assert len(result.keys) == self.Variable_2
        assert len(result.values) == self.Variable_2

    def test_literal_float32_simple(self):
        """Test astx.LiteralFloat32 with simple value."""
        node = astx.LiteralFloat32(value=self.Variable_3_14)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == self.Variable_3_14

    def test_literal_float64_simple(self):
        """Test astx.LiteralFloat64 with simple value."""
        node = astx.LiteralFloat64(value=self.Variable_2_718281828)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == self.Variable_2_718281828

    def test_literal_int16_simple(self):
        """Test astx.LiteralInt16 with simple value."""
        node = astx.LiteralInt16(value=self.Variable_1024)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == self.Variable_1024

    def test_literal_int64_simple(self):
        """Test astx.LiteralInt64 with simple value."""
        node = astx.LiteralInt64(value=self.Variable_9223372036854775807)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == self.Variable_9223372036854775807

    def test_literal_int8_simple(self):
        """Test astx.LiteralInt8 with simple value."""
        node = astx.LiteralInt8(value=self.Variable_42)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == self.Variable_42

    def test_literal_list_simple(self):
        """Test astx.LiteralList with elements."""
        elements = [
            astx.LiteralInt32(value=self.Variable_1),
            astx.LiteralInt32(value=self.Variable_2),
        ]
        node = astx.LiteralList(elements=elements)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.List)
        assert len(result.elts) == self.Variable_2
        assert isinstance(result.elts[0], ast.Constant)
        assert result.elts[0].value == self.Variable_1

    def test_literal_none_simple(self):
        """Test astx.LiteralNone."""
        node = astx.LiteralNone()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value is None

    def test_literal_set_simple(self):
        """Test astx.LiteralSet with elements."""
        elements = {
            astx.LiteralInt32(value=self.Variable_1),
            astx.LiteralInt32(value=self.Variable_2),
        }
        node = astx.LiteralSet(elements=elements)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Set)
        assert len(result.elts) == self.Variable_2

    def test_literal_time_simple(self):
        """Test astx.LiteralTime with time string."""
        node = astx.LiteralTime(value="10:30:00")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Call)

    def test_literal_timestamp_simple(self):
        """Test astx.LiteralTimestamp with timestamp string."""
        node = astx.LiteralTimestamp(value="2023-12-25 10:30:00")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Call)

    def test_literal_tuple_simple(self):
        """Test astx.LiteralTuple with elements."""
        elements = (
            astx.LiteralInt32(value=self.Variable_1),
            astx.LiteralInt32(value=self.Variable_2),
        )
        node = astx.LiteralTuple(elements=elements)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Tuple)
        assert len(result.elts) == self.Variable_2


class TestAdditionalOperatorNodes:
    """Test additional operator node types."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = ASTxPythonASTTranspiler()
        self.Variable_2 = 2

    def test_not_op_simple(self):
        """Test astx.NotOp with simple operand."""
        operand = astx.LiteralBoolean(value=True)
        node = astx.NotOp(operand=operand)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.UnaryOp)
        assert isinstance(result.op, ast.Not)

    def test_or_op_simple(self):
        """Test astx.OrOp with two operands."""
        lhs = astx.LiteralBoolean(value=True)
        rhs = astx.LiteralBoolean(value=False)
        node = astx.OrOp(lhs=lhs, rhs=rhs)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.BoolOp)
        assert isinstance(result.op, ast.Or)
        assert len(result.values) == self.Variable_2

    def test_unary_op_negation(self):
        """Test astx.UnaryOp with negation."""
        operand = astx.LiteralInt32(value=5)
        node = astx.UnaryOp(op_code="-", operand=operand)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.UnaryOp)
        assert isinstance(result.op, ast.USub)

    def test_unary_op_not(self):
        """Test astx.UnaryOp with not operator."""
        operand = astx.LiteralBoolean(value=True)
        node = astx.UnaryOp(op_code="not", operand=operand)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.UnaryOp)
        assert isinstance(result.op, ast.Not)

    def test_walrus_op_simple(self):
        """Test astx.WalrusOp (assignment expression)."""
        lhs = astx.Variable(name="x")
        rhs = astx.LiteralInt32(value=42)
        node = astx.WalrusOp(lhs=lhs, rhs=rhs)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.NamedExpr)
        assert isinstance(result.target, ast.Name)
        assert result.target.id == "x"


class TestAdditionalVariableNodes:
    """Test additional variable-related node types."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = ASTxPythonASTTranspiler()

    def test_variable_assignment_simple(self):
        """Test astx.VariableAssignment with simple assignment."""
        value = astx.LiteralInt32(value=42)
        node = astx.VariableAssignment(name="x", value=value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Assign)
        assert len(result.targets) == 1
        assert isinstance(result.targets[0], ast.Name)
        assert result.targets[0].id == "x"

    def test_variable_declaration_simple(self):
        """Test astx.VariableDeclaration with type annotation."""
        var_type = astx.Int32()
        value = astx.LiteralInt32(value=42)
        node = astx.VariableDeclaration(name="x", type_=var_type, value=value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.AnnAssign)
        assert isinstance(result.target, ast.Name)
        assert result.target.id == "x"


class TestClassStructNodes:
    """Test cases for class and struct node transpilation."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.transpiler = ASTxPythonASTTranspiler()

    def test_class_def_stmt_simple(self):
        """Test astx.ClassDefStmt with simple class."""
        body_stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(body_stmt)
        node = astx.ClassDefStmt(name="MyClass", body=body)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.ClassDef)
        assert result.name == "MyClass"

    def test_struct_decl_stmt_simple(self):
        """Test astx.StructDeclStmt with struct declaration."""
        attr1 = astx.VariableDeclaration(
            name="x",
            type_=astx.DataType(),
            value=astx.LiteralInt32(value=0),
        )
        attr2 = astx.VariableDeclaration(
            name="y",
            type_=astx.DataType(),
            value=astx.LiteralInt32(value=0),
        )
        node = astx.StructDeclStmt(name="Point", attributes=[attr1, attr2])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.ClassDef)
        assert result.name == "Point"
        assert len(result.decorator_list) == 1
        assert result.decorator_list[0].id == "dataclass"

    def test_struct_def_stmt_simple(self):
        """Test astx.StructDefStmt with struct definition."""
        attr1 = astx.VariableDeclaration(
            name="x",
            type_=astx.DataType(),
            value=astx.LiteralInt32(value=0),
        )
        node = astx.StructDefStmt(name="Point", attributes=[attr1])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.ClassDef)
        assert result.name == "Point"
        assert len(result.decorator_list) == 1
        assert result.decorator_list[0].id == "dataclass"


class TestComprehensionNodes:
    """Test cases for comprehension node transpilation."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.transpiler = ASTxPythonASTTranspiler()

    def test_comprehension_clause_simple(self):
        """Test astx.ComprehensionClause with simple iteration."""
        target = astx.Variable(name="x")
        iterable = astx.Variable(name="items")
        node = astx.ComprehensionClause(target=target, iterable=iterable)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.comprehension)
        assert isinstance(result.target, ast.Name)
        assert result.target.id == "x"
        assert isinstance(result.iter, ast.Name)
        assert result.iter.id == "items"
        assert len(result.ifs) == 0
        assert result.is_async == 0

    def test_generator_expr_simple(self):
        """Test astx.GeneratorExpr with generator expression."""
        element = astx.Variable(name="x")
        target = astx.Variable(name="x")
        iterable = astx.Variable(name="items")
        generator = astx.ComprehensionClause(target=target, iterable=iterable)
        node = astx.GeneratorExpr(element=element, generators=[generator])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.GeneratorExp)
        assert isinstance(result.elt, ast.Name)
        assert result.elt.id == "x"
        assert len(result.generators) == 1

    def test_list_comprehension_simple(self):
        """Test astx.ListComprehension with element and generator."""
        element = astx.Variable(name="x")
        target = astx.Variable(name="x")
        iterable = astx.Variable(name="items")
        generator = astx.ComprehensionClause(target=target, iterable=iterable)
        node = astx.ListComprehension(element=element, generators=[generator])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.ListComp)
        assert isinstance(result.elt, ast.Name)
        assert result.elt.id == "x"
        assert len(result.generators) == 1

    def test_set_comprehension_simple(self):
        """Test astx.SetComprehension with element and generator."""
        element = astx.Variable(name="x")
        target = astx.Variable(name="x")
        iterable = astx.Variable(name="items")
        generator = astx.ComprehensionClause(target=target, iterable=iterable)
        node = astx.SetComprehension(element=element, generators=[generator])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.SetComp)
        assert isinstance(result.elt, ast.Name)
        assert result.elt.id == "x"
        assert len(result.generators) == 1


class TestControlFlowNodes:
    """Test cases for control flow node transpilation."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.transpiler = ASTxPythonASTTranspiler()
        self.Variable_2 = 2
        self.Variable_42 = 42

    def test_async_for_range_loop_expr_simple(self):
        """Test astx.AsyncForRangeLoopExpr with range."""
        variable = astx.InlineVariableDeclaration(name="i", type_=astx.Int32())
        start = astx.LiteralInt32(value=0)
        end = astx.LiteralInt32(value=10)
        step = astx.LiteralInt32(value=1)
        body_expr = astx.Variable(name="result")
        body = astx.Block()
        body.append(body_expr)
        node = astx.AsyncForRangeLoopExpr(
            variable=variable, start=start, end=end, step=step, body=body
        )
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.ListComp)

    def test_break_stmt(self):
        """Test astx.BreakStmt conversion."""
        node = astx.BreakStmt()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Break)
        code = ast.unparse(result)
        assert code == "break"

    def test_case_stmt_simple(self):
        """Test astx.CaseStmt with condition."""
        condition = astx.LiteralInt32(value=42)
        body_stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(body_stmt)
        node = astx.CaseStmt(condition=condition, body=body)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.match_case)
        assert isinstance(result.pattern, ast.Constant)
        assert result.pattern.value == self.Variable_42
        assert len(result.body) == 1
        assert isinstance(result.body[0], ast.Break)

    def test_continue_stmt(self):
        """Test astx.ContinueStmt conversion."""
        node = astx.ContinueStmt()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Continue)
        # Test round-trip conversion
        code = ast.unparse(result)
        assert code == "continue"

    def test_do_while_stmt_simple(self):
        """Test astx.DoWhileStmt with condition and body."""
        condition = astx.LiteralBoolean(value=True)
        body_stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(body_stmt)
        node = astx.DoWhileStmt(condition=condition, body=body)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.While)
        assert isinstance(result.test, ast.Constant)
        assert result.test.value is True

    def test_for_count_loop_stmt_simple(self):
        """Test astx.ForCountLoopStmt with range."""
        initializer = astx.InlineVariableDeclaration(
            name="i", type_=astx.DataType(), value=astx.LiteralInt32(value=0)
        )
        condition = astx.CompareOp(
            left=astx.Variable(name="i"),
            ops=["<"],
            comparators=[astx.LiteralInt32(value=10)],
        )
        update = astx.AugAssign(
            target=astx.Identifier(value="i"),
            value=astx.LiteralInt32(value=1),
            op_code="+=",
        )
        body_stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(body_stmt)
        node = astx.ForCountLoopStmt(
            initializer=initializer,
            condition=condition,
            update=update,
            body=body,
        )
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.For)
        assert isinstance(result.target, ast.Name)
        assert result.target.id == "i"
        assert isinstance(result.iter, ast.Call)
        assert result.iter.func.id == "range"
        assert len(result.iter.args) == self.Variable_2
        assert result.iter.args[0].value == 0
        MAX_LOOP_END = 10
        assert result.iter.args[1].value == MAX_LOOP_END
        assert len(result.body) == 1
        assert isinstance(result.body[0], ast.Break)

    def test_for_range_loop_expr_simple(self):
        """Test astx.ForRangeLoopExpr with range expression."""
        variable = astx.InlineVariableDeclaration(name="i", type_=astx.Int32())
        start = astx.LiteralInt32(value=0)
        end = astx.LiteralInt32(value=10)
        step = astx.LiteralInt32(value=1)
        body_expr = astx.Variable(name="result")
        body = astx.Block()
        body.append(body_expr)
        node = astx.ForRangeLoopExpr(
            variable=variable, start=start, end=end, step=step, body=body
        )
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.ListComp)
        assert len(result.generators) == 1
        assert isinstance(result.generators[0].target, ast.Name)
        assert result.generators[0].target.id == "i"

    def test_for_range_loop_stmt_simple(self):
        """Test astx.ForRangeLoopStmt with target and iter."""
        variable = astx.InlineVariableDeclaration(
            name="item",
            type_=astx.DataType(),
            value=astx.LiteralInt32(value=0),
        )
        start = astx.LiteralInt32(value=0)
        end = astx.LiteralInt32(value=10)
        step = astx.LiteralInt32(value=1)
        body_stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(body_stmt)
        node = astx.ForRangeLoopStmt(
            variable=variable, start=start, end=end, step=step, body=body
        )
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.For)
        assert isinstance(result.target, ast.Name)
        assert result.target.id == "item"
        assert isinstance(result.iter, ast.Call)
        assert result.iter.func.id == "range"
        assert len(result.body) == 1
        assert isinstance(result.body[0], ast.Break)

    def test_if_expr_simple(self):
        """Test astx.IfExpr with condition and branches."""
        condition = astx.LiteralBoolean(value=True)
        then_expr = astx.LiteralInt32(value=1)
        else_expr = astx.LiteralInt32(value=2)
        then_block = astx.Block()
        then_block.append(then_expr)
        else_block = astx.Block()
        else_block.append(else_expr)
        node = astx.IfExpr(
            condition=condition, then=then_block, else_=else_block
        )
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.IfExp)
        assert isinstance(result.test, ast.Constant)
        assert result.test.value is True

    def test_if_stmt_simple(self):
        """Test astx.IfStmt with condition and body."""
        condition = astx.LiteralBoolean(value=True)
        then_stmt = astx.BreakStmt()
        then_body = astx.Block()
        then_body.append(then_stmt)
        node = astx.IfStmt(condition=condition, then=then_body)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.If)
        assert isinstance(result.test, ast.Constant)
        assert result.test.value is True

    def test_switch_stmt_simple(self):
        """Test astx.SwitchStmt with value and cases."""
        value = astx.Variable(name="x")
        case_body = astx.Block()
        case_body.append(astx.BreakStmt())
        case1 = astx.CaseStmt(
            condition=astx.LiteralInt32(value=1),
            body=case_body,
        )
        cases = astx.ASTNodes()
        cases.append(case1)
        node = astx.SwitchStmt(value=value, cases=cases)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Match)
        assert isinstance(result.subject, ast.Name)
        assert result.subject.id == "x"
        assert len(result.cases) == 1
        assert isinstance(result.cases[0], ast.match_case)

    def test_while_expr_simple(self):
        """Test astx.WhileExpr with condition and body."""
        condition = astx.LiteralBoolean(value=True)
        body_expr = astx.Variable(name="result")
        body = astx.Block()
        body.append(body_expr)
        node = astx.WhileExpr(condition=condition, body=body)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.ListComp)
        assert len(result.generators) == 1
        assert len(result.generators) == 1
        assert isinstance(result.elt, ast.Name)

    def test_while_stmt_simple(self):
        """Test astx.WhileStmt with condition and body."""
        condition = astx.LiteralBoolean(value=True)
        body_stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(body_stmt)
        node = astx.WhileStmt(condition=condition, body=body)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.While)
        assert isinstance(result.test, ast.Constant)
        assert result.test.value is True


class TestEnumNodes:
    """Test enum-related node types."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = ASTxPythonASTTranspiler()

    def test_enum_decl_stmt_simple(self):
        """Test astx.EnumDeclStmt with simple enum."""
        attr1 = astx.Variable(name="RED")
        attr2 = astx.Variable(name="BLUE")
        node = astx.EnumDeclStmt(name="Color", attributes=[attr1, attr2])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.ClassDef)
        assert result.name == "Color"
        assert len(result.bases) == 1
        assert isinstance(result.bases[0], ast.Name)
        assert result.bases[0].id == "Enum"


class TestExceptionNodes:
    """Test cases for exception handling node transpilation."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.transpiler = ASTxPythonASTTranspiler()

    def test_catch_handler_stmt_simple(self):
        """Test astx.CatchHandlerStmt with exception type."""
        exception_type = astx.DataType()
        body_stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(body_stmt)
        node = astx.CatchHandlerStmt(
            types=[exception_type], name=astx.Identifier(value="e"), body=body
        )
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.ExceptHandler)
        assert result.name == "e"

    def test_exception_handler_stmt_simple(self):
        """Test astx.ExceptionHandlerStmt with try-except."""
        body_stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(body_stmt)
        handler = astx.CatchHandlerStmt(
            types=[astx.DataType()], name=astx.Identifier(value="e"), body=body
        )
        node = astx.ExceptionHandlerStmt(body=body, handlers=[handler])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Try)

    def test_finally_handler_stmt_simple(self):
        """Test astx.FinallyHandlerStmt with finally block."""
        body_stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(body_stmt)
        node = astx.FinallyHandlerStmt(body=body)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Try)
        assert len(result.finalbody) == 1
        assert isinstance(result.finalbody[0], ast.Break)

    def test_throw_stmt_simple(self):
        """Test astx.ThrowStmt with exception."""
        args = astx.Arguments()
        prototype = astx.FunctionPrototype(
            name="ValueError", args=args, return_type=astx.Int32()
        )
        body = astx.Block()
        fn_def = astx.FunctionDef(prototype=prototype, body=body)
        exception = astx.FunctionCall(
            fn=fn_def,
            args=[astx.LiteralString(value="Error message")],
        )
        node = astx.ThrowStmt(exception=exception)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Raise)
        assert isinstance(result.exc, ast.Call)
        assert result.exc.func.id == "ValueError"
        assert result.cause is None


class TestFunctionNodes:
    """Test cases for function-related node transpilation."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.transpiler = ASTxPythonASTTranspiler()
        self.Variable_2 = 2

    def test_argument_simple(self):
        """Test astx.Argument with simple name."""
        node = astx.Argument(name="param", type_=astx.DataType())
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.arg)
        assert result.arg == "param"
        assert result.annotation is not None

    def test_argument_with_type(self):
        """Test astx.Argument with type annotation."""
        type_annotation = astx.DataType()
        node = astx.Argument(name="param", type_=type_annotation)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.arg)
        assert result.arg == "param"
        assert isinstance(result.annotation, ast.Name)

    def test_arguments_empty(self):
        """Test astx.Arguments with empty args."""
        node = astx.Arguments()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.arguments)
        assert len(result.args) == 0
        assert len(result.posonlyargs) == 0
        assert len(result.kwonlyargs) == 0

    def test_arguments_with_args(self):
        """Test astx.Arguments with arguments."""
        arg1 = astx.Argument(name="x", type_=astx.DataType())
        arg2 = astx.Argument(name="y", type_=astx.DataType())
        node = astx.Arguments(arg1, arg2)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.arguments)
        assert len(result.args) == self.Variable_2
        assert result.args[0].arg == "x"
        assert result.args[1].arg == "y"

    def test_function_async_def_simple(self):
        """Test astx.FunctionAsyncDef with simple async function."""
        args = astx.Arguments()
        prototype = astx.FunctionPrototype(
            name="async_func", args=args, return_type=astx.Int32()
        )
        body_stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(body_stmt)
        node = astx.FunctionAsyncDef(prototype=prototype, body=body)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.AsyncFunctionDef)
        assert result.name == "async_func"

    def test_function_call_simple(self):
        """Test astx.FunctionCall with simple function call."""
        args = astx.Arguments()
        prototype = astx.FunctionPrototype(
            name="print", args=args, return_type=astx.Int32()
        )
        body = astx.Block()
        fn_def = astx.FunctionDef(
            prototype=prototype,
            body=body,
        )
        arg = astx.LiteralString(value="Hello")
        node = astx.FunctionCall(fn=fn_def, args=[arg])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Call)
        assert isinstance(result.func, ast.Name)
        assert result.func.id == "print"

    def test_function_def_simple(self):
        """Test astx.FunctionDef with simple function."""
        args = astx.Arguments()
        prototype = astx.FunctionPrototype(
            name="my_func", args=args, return_type=astx.Int32()
        )
        body_stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(body_stmt)
        node = astx.FunctionDef(prototype=prototype, body=body)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.FunctionDef)
        assert result.name == "my_func"

    def test_function_prototype_simple(self):
        """Test astx.FunctionPrototype with simple prototype."""
        args = astx.Arguments()
        node = astx.FunctionPrototype(
            name="proto_func", args=args, return_type=astx.Int32()
        )
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.FunctionDef)
        assert result.name == "proto_func"

    def test_lambda_expr_simple(self):
        """Test astx.LambdaExpr with simple lambda."""
        param = astx.Argument(name="x", type_=astx.DataType())
        params = astx.Arguments(param)
        body = astx.BinaryOp(
            lhs=astx.Variable(name="x"),
            rhs=astx.LiteralInt32(value=1),
            op_code="+",
        )
        node = astx.LambdaExpr(params=params, body=body)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Lambda)
        assert len(result.args.args) == 1
        assert result.args.args[0].arg == "x"
        assert isinstance(result.body, ast.BinOp)


class TestImportNodes:
    """Test import-related node types."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = ASTxPythonASTTranspiler()

    def test_import_expr_simple(self):
        """Test astx.ImportExpr with single module."""
        alias = astx.AliasExpr(name="os")
        node = astx.ImportExpr(names=[alias])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Assign)

    def test_import_from_expr_simple(self):
        """Test astx.ImportFromExpr with module and names."""
        alias = astx.AliasExpr(name="path")
        node = astx.ImportFromExpr(module="os", names=[alias])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Assign)

    def test_import_from_stmt_simple(self):
        """Test astx.ImportFromStmt with module and names."""
        alias = astx.AliasExpr(name="sqrt")
        node = astx.ImportFromStmt(module="math", names=[alias])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.ImportFrom)
        assert result.module == "math"
        assert len(result.names) == 1

    def test_import_stmt_simple(self):
        """Test astx.ImportStmt with single module."""
        alias = astx.AliasExpr(name="math")
        node = astx.ImportStmt(names=[alias])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Import)
        assert len(result.names) == 1
        assert result.names[0].name == "math"


class TestLiteralNodes:
    """Test cases for literal node transpilation."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.transpiler = ASTxPythonASTTranspiler()
        self.Variable_2 = 2
        self.Variable_42 = 42
        self.Variable_3_14 = 3.14

    def test_literal_boolean_false(self):
        """Test astx.LiteralBoolean with False value."""
        node = astx.LiteralBoolean(value=False)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value is False
        code = ast.unparse(result)
        assert code == "False"

    def test_literal_boolean_true(self):
        """Test astx.LiteralBoolean with True value."""
        node = astx.LiteralBoolean(value=True)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value is True
        code = ast.unparse(result)
        assert code == "True"

    def test_literal_complex32_simple(self):
        """Test astx.LiteralComplex32 with complex value."""
        node = astx.LiteralComplex32(real=3.0, imag=4.0)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Call)
        assert isinstance(result.func, ast.Name)
        assert result.func.id == "complex"
        assert len(result.args) == self.Variable_2

    def test_literal_complex64_simple(self):
        """Test astx.LiteralComplex64 with complex value."""
        node = astx.LiteralComplex64(real=3.0, imag=4.0)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Call)
        assert isinstance(result.func, ast.Name)
        assert result.func.id == "complex"
        assert len(result.args) == self.Variable_2

    def test_literal_complex_simple(self):
        """Test astx.LiteralComplex with complex value."""
        node = astx.LiteralComplex(real=3.0, imag=4.0)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)

    def test_literal_float16_simple(self):
        """Test astx.LiteralFloat16 with float value."""
        node = astx.LiteralFloat16(value=3.14)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        LITERAL_FLOAT16_VALUE = 3.14
        assert result.value == LITERAL_FLOAT16_VALUE

    def test_literal_int32_negative(self):
        """Test astx.LiteralInt32 with negative value."""
        NEGATIVE_INT = -15
        node = astx.LiteralInt32(value=NEGATIVE_INT)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == NEGATIVE_INT
        code = ast.unparse(result)
        assert code == str(NEGATIVE_INT)

    def test_literal_int32_positive(self):
        """Test astx.LiteralInt32 with positive value."""
        POSITIVE_INT = 42
        node = astx.LiteralInt32(value=POSITIVE_INT)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == POSITIVE_INT
        code = ast.unparse(result)
        assert code == str(POSITIVE_INT)

    def test_literal_int32_zero(self):
        """Test astx.LiteralInt32 with zero value."""
        node = astx.LiteralInt32(value=0)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == 0
        code = ast.unparse(result)
        assert code == "0"

    def test_literal_string_empty(self):
        """Test astx.LiteralString with empty string."""
        node = astx.LiteralString(value="")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == ""
        code = ast.unparse(result)
        assert code == "''"

    def test_literal_string_simple(self):
        """Test astx.LiteralString with simple string."""
        test_string = "Hello, World!"
        node = astx.LiteralString(value=test_string)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == test_string
        code = ast.unparse(result)
        assert code == "'Hello, World!'"

    def test_literal_utf8_char_simple(self):
        """Test astx.LiteralUTF8Char with character value."""
        node = astx.LiteralUTF8Char(value="A")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == "A"

    def test_literal_utf8_string_simple(self):
        """Test astx.LiteralUTF8String with string value."""
        node = astx.LiteralUTF8String(value="Hello UTF8")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == "Hello UTF8"


class TestOperatorNodes:
    """Test cases for operator node transpilation."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.transpiler = ASTxPythonASTTranspiler()
        self.OR_OP_NUM_VALUES = 2

    def test_and_op_simple(self):
        """Test astx.AndOp with boolean operands."""
        left = astx.LiteralBoolean(value=True)
        right = astx.LiteralBoolean(value=False)
        node = astx.AndOp(lhs=left, rhs=right)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.BoolOp)
        assert isinstance(result.op, ast.And)
        assert len(result.values) == self.OR_OP_NUM_VALUES
        assert result.values[0].value is True
        assert result.values[1].value is False
        code = ast.unparse(result)
        assert code == "True and False"

    def test_aug_assign_add(self):
        """Test astx.AugAssign with addition."""
        target = astx.Identifier(value="x")
        value = astx.LiteralInt32(value=5)
        node = astx.AugAssign(target=target, value=value, op_code="+=")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.AugAssign)
        assert isinstance(result.target, ast.Name)
        assert result.target.id == "x"
        assert isinstance(result.target.ctx, ast.Store)
        assert isinstance(result.op, ast.Add)
        assert isinstance(result.value, ast.Constant)
        TEST_VALUE = 5
        assert result.value.value == TEST_VALUE
        code = ast.unparse(result)
        assert code == "x += 5"

    def test_binary_op_addition(self):
        """Test astx.BinaryOp with addition operation."""
        LEFT_VALUE = 5
        RIGHT_VALUE = 3
        left = astx.LiteralInt32(value=LEFT_VALUE)
        right = astx.LiteralInt32(value=RIGHT_VALUE)
        node = astx.BinaryOp(lhs=left, rhs=right, op_code="+")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.BinOp)
        assert isinstance(result.op, ast.Add)
        assert isinstance(result.left, ast.Constant)
        assert isinstance(result.right, ast.Constant)
        assert result.left.value == LEFT_VALUE
        assert result.right.value == RIGHT_VALUE
        code = ast.unparse(result)
        assert code == f"{LEFT_VALUE} + {RIGHT_VALUE}"

    def test_binary_op_multiplication(self):
        """Test astx.BinaryOp with multiplication operation."""
        LEFT_VALUE = 4
        RIGHT_VALUE = 7
        left = astx.LiteralInt32(value=LEFT_VALUE)
        right = astx.LiteralInt32(value=RIGHT_VALUE)
        node = astx.BinaryOp(lhs=left, rhs=right, op_code="*")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.BinOp)
        assert isinstance(result.op, ast.Mult)
        assert result.left.value == LEFT_VALUE
        assert result.right.value == RIGHT_VALUE

    def test_compare_op_equal(self):
        """Test astx.CompareOp with equality."""
        TEST_INT = 5
        left = astx.LiteralInt32(value=TEST_INT)
        right = astx.LiteralInt32(value=TEST_INT)
        node = astx.CompareOp(left=left, ops=["=="], comparators=[right])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Compare)
        assert isinstance(result.left, ast.Constant)
        assert result.left.value == TEST_INT
        assert len(result.ops) == 1
        assert isinstance(result.ops[0], ast.Eq)
        assert len(result.comparators) == 1
        assert result.comparators[0].value == TEST_INT
        code = ast.unparse(result)
        assert code == f"{TEST_INT} == {TEST_INT}"

    def test_nand_op_simple(self):
        """Test astx.NandOp with boolean operands."""
        left = astx.LiteralBoolean(value=True)
        right = astx.LiteralBoolean(value=False)
        node = astx.NandOp(lhs=left, rhs=right)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.UnaryOp)
        assert isinstance(result.op, ast.Not)
        assert isinstance(result.operand, ast.BoolOp)
        assert isinstance(result.operand.op, ast.And)

    def test_nor_op_simple(self):
        """Test astx.NorOp with boolean operands."""
        left = astx.LiteralBoolean(value=True)
        right = astx.LiteralBoolean(value=False)
        node = astx.NorOp(lhs=left, rhs=right)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.UnaryOp)
        assert isinstance(result.op, ast.Not)
        assert isinstance(result.operand, ast.BoolOp)
        assert isinstance(result.operand.op, ast.Or)

    def test_xnor_op_simple(self):
        """Test astx.XnorOp with boolean operands."""
        left = astx.LiteralBoolean(value=True)
        right = astx.LiteralBoolean(value=False)
        node = astx.XnorOp(lhs=left, rhs=right)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.UnaryOp)
        assert isinstance(result.op, ast.Not)
        assert isinstance(result.operand, ast.BinOp)
        assert isinstance(result.operand.op, ast.BitXor)

    def test_xor_op_simple(self):
        """Test astx.XorOp with boolean operands."""
        left = astx.LiteralBoolean(value=True)
        right = astx.LiteralBoolean(value=False)
        node = astx.XorOp(lhs=left, rhs=right)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.BinOp)
        assert isinstance(result.op, ast.BitXor)
        assert isinstance(result.left, ast.Constant)
        assert isinstance(result.right, ast.Constant)


class TestSpecialNodes:
    """Test cases for special and miscellaneous node transpilation."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.transpiler = ASTxPythonASTTranspiler()
        self.Variable_2 = 2
        self.Variable_42 = 42

    def test_alias_expr_no_asname(self):
        """Test astx.AliasExpr without asname."""
        node = astx.AliasExpr(name="os", asname="")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.alias)
        assert result.name == "os"
        assert result.asname == ""

    def test_alias_expr_simple(self):
        """Test astx.AliasExpr with simple alias."""
        node = astx.AliasExpr(name="numpy", asname="np")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.alias)
        assert result.name == "numpy"
        assert result.asname == "np"

    def test_ast_nodes_list(self):
        """Test astx.ASTNodes with multiple nodes."""
        node1 = astx.LiteralInt32(value=1)
        node2 = astx.LiteralInt32(value=2)
        node = astx.ASTNodes()
        node.append(node1)
        node.append(node2)
        result = self.transpiler.visit(node)
        assert isinstance(result, list)
        assert len(result) == self.Variable_2
        assert all(isinstance(r, ast.Constant) for r in result)
        assert result[0].value == 1
        assert result[1].value == self.Variable_2

    def test_await_expr_simple(self):
        """Test astx.AwaitExpr with simple value."""
        value = astx.Variable(name="async_func")
        node = astx.AwaitExpr(value=value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Await)
        assert isinstance(result.value, ast.Name)
        assert result.value.id == "async_func"
        code = ast.unparse(result)
        assert code == "await async_func"

    def test_block_simple(self):
        """Test astx.Block with statements."""
        stmt1 = astx.BreakStmt()
        stmt2 = astx.ContinueStmt()
        node = astx.Block()
        node.append(stmt1)
        node.append(stmt2)
        result = self.transpiler.visit(node)
        assert isinstance(result, list)
        assert len(result) == self.Variable_2
        assert isinstance(result[0], ast.Break)
        assert isinstance(result[1], ast.Continue)

    def test_delete_stmt_simple(self):
        """Test astx.DeleteStmt with variable."""
        target = astx.Variable(name="x")
        node = astx.DeleteStmt(value=[target])
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Delete)
        assert len(result.targets) == 1
        assert isinstance(result.targets[0], ast.Name)
        assert result.targets[0].id == "x"
        code = ast.unparse(result)
        assert code == "del x"

    def test_ellipsis_simple(self):
        """Test astx.Ellipsis conversion."""
        node = astx.Ellipsis()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value is ...
        code = ast.unparse(result)
        assert code == "..."

    def test_identifier_simple(self):
        """Test astx.Identifier with simple value."""
        node = astx.Identifier(value="my_id")
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "my_id"

    def test_module_simple(self):
        """Test astx.Module with body."""
        stmt = astx.BreakStmt()
        body = astx.Block()
        body.append(stmt)
        node = astx.Module()
        node.body = body
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Module)

    def test_parenthesized_expr_simple(self):
        """Test astx.ParenthesizedExpr with inner value."""
        inner_value = astx.LiteralInt32(value=42)
        node = astx.ParenthesizedExpr(value=inner_value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Constant)
        assert result.value == self.Variable_42

    def test_starred_simple(self):
        """Test astx.Starred with value."""
        value = astx.Variable(name="args")
        node = astx.Starred(value=value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Starred)
        assert isinstance(result.value, ast.Name)
        assert result.value.id == "args"
        assert isinstance(result.ctx, ast.Load)


class TestTypeDataNodes:
    """Test cases for type and data node transpilation."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.transpiler = ASTxPythonASTTranspiler()

    def test_complex32_simple(self):
        """Test astx.Complex32 type."""
        node = astx.Complex32()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "complex"
        assert isinstance(result.ctx, ast.Load)

    def test_complex64_simple(self):
        """Test astx.Complex64 type."""
        node = astx.Complex64()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "complex"
        assert isinstance(result.ctx, ast.Load)

    def test_data_type_simple(self):
        """Test astx.DataType with simple type."""
        node = astx.DataType()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "object"
        assert isinstance(result.ctx, ast.Load)

    def test_date_simple(self):
        """Test astx.Date type."""
        node = astx.Date()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "date"
        assert isinstance(result.ctx, ast.Load)

    def test_datetime_simple(self):
        """Test astx.DateTime type."""
        node = astx.DateTime()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "datetime"
        assert isinstance(result.ctx, ast.Load)

    def test_float16_simple(self):
        """Test astx.Float16 type."""
        node = astx.Float16()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "float"
        assert isinstance(result.ctx, ast.Load)

    def test_float32_simple(self):
        """Test astx.Float32 type."""
        node = astx.Float32()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "float"
        assert isinstance(result.ctx, ast.Load)

    def test_float64_simple(self):
        """Test astx.Float64 type."""
        node = astx.Float64()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "float"
        assert isinstance(result.ctx, ast.Load)

    def test_int32_simple(self):
        """Test astx.Int32 type."""
        node = astx.Int32()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "int"
        assert isinstance(result.ctx, ast.Load)

    def test_time_simple(self):
        """Test astx.Time type."""
        node = astx.Time()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "time"
        assert isinstance(result.ctx, ast.Load)

    def test_timestamp_simple(self):
        """Test astx.Timestamp type."""
        node = astx.Timestamp()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "timestamp"
        assert isinstance(result.ctx, ast.Load)

    def test_type_cast_expr_simple(self):
        """Test astx.TypeCastExpr with cast."""
        target_type = astx.DataType()
        expr = astx.LiteralFloat32(value=3.14)
        node = astx.TypeCastExpr(target_type=target_type, expr=expr)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Call)
        assert isinstance(result.func, ast.Name)

    def test_utf8_char_simple(self):
        """Test astx.UTF8Char type."""
        node = astx.UTF8Char()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "str"
        assert isinstance(result.ctx, ast.Load)

    def test_utf8_string_simple(self):
        """Test astx.UTF8String type."""
        node = astx.UTF8String()
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == "str"
        assert isinstance(result.ctx, ast.Load)


class TestVariableAssignmentNodes:
    """Test cases for variable and assignment node transpilation."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.transpiler = ASTxPythonASTTranspiler()
        self.Variable_42 = 42

    def test_assignment_expr_single_target(self):
        """Test astx.AssignmentExpr with single target."""
        target = astx.Variable(name="x")
        value = astx.LiteralInt32(value=42)
        node = astx.AssignmentExpr(targets=[target], value=value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Assign)
        assert len(result.targets) == 1
        assert isinstance(result.targets[0], ast.Name)
        assert result.targets[0].id == "x"
        assert isinstance(result.targets[0].ctx, ast.Store)
        assert isinstance(result.value, ast.Constant)
        assert result.value.value == self.Variable_42

    def test_inline_variable_declaration_simple(self):
        """Test astx.InlineVariableDeclaration with type annotation."""
        var_type = astx.DataType()
        value = astx.LiteralInt32(value=42)
        node = astx.InlineVariableDeclaration(
            name="x", type_=var_type, value=value
        )
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.AnnAssign)
        assert isinstance(result.target, ast.Name)
        assert result.target.id == "x"

    def test_variable_declaration_simple(self):
        """Test astx.VariableDeclaration with type annotation."""
        var_type = astx.DataType()
        value = astx.LiteralInt32(value=42)
        node = astx.VariableDeclaration(name="x", type_=var_type, value=value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.AnnAssign)
        assert isinstance(result.target, ast.Name)
        assert result.target.id == "x"

    def test_variable_simple_name(self):
        """Test astx.Variable with simple identifier."""
        variable_name = "my_variable"
        node = astx.Variable(name=variable_name)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == variable_name
        assert isinstance(result.ctx, ast.Load)
        code = ast.unparse(result)
        assert code == "my_variable"

    def test_variable_underscore_name(self):
        """Test astx.Variable with underscore identifier."""
        variable_name = "_private_var"
        node = astx.Variable(name=variable_name)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Name)
        assert result.id == variable_name
        assert isinstance(result.ctx, ast.Load)
        code = ast.unparse(result)
        assert code == "_private_var"


class TestYieldNodes:
    """Test yield-related node types."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = ASTxPythonASTTranspiler()

    def test_yield_expr_simple(self):
        """Test astx.YieldExpr with value."""
        value = astx.LiteralInt32(value=1)
        node = astx.YieldExpr(value=value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Yield)
        assert isinstance(result.value, ast.Constant)

    def test_yield_from_expr_simple(self):
        """Test astx.YieldFromExpr with iterator."""
        value = astx.Variable(name="iterator")
        node = astx.YieldFromExpr(value=value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.YieldFrom)
        assert isinstance(result.value, ast.Name)

    def test_yield_stmt_simple(self):
        """Test astx.YieldStmt with value."""
        value = astx.LiteralInt32(value=1)
        node = astx.YieldStmt(value=value)
        result = self.transpiler.visit(node)
        assert isinstance(result, ast.Expr)
        assert isinstance(result.value, ast.Yield)