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

        key = "IF-STMT"
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

        key = "FOR-RANGE-LOOP-STMT"
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

        key = "FOR-COUNT-STMT"
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

        key = "WHILE-STMT"
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
