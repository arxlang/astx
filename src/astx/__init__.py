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
    ASTNodes,
    DataType,
    Expr,
    ExprType,
    Identifier,
    OperatorType,
    ParenthesizedExpr,
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
    AwaitExpr,
    FunctionAsyncDef,
    FunctionCall,
    FunctionDef,
    FunctionPrototype,
    FunctionReturn,
    LambdaExpr,
    YieldExpr,
)
from astx.classes import (
    ClassDeclStmt,
    ClassDefStmt,
    EnumDeclStmt,
    StructDeclStmt,
    StructDefStmt,
)
from astx.exceptions import (
    CatchHandlerStmt,
    ExceptionHandlerStmt,
    FinallyHandlerStmt,
    ThrowStmt,
)
from astx.flows import (
    CaseStmt,
    ForCountLoopExpr,
    ForCountLoopStmt,
    ForRangeLoopExpr,
    ForRangeLoopStmt,
    GotoStmt,
    IfExpr,
    IfStmt,
    SwitchStmt,
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
    LiteralDict,
    LiteralFloat16,
    LiteralFloat32,
    LiteralFloat64,
    LiteralInt8,
    LiteralInt16,
    LiteralInt32,
    LiteralInt64,
    LiteralInt128,
    LiteralList,
    LiteralNone,
    LiteralSet,
    LiteralString,
    LiteralTime,
    LiteralTimestamp,
    LiteralTuple,
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
from astx.operators import (
    AssignmentExpr,
    CompareOp,
    VariableAssignment,
    WalrusOp,
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
from astx.subscript import SubscriptExpr
from astx.types import (
    AndOp,
    BinaryOp,
    BoolBinaryOp,
    Boolean,
    BoolUnaryOp,
    CollectionType,
    Complex,
    Complex32,
    Complex64,
    DataTypeOps,
    Date,
    DateTime,
    DictType,
    Float16,
    Float32,
    Float64,
    Floating,
    Int8,
    Int16,
    Int32,
    Int64,
    Integer,
    ListType,
    NandOp,
    NorOp,
    NotOp,
    Number,
    OrOp,
    SetType,
    SignedInteger,
    String,
    Time,
    Timestamp,
    TupleType,
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
    XnorOp,
    XorOp,
)
from astx.variables import (
    InlineVariableDeclaration,
    Variable,
    VariableDeclaration,
)


def get_version() -> str:
    """Return the program version."""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "0.18.2"  # semantic-release


__all__ = [
    "AST",
    "ASTKind",
    "ASTNodes",
    "AliasExpr",
    "AndOp",
    "Argument",
    "Arguments",
    "AssignmentExpr",
    "AwaitExpr",
    "BinaryOp",
    "Block",
    "BoolBinaryOp",
    "BoolUnaryOp",
    "Boolean",
    "CaseStmt",
    "CatchHandlerStmt",
    "ClassDeclStmt",
    "ClassDefStmt",
    "CollectionType",
    "CompareOp",
    "Complex",
    "Complex32",
    "Complex64",
    "DataType",
    "DataTypeOps",
    "Date",
    "DateTime",
    "DictType",
    "EnumDeclStmt",
    "ExceptionHandlerStmt",
    "Expr",
    "ExprType",
    "FinallyHandlerStmt",
    "Float16",
    "Float32",
    "Float64",
    "Floating",
    "ForCountLoopExpr",
    "ForCountLoopStmt",
    "ForRangeLoopExpr",
    "ForRangeLoopStmt",
    "FunctionAsyncDef",
    "FunctionCall",
    "FunctionDef",
    "FunctionPrototype",
    "FunctionReturn",
    "GotoStmt",
    "Identifier",
    "IfExpr",
    "IfStmt",
    "ImportExpr",
    "ImportFromExpr",
    "ImportFromStmt",
    "ImportStmt",
    "InlineVariableDeclaration",
    "Int8",
    "Int16",
    "Int32",
    "Int64",
    "Integer",
    "LambdaExpr",
    "ListType",
    "Literal",
    "LiteralBoolean",
    "LiteralComplex",
    "LiteralComplex32",
    "LiteralComplex64",
    "LiteralDate",
    "LiteralDateTime",
    "LiteralDict",
    "LiteralFloat16",
    "LiteralFloat32",
    "LiteralFloat64",
    "LiteralInt8",
    "LiteralInt16",
    "LiteralInt32",
    "LiteralInt64",
    "LiteralInt128",
    "LiteralList",
    "LiteralNone",
    "LiteralSet",
    "LiteralString",
    "LiteralTime",
    "LiteralTimestamp",
    "LiteralTuple",
    "LiteralUInt8",
    "LiteralUInt16",
    "LiteralUInt32",
    "LiteralUInt64",
    "LiteralUInt128",
    "LiteralUTF8Char",
    "LiteralUTF8String",
    "Module",
    "MutabilityKind",
    "NamedExpr",
    "NandOp",
    "NorOp",
    "NotOp",
    "Number",
    "OperatorType",
    "OrOp",
    "Package",
    "ParenthesizedExpr",
    "Program",
    "ScopeKind",
    "SetType",
    "SignedInteger",
    "SourceLocation",
    "StatementType",
    "String",
    "StructDeclStmt",
    "StructDefStmt",
    "SubscriptExpr",
    "SwitchStmt",
    "Target",
    "ThrowStmt",
    "Time",
    "Timestamp",
    "TupleType",
    "TypeCastExpr",
    "UInt8",
    "UInt16",
    "UInt32",
    "UInt64",
    "UInt128",
    "UTF8Char",
    "UTF8String",
    "UnaryOp",
    "Undefined",
    "UnsignedInteger",
    "Variable",
    "VariableAssignment",
    "VariableDeclaration",
    "VisibilityKind",
    "WalrusOp",
    "WhileExpr",
    "WhileStmt",
    "XnorOp",
    "XorOp",
    "YieldExpr",
    "base",
    "blocks",
    "callables",
    "datatypes",
    "flows",
    "get_version",
    "literals",
    "mixes",
    "packages",
    "symbol_table",
    "types",
    "variables",
]


version: str = get_version()

__author__ = "Ivan Ogasawara"
__email__ = "ivan.ogasawara@gmail.com"
__version__: str = version
