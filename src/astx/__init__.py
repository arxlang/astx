# mypy: disable-error-code="attr-defined"
"""ASTx."""

from importlib import metadata as importlib_metadata

from astx import (
    base,
    blocks,
    callables,
    flows,
    literals,
    mixes,
    packages,
    symbol_table,
    types,
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
from astx.classes import (
    ClassDeclStmt,
    ClassDefStmt,
    EnumDeclStmt,
)
from astx.flows import (
    ForCountLoopExpr,
    ForCountLoopStmt,
    ForRangeLoopExpr,
    ForRangeLoopStmt,
    IfExpr,
    IfStmt,
    WhileExpr,
    WhileStmt,
)
from astx.literals import (
    Literal,
    LiteralBoolean,
    LiteralComplex,
    LiteralComplex32,
    LiteralComplex64,
    LiteralDate,
    LiteralDateTime,
    LiteralFloat16,
    LiteralFloat32,
    LiteralFloat64,
    LiteralInt8,
    LiteralInt16,
    LiteralInt32,
    LiteralInt64,
    LiteralInt128,
    LiteralTime,
    LiteralTimestamp,
    LiteralUInt8,
    LiteralUInt16,
    LiteralUInt32,
    LiteralUInt64,
    LiteralUInt128,
    LiteralUTF8Char,
    LiteralUTF8String,
)
from astx.mixes import (
    NamedExpr,
)
from astx.modifiers import (
    MutabilityKind,
    ScopeKind,
    VisibilityKind,
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
from astx.types import (
    BinaryOp,
    Boolean,
    Complex,
    Complex32,
    Complex64,
    DataTypeOps,
    Date,
    DateTime,
    Float16,
    Float32,
    Float64,
    Floating,
    Int8,
    Int16,
    Int32,
    Int64,
    Integer,
    Number,
    SignedInteger,
    Time,
    Timestamp,
    TypeCastExpr,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    UInt128,
    UnaryOp,
    UnsignedInteger,
    UTF8Char,
    UTF8String,
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
        return "0.17.0"  # semantic-release


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
    "ForCountLoopStmt",
    "ForCountLoopExpr",
    "ForRangeLoopStmt",
    "ForRangeLoopExpr",
    "Function",
    "FunctionCall",
    "FunctionPrototype",
    "FunctionReturn",
    "get_version",
    "IfStmt",
    "IfExpr",
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
    "TypeCastExpr",
    "UnaryOp",
    "Undefined",
    "VariableAssignment",
    "VariableDeclaration",
    "Variable",
    "variables",
    "VisibilityKind",
    "WhileStmt",
    "WhileExpr",
    "Complex",
    "Complex32",
    "Complex64",
    "ClassDefStmt",
    "ClassDeclStmt",
    "EnumDeclStmt",
    "LiteralComplex",
    "LiteralComplex32",
    "LiteralComplex64",
    "LiteralUTF8Char",
    "LiteralUTF8String",
    "UTF8Char",
    "UTF8String",
    "Date",
    "DateTime",
    "Timestamp",
    "Time",
    "LiteralDate",
    "LiteralDateTime",
    "LiteralTimestamp",
    "LiteralTime",
    "types",
    "literals",
]


version: str = get_version()

__author__ = "Ivan Ogasawara"
__email__ = "ivan.ogasawara@gmail.com"
__version__: str = version
