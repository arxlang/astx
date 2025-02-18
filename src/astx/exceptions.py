"""Module for Exceptions."""

from __future__ import annotations

from typing import Optional, cast

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    DictDataTypesStruct,
    Expr,
    Identifier,
    ReprStruct,
    SourceLocation,
    StatementType,
)
from astx.tools.typing import typechecked


@public
@typechecked
class ThrowStmt(StatementType):
    """AST class for throw statements."""

    exception: Optional[Expr]

    def __init__(
        self,
        exception: Optional[Expr] = None,
        parent: Optional[ASTNodes] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the instance."""
        super().__init__(loc=loc, parent=parent)
        self.exception = exception
        self.kind = ASTKind.ThrowStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        throw_str = (
            f"ThrowStmt[{self.exception}]" if self.exception else "ThrowStmt"
        )
        return throw_str

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "THROW-STMT"
        value = self.exception.get_struct(simplified) if self.exception else ""
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class CatchHandlerStmt(StatementType):
    """AST class for catch statements."""

    body: ASTNodes[Expr]
    name: Optional[Identifier]
    types: Optional[ASTNodes[Identifier]]

    def __init__(
        self,
        body: list[Expr] | ASTNodes[Expr],
        name: Optional[Identifier] = None,
        types: Optional[list[Identifier] | ASTNodes[Identifier]] = None,
        parent: Optional[ASTNodes] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the instance."""
        super().__init__(loc=loc, parent=parent)

        if isinstance(body, ASTNodes):
            self.body = body
        else:
            self.body = ASTNodes[Expr]()
            for b in body:
                self.body.append(b)

        self.name = name

        if types:
            if isinstance(types, ASTNodes):
                self.types = types
            else:
                self.types = ASTNodes[Identifier]()
                for t in types:
                    self.types.append(t)
        else:
            self.types = None

        self.kind = ASTKind.ThrowStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"CatchHandlerStmt[{self.name}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "CATCH-HANDLER-STMT"
        body_dict = {"body": self.body.get_struct(simplified)}
        name_dict = (
            {"name": self.name.get_struct(simplified)} if self.name else {}
        )
        types_dict = (
            {"types": self.types.get_struct(simplified)} if self.types else {}
        )

        value: DictDataTypesStruct = {
            **cast(DictDataTypesStruct, body_dict),
            **cast(DictDataTypesStruct, name_dict),
            **cast(DictDataTypesStruct, types_dict),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ExceptionHandlerStmt(StatementType):
    """AST class for try statements."""

    body: ASTNodes[Expr]
    handlers: ASTNodes[CatchHandlerStmt]

    def __init__(
        self,
        body: ASTNodes[Expr],
        handlers: list[CatchHandlerStmt] | ASTNodes[CatchHandlerStmt],
        parent: Optional[ASTNodes] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the instance."""
        super().__init__(loc=loc, parent=parent)
        self.body = body

        if isinstance(handlers, ASTNodes):
            self.handlers = handlers
        else:
            self.handlers = ASTNodes[CatchHandlerStmt]()
            for h in handlers:
                self.handlers.append(h)

        # self.final_body = final_body
        self.kind = ASTKind.ThrowStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"ExceptionHandlerStmt[{self.body}]"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "EXCEPTION-HANDLER-STMT"

        body_dict = {"body": self.body.get_struct(simplified)}
        handlers_dict = {"handlers": self.handlers.get_struct(simplified)}

        value: DictDataTypesStruct = {
            **cast(DictDataTypesStruct, body_dict),
            **cast(DictDataTypesStruct, handlers_dict),
        }
        return self._prepare_struct(key, value, simplified)
