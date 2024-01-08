"""Module for callable ASTx."""
from typing import List, cast

from public import public

from astx.base import (
    ASTKind,
    DataType,
    Expr,
    ExprType,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.blocks import Block
from astx.modifiers import ScopeKind, VisibilityKind
from astx.variables import Variable


@public
class FunctionCall(Expr):
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

    def __str__(self) -> str:
        """Return a string representation of the object."""
        args = [str(arg) for arg in self.args]
        return f"Call[{self.callee}: {', '.join(args)}]"

    def get_struct(self) -> ReprStruct:
        """Return the AST structure of the object."""
        call_args = []

        for node in self.args:
            call_args.append(node.get_struct())

        call_node = {f"CALL[{self.callee}]": {"args": call_args}}
        return cast(ReprStruct, call_node)


@public
class FunctionPrototype(StatementType):
    """AST class for function prototype declaration."""

    name: str
    args: List[Variable]
    return_type: ExprType
    scope: ScopeKind
    visibility: VisibilityKind

    def __init__(  # noqa: PLR0913
        self,
        name: str,
        args: List[Variable],
        return_type: ExprType,
        scope: ScopeKind = ScopeKind.global_,
        visibility: VisibilityKind = VisibilityKind.public,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the FunctionPrototype instance."""
        self.name = name
        self.args = args
        self.return_type = return_type
        self.loc = loc
        self.kind = ASTKind.PrototypeKind
        self.scope = scope
        self.visibility = visibility

    def get_struct(self) -> ReprStruct:
        """Get the AST structure that represent the object."""
        raise Exception("Visitor method not necessary")


@public
class FunctionReturn(StatementType):
    """AST class for function `return` statement."""

    value: DataType

    def __init__(
        self, value: DataType, loc: SourceLocation = SourceLocation(0, 0)
    ) -> None:
        """Initialize the Return instance."""
        self.loc = loc
        self.value = value
        self.kind = ASTKind.ReturnKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"Return[{self.value}]"

    def get_struct(self) -> ReprStruct:
        """Return the AST structure of the object."""
        return {"RETURN": self.value.get_struct()}


@public
class Function(StatementType):
    """AST class for function definition."""

    prototype: FunctionPrototype
    body: Block

    def __init__(
        self,
        prototype: FunctionPrototype,
        body: Block,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the Function instance."""
        self.loc = loc
        self.prototype = prototype
        self.body = body
        self.kind = ASTKind.FunctionKind

    @property
    def name(self) -> str:
        """Return the function prototype name."""
        return self.prototype.name

    def __str__(self) -> str:
        """Return a string that represent the object."""
        return f"Function[{self.name}]"

    def get_struct(self) -> ReprStruct:
        """Get the AST structure that represent the object."""
        fn_args = []
        for arg in self.prototype.args:
            fn_args.append(arg.get_struct())

        fn_body = self.body.get_struct()

        node = {
            f"FUNCTION[{self.prototype.name}]": {
                "args": fn_args,
                "body": fn_body,
            }
        }
        return cast(ReprStruct, node)
