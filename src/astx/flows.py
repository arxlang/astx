"""Module for controle flow AST."""
from typing import Optional

from astx.base import StatementType, Expr, SourceLocation, ASTKind
from astx.blocks import Block


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
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the IfStmt instance."""
        self.loc = loc
        self.condition = condition
        self.then = then
        self.else_ = else_
        self.kind = ASTKind.IfKind


class ForStmt(StatementType):
    """AST class for `For` statement."""

    var_name: str
    start: Expr
    end: Expr
    step: Expr
    body: Block

    def __init__(
        self,
        var_name: str,
        start: Expr,
        end: Expr,
        step: Expr,
        body: Block,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the ForStmt instance."""
        self.loc = loc
        self.var_name = var_name
        self.start = start
        self.end = end
        self.step = step
        self.body = body
        self.kind = ASTKind.ForKind
