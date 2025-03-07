"""Module for callable ASTx."""

from __future__ import annotations

from typing import Any, Iterable, Optional, cast

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    DataType,
    Expr,
    ReprStruct,
    SourceLocation,
    StatementType,
    Undefined,
)
from astx.blocks import Block
from astx.modifiers import MutabilityKind, ScopeKind, VisibilityKind
from astx.tools.typing import typechecked
from astx.types import AnyType
from astx.variables import Variable

UNDEFINED = Undefined()


@public
@typechecked
class Argument(Variable):
    """AST class for argument definition."""

    mutability: MutabilityKind
    name: str
    type_: DataType
    default: Expr

    def __init__(
        self,
        name: str,
        type_: DataType,
        mutability: MutabilityKind = MutabilityKind.constant,
        default: Expr = UNDEFINED,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the VarExprAST instance."""
        super().__init__(name=name, loc=loc, parent=parent)
        self.mutability = mutability
        self.type_ = type_
        self.default = default
        self.kind = ASTKind.ArgumentKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        type_ = self.type_.__class__.__name__
        return f"Argument[{self.name}, {type_}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = f"Argument[{self.name}, {self.type_}] = {self.default}"
        value = self.default.get_struct()
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class Arguments(ASTNodes[Argument]):
    """AST class for argument definition."""

    def __init__(self, *args: Argument, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        for arg in args:
            self.append(arg)

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"Arguments({len(self.nodes)})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        args_nodes = []

        for node in self.nodes:
            args_nodes.append(node.get_struct(simplified))

        key = str(self)
        value = cast(ReprStruct, args_nodes)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class FunctionCall(DataType):
    """AST class for function call."""

    fn: FunctionDef
    args: Iterable[DataType]
    type_: DataType = AnyType()

    def __init__(
        self,
        fn: FunctionDef,
        args: Iterable[DataType],
        type_: DataType = AnyType(),
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the Call instance."""
        super().__init__(loc=loc, parent=parent)
        self.fn = fn
        self.args = args
        self.kind = ASTKind.CallKind
        self.type_ = type_

    def __str__(self) -> str:
        """Return a string representation of the object."""
        args = [str(arg) for arg in self.args]
        return f"Call[{self.fn}: {', '.join(args)}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        call_params = []

        for node in self.args:
            call_params.append(node.get_struct(simplified))

        key = f"FUNCTION-CALL[{self.fn.name}]"
        value = cast(
            ReprStruct,
            {
                f"Parameters ({len(call_params)})": {
                    f"param({idx})": param
                    for idx, param in enumerate(call_params)
                }
            },
        )

        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class FunctionPrototype(StatementType):
    """AST class for function prototype declaration."""

    name: str
    args: Arguments
    return_type: AnyType
    scope: ScopeKind
    visibility: VisibilityKind

    def __init__(
        self,
        name: str,
        args: Arguments,
        return_type: AnyType,
        scope: ScopeKind = ScopeKind.global_,
        visibility: VisibilityKind = VisibilityKind.public,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the FunctionPrototype instance."""
        super().__init__(loc=loc, parent=parent)
        self.name = name
        self.args = args
        self.return_type = return_type
        self.loc = loc
        self.kind = ASTKind.PrototypeKind
        self.scope = scope
        self.visibility = visibility

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Get the AST structure that represent the object."""
        raise Exception("Visitor method not necessary")


@public
@typechecked
class FunctionReturn(StatementType):
    """AST class for function `return` statement."""

    value: DataType

    def __init__(
        self,
        value: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the Return instance."""
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.kind = ASTKind.ReturnKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"Return[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "RETURN"
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class FunctionDef(StatementType):
    """AST class for function definition."""

    prototype: FunctionPrototype
    body: Block

    def __init__(
        self,
        prototype: FunctionPrototype,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the Function instance."""
        super().__init__(loc=loc, parent=parent)
        self.prototype = prototype
        self.body = body
        self.kind = ASTKind.FunctionDefKind

    @property
    def name(self) -> str:
        """Return the function prototype name."""
        return self.prototype.name

    def __str__(self) -> str:
        """Return a string that represent the object."""
        return f"FunctionDef[{self.name}]"

    def __call__(
        self,
        args: tuple[DataType, ...],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> FunctionCall:
        """Initialize the Call instance."""
        return FunctionCall(fn=self, args=args, loc=loc, parent=parent)

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Get the AST structure that represent the object."""
        fn_args = self.prototype.args.get_struct(simplified)
        fn_body = self.body.get_struct(simplified)

        key = f"FUNCTION-DEF[{self.prototype.name}]"
        args_struct = {"args": fn_args}
        body_struct = {"body": fn_body}

        value: ReprStruct = {**args_struct, **body_struct}
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class LambdaExpr(Expr):
    """AST class for lambda expressions."""

    params: Arguments = Arguments()
    body: Expr

    def __init__(
        self,
        body: Expr,
        params: Arguments = Arguments(),
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.params = params
        self.body = body
        self.kind = ASTKind.LambdaExprKind

    def __str__(self) -> str:
        """Return a string representation of the lambda expression."""
        params_str = ", ".join(param.name for param in self.params)
        return f"lambda {params_str}: {self.body}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the lambda expression."""
        key = "LambdaExpr"
        value: ReprStruct = {
            "params": self.params.get_struct(simplified),
            "body": self.body.get_struct(simplified),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class FunctionAsyncDef(FunctionDef):
    """AST class for async function definition."""

    prototype: FunctionPrototype
    body: Block

    def __init__(
        self,
        prototype: FunctionPrototype,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the FunctionAsync instance."""
        super().__init__(
            loc=loc, parent=parent, body=body, prototype=prototype
        )
        self.kind = ASTKind.FunctionAsyncDefKind

    def __str__(self) -> str:
        """Return a string that represent the object."""
        return f"FunctionAsyncDef[{self.name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Get the AST structure that represent the object."""
        fn_args = self.prototype.args.get_struct(simplified)
        fn_body = self.body.get_struct(simplified)

        key = f"FUNCTIONASYNC-DEF[{self.prototype.name}]"
        args_struct = {"args": fn_args}
        body_struct = {"body": fn_body}

        value: ReprStruct = {**args_struct, **body_struct}
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class AwaitExpr(Expr):
    """AST class for AwaitExpr."""

    value: Optional[Expr]

    def __init__(
        self,
        value: Optional[Expr],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the AwaitExpr instance."""
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.kind = ASTKind.AwaitExprKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"AwaitExpr[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "AWAIT-EXPR"
        value = {} if self.value is None else self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class YieldExpr(Expr):
    """AST class for YieldExpr."""

    value: Optional[Expr]

    def __init__(
        self,
        value: Optional[Expr],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the YieldExpr instance."""
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.kind = ASTKind.YieldExprKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"YieldExpr[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "YIELD-EXPR"
        value = {} if self.value is None else self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class YieldFromExpr(Expr):
    """AST class for YieldFromExpr."""

    value: Expr

    def __init__(
        self,
        value: Expr,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the YieldFromExpr instance."""
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.kind = ASTKind.YieldFromExprKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"YieldFromExpr[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "YIELDFROM-EXPR"
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)
