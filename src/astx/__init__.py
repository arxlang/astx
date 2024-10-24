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
    packages,
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
)
from astx.callables import (
    Argument,
    Arguments,
    Function,
    FunctionCall,
    FunctionPrototype,
    FunctionReturn,
    LambdaExpr,
)
from astx.datatypes import (
    Boolean,
    Complex,
    Complex32,
    Complex64,
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
    LiteralBoolean,
    LiteralComplex,
    LiteralComplex32,
    LiteralComplex64,
    LiteralFloat16,
    LiteralFloat32,
    LiteralFloat64,
    LiteralInt8,
    LiteralInt16,
    LiteralInt32,
    LiteralInt64,
    LiteralInt128,
    LiteralUInt8,
    LiteralUInt16,
    LiteralUInt32,
    LiteralUInt64,
    LiteralUInt128,
    Number,
    SignedInteger,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    UInt128,
    UnsignedInteger,
)
from astx.flows import (
    ForCountLoop,
    ForRangeLoop,
    If,
    While,
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
from astx.packages import (
    AliasExpr,
    ImportExpr,
    ImportFromExpr,
    ImportFromStmt,
    ImportStmt,
    Module,
    Package,
    Program,
    Target,
)
from astx.variables import (
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
        return "0.15.0"  # semantic-release


__all__ = [
    "AliasExpr",
    "Argument",
    "Arguments",
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
    "LiteralFloat16",
    "LiteralFloat32",
    "LiteralFloat64",
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
    "ImportFromExpr",
    "ImportExpr",
    "ImportStmt",
    "ImportFromStmt",
    "InlineVariableDeclaration",
    "Int16",
    "Int32",
    "Int64",
    "Int8",
    "Integer",
    "UnsignedInteger",
    "UInt8",
    "UInt16",
    "UInt32",
    "UInt64",
    "UInt128",
    "LambdaExpr",
    "Literal",
    "LiteralBoolean",
    "LiteralInt8",
    "LiteralInt16",
    "LiteralInt32",
    "LiteralInt64",
    "LiteralInt128",
    "LiteralUInt8",
    "LiteralUInt16",
    "LiteralUInt32",
    "LiteralUInt64",
    "LiteralUInt128",
    "mixes",
    "Module",
    "MutabilityKind",
    "NamedExpr",
    "Number",
    "operators",
    "OperatorType",
    "packages",
    "Package",
    "Program",
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
    "While",
    "Complex",
    "Complex32",
    "Complex64",
    "LiteralComplex",
    "LiteralComplex32",
    "LiteralComplex64",
]


version: str = get_version()

__author__ = "Ivan Ogasawara"
__email__ = "ivan.ogasawara@gmail.com"
__version__: str = version
