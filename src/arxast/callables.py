from typing import List

from arxast.base import (
    ASTKind,
    SourceLocation,
    Expr,
    ExprType,
    StatementType,
)
from arxast.blocks import Block
from arxast.datatypes import Variable
from arxast.modifiers import ScopeKind, VisibilityKind


class Call(Expr):
    """AST class for function call."""

    def __init__(
        self,
        callee: str,
        args: List[Variable],
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the Call instance."""
        super().__init__(loc)
        self.callee = callee
        self.args = args
        self.kind = ASTKind.CallKind


class FunctionPrototype(StatementType):
    """AST class for function prototype declaration."""

    name: str
    args: List[Variable]
    return_type: ExprType
    scope: ScopeKind
    visibility: VisibilityKind

    def __init__(
        self,
        name: str,
        return_type: ExprType,
        args: List[Variable],
        scope: ScopeKind = ScopeKind.global_,
        visibility: VisibilityKind = VisibilityKind.public,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the FunctionPrototype instance."""
        self.name = name
        self.args = args
        self.type_name = type_name
        self.line = loc.line
        self.kind = ASTKind.PrototypeKind
        self.scope = scope
        self.visibility = visibility


class Return(StatementType):
    """AST class for function `return` statement."""

    value: Expr

    def __init__(
        self, value: Expr, loc: SourceLocation = SourceLocation(0, 0)
    ) -> None:
        """Initialize the Return instance."""
        self.loc = loc
        self.value = value
        self.kind = ASTKind.ReturnKind


class Function(StatementType):
    """AST class for function definition."""

    proto: FunctionPrototype
    body: Block

    def __init__(
        self,
        proto: FunctionPrototype,
        body: Block,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the Function instance."""
        self.loc = loc
        self.proto = proto
        self.body = body
        self.kind = ASTKind.FunctionKind
