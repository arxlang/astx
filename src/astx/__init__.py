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
    ScopeKind,
    VisibilityKind,
)
from astx.operators import (
    BinaryOp,
    UnaryOp,
)
from astx.variables import (
    VarDecl,
    Variable,
)


def get_version() -> str:
    """Return the program version."""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "0.8.0"  # semantic-release


__all__ = [
    "AST",
    "ASTKind",
    "DataType",
    "Expr",
    "ExprType",
    "OperatorType",
    "SourceLocation",
    "StatementType",
    "FunctionCall",
    "Function",
    "FunctionPrototype",
    "FunctionReturn",
    "Boolean",
    "DataTypeOps",
    "Float16",
    "Float32",
    "Float64",
    "Floating",
    "Int8",
    "Int16",
    "Int32",
    "LiteralInt8",
    "LiteralInt16",
    "LiteralInt32",
    "LiteralInt64",
    "Int64",
    "Integer",
    "Literal",
    "Number",
    "SignedInteger",
    "ForCountLoop",
    "ForRangeLoop",
    "If",
    "NamedExpr",
    "ScopeKind",
    "VisibilityKind",
    "BinaryOp",
    "UnaryOp",
    "VarDecl",
    "Variable",
    "Block",
    "Module",
    "Target",
    "base",
    "blocks",
    "callables",
    "datatypes",
    "flows",
    "mixes",
    "operators",
    "symbol_table",
    "variables",
    "get_version",
]


version: str = get_version()

__author__ = "Ivan Ogasawara"
__email__ = "ivan.ogasawara@gmail.com"
__version__: str = version
