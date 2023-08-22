"""Module for controle flow AST."""
from typing import Optional

from public import public

from astx.base import ASTKind, Expr, SourceLocation, StatementType
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
