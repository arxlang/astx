"""ASTx Python transpiler."""

from typing import Union, cast

import astx
import astx.operators

from astx.tools.typing import typechecked
from plum import dispatch


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
        target_str = " = ".join(self.visit(target) for target in node.targets)
        return f"{target_str} = {self.visit(node.value)}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ASTNodes) -> str:
        """Handle AliasExpr nodes."""
        lines = [self.visit(node) for node in node.nodes]
        return " ".join(lines)

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
        value = self.visit(node.value) if node.value else ""
        return f"await {value}".strip()

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BinaryOp) -> str:
        """Handle BinaryOp nodes."""
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return f"({lhs} {node.op_code} {rhs})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Block) -> str:
        """Handle Block nodes."""
        return self._generate_block(node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BreakStmt) -> str:
        """Handle BreakStmt nodes."""
        return "break"

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
    def visit(self, node: astx.CompareOp) -> str:
        """Handle CompareOp nodes."""
        comparisons = []
        left = self.visit(node.left)

        for op, comparator in zip(node.ops, node.comparators):
            comparisons.append(f"{op} {self.visit(comparator)}")

        chain = " ".join(comparisons)
        return f"({left} {chain})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ClassDefStmt) -> str:
        """Handle ClassDefStmt nodes."""
        class_type = "(ABC)" if node.is_abstract else ""
        return f"class {node.name}{class_type}:\n{self.visit(node.body)}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ContinueStmt) -> str:
        """Handle ContinueStmt nodes."""
        return "continue"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ComprehensionClause) -> str:
        """Handle ComprehensionClause nodes."""
        conditions = " if ".join(
            [self.visit(condition) for condition in node.conditions]
        )
        if conditions:
            conditions = f"if {conditions}"

        async_kw = "async " if node.is_async else ""
        target = self.visit(node.target)
        iter = self.visit(node.iterable)
        return f"{async_kw}for {target} in {iter} {conditions}".strip()

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DeleteStmt) -> str:
        """Transpile a DeleteStmt node to Python code."""
        targets = ", ".join(self.visit(target) for target in node.value)
        return f"del {targets}"

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
        if len(node.body) > 1:
            raise ValueError(
                "ForRangeLoopExpr in Python just accept 1 node in the body "
                "attribute."
            )
        return (
            f"result = [{self.visit(node.body).strip()} for "
            f"{node.variable.name} in range"
            f"({self.visit(node.start)}, {self.visit(node.end)}, "
            f"{self.visit(node.step)})]"
        )

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
        args = self.visit(node.prototype.args)
        returns = (
            f" -> {self.visit(node.prototype.return_type)}"
            if node.prototype.return_type
            else ""
        )
        header = f"def {node.name}({args}){returns}:"
        body = self.visit(node.body)
        return f"{header}\n{body}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionCall) -> str:
        """Handle FunctionCall nodes."""
        args = ", ".join([self.visit(arg) for arg in node.args])
        return f"{node.fn.name}({args})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionReturn) -> str:
        """Handle FunctionReturn nodes."""
        value = self.visit(node.value) if node.value else ""
        return f"return {value}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.GeneratorExpr) -> str:
        """Handle GeneratorExpr nodes."""
        generators = [self.visit(node.generators)]
        return f"({self.visit(node.element).strip()} {' '.join(generators)})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Identifier) -> str:
        """Handle Identifier nodes."""
        return f"{node.value}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfExpr) -> str:
        """Handle IfExpr nodes."""
        if node.else_ is not None and len(node.else_) > 1:
            raise ValueError(
                "IfExpr in Python just accept 1 node in the else attribute."
            )

        if len(node.then) > 1:
            raise ValueError(
                "IfExpr in Python just accept 1 node in the then attribute."
            )

        if_ = self.visit(node.condition)
        else_ = self.visit(node.else_).strip() if node.else_ else "None"
        then_ = self.visit(node.then).strip()
        return f"{then_} if {if_} else {else_}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfStmt) -> str:
        """Handle IfStmt nodes."""
        else_ = (
            (f"\nelse:\n{self._generate_block(node.else_)}")
            if node.else_ is not None
            else ""
        )

        return (
            f"if {self.visit(node.condition)}:"
            f"\n{self._generate_block(node.then)}"
            f"{else_}"
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromStmt) -> str:
        """Handle ImportFromStmt nodes."""
        names = [self.visit(name) for name in node.names]
        level_dots = "." * node.level
        module_str = (
            f"{level_dots}{node.module}" if node.module else level_dots
        )
        names_str = ", ".join(str(name) for name in names)
        return f"from {module_str} import {names_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportExpr) -> str:
        """Handle ImportExpr nodes."""
        names = [self.visit(name) for name in node.names]
        names_list = []
        for name in names:
            str_ = f"__import__('{name}') "
            names_list.append(str_)
        names_str = ", ".join(x for x in names_list)

        # name if one import or name1, name2, etc if multiple imports
        num = [
            "" if len(names) == 1 else str(n) for n in range(1, len(names) + 1)
        ]
        call = ["module" + str(n) for n in num]
        call_str = ", ".join(x for x in call)

        # assign tuple if multiple imports
        names_str = (
            names_str if len(names_list) == 1 else "(" + names_str + ")"
        )

        return f"{call_str} = {names_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromExpr) -> str:
        """Handle ImportFromExpr nodes."""
        names = [self.visit(name) for name in node.names]
        level_dots = "." * node.level
        module_str = (
            f"{level_dots}{node.module}" if node.module else level_dots
        )
        names_list = []
        for name in names:
            str_ = (
                f"getattr(__import__('{module_str}', "
                f"fromlist=['{name}']), '{name}')"
            )
            names_list.append(str_)
        names_str = ", ".join(x for x in names_list)

        # name if one import or name1, name2, etc if multiple imports
        num = [
            "" if len(names) == 1 else str(n) for n in range(1, len(names) + 1)
        ]
        call = ["name" + str(n) for n in num]
        call_str = ", ".join(x for x in call)

        # assign tuple if multiple imports
        names_str = (
            names_str if len(names_list) == 1 else "(" + names_str + ")"
        )

        return f"{call_str} = {names_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportStmt) -> str:
        """Handle ImportStmt nodes."""
        names = [self.visit(name) for name in node.names]
        names_str = ", ".join(x for x in names)
        return f"import {names_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromStmt) -> str:
        """Handle ImportFromStmt nodes."""
        names = [self.visit(name) for name in node.names]
        level_dots = "." * node.level
        module_str = (
            f"{level_dots}{node.module}" if node.module else level_dots
        )
        names_str = ", ".join(str(name) for name in names)
        return f"from {module_str} import {names_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LambdaExpr) -> str:
        """Handle LambdaExpr nodes."""
        params_str = ", ".join(param.name for param in node.params)
        return f"lambda {params_str}: {self.visit(node.body)}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ListComprehension) -> str:
        """Handle ListComprehension nodes."""
        generators = [self.visit(node.generators)]
        return f"[{self.visit(node.element).strip()} {' '.join(generators)}]"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralBoolean) -> str:
        """Handle LiteralBoolean nodes."""
        return "True" if node.value else "False"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex32) -> str:
        """Handle LiteralComplex32 nodes."""
        real = node.value[0]
        imag = node.value[1]
        return f"complex({real}, {imag})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex) -> str:
        """Handle LiteralComplex nodes."""
        real = node.value[0]
        imag = node.value[1]
        return f"complex({real}, {imag})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex64) -> str:
        """Handle LiteralComplex64 nodes."""
        real = node.value[0]
        imag = node.value[1]
        return f"complex({real}, {imag})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat16) -> str:
        """Handle LiteralFloat nodes."""
        return str(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat32) -> str:
        """Handle LiteralFloat nodes."""
        return str(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat64) -> str:
        """Handle LiteralFloat nodes."""
        return str(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt32) -> str:
        """Handle LiteralInt32 nodes."""
        return str(node.value)

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
    def visit(self, node: astx.SetComprehension) -> str:
        """Handle SetComprehension nodes."""
        generators = [self.visit(gen) for gen in node.generators]
        return f"{{{self.visit(node.element)} {' '.join(generators)}}}"

    @dispatch  # type: ignore[no-redef]
    def visit(
        self, node: Union[astx.StructDeclStmt, astx.StructDefStmt]
    ) -> str:
        """Handle StructDeclStmt and StructDefStmt nodes."""
        attrs_str = "\n    ".join(self.visit(attr) for attr in node.attributes)
        return f"@dataclass \nclass {node.name}:\n    {attrs_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SubscriptExpr) -> str:
        """Handle SubscriptExpr nodes."""
        lower_str = (
            str(node.lower.value)
            if not isinstance(node.lower, astx.LiteralNone)
            else str(node.index.value)
        )
        upper_str = (
            ":" + str(node.upper.value)
            if not isinstance(node.upper, astx.LiteralNone)
            else ""
        )
        step_str = (
            ":" + str(node.step.value)
            if not isinstance(node.step, astx.LiteralNone)
            else ""
        )
        return f"{node.value.name}[{lower_str}{upper_str}{step_str}]"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.SwitchStmt) -> str:
        """Handle SwitchStmt nodes."""
        cases_visited = self._generate_block(cast(astx.Block, node.cases))
        return f"match {self.visit(node.value)}:\n{cases_visited}"

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
        return f"cast({self.visit(node.target_type)}, {node.expr.name})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ThrowStmt) -> str:
        """Handle ThrowStmt nodes."""
        exception_str = (
            f" {self.visit(node.exception)}" if node.exception else ""
        )
        return f"raise{exception_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UnaryOp) -> str:
        """Handle UnaryOp nodes."""
        operand = self.visit(node.operand)
        return f"({node.op_code}{operand})"

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
        target = node.name
        value = self.visit(node.value)
        return f"{target} = {value}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableDeclaration) -> str:
        """Handle VariableDeclaration nodes."""
        value = self.visit(node.value)
        return f"{node.name}: {node.value.type_.__class__.__name__} = {value}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WalrusOp) -> str:
        """Handle Walrus operator."""
        return f"({self.visit(node.lhs)} := {self.visit(node.rhs)})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AugAssign) -> str:
        """Handle Augmented assign operator."""
        target = self.visit(node.target)
        value = self.visit(node.value)
        return f"{target} {node.op_code} {value}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileExpr) -> str:
        """Handle WhileExpr nodes."""
        if len(node.body) > 1:
            raise ValueError(
                "WhileExpr in Python just accept 1 node in the body attribute."
            )

        condition = self.visit(node.condition)
        body = self.visit(node.body).strip()
        return f"[{body} for _ in iter(lambda: {condition}, False)]"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileStmt) -> str:
        """Handle WhileStmt nodes."""
        condition = self.visit(node.condition)
        body = self._generate_block(node.body)
        return f"while {condition}:\n{body}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldExpr) -> str:
        """Handle YieldExpr nodes."""
        value = self.visit(node.value) if node.value else ""
        return f"yield {value}".strip()

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldStmt) -> str:
        """Handle YieldStmt nodes."""
        value = self.visit(node.value) if node.value else ""
        return f"yield {value}".strip()

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.YieldFromExpr) -> str:
        """Handle YieldFromExpr nodes."""
        value = self.visit(node.value)
        return f"yield from {value}".strip()

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
        return f"datetime.strptime({node.value!r}, '%Y-%m-%d').date()"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTime) -> str:
        """Handle LiteralTime nodes."""
        return f"datetime.strptime({node.value!r}, '%H:%M:%S').time()"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTimestamp) -> str:
        """Handle LiteralTimestamp nodes."""
        return f"datetime.strptime({node.value!r}, '%Y-%m-%d %H:%M:%S')"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDateTime) -> str:
        """Handle LiteralDateTime nodes."""
        return f"datetime.strptime({node.value!r}, '%Y-%m-%dT%H:%M:%S')"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ParenthesizedExpr) -> str:
        """Handle ParenthesizedExpr nodes."""
        return f"({self.visit(node.value)})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AndOp) -> str:
        """Handle AndOp nodes."""
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return f"{lhs} and {rhs}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.OrOp) -> str:
        """Handle OrOp nodes."""
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return f"{lhs} or {rhs}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.XorOp) -> str:
        """Handle XorOp nodes."""
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return f"{lhs} ^ {rhs}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NandOp) -> str:
        """Handle NandOp nodes."""
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return f"not ({lhs} and {rhs})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.NorOp) -> str:
        """Handle NorOp nodes."""
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return f"not ({lhs} or {rhs})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.XnorOp) -> str:
        """Handle XnorOp nodes."""
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return f"not ({lhs} ^ {rhs})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralList) -> str:
        """Handle LiteralList nodes."""
        elements_code = ", ".join(
            self.visit(element) for element in node.elements
        )
        return f"[{elements_code}]"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralTuple) -> str:
        """Handle LiteralTuple nodes."""
        elements_code = ", ".join(
            self.visit(element) for element in node.elements
        )
        return (
            f"({elements_code},)"
            if len(node.elements) == 1
            else f"({elements_code})"
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralSet) -> str:
        """Handle LiteralSet nodes."""
        elements_code = ", ".join(
            self.visit(element) for element in node.elements
        )
        return f"{{{elements_code}}}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralDict) -> str:
        """Handle LiteralDict nodes."""
        items_code = ", ".join(
            f"{self.visit(key)}: {self.visit(value)}"
            for key, value in node.elements.items()
        )
        return f"{{{items_code}}}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DoWhileExpr) -> str:
        """Handle DoWhileExpr nodes."""
        body = self.visit(node.body)
        condition = self.visit(node.condition)
        return f"[{body} for _ in iter(lambda: True, False) if ({condition})]"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.DoWhileStmt) -> str:
        """Handle DoWhileStmt nodes."""
        body = self._generate_block(node.body)
        condition = self.visit(node.condition)
        return f"while True:\n{body}\n    if not {condition}:\n        break"
