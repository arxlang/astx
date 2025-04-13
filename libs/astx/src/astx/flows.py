"""Module for controle flow AST."""

from __future__ import annotations

from typing import Optional, cast

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    DictDataTypesStruct,
    Expr,
    Identifier,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.blocks import Block
from astx.tools.typing import typechecked
from astx.variables import InlineVariableDeclaration


@public
@typechecked
class IfStmt(StatementType):
    """AST class for `if` statement."""

    condition: Expr
    then: Block
    else_: Optional[Block]

    def __init__(
        self,
        condition: Expr,
        then: Block,
        else_: Optional[Block] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the IfStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.loc = loc
        self.condition = condition
        self.then = then
        self.else_ = else_
        self.kind = ASTKind.IfStmtKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"IfStmt[{self.condition}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        if_condition = {"condition": self.condition.get_struct(simplified)}
        if_then = {"then-block": self.then.get_struct(simplified)}
        if_else: ReprStruct = {}

        if self.else_ is not None:
            if_else = {"else-block": self.else_.get_struct(simplified)}

        key = f"IF-STMT[{id(self)}]" if simplified else "IF-STMT"
        value: ReprStruct = {
            **cast(DictDataTypesStruct, if_condition),
            **cast(DictDataTypesStruct, if_then),
            **cast(DictDataTypesStruct, if_else),
        }

        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class IfExpr(Expr):
    """AST class for `if` expression."""

    condition: Expr
    then: Block
    else_: Optional[Block]

    def __init__(
        self,
        condition: Expr,
        then: Block,
        else_: Optional[Block] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the IfExpr instance."""
        super().__init__(loc=loc, parent=parent)
        self.loc = loc
        self.condition = condition
        self.then = then
        self.else_ = else_
        self.kind = ASTKind.IfExprKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"IfExpr[{self.condition}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        if_condition = {"condition": self.condition.get_struct(simplified)}
        if_then = {"then-block": self.then.get_struct(simplified)}
        if_else: ReprStruct = {}

        if self.else_ is not None:
            if_else = {"else-block": self.else_.get_struct(simplified)}

        key = "IF-EXPR"
        value: ReprStruct = {
            **cast(DictDataTypesStruct, if_condition),
            **cast(DictDataTypesStruct, if_then),
            **cast(DictDataTypesStruct, if_else),
        }

        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ForRangeLoopStmt(StatementType):
    """AST class for `For` Range Statement."""

    variable: InlineVariableDeclaration
    start: Expr
    end: Expr
    step: Expr
    body: Block

    def __init__(
        self,
        variable: InlineVariableDeclaration,
        start: Expr,
        end: Expr,
        step: Expr,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the ForRangeLoopStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.variable = variable
        self.start = start
        self.end = end
        self.step = step
        self.body = body
        self.kind = ASTKind.ForRangeLoopStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        start = self.start
        end = self.end
        step = self.step
        var_name = self.variable.name
        return f"ForRangeLoopStmt({var_name}=[{start}:{end}:{step}])"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        for_start = {"start": self.start.get_struct(simplified)}
        for_end = {"end": self.end.get_struct(simplified)}
        for_step = {"step": self.step.get_struct(simplified)}
        for_body = self.body.get_struct(simplified)

        key = (
            f"FOR-RANGE-LOOP-STMT[{id(self)}]"
            if simplified
            else "FOR-RANGE-LOOP-STMT"
        )
        value: ReprStruct = {
            **cast(DictDataTypesStruct, for_start),
            **cast(DictDataTypesStruct, for_end),
            **cast(DictDataTypesStruct, for_step),
            **cast(DictDataTypesStruct, for_body),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ForRangeLoopExpr(Expr):
    """AST class for `For` Range Expression."""

    variable: InlineVariableDeclaration
    start: Expr
    end: Expr
    step: Expr
    body: Block

    def __init__(
        self,
        variable: InlineVariableDeclaration,
        start: Expr,
        end: Expr,
        step: Expr,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the ForRangeLoopExpr instance."""
        super().__init__(loc=loc, parent=parent)
        self.variable = variable
        self.start = start
        self.end = end
        self.step = step
        self.body = body
        self.kind = ASTKind.ForRangeLoopExprKind
        # self.step = step if step is not None else LiteralInt32(1)

    def __str__(self) -> str:
        """Return a string that represents the object."""
        var_name = self.variable.name
        # note: it would be nice to have the following structure
        #    ForRangeLoopExpr({var_name}=[{start}:{end}:{step}])
        #    but we would need to have first something like a resolver
        #    otherwise it could be a very large output
        return f"ForRangeLoopExpr[{var_name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        for_var = {"var": self.variable.get_struct(simplified)}
        for_start = {"start": self.start.get_struct(simplified)}
        for_end = {"end": self.end.get_struct(simplified)}
        for_step = {"step": self.step.get_struct(simplified)}
        for_body = self.body.get_struct(simplified)

        key = "FOR-RANGE-LOOP-EXPR"
        value: ReprStruct = {
            **cast(DictDataTypesStruct, for_var),
            **cast(DictDataTypesStruct, for_start),
            **cast(DictDataTypesStruct, for_end),
            **cast(DictDataTypesStruct, for_step),
            **cast(DictDataTypesStruct, for_body),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ForCountLoopStmt(StatementType):
    """
    AST class for a simple Count-Controlled `For` Loop statement.

    This is a very basic `for` loop, used by languages like C or C++.
    """

    initializer: InlineVariableDeclaration
    condition: Expr
    update: Expr
    body: Block

    def __init__(
        self,
        initializer: InlineVariableDeclaration,
        condition: Expr,
        update: Expr,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the ForCountLoopStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.initializer = initializer
        self.condition = condition
        self.update = update
        self.body = body
        self.kind = ASTKind.ForCountLoopStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        init = self.initializer
        cond = self.condition
        update = self.update
        return f"ForCountLoopStmt({init};{cond};{update})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        for_init = {"initialization": self.initializer.get_struct(simplified)}
        for_cond = {"condition": self.condition.get_struct(simplified)}
        for_update = {"update": self.update.get_struct(simplified)}
        for_body = self.body.get_struct(simplified)

        key = f"FOR-COUNT-STMT[{id(self)}]" if simplified else "FOR-COUNT-STMT"
        value: ReprStruct = {
            **cast(DictDataTypesStruct, for_init),
            **cast(DictDataTypesStruct, for_cond),
            **cast(DictDataTypesStruct, for_update),
            **cast(DictDataTypesStruct, for_body),
        }

        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ForCountLoopExpr(Expr):
    """
    AST class for a simple Count-Controlled `For` Loop expression.

    This is a very basic `for` loop, used by languages like C or C++.
    """

    initializer: InlineVariableDeclaration
    condition: Expr
    update: Expr
    body: Block

    def __init__(
        self,
        initializer: InlineVariableDeclaration,
        condition: Expr,
        update: Expr,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the ForLoopCountExpr instance."""
        super().__init__(loc=loc, parent=parent)
        self.initializer = initializer
        self.condition = condition
        self.update = update
        self.body = body
        self.kind = ASTKind.ForCountLoopExprKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        init = self.initializer
        cond = self.condition
        update = self.update
        return f"ForCountLoopExpr({init};{cond};{update})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        for_init = {"initialization": self.initializer.get_struct(simplified)}
        for_cond = {"condition": self.condition.get_struct(simplified)}
        for_update = {"update": self.update.get_struct(simplified)}
        for_body = self.body.get_struct(simplified)

        key = "FOR-COUNT-EXPR"
        value: ReprStruct = {
            **cast(DictDataTypesStruct, for_init),
            **cast(DictDataTypesStruct, for_cond),
            **cast(DictDataTypesStruct, for_update),
            **cast(DictDataTypesStruct, for_body),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class AsyncForRangeLoopStmt(StatementType):
    """AST class for asynchronous `For` Range Statement."""

    variable: InlineVariableDeclaration
    start: Optional[Expr]
    end: Expr
    step: Optional[Expr]
    body: Block

    def __init__(
        self,
        variable: InlineVariableDeclaration,
        start: Optional[Expr],
        end: Expr,
        step: Optional[Expr],
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the AsyncForRangeLoopStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.variable = variable
        self.start = start
        self.end = end
        self.step = step
        self.body = body
        self.kind = ASTKind.AsyncRangeLoopStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        start = self.start
        end = self.end
        step = self.step
        var_name = self.variable.name
        return f"AsyncForRangeLoopStmt({var_name}=[{start}:{end}:{step}])"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        for_start = {
            "start": {}
            if self.start is None
            else self.start.get_struct(simplified)
        }
        for_end = {"end": self.end.get_struct(simplified)}
        for_step = {
            "step": {}
            if self.step is None
            else self.step.get_struct(simplified)
        }
        for_body = self.body.get_struct(simplified)

        key = "ASYNC-FOR-RANGE-LOOP-STMT"
        value: ReprStruct = {
            **cast(DictDataTypesStruct, for_start),
            **cast(DictDataTypesStruct, for_end),
            **cast(DictDataTypesStruct, for_step),
            **cast(DictDataTypesStruct, for_body),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class AsyncForRangeLoopExpr(Expr):
    """AST class for asynchronous `For` Range Expression."""

    variable: InlineVariableDeclaration
    start: Optional[Expr]
    end: Expr
    step: Optional[Expr]
    body: Block

    def __init__(
        self,
        variable: InlineVariableDeclaration,
        start: Optional[Expr],
        end: Expr,
        step: Optional[Expr],
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the AsyncForRangeLoopExpr instance."""
        super().__init__(loc=loc, parent=parent)
        self.variable = variable
        self.start = start
        self.end = end
        self.step = step
        self.body = body
        self.kind = ASTKind.AsyncRangeLoopExprKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        var_name = self.variable.name
        return f"AsyncForRangeLoopExpr[{var_name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        for_var = {"var": self.variable.get_struct(simplified)}
        for_start = {
            "start": {}
            if self.start is None
            else self.start.get_struct(simplified)
        }
        for_end = {"end": self.end.get_struct(simplified)}
        for_step = {
            "step": {}
            if self.step is None
            else self.step.get_struct(simplified)
        }
        for_body = self.body.get_struct(simplified)

        key = "ASYNC-FOR-RANGE-LOOP-EXPR"
        value: ReprStruct = {
            **cast(DictDataTypesStruct, for_var),
            **cast(DictDataTypesStruct, for_start),
            **cast(DictDataTypesStruct, for_end),
            **cast(DictDataTypesStruct, for_step),
            **cast(DictDataTypesStruct, for_body),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class BreakStmt(StatementType):
    """AST class for break statement."""

    def __init__(
        self,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the BreakStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.kind = ASTKind.BreakStmtKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return "BreakStmt"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "BREAK-STMT"
        value: DictDataTypesStruct = {}
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ContinueStmt(StatementType):
    """AST class for continue statement."""

    def __init__(
        self,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the ContinueStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.kind = ASTKind.ContinueStmtKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return "ContinueStmt"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "CONTINUE-STMT"
        value: DictDataTypesStruct = {}
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class WhileStmt(StatementType):
    """AST class for `while` statement."""

    condition: Expr
    body: Block

    def __init__(
        self,
        condition: Expr,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the WhileStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.condition = condition
        self.body = body
        self.kind = ASTKind.WhileStmtKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"WhileStmt[{self.condition}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        while_condition = self.condition.get_struct(simplified)
        while_body = self.body.get_struct(simplified)

        key = f"WHILE-STMT[{id(self)}]" if simplified else "WHILE-STMT"
        value: ReprStruct = {
            **cast(DictDataTypesStruct, while_condition),
            **cast(DictDataTypesStruct, while_body),
        }

        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class WhileExpr(Expr):
    """AST class for `while` expression."""

    condition: Expr
    body: Block

    def __init__(
        self,
        condition: Expr,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the WhileExpr instance."""
        super().__init__(loc=loc, parent=parent)
        self.condition = condition
        self.body = body
        self.kind = ASTKind.WhileExprKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"WhileExpr[{self.condition}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        while_condition = self.condition.get_struct(simplified)
        while_body = self.body.get_struct(simplified)

        key = "WHILE-EXPR"
        value: ReprStruct = {
            **cast(DictDataTypesStruct, while_condition),
            **cast(DictDataTypesStruct, while_body),
        }

        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class CaseStmt(StatementType):
    """AST class for a case in a Switch statement."""

    condition: Optional[Expr] = None
    body: Block
    default: bool = False

    def __init__(
        self,
        body: Block,
        condition: Optional[Expr] = None,
        default: bool = False,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the CaseStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.condition = condition
        self.body = body
        self.default = default
        self.kind = ASTKind.CaseStmtKind

        if self.default is False and self.condition is None:
            raise ValueError(
                "Condition must be provided for non-default branches."
            )

        if self.default is True and self.condition is not None:
            raise ValueError(
                "Condition must NOT be provided for default branches."
            )

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return (
            f"CaseStmt[{self.condition}]"
            if self.condition
            else "CaseStmt[default]"
        )

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        default_case = "default" if self.condition is None else ""
        default_only = "[default]" if self.condition is None else ""
        id_str = f"{id(self)}" if simplified else ""

        key = (
            f"CASE-STMT[{id_str}{default_case}]"
            if simplified and self.condition is not None
            else f"CASE-STMT[{id_str}, {default_case}]"
            if simplified
            else f"CASE-STMT{default_only}"
        )

        condition_dict = (
            {}
            if self.condition is None
            else {"condition": self.condition.get_struct(simplified)}
        )
        value = {
            **cast(DictDataTypesStruct, condition_dict),
            "body": self.body.get_struct(simplified),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class SwitchStmt(StatementType):
    """AST class for Switch statements based on Rust's match syntax."""

    value: Expr
    cases: ASTNodes[CaseStmt]

    def __init__(
        self,
        value: Expr,
        cases: list[CaseStmt] | ASTNodes[CaseStmt],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the SwitchStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.value = value

        if isinstance(cases, ASTNodes):
            self.cases = cases
        else:
            self.cases = ASTNodes[CaseStmt]()
            for case in cases:
                self.cases.append(case)

        self.kind = ASTKind.SwitchStmtKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"SwitchStmt[{len(self.cases)}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = f"SWITCH-STMT[{id(self)}]" if simplified else "SWITCH-STMT"
        case_dict = {}
        for d in range(len(self.cases)):
            case_dict[f"case_{d}"] = self.cases[d].get_struct(simplified)

        value: DictDataTypesStruct = {
            "value": self.value.get_struct(simplified),
            **cast(DictDataTypesStruct, {"cases": case_dict}),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class GotoStmt(StatementType):
    """AST class for function `Goto` statement."""

    label: Identifier

    def __init__(
        self,
        label: Identifier,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the Return instance."""
        super().__init__(loc=loc, parent=parent)
        self.label = label
        self.kind = ASTKind.GotoStmtKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"Goto[{self.label.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = f"GOTO-STMT[{self.label.value}]"
        value: DictDataTypesStruct = {}
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class DoWhileStmt(WhileStmt):
    """AST class for `do-while` statement."""

    def __init__(
        self,
        condition: Expr,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the DoWhileStmt instance."""
        super().__init__(
            condition=condition, body=body, loc=loc, parent=parent
        )
        self.kind = ASTKind.DoWhileStmtKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"DoWhileStmt[{self.condition}]"


@public
@typechecked
class DoWhileExpr(WhileExpr):
    """AST class for `do-while` expression."""

    def __init__(
        self,
        condition: Expr,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the DoWhileExpr instance."""
        super().__init__(
            condition=condition, body=body, loc=loc, parent=parent
        )
        self.kind = ASTKind.DoWhileExprKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"DoWhileExpr[{self.condition}]"
