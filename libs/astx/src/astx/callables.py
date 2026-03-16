"""
title: Module for callable ASTx.
"""

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
from astx.data import Variable
from astx.modifiers import MutabilityKind, ScopeKind, VisibilityKind
from astx.tools.typing import typechecked
from astx.types import AnyType

UNDEFINED = Undefined()


@public
@typechecked
class Argument(Variable):
    """
    title: AST class for argument definition.
    attributes:
      kind:
        type: ASTKind
      mutability:
        type: MutabilityKind
      name:
        type: str
      type_:
        type: DataType
      default:
        type: Expr
    """

    kind: ASTKind

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
        """
        title: Initialize the VarExprAST instance.
        parameters:
          name:
            type: str
          type_:
            type: DataType
          mutability:
            type: MutabilityKind
          default:
            type: Expr
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(name=name, loc=loc, parent=parent)
        self.mutability = mutability
        self.type_ = type_
        self.default = default
        self.kind = ASTKind.ArgumentKind

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        type_ = self.type_.__class__.__name__
        return f"Argument[{self.name}, {type_}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"Argument[{self.name}, {self.type_}] = {self.default}"
        value = self.default.get_struct()
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class Arguments(ASTNodes[Argument]):
    """
    title: AST class for argument definition.
    """

    def __init__(self, *args: Argument, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        for arg in args:
            self.append(arg)

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"Arguments({len(self.nodes)})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        args_nodes = []

        for node in self.nodes:
            args_nodes.append(node.get_struct(simplified))

        key = str(self)
        value = cast(ReprStruct, args_nodes)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class FunctionCall(DataType):
    """
    title: AST class for function call.
    attributes:
      kind:
        type: ASTKind
      fn:
        type: str
      args:
        type: Iterable[DataType]
      type_:
        type: DataType
    """

    kind: ASTKind

    fn: str
    args: Iterable[DataType]
    type_: DataType = AnyType()

    def __init__(
        self,
        fn: FunctionDef | str,
        args: Iterable[DataType],
        type_: DataType = AnyType(),
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the Call instance.
        parameters:
          fn:
            type: FunctionDef | str
          args:
            type: Iterable[DataType]
          type_:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.fn = fn if not isinstance(fn, FunctionDef) else fn.name
        self.args = args
        self.kind = ASTKind.CallKind
        self.type_ = type_

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        args = [str(arg) for arg in self.args]
        return f"Call[{self.fn}: {', '.join(args)}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        call_params = []

        for node in self.args:
            call_params.append(node.get_struct(simplified))

        key = f"FUNCTION-CALL[{self.fn}]"
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
    """
    title: AST class for function prototype declaration.
    attributes:
      loc:
        type: SourceLocation
      kind:
        type: ASTKind
      name:
        type: str
      args:
        type: Arguments
      return_type:
        type: AnyType
      scope:
        type: ScopeKind
      visibility:
        type: VisibilityKind
    """

    loc: SourceLocation
    kind: ASTKind

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
        """
        title: Initialize the FunctionPrototype instance.
        parameters:
          name:
            type: str
          args:
            type: Arguments
          return_type:
            type: AnyType
          scope:
            type: ScopeKind
          visibility:
            type: VisibilityKind
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.name = name
        self.args = args
        self.return_type = return_type
        self.loc = loc
        self.kind = ASTKind.PrototypeKind
        self.scope = scope
        self.visibility = visibility

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Get the AST structure that represent the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        raise Exception("Visitor method not necessary")


