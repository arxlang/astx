from typing import List, Tuple

from arxast.base import StatementType, Expr, SourceLocation
from arxast.blocks import Block


class IfStmtAST(StatementType):
    """AST class for `if` statement."""

    cond: Expr
    then_: Block
    else_: Block

    def __init__(
        self,
        cond: Expr,
        then_: Block,
        else_: Block,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the IfStmtAST instance."""
        self.loc = loc
        self.cond = cond
        self.then_ = then_
        self.else_ = else_
        self.kind = ASTKind.IfKind


class ForStmtAST(StatementType):
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
        """Initialize the ForStmtAST instance."""
        self.loc = loc
        self.var_name = var_name
        self.start = start
        self.end = end
        self.step = step
        self.body = body
        self.kind = ASTKind.ForKind


class VarExprAST(StatementType):
    """AST class for variable declaration."""

    var_names: List[Tuple[str, Expr]]
    type_name: str
    body: Block

    def __init__(
        self,
        var_names: List[Tuple[str, Expr]],
        type_name: str,
        body: Block,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the VarExprAST instance."""
        self.loc = loc
        self.var_names = var_names
        self.type_name = type_name
        self.body = body
        self.kind = ASTKind.VarKind
