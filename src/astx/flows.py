"""Module for controle flow AST."""

from typing import Optional, cast

from public import public

from astx.base import ASTKind, Expr, ReprStruct, SourceLocation, StatementType
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
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the If instance."""
        self.loc = loc
        self.condition = condition
        self.then = then
        self.else_ = else_
        self.kind = ASTKind.IfKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"If[{self.condition}]"

    def get_struct(self, simplified: bool = True) -> ReprStruct:
        """Return the AST structure of the object."""
        if_condition = self.condition.get_struct(simplified)
        if_then = self.then.get_struct(simplified)

        if self.else_:
            if_else = {"ELSE": self.else_.get_struct(simplified)}
        else:
            if_else = {}

        key = "IF-STMT"
        value = cast(
            ReprStruct, {"CONDITION": if_condition, "THEN": if_then, **if_else}
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
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the ForStmt instance."""
        self.loc = loc
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

    def get_struct(self, simplified: bool = True) -> ReprStruct:
        """Return the AST structure of the object."""
        for_start = self.start.get_struct(simplified)
        for_end = self.end.get_struct(simplified)
        for_step = self.step.get_struct(simplified)
        for_body = self.body.get_struct(simplified)

        key = "FOR-RANGE-STMT"
        value = cast(
            ReprStruct,
            {
                "start": for_start,
                "end": for_end,
                "step": for_step,
                "body": for_body,
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
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the ForStmt instance."""
        self.loc = loc
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

    def get_struct(self, simplified: bool = True) -> ReprStruct:
        """Return the AST structure of the object."""
        for_init = self.initializer.get_struct(simplified)
        for_cond = self.condition.get_struct(simplified)
        for_update = self.update.get_struct(simplified)
        for_body = self.body.get_struct(simplified)

        key = "FOR-COUNT-STMT"
        value = cast(
            ReprStruct,
            {
                "initializer": for_init,
                "condition": for_cond,
                "update": for_update,
                "body": for_body,
            },
        )

        return self._prepare_struct(key, value, simplified)