@public
@typechecked
class FunctionReturn(StatementType):
    """
    title: AST class for function `return` statement.
    attributes:
      kind:
        type: ASTKind
      value:
        type: DataType
    """

    kind: ASTKind

    value: DataType

    def __init__(
        self,
        value: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the Return instance.
        parameters:
          value:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.kind = ASTKind.ReturnKind

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        return f"Return[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = "RETURN"
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class FunctionDef(StatementType):
    """
    title: AST class for function definition.
    attributes:
      kind:
        type: ASTKind
      prototype:
        type: FunctionPrototype
      body:
        type: Block
    """

    kind: ASTKind

    prototype: FunctionPrototype
    body: Block

    def __init__(
        self,
        prototype: FunctionPrototype,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the Function instance.
        parameters:
          prototype:
            type: FunctionPrototype
          body:
            type: Block
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.prototype = prototype
        self.body = body
        self.kind = ASTKind.FunctionDefKind

    @property
    def name(self) -> str:
        """
        title: Return the function prototype name.
        returns:
          type: str
        """
        return self.prototype.name

    def __str__(self) -> str:
        """
        title: Return a string that represent the object.
        returns:
          type: str
        """
        return f"FunctionDef[{self.name}]"

    def __call__(
        self,
        args: tuple[DataType, ...],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> FunctionCall:
        """
        title: Initialize the Call instance.
        parameters:
          args:
            type: tuple[DataType, Ellipsis]
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        returns:
          type: FunctionCall
        """
        return FunctionCall(fn=self, args=args, loc=loc, parent=parent)

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Get the AST structure that represent the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
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
    """
    title: AST class for lambda expressions.
    attributes:
      kind:
        type: ASTKind
      params:
        type: Arguments
      body:
        type: Expr
    """

    kind: ASTKind

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
        """
        title: Return a string representation of the lambda expression.
        returns:
          type: str
        """
        params_str = ", ".join(param.name for param in self.params)
        return f"lambda {params_str}: {self.body}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the lambda expression.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = "LambdaExpr"
        value: ReprStruct = {
            "params": self.params.get_struct(simplified),
            "body": self.body.get_struct(simplified),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class FunctionAsyncDef(FunctionDef):
    """
    title: AST class for async function definition.
    attributes:
      kind:
        type: ASTKind
      prototype:
        type: FunctionPrototype
      body:
        type: Block
    """

    kind: ASTKind

    prototype: FunctionPrototype
    body: Block

    def __init__(
        self,
        prototype: FunctionPrototype,
        body: Block,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the FunctionAsync instance.
        parameters:
          prototype:
            type: FunctionPrototype
          body:
            type: Block
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(
            loc=loc, parent=parent, body=body, prototype=prototype
        )
        self.kind = ASTKind.FunctionAsyncDefKind

    def __str__(self) -> str:
        """
        title: Return a string that represent the object.
        returns:
          type: str
        """
        return f"FunctionAsyncDef[{self.name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Get the AST structure that represent the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
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
    """
    title: AST class for AwaitExpr.
    attributes:
      kind:
        type: ASTKind
      value:
        type: Optional[Expr]
    """

    kind: ASTKind

    value: Optional[Expr]

    def __init__(
        self,
        value: Optional[Expr],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the AwaitExpr instance.
        parameters:
          value:
            type: Optional[Expr]
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.kind = ASTKind.AwaitExprKind

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        return f"AwaitExpr[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = "AWAIT-EXPR"
        value = {} if self.value is None else self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class YieldExpr(Expr):
    """
    title: AST class for YieldExpr.
    attributes:
      kind:
        type: ASTKind
      value:
        type: Optional[Expr]
    """

    kind: ASTKind

    value: Optional[Expr]

    def __init__(
        self,
        value: Optional[Expr],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the YieldExpr instance.
        parameters:
          value:
            type: Optional[Expr]
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.kind = ASTKind.YieldExprKind

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        return f"YieldExpr[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = "YIELD-EXPR"
        value = {} if self.value is None else self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class YieldStmt(StatementType):
    """
    title: AST class for yield statement.
    attributes:
      kind:
        type: ASTKind
      value:
        type: Optional[Expr]
    """

    kind: ASTKind

    value: Optional[Expr]

    def __init__(
        self,
        value: Optional[Expr] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the YieldStmt instance.
        summary: |-

          value: The expression to yield (optional)
          loc: Source location of the statement
          parent: Parent AST node
        parameters:
          value:
            type: Optional[Expr]
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.kind = ASTKind.YieldStmtKind

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        return (
            f"YieldStmt[{self.value}]"
            if self.value is not None
            else "YieldStmt"
        )

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"YIELD-STMT[{id(self)}]" if simplified else "YIELD-STMT"
        value = (
            self.value.get_struct(simplified) if self.value is not None else {}
        )
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class YieldFromExpr(Expr):
    """
    title: AST class for YieldFromExpr.
    attributes:
      kind:
        type: ASTKind
      value:
        type: Expr
    """

    kind: ASTKind

    value: Expr

    def __init__(
        self,
        value: Expr,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the YieldFromExpr instance.
        parameters:
          value:
            type: Expr
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.kind = ASTKind.YieldFromExprKind

    def __str__(self) -> str:
        """
        title: Return a string representation of the object.
        returns:
          type: str
        """
        return f"YieldFromExpr[{self.value}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = "YIELDFROM-EXPR"
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)
