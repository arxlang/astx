"""Module for controle flow AST."""

from typing import Optional, cast

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    Expr,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.blocks import Block
from astx.variables import InlineVariableDeclaration


@public
class If(StatementType):
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
        """Initialize the If instance."""
        super().__init__(loc=loc, parent=parent)
        self.loc = loc
        self.condition = condition
        self.then = then
        self.else_ = else_
        self.kind = ASTKind.IfKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"If[{self.condition}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        if_condition = self.condition.get_struct(simplified)
        if_then = self.then.get_struct(simplified)

        if self.else_:
            if_else = self.else_.get_struct(simplified)
            if_else_struct = self._prepare_struct("ELSE", if_else, simplified)
        else:
            if_else_struct = {}

        if_condition_struct = self._prepare_struct(
            "CONDITION", if_condition, simplified
        )
        if_then_struct = self._prepare_struct("THEN", if_then, simplified)

        key = "IF-STMT"
        value = cast(
            ReprStruct,
            {
                **if_condition_struct,
                **if_then_struct,
                **if_else_struct,
            },
        )

        return self._prepare_struct(key, value, simplified)


@public
class ForRangeLoop(StatementType):
    """AST class for `For` Loop Range statement."""

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
        """Initialize the ForStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.variable = variable
        self.start = start
        self.end = end
        self.step = step
        self.body = body
        self.kind = ASTKind.ForKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        start = self.start
        end = self.end
        step = self.step
        var_name = self.variable.name
        return f"ForRangeLoop({var_name}=[{start}:{end}:{step}])"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        for_start = self.start.get_struct(simplified)
        for_end = self.end.get_struct(simplified)
        for_step = self.step.get_struct(simplified)
        for_body = self.body.get_struct(simplified)

        for_start_struct = self._prepare_struct("start", for_start, simplified)
        for_end_struct = self._prepare_struct("end", for_end, simplified)
        for_step_struct = self._prepare_struct("step", for_step, simplified)
        for_body_struct = self._prepare_struct("body", for_body, simplified)

        key = "FOR-RANGE-STMT"
        value = cast(
            ReprStruct,
            {
                **for_start_struct,
                **for_end_struct,
                **for_step_struct,
                **for_body_struct,
            },
        )

        return self._prepare_struct(key, value, simplified)


@public
class ForCountLoop(StatementType):
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
        """Initialize the ForStmt instance."""
        super().__init__(loc=loc, parent=parent)
        self.initializer = initializer
        self.condition = condition
        self.update = update
        self.body = body
        self.kind = ASTKind.ForKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        init = self.initializer
        cond = self.condition
        update = self.update
        return f"ForCountLoop({init};{cond};{update})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        for_init = self.initializer.get_struct(simplified)
        for_cond = self.condition.get_struct(simplified)
        for_update = self.update.get_struct(simplified)
        for_body = self.body.get_struct(simplified)

        for_init_struct = self._prepare_struct(
            "initializer", for_init, simplified
        )
        for_cond_struct = self._prepare_struct(
            "condition", for_cond, simplified
        )
        for_update_struct = self._prepare_struct(
            "update", for_update, simplified
        )
        for_body_struct = self._prepare_struct("body", for_body, simplified)

        key = "FOR-COUNT-STMT"
        value = cast(
            ReprStruct,
            {
                **for_init_struct,
                **for_cond_struct,
                **for_update_struct,
                **for_body_struct,
            },
        )

        return self._prepare_struct(key, value, simplified)
