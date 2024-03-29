# mypy: disable-error-code="attr-defined"
"""ASTx."""
from importlib import metadata as importlib_metadata

from astx import (
    base,
    blocks,
    callables,
    datatypes,
    flows,
    mixes,
    operators,
    symbol_table,
    variables,
)
from astx.base import (
    AST,
    ASTKind,
    DataType,
    Expr,
    ExprType,
    OperatorType,
    SourceLocation,
    StatementType,
    Undefined,
)
from astx.blocks import (
    Block,
    Module,
)
from astx.callables import (
    Function,
    FunctionCall,
    FunctionPrototype,
    FunctionReturn,
)
from astx.datatypes import (
    Boolean,
    DataTypeOps,
    Float16,
    Float32,
    Float64,
    Floating,
    Int8,
    Int16,
    Int32,
    Int64,
    Integer,
    Literal,
    LiteralInt8,
    LiteralInt16,
    LiteralInt32,
    LiteralInt64,
    Number,
    SignedInteger,
)
from astx.flows import (
    ForCountLoop,
    ForRangeLoop,
    If,
)
from astx.mixes import (
    NamedExpr,
)
from astx.modifiers import (
    MutabilityKind,
    ScopeKind,
    VisibilityKind,
)
from astx.operators import (
    BinaryOp,
    UnaryOp,
)
from astx.variables import (
    Argument,
    InlineVariableDeclaration,
    Variable,
    VariableAssignment,
    VariableDeclaration,
)


def get_version() -> str:
    """Return the program version."""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "0.9.1"  # semantic-release


__all__ = [
    "Argument",
    "AST",
    "ASTKind",
    "base",
    "BinaryOp",
    "Block",
    "blocks",
    "Boolean",
    "callables",
    "DataType",
    "DataTypeOps",
    "datatypes",
    "Expr",
    "ExprType",
    "Float16",
    "Float32",
    "Float64",
    "Floating",
    "flows",
    "ForCountLoop",
    "ForRangeLoop",
    "Function",
    "FunctionCall",
    "FunctionPrototype",
    "FunctionReturn",
    "get_version",
    "If",
    "InlineVariableDeclaration",
    "Int16",
    "Int32",
    "Int64",
    "Int8",
    "Integer",
    "Literal",
    "LiteralInt16",
    "LiteralInt32",
    "LiteralInt64",
    "LiteralInt8",
    "mixes",
    "Module",
    "MutabilityKind",
    "NamedExpr",
    "Number",
    "operators",
    "OperatorType",
    "ScopeKind",
    "SignedInteger",
    "SourceLocation",
    "StatementType",
    "symbol_table",
    "Target",
    "UnaryOp",
    "Undefined",
    "VariableAssignment",
    "VariableDeclaration",
    "Variable",
    "variables",
    "VisibilityKind",
]


version: str = get_version()

__author__ = "Ivan Ogasawara"
__email__ = "ivan.ogasawara@gmail.com"
__version__: str = version
