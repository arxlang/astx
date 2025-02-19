"""Module for Exceptions."""

from __future__ import annotations

from typing import Iterable, Optional, cast

from public import public

from astx.base import (
    AST,
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
from astx.blocks import Block
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

    body: Block[AST]
    name: Optional[Identifier]
    types: Optional[ASTNodes[Identifier]]

    def __init__(
        self,
        body: Block[AST],
        name: Optional[Identifier] = None,
        types: Optional[Iterable[Identifier] | ASTNodes[Identifier]] = None,
        parent: Optional[ASTNodes] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the instance."""
        super().__init__(loc=loc, parent=parent)
        self.body = body
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

        self.kind = ASTKind.CatchHandlerStmtKind

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

    body: Block[AST]
    handlers: ASTNodes[CatchHandlerStmt]
    finally_handler: Optional[FinallyHandlerStmt]

    def __init__(
        self,
        body: Block[AST],
        handlers: Iterable[CatchHandlerStmt] | ASTNodes[CatchHandlerStmt],
        finally_handler: Optional[FinallyHandlerStmt] = None,
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

        self.finally_handler = finally_handler

        self.kind = ASTKind.ExceptionHandlerStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return "ExceptionHandlerStmt"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "EXCEPTION-HANDLER-STMT"

        body_dict = {"body": self.body.get_struct(simplified)}
        handlers_dict = {"handlers": self.handlers.get_struct(simplified)}
        finally_dict = (
            {"finally_handler": self.finally_handler.get_struct(simplified)}
            if self.finally_handler
            else {}
        )

        value: DictDataTypesStruct = {
            **cast(DictDataTypesStruct, body_dict),
            **cast(DictDataTypesStruct, handlers_dict),
            **cast(DictDataTypesStruct, finally_dict),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class FinallyHandlerStmt(StatementType):
    """AST class for finally statements."""

    body: Block[AST]

    def __init__(
        self,
        body: Block[AST],
        parent: Optional[ASTNodes] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize the instance."""
        super().__init__(loc=loc, parent=parent)
        self.body = body
        self.kind = ASTKind.FinallyHandlerStmtKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return "FinallyStmt"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "FINALLY-STMT"
        value: DictDataTypesStruct = {"body": self.body.get_struct(simplified)}

        return self._prepare_struct(key, value, simplified)
