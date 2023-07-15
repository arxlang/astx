"""AST classes and functions."""
from enum import Enum
from typing import List, Tuple, TypeAlias, Type


class SourceLocation:
    line: int
    col: int

    def __init__(self, line: int, col: int):
        self.line = line
        self.col = col


class ASTKind(Enum):
    """The expression kind class used for downcasting."""

    GenericKind = -1
    ModuleKind = -2

    # variables
    VariableKind = -10
    VarKind = -11  # var keyword for variable declaration

    # operators
    UnaryOpKind = -20
    BinaryOpKind = -21

    # functions
    PrototypeKind = -30
    FunctionKind = -31
    CallKind = -32
    ReturnKind = -33

    # control flow
    IfKind = -40
    ForKind = -41

    # data types
    NullDTKind = -100
    BooleanDTKind = -101
    Int8DTKind = -102
    UInt8DTKind = -103
    Int16DTKind = -104
    UInt16DTKind = -105
    Int32DTKind = -106
    UInt32DTKind = -107
    Int64DTKind = -108
    UInt64DTKind = -109
    FloatDTKind = -110
    DoubleDTKind = -111
    BinaryDTKind = -112
    StringDTKind = -113
    FixedSizeBinaryDTKind = -114
    Date32DTKind = -115
    Date64DTKind = -116
    TimestampDTKind = -117
    Time32DTKind = -118
    Time64DTKind = -119
    Decimal128DTKind = -120
    Decimal256DTKind = -121


class AST:
    """AST main expression class."""

    loc: SourceLocation
    kind: ASTKind

    def __init__(self, loc: SourceLocation = SourceLocation(0, 0)) -> None:
        """Initialize the AST instance."""
        self.kind = ASTKind.GenericKind
        self.loc = loc


class Expr(AST):
    """AST main expression class."""

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self.__class__.__name__


ExprType: TypeAlias = Type[Expr]


class DataType(Expr):
    """AST main expression class."""


class OperatorType(Expr):
    """AST main expression class."""


class StatementType(AST):
    """AST main expression class."""
