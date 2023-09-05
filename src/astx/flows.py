"""Module for controle flow AST."""
from typing import Optional, cast

from public import public

from astx.base import ASTKind, Expr, ReprStruct, SourceLocation, StatementType
from astx.blocks import Block
from astx.variables import Variable


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

    def get_struct(self) -> ReprStruct:
        """Return the AST structure of the object."""
        if_condition = self.condition.get_struct()
        if_then = self.then.get_struct()

        if self.else_:
            if_else = self.else_.get_struct()
        else:
            if_else = []

        node = {
            "IF-STMT": {
                "CONDITION": if_condition,
                "THEN": if_then,
            }
        }

        if if_else:
            node["IF-STMT"]["ELSE"] = if_else

        return cast(ReprStruct, node)


@public
class ForRangeLoop(StatementType):
    """AST class for `For` Loop Range statement."""

    variable: Variable
    start: Expr
    end: Expr
    step: Expr
    body: Block

    def __init__(  # noqa: PLR0913
        self,
        variable: Variable,
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

    def get_struct(self) -> ReprStruct:
        """Return the AST structure of the object."""
        for_start = self.start.get_struct()
        for_end = self.end.get_struct()
        for_step = self.step.get_struct()
        for_body = self.body.get_struct()

        return {
            "FOR-RANGE-STMT": {
                "start": for_start,
                "end": for_end,
                "step": for_step,
                "body": for_body,
            }
        }


@public
class ForCountLoop(StatementType):
    """
    AST class for a simple Count-Controlled `For` Loop statement.

    This is a very basic `for` loop, used by languages like C or C++.
    """

    initializer: Expr
    condition: Expr
    update: Expr
    body: Block

    def __init__(  # noqa: PLR0913
        self,
        initializer: Expr,
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

    def get_struct(self) -> ReprStruct:
        """Return the AST structure of the object."""
        for_init = self.initializer.get_struct()
        for_cond = self.condition.get_struct()
        for_update = self.update.get_struct()
        for_body = self.body.get_struct()

        return {
            "FOR-COUNT-STMT": {
                "initializer": for_init,
                "condition": for_cond,
                "update": for_update,
                "body": for_body,
            }
        }
